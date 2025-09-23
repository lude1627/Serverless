document.addEventListener("DOMContentLoaded", async () => {
    const userCc = sessionStorage.getItem("user_cc");
    if (!userCc) {
        window.location.href = "/views/login/login.html";
        return;
    }

    const API_BASE = "http://localhost:8000";
    const list = document.getElementById("detalleList");
    const subtotalSpan = document.getElementById("detalleSubtotal");
    const resumenSubtotal = document.getElementById("detalleSubtotalResumen");
    const resumenTotal = document.getElementById("detalleTotal");
    const template = list.querySelector(".template");
    const finalizarBtn = document.getElementById("finalizarBtn");

    // 🔹 Formateador de moneda COP
    const formatoCOP = new Intl.NumberFormat("es-CO", {
        style: "currency",
        currency: "COP",
        minimumFractionDigits: 0
    });

    async function actualizarResumen(monto) {
        const dinero = formatoCOP.format(monto);
        subtotalSpan.textContent = dinero;
        resumenSubtotal.textContent = dinero;
        resumenTotal.textContent = dinero;
    }

    async function cargarDetalle() {
        try {
            const carritoResp = await fetch(`${API_BASE}/carro/usuario/${userCc}`);
            const carritoData = await carritoResp.json();
            if (!carritoData.success || !carritoData.carrito) {
                actualizarResumen(0);
                list.querySelectorAll("li:not(.template)").forEach(el => el.remove());
                return;
            }
            const carId = carritoData.carrito.car_id;

            const resp = await fetch(`${API_BASE}/carro/dcarrito/${carId}`);
            const data = await resp.json();

            list.querySelectorAll("li:not(.template)").forEach(el => el.remove());

            if (!data.success || !data.detalles || data.detalles.length === 0) {
                actualizarResumen(0);
                return;
            }

            let subtotalTotal = 0;

            data.detalles.forEach(item => {
                const clone = template.cloneNode(true);
                clone.classList.remove("template", "d-none");

                const precioNum = parseFloat(item.precio_unitario);
                const subtotalItem = item.detalle_cantidad * precioNum;

                clone.querySelector(".nombre").textContent =
                    item.nombre_producto || `Producto ${item.product_id}`;
                clone.querySelector(".precio-unitario").textContent =
                    `Precio: ${formatoCOP.format(precioNum)}`;
                clone.querySelector(".cantidad").value = item.detalle_cantidad;
                clone.querySelector(".cantidad").dataset.price = precioNum;

                clone.querySelector(".cantidad").dataset.detalleId = item.detalle_id;
                clone.querySelector(".cantidad").dataset.carId = item.car_id;

                clone.querySelector(".guardar").dataset.detalleId = item.detalle_id;
                clone.querySelector(".guardar").dataset.carId = item.car_id;

                clone.querySelector(".eliminar").dataset.id = item.detalle_id;
                clone.querySelector(".eliminar").dataset.carid = item.car_id;

                // ✅ subtotal con formato de moneda
                clone.querySelector(".subtotal").textContent = formatoCOP.format(subtotalItem);

                list.appendChild(clone);
                subtotalTotal += subtotalItem;
            });

            actualizarResumen(subtotalTotal);
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

        if (e.target.classList.contains("guardar")) {
            const { detalleId, carId } = e.target.dataset;
            const input = e.target.closest("li").querySelector(".cantidad");
            const nuevaCantidad = parseInt(input.value, 10);
            if (nuevaCantidad < 1) return;

            try {
                await fetch(`${API_BASE}/carro/actualizar/${detalleId}/${carId}`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ detalle_cantidad: nuevaCantidad })
                });
                cargarDetalle();
            } catch (err) {
                console.error("Error actualizando cantidad:", err);
            }
        }
    });

    cargarDetalle();
});
