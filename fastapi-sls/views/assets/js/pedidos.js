const API_BASE = "http://localhost:8000";

document.addEventListener("DOMContentLoaded", cargarCarritos);

async function cargarCarritos() {
  try {
    const r = await fetch(`${API_BASE}/carro/view/all`);
    const data = await r.json();
    const tbody = document.querySelector("#tablaCarritos tbody");
    tbody.innerHTML = "";

    if (data.success && data.data.length) {
      data.data.forEach((c) => {
        const badge = estadoBadge1(c.car_state);
        const badge1 = fases(c.cf_fase);
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${c.car_id}</td>
          <td>${c.user_name}<br><small class="text-muted">${c.user_cc}</small></td>
          <td>${c.car_creation_date}</td>
          <td>${badge}</td>
          <td>${badge1}</td>
          <td class="text-end">
            <button class="btn btn-primary btn-sm" onclick="verDetalleCarrito(${c.car_id})">
              <i class="fas fa-eye"></i> Ver Detalle
            </button>
          </td>`;
        tbody.appendChild(tr);
      });
    } else {
      tbody.innerHTML = `<tr><td colspan="5" class="text-center text-muted">⚠️ No hay carritos</td></tr>`;
    }
  } catch (e) {
    Swal.fire({
      title: "🚨 Error de conexión",
      text: "No se pudo establecer conexión. Intenta más tarde.",
      icon: "error",
      showConfirmButton: false,
      timer: 3500,
      timerProgressBar: true,
    });
  }
}

function estadoBadge1(estado) {
  estado = Number(estado);

  const map = {
    0: { text: "Cerrado", color: "danger" },
    1: { text: "Abierto", color: "success" },
  };
  const item = map[estado] || { text: "?", color: "dark" };

  return `<span class="badge bg-${item.color}">${item.text}</span>`;
}

function fases(estado) {
  estado = Number(estado);

   const map = {
    0: { text: "Abierto", color: "secondary" },   
    1: { text: "Pagado", color: "success" },      
    2: { text: "En Proceso", color: "warning" },  
    3: { text: "Enviado", color: "info" },        
    4: { text: "Entregado", color: "primary" },
    5: { text: "Cancelado", color: "danger" } 
  };

  const item = map[estado] || { text: "?", color: "dark" };

  return `<span class="badge bg-${item.color}">${item.text}</span>`;
}

async function verDetalleCarrito(id) {
  try {
    const r = await fetch(`${API_BASE}/carro/admin/${id}`);
    const d = await r.json();
    if (!d.success)
      return Swal.fire({
        title: "Aviso",
        icon: "warning",
        text: d.message,
        timer: 3000,
        timerProgressBar: true,
        showConfirmButton: false,
      });

    document.getElementById("detalleCarritoID").textContent = d.carrito.car_id;
    document.getElementById("detalleUsuario").textContent = d.usuario;
    document.getElementById("detalleFecha").textContent = d.carrito.car_creation_date;
    document.getElementById("detalleEstado").innerHTML = estadoBadge1(d.carrito.car_state);

    const tbody = document.getElementById("detalleProductos");
    tbody.innerHTML = d.productos
      .map(
        (p) => `
      <tr>
        <td>${p.nombre_producto}</td>
        <td>${p.cantidad}</td>
        <td>${p.precio_unitario.toLocaleString()}</td>
        <td>${p.subtotal.toLocaleString()}</td>
      </tr>`
      )
      .join("");
    document.getElementById(
      "detalleTotal"
    ).textContent = `${d.total_pagar.toLocaleString()}`;

    // 🔹 Validación de botones dependerá del historial
    await cargarHistorialEstados(id);

    const btnNext = document.getElementById("btnNext");
    const btnCancel = document.getElementById("btnCancel");

    btnNext.dataset.id = id;
    btnCancel.dataset.id = id;

    new bootstrap.Modal(document.getElementById("modalDetalleCarrito")).show();
  } catch (e) {
    console.error(e);
    Swal.fire("Error", "Ocurrió un problema al obtener el detalle", "error");
  }
}

async function cargarHistorialEstados(id) {
  const ul = document.getElementById("historialEstados");
  ul.innerHTML =
    "<li class='list-group-item text-center text-muted'>Cargando...</li>";
  try {
    const r = await fetch(`${API_BASE}/carro/${id}/historial`);
    const d = await r.json();

    const btnNext = document.getElementById("btnNext");
    const btnCancel = document.getElementById("btnCancel");

    if (d.success && d.data.length) {
      ul.innerHTML = d.data
        .map(
          (e) => `
          <li class="list-group-item">
            <strong>${e.fecha}</strong> -
            <span class="badge" style="color: black;">${e.estado}</span>
            <br><small>${e.comentario || "Sin comentario"}</small>
          </li>`
        )
        .join("");

      // Tomamos el último estado del historial
      const ultimoEstado = d.data[d.data.length - 1].estado;

      // 🔹 Validación: si el estado <= 0 ocultamos botones
      if (Number(ultimoEstado) > 0) {
        btnNext.style.display = "inline-block";
        btnCancel.style.display = "inline-block";
      } 
    } else {
      ul.innerHTML =
        "<li class='list-group-item text-center text-muted'>Sin historial</li>";

      // Sin historial → ocultar botones
      btnNext.style.display = "none";
      btnCancel.style.display = "none";
    }
  } catch (err) {
    console.error(err);
    ul.innerHTML =
      "<li class='list-group-item text-center text-danger'>Error al cargar</li>";
  }
}

async function siguienteEstado(carId) {
  try {
    const resp = await fetch(`${API_BASE}/carro/${carId}/next`, {
      method: "PUT",
    });
    const data = await resp.json();

    if (data.success) {
      Swal.fire({
        text: data.message,
        title: "✅ Éxito",
        icon: "success",
        timer: 3500,
        timerProgressBar: true,
        showConfirmButton: false,
      });
      cargarCarritos();
      await cargarHistorialEstados(carId);
    } else {
      Swal.fire({
        text: data.message,
        icon: "warning",
        title: "Aviso",
        timer: 3000,
        timerProgressBar: true,
        showConfirmButton: false,
      });
    }
  } catch (err) {
    console.error(err);
    Swal.fire("Error", "El producto ya ha sido entregado o cancelado", "error");
  }
}

async function cancelarPedido(carId) {
  try {
    const resp = await fetch(`${API_BASE}/carro/${carId}/cancelar`, {
      method: "PUT",
    });
    const data = await resp.json();

    if (data.success) {
      Swal.fire("🚫 Pedido cancelado", "", "success");
      cargarCarritos();
      await cargarHistorialEstados(carId);
    } else {
      Swal.fire("Aviso", data.message, "warning");
    }
  } catch (err) {
    console.error(err);
    Swal.fire("Error", "No se pudo cancelar el pedido", "error");
  }
}

// ---------------------------------------------------
//  Listeners de botones del modal
// ---------------------------------------------------
document.getElementById("btnNext").addEventListener("click", (e) => {
  const id = e.currentTarget.dataset.id;
  if (id) siguienteEstado(id);
});

document.getElementById("btnCancel").addEventListener("click", (e) => {
  const id = e.currentTarget.dataset.id;
  if (id) cancelarPedido(id);
});
