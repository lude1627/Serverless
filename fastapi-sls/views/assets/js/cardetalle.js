document.addEventListener("DOMContentLoaded", async () => {
    const userCc = sessionStorage.getItem("user_cc");
    if (!userCc) {
        window.location.href = "/views/login/login.html";
        return;
    }

    const API_BASE = "http://localhost:8000";
    const list = document.getElementById("detalleList");
    const subtotalSpan = document.getElementById("detalleSubtotal");
    const template = list.querySelector(".template");
    const finalizarBtn = document.getElementById("finalizarBtn");

  async function cargarDetalle() {
    try {
        const resp = await fetch(`${API_BASE}/carro/usuario/${userCc}`);
        const data = await resp.json();

        
        list.querySelectorAll("li:not(.template)").forEach(el => el.remove());

        if (!data.success || !data.productos || data.productos.length === 0) {
            subtotalSpan.textContent = "$0";
            return;
        }

        let subtotalTotal = 0;

        data.productos.forEach(item => {
            const clone = template.cloneNode(true);
            clone.classList.remove("template", "d-none");

            const precioNum = parseFloat(item.precio_unitario.replace(/[^\d.]/g, ""));

            clone.querySelector(".nombre").textContent = item.nombre_producto;
            clone.querySelector(".precio-unitario").textContent = `Precio: ${item.precio_unitario}`;
            clone.querySelector(".cantidad").value = item.cantidad;
            clone.querySelector(".cantidad").dataset.price = precioNum;
            clone.querySelector(".subtotal").textContent = `$${item.cantidad * precioNum}`;

            list.appendChild(clone);

            subtotalTotal += item.cantidad * precioNum;
        });

        subtotalSpan.textContent = `$${subtotalTotal}`;
    } catch (err) {
        console.error("Error cargando detalles:", err);
    }
}


    list.addEventListener("click", async e => {
        if (e.target.classList.contains("eliminar")) {
            const { id: detalleId, carid: carId } = e.target.dataset;
            try {
                await fetch(`${API_BASE}/carro/eliminar/${detalleId}/${carId}`, { method: "DELETE" });
                cargarDetalle();
            } catch (err) {
                console.error("Error eliminando producto:", err);
            }
        }
    });

    finalizarBtn.addEventListener("click", async () => {
        try {
            const resp = await fetch(`${API_BASE}/carro/usuario/${userCc}`);
            const data = await resp.json();
            if (data.carrito?.car_id) {
                await fetch(`${API_BASE}/carro/finalizar/${data.carrito.car_id}`, { method: "PUT" });
                alert("Compra finalizada con éxito");
                cargarDetalle();
            }
        } catch (err) {
            console.error("Error finalizando compra:", err);
        }
    });

    cargarDetalle();
});
