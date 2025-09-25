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

        // Ahora la respuesta tiene { success: true, data: [ ... ] }
        if (!data.success || !Array.isArray(data.data) || data.data.length === 0) {
            list.innerHTML = `
                <li class="list-group-item text-center text-muted">
                    No se encontraron carritos.
                </li>`;
            return;
        }

        // Generar las filas de todos los carritos
        const filas = data.data.map(c => {
            const estadoTexto = estadoBadge(c.estado);

            return `
                <tr>
                    <td>${c.user_name}</td>
                    <td>${c.fecha_creacion}</td>
                    <td>${estadoTexto}</td>
                    <td>${c.total}</td>
                </tr>`;
        }).join("");

   
        function estadoBadge(estado) {
        
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
                            </tr>
                        </thead>
                        <tbody>
                            ${filas}
                        </tbody>
                    </table>
                </div>
            </li>
        `;
    } catch (err) {
        // console.error("Error cargando carritos:", err);
        list.innerHTML = `
            <li class="list-group-item text-center text-danger"><strong>
                Esta informacion no esta disponible en este momento.
            </strong></li>`;

        Swal.fire({
            title: "🚨 Error de conexión",
            text: "No se pudo establecer conexión. Intenta más tarde.",
            icon: "error",
            showConfirmButton: false,
            timer: 3500,
            timerProgressBar: true,
            
        });     
    }
});
