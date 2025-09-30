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

  let carritoActivoId = null; 

  const formatoCOP = new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    minimumFractionDigits: 0,
  });

  async function actualizarResumen(monto) {
    const dinero = formatoCOP.format(monto);
    subtotalSpan.textContent = dinero;
    if (resumenSubtotal) resumenSubtotal.textContent = dinero;
    if (resumenTotal) resumenTotal.textContent = dinero;
  }

  async function cargarDetalle() {
    try {
      const carritoResp = await fetch(`${API_BASE}/carro/usuario/${userCc}`);
      const carritoData = await carritoResp.json();
      if (!carritoData.success || !carritoData.carrito) {
        actualizarResumen(0);
        list.querySelectorAll("li:not(.template)").forEach((el) => el.remove());
        carritoActivoId = null;
        return;
      }

   
      carritoActivoId = carritoData.carrito.car_id;

      const resp = await fetch(`${API_BASE}/carro/dcarrito/${carritoActivoId}`);
      const data = await resp.json();

      list.querySelectorAll("li:not(.template)").forEach((el) => el.remove());

      if (!data.success || !data.detalles || data.detalles.length === 0) {
        actualizarResumen(0);
        return;
      }

      let subtotalTotal = 0;

      data.detalles.forEach((item) => {
        const clone = template.cloneNode(true);
        clone.classList.remove("template", "d-none");

        const precioNum = parseFloat(item.cd_unit_price);
        const subtotalItem = item.cd_cant * precioNum;

        clone.querySelector(".nombre").textContent =
          item.nombre_producto || `Producto ${item.product_id}`;
        clone.querySelector(
          ".cd_unit_price"
        ).textContent = `Precio: ${formatoCOP.format(precioNum)}`;
        clone.querySelector(".cantidad").value = item.cd_cant;
        clone.querySelector(".cantidad").dataset.price = precioNum;
        clone.querySelector(".cantidad").dataset.detalleId = item.cd_id;
        clone.querySelector(".cantidad").dataset.carId = item.car_id;
        clone.querySelector(".guardar").dataset.detalleId = item.cd_id;
        clone.querySelector(".guardar").dataset.carId = item.car_id;
        clone.querySelector(".eliminar").dataset.id = item.cd_id;
        clone.querySelector(".eliminar").dataset.carid = item.car_id;

        clone.querySelector(".subtotal").textContent =
          formatoCOP.format(subtotalItem);

        list.appendChild(clone);
        subtotalTotal += subtotalItem;
      });

      actualizarResumen(subtotalTotal);
    } catch (err) {
      
      Swal.fire({
        title: "🚨 Error de conexión",
        text: "No se pudo establecer conexión. Intenta más tarde.",
        icon: "error",
        showConfirmButton: false,
        timer: 3500,
        timerProgressBar: true,
      });
      list.querySelectorAll("li:not(.template)").forEach((el) => el.remove());
      actualizarResumen(0);
      carritoActivoId = null;
    }
  }

  list.addEventListener("click", async (e) => {
    if (e.target.classList.contains("eliminar")) {
      const { id: detalleId, carid: carId } = e.target.dataset;
      try {
        await fetch(`${API_BASE}/carro/eliminar/${detalleId}/${carId}`, {
          method: "DELETE",
        });
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
          body: JSON.stringify({ detalle_cantidad: nuevaCantidad }),
        });
        cargarDetalle();
      } catch (err) {
        Swal.fire({
          title: "🚨 Error de conexión",
          text: "Error al actualizar la cantidad.",
          icon: "error",
          showConfirmButton: false,
          timer: 3500,
          timerProgressBar: true,
        });
      }
    }
  });

  finalizarBtn.addEventListener("click", async () => {
    if (!carritoActivoId) {
      Swal.fire({
        icon: "warning",
        title: "Sin carrito activo",
        text: "No hay carrito activo para finalizar.",
        confirmButtonColor: "#0d6efd",
      });
      return;
    }

    try {
      const resp = await fetch(
        `${API_BASE}/carro/finalizar/${carritoActivoId}`,
        {
          method: "PUT",
        }
      );
      const result = await resp.json();

      if (result.success) {
        Swal.fire({
          icon: "success",
          title: "✅ Compra finalizada con éxito.",
          text: "La compra se ha completado correctamente.",
          confirmButtonColor: "#198754",
        }).then(() => {
          cargarDetalle(); 
        });
      } else {
        Swal.fire({
          icon: "error",
          title: "❌ No se pudo finalizar la compra",
          text: result.message || "",
          confirmButtonColor: "#dc3545",
        });
      }
    } catch (err) {
      Swal.fire({
        icon: "error",
        title: "Error de conexión",
        text: "Error al finalizar la compra.",
        confirmButtonColor: "#dc3545",
      });
    }
  });

  cargarDetalle();
});
