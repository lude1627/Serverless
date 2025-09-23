const API_BASE = "http://localhost:8000";

document.addEventListener("DOMContentLoaded", cargarCarritos);

// 📌 CARGAR LISTA DE CARRITOS
async function cargarCarritos() {
  try {
    const response = await fetch(`${API_BASE}/carro/view/all`);
    const result = await response.json();

    const tbody = document.querySelector("#tablaCarritos tbody");
    tbody.innerHTML = "";

    if (result.success && result.data.length > 0) {
      result.data.forEach((carrito) => {
        const estadoBadge =
          carrito.estado == 1
            ? '<span class="badge bg-success"><i class="fas fa-lock-open"></i> Abierto</span>'
            : '<span class="badge bg-secondary"><i class="fas fa-lock"></i> Cerrado</span>';

        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${carrito.car_id}</td>
          <td>${carrito.user_name} <br>
              <small class="text-muted">${carrito.user_cc}</small>
          </td>
          <td>${carrito.fecha_creacion}</td>
          <td>${estadoBadge}</td>
          <td class="text-end">
            <button class="btn btn-primary btn-sm" onclick="verDetalleCarrito(${carrito.user_cc})">
              <i class="fas fa-eye"></i> Ver Detalle
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    } else {
      tbody.innerHTML = `<tr><td colspan="5" class="text-center text-muted">⚠️ No hay carritos registrados</td></tr>`;
    }
  } catch (error) {
    console.error("Error cargando carritos:", error);
    Swal.fire("❌ Error", "No se pudieron cargar los carritos", "error");
  }
}

// 📌 VER DETALLE DE UN CARRITO + HISTORIAL
async function verDetalleCarrito(user_cc) {
  try {
    const response = await fetch(`${API_BASE}/carro/admin/${user_cc}`);
    const data = await response.json();

    if (!data.success) {
      Swal.fire(
        "❌ Error",
        "No se pudo cargar el detalle del carrito",
        "error"
      );
      return;
    }

    // Llenar info principal
    document.getElementById("detalleCarritoID").textContent =
      data.carrito.car_id;
    document.getElementById("detalleUsuario").textContent = data.usuario;
    document.getElementById("detalleFecha").textContent =
      data.carrito.fecha_creacion;
    document.getElementById("detalleEstado").innerHTML =
      data.carrito.estado == 1
        ? '<span class="badge bg-success"><i class="fas fa-lock-open"></i> Abierto</span>'
        : '<span class="badge bg-secondary"><i class="fas fa-lock"></i> Cerrado</span>';

    // Llenar productos
    let productosHTML = "";
    data.productos.forEach((prod) => {
      productosHTML += `
        <tr>
          <td>${prod.nombre_producto}</td>
          <td>${prod.cantidad}</td>
          <td>$${prod.precio_unitario.toLocaleString()}</td>
          <td>$${prod.subtotal.toLocaleString()}</td>
        </tr>`;
    });

    document.getElementById("detalleProductos").innerHTML = productosHTML;
    document.getElementById(
      "detalleTotal"
    ).textContent = `$${data.total_pagar.toLocaleString()}`;
    // Cargar historial de estados
    await cargarHistorialEstados((car_id = data.carrito.car_id));

    // Guardar carritoId en el formulario
    const form = document.getElementById("formActualizarEstado");
    form.dataset.carritoId = user_cc;
    form.reset();

    // Mostrar modal
    const modal = new bootstrap.Modal(
      document.getElementById("modalDetalleCarrito")
    );
    modal.show();
  } catch (error) {
    console.error(error);
    Swal.fire(
      "❌ Error",
      "Ocurrió un problema al obtener el detalle del carrito",
      "error"
    );
  }
}

// 📌 CARGAR HISTORIAL DE ESTADOS
async function cargarHistorialEstados(car_id) {
  const ulHistorial = document.getElementById("historialEstados");
  ulHistorial.innerHTML = `<li class="list-group-item text-muted text-center">Cargando...</li>`;

  try {
    const response = await fetch(`${API_BASE}/carro/${car_id}/historial`);
    const result = await response.json();

    if (result.success && result.data.length > 0) {
      ulHistorial.innerHTML = "";
      result.data.forEach((estado) => {
        const li = document.createElement("li");
        li.classList.add("list-group-item");
        li.innerHTML = `
          <strong>${estado.fecha}</strong> - 
          <span class="badge bg-info">${mapEstadoTexto(estado.estado)}</span>
          <br><small>${estado.comentario || "Sin comentario"}</small>
        `;
        ulHistorial.appendChild(li);
      });
    } else {
      ulHistorial.innerHTML = `<li class="list-group-item text-center text-muted">No hay historial</li>`;
    }
  } catch (error) {
    console.error("Error cargando historial:", error);
    ulHistorial.innerHTML = `<li class="list-group-item text-center text-danger">Error al cargar historial</li>`;
  }
}

// 📌 MAPEO DE ESTADOS
function mapEstadoTexto(estado) {
  switch (estado) {
    case 1:
      return "Pendiente";
    case 2:
      return "Procesando";
    case 3:
      return "Enviado";
    case 4:
      return "Entregado";
    case 5:
      return "Cancelado";
    default:
      return "Desconocido";
  }
}

// 📌 ABRIR MODAL ACTUALIZAR ESTADO
function abrirModalActualizarEstado(car_id) {
  const form = document.getElementById("formActualizarEstado");
  form.dataset.carritoId = car_id;
}

// 📌 ACTUALIZAR ESTADO DEL CARRITO

async function actualizarEstadoCarrito() {
 
    
  if (!car_id || isNaN(estado)) {
    Swal.fire("❌ Error", "Datos inválidos para actualizar estado", "error");
    return;
  }
  try {
    const response = await fetch(`${API_BASE}/carro/${car_id}/estado`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ estado, comentario }),
    });
    const result = await response.json();
    
    if (result.success) {   
      Swal.fire("✅ Éxito", "Estado actualizado correctamente", "success");
      cargarCarritos();
      verDetalleCarrito(car_id);
      const modalElement = document.getElementById("modalDetalleCarrito");
      const modalInstance = bootstrap.Modal.getInstance(modalElement);
      modalInstance.hide();
    }
    else {
      Swal.fire("❌ Error", result.message || "No se pudo actualizar el estado", "error");
    }
  }
  catch (error) {
    console.error("Error actualizando estado:", error);
    Swal.fire("❌ Error", "Ocurrió un problema al actualizar el estado", "error");
  }
}

// 📌 EVENTO SUBMIT FORM ACTUALIZAR ESTADO
document
  .getElementById("formActualizarEstado")
  .addEventListener("submit", actualizarEstadoCarrito);





