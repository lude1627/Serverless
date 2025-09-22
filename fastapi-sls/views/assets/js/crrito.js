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
        const resp = await fetch(`${API_BASE}/carro/usuario/${userCc}`);
        const data = await resp.json();

        if (!data.success || !data.carrito) {
            list.innerHTML = `
                <li class="list-group-item text-center text-muted">
                    No se encontró información del carrito.
                </li>`;
            return;
        }

        const estadoActivo = data.carrito.estado === "1";
        const estadoTexto  = estadoActivo ? "Activo" : "Inactivo";
        const estadoClase  = estadoActivo ? "bg-primary" : "bg-danger";

       
        list.innerHTML = `
            <li class="list-group-item p-0">
                <div class="table-responsive m-0">
                    <table class="table table-bordered text-center align-middle mb-0">
                        <thead class="table-light">
                            <tr>
                                <th>Usuario</th>
                                <th>Fecha de Creación</th>
                                <th>Estado</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>${data.usuario}</td>
                                <td>${data.carrito.fecha_creacion}</td>
                                <td>
                                    <span class="badge ${estadoClase} px-3 py-2">${estadoTexto}</span>
                                </td>
                                <td>
                                    <a href="/views/carrito/carrito.html" 
                                       class="btn btn-sm btn-outline-primary">
                                       Ver Detalles
                                    </a>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </li>
        `;
    } catch (err) {
        console.error("Error cargando carrito:", err);
        list.innerHTML = `
            <li class="list-group-item text-center text-danger">
                Error de conexión con el servidor.
            </li>`;
    }
});
