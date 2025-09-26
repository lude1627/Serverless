document.addEventListener("DOMContentLoaded", async () => {
    const userCc = sessionStorage.getItem("user_cc");
    if (!userCc) {
        window.location.href = "/views/login/login.html";
        return;
    }

    const API_BASE = "http://localhost:8000";
    const list = document.getElementById("pedidosList");
    if (!list) return;

    try {
        const resp = await fetch(`${API_BASE}/carro/view/all/${userCc}`);
        const data = await resp.json();

        if (!data.success || !Array.isArray(data.data) || data.data.length === 0) {
            list.innerHTML = `
                <li class="list-group-item text-center text-muted">
                    No se encontraron carritos.
                </li>`;
            return;
        }

       
        const filas = data.data.map(c => {
            const estadoActivo = c.estado === "1";
            const estadoTexto  = estadoActivo ? "Abierto" : "Cerrado";
            const estadoClase  = estadoActivo ? "bg-success" : "bg-danger";

            return `
                <tr>
                    <td>${c.user_name}</td>
                    <td>${c.fecha_creacion}</td>
                    <td><span class="badge ${estadoClase} px-3 py-2">${estadoTexto}</span></td>
                    <td>${c.total}</td>
                    <td>
                      <button class="btn btn-outline-primary btn-sm"
                              onclick="verDetalleSoloLectura(${c.car_id})">
                        Ver Detalle
                      </button>
                    </td>
                </tr>`;
        }).join("");

        list.innerHTML = `
            <li class="list-group-item p-0">
                <div class="table-responsive m-0">
                    <table class="table table-bordered text-center align-middle mb-0">
                        <thead class="table-light">
                            <tr>
                                <th>Usuario</th>
                                <th>Fecha de Creación</th>
                                <th>Estado</th>
                                <th>Total</th>
                                <th>Detalle</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${filas}
                        </tbody>
                    </table>
                </div>
            </li>`;
    } catch (err) {
        console.error("Error cargando carritos:", err);
        list.innerHTML = `
            <li class="list-group-item text-center text-danger">
                Error de conexión con el servidor.
            </li>`;
    }
});
function estadoBadge(estado) {
  
  estado = Number(estado);

  const map = {
   
    1: { text: "Pagado",     color: "primary"   }, 
    2: { text: "En Proceso", color: "warning"   }, 
    3: { text: "Enviado",    color: "info"      }, 
    4: { text: "Entregado",  color: "success"   }, 
    5: { text: "Cancelado",  color: "danger"    }  
  };

  const item = map[estado] || { text: "?", color: "dark" };

  return `<span class="badge bg-${item.color}">${item.text}</span>`;
}


async function verDetalleSoloLectura(carId) {
    const API_BASE = "http://localhost:8000";

    try {
     
        const r = await fetch(`${API_BASE}/carro/admin/${carId}`);
        const d = await r.json();
        if (!d.success) {
            Swal.fire("Error", "No se pudo cargar el detalle", "error");
            return;
        }

        
        document.getElementById("detalleCarritoID").textContent = d.carrito.car_id;
        document.getElementById("detalleUsuario").textContent   = d.usuario;
        document.getElementById("detalleFecha").textContent     = d.carrito.fecha_creacion;
        document.getElementById("detalleEstado").innerHTML      = d.carrito.estado == 1
            ? '<span class="badge bg-primary">Activo</span>'
            : '<span class="badge bg-danger">Inactivo</span>';

        const tbody = document.getElementById("detalleProductos");
        tbody.innerHTML = d.productos.map(p => `
            <tr>
                <td>${p.nombre_producto}</td>
                <td>${p.cantidad}</td>
                <td>$${p.precio_unitario}</td>
                <td>$${p.subtotal}</td>
            </tr>`).join("");

        document.getElementById("detalleTotal").textContent =
            `$${d.total_pagar}`;

    
        const ul = document.getElementById("historialEstados");
        ul.innerHTML = "<li class='list-group-item text-center text-muted'>Cargando...</li>";

        const h = await fetch(`${API_BASE}/carro/${carId}/historial`);
        const hist = await h.json();

        if (hist.success && hist.data.length) {
            ul.innerHTML = hist.data.map(e => `
                <li class="list-group-item">
                    <strong>${e.fecha}</strong> -
                    <span class="badge">${estadoBadge(e.estado)}</span>
                    <br><small>${e.comentario || "Sin comentario"}</small>
                </li>`).join("");
        } else {
            ul.innerHTML = "<li class='list-group-item text-center text-muted'>Sin historial</li>";
        }

       
        const modalEl = document.getElementById("modalDetalleCarrito");
        const modal   = new bootstrap.Modal(modalEl, {backdrop: false});
        modal.show();

    } catch (err) {
        console.error(err);
        Swal.fire("Error", "Ocurrió un problema al obtener el detalle", "error");
    }
}
