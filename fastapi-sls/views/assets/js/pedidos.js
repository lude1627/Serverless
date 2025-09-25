const API_BASE = "http://localhost:8000";

document.addEventListener("DOMContentLoaded", cargarCarritos);

// ---------------------------------------------------
//  Cargar lista de carritos
// ---------------------------------------------------
async function cargarCarritos() {
  try {
    const r = await fetch(`${API_BASE}/carro/view/all`);
    const data = await r.json();
    const tbody = document.querySelector("#tablaCarritos tbody");
    tbody.innerHTML = "";

    if (data.success && data.data.length) {
      data.data.forEach(c => {
        const badge = estadoBadge1(c.estado);
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${c.car_id}</td>
          <td>${c.user_name}<br><small class="text-muted">${c.user_cc}</small></td>
          <td>${c.fecha_creacion}</td>
          <td>${badge}</td>
          <td class="text-end">
            <button class="btn btn-primary btn-sm" onclick="verDetalleCarrito(${c.car_id})">
              <i class="fas fa-eye"></i> Ver Detalle
            </button>
          </td>`;
        tbody.appendChild(tr);
      });
    } else {
      tbody.innerHTML =
        `<tr><td colspan="5" class="text-center text-muted">⚠️ No hay carritos</td></tr>`;
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
  // Forzar a número por si llega como string
  estado = Number(estado);

  const map = {
    0: { text: "Inactivo",    color: "danger" }, 
    1: { text: "Activo",  color: "success"    }  
  };
  const item = map[estado] || { text: "?", color: "dark" };

  return `<span class="badge bg-${item.color}">${item.text}</span>`;
}
// ---------------------------------------------------
//  Badge de estado
// ---------------------------------------------------
function estadoBadge(estado) {
  // Forzar a número por si llega como string
  estado = Number(estado);

  const map = {
    0: { text: "Abierto",    color: "secondary" }, // gris
    1: { text: "Pagado",     color: "primary"   }, // azul
    2: { text: "En Proceso", color: "warning"   }, // amarillo
    3: { text: "Enviado",    color: "info"      }, // celeste
    4: { text: "Entregado",  color: "success"   }, // verde
    5: { text: "Cancelado",  color: "danger"    }  // rojo
  };

  const item = map[estado] || { text: "?", color: "dark" };

  return `<span class="badge bg-${item.color}">${item.text}</span>`;
}

// ---------------------------------------------------
//  Ver detalle de un carrito
// ---------------------------------------------------
async function verDetalleCarrito(id) {
  try {
    const r = await fetch(`${API_BASE}/carro/admin/${id}`);
    const d = await r.json();
    if (!d.success) return Swal.fire("Error", "No se pudo cargar el detalle", "error");

    document.getElementById("detalleCarritoID").textContent = d.carrito.car_id;
    document.getElementById("detalleUsuario").textContent   = d.usuario;
    document.getElementById("detalleFecha").textContent     = d.carrito.fecha_creacion;
    document.getElementById("detalleEstado").innerHTML      = estadoBadge1(d.carrito.estado);

    const tbody = document.getElementById("detalleProductos");
    tbody.innerHTML = d.productos.map(p => `
      <tr>
        <td>${p.nombre_producto}</td>
        <td>${p.cantidad}</td>
        <td>$${p.precio_unitario.toLocaleString()}</td>
        <td>$${p.subtotal.toLocaleString()}</td>
      </tr>`).join("");
    document.getElementById("detalleTotal").textContent =
      `$${d.total_pagar.toLocaleString()}`;

    await cargarHistorialEstados(id);

    // Guardar ID en los botones de acción
    document.getElementById("btnNext").dataset.id = id;
    document.getElementById("btnCancel").dataset.id = id;

    new bootstrap.Modal(document.getElementById("modalDetalleCarrito")).show();
  } catch (e) {
    console.error(e);
    Swal.fire("Error", "Ocurrió un problema al obtener el detalle", "error");
  }
}

// ---------------------------------------------------
//  Cargar historial de estados
// ---------------------------------------------------
async function cargarHistorialEstados(id) {
  const ul = document.getElementById("historialEstados");
  ul.innerHTML =
    "<li class='list-group-item text-center text-muted'>Cargando...</li>";
  try {
    const r = await fetch(`${API_BASE}/carro/${id}/historial`);
    const d = await r.json();
    if (d.success && d.data.length) {
      ul.innerHTML = d.data
        .map(e => `
          <li class="list-group-item">
            <strong>${e.fecha}</strong> -
            <span class="badge bg-info">${estadoBadge(e.estado)}</span>
            <br><small>${e.comentario || "Sin comentario"}</small>
          </li>`)
        .join("");
    } else {
      ul.innerHTML =
        "<li class='list-group-item text-center text-muted'>Sin historial</li>";
    }
  } catch (e) {
    console.error(e);
    ul.innerHTML =
      "<li class='list-group-item text-center text-danger'>Error al cargar</li>";
  }
}

// ---------------------------------------------------
//  Avanzar al siguiente estado
// ---------------------------------------------------
async function siguienteEstado(carId) {
  try {
    const resp = await fetch(`${API_BASE}/carro/${carId}/next`, { method: "PUT" });
    const data = await resp.json();

    if (data.success) {
      Swal.fire("✅ Éxito", data.message, "success");
      cargarCarritos();
      await cargarHistorialEstados(carId);
    } else {
      Swal.fire("Aviso", data.message, "warning");
    }
  } catch (err) {
    console.error(err);
    Swal.fire("Error", "El producto ya ha sido entregado o cancelado", "error");
  }
}

// ---------------------------------------------------
//  Cancelar carrito
// ---------------------------------------------------
async function cancelarPedido(carId) {
 

  try {
    const resp = await fetch(`${API_BASE}/carro/${carId}/cancelar`, { method: "PUT" });
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
document.getElementById("btnNext").addEventListener("click", e => {
  const id = e.currentTarget.dataset.id;
  if (id) siguienteEstado(id);
});

document.getElementById("btnCancel").addEventListener("click", e => {
  const id = e.currentTarget.dataset.id;
  if (id) cancelarPedido(id);
});
