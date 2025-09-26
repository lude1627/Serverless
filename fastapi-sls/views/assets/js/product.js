const API_BASE = "http://localhost:8000";

const userCc = sessionStorage.getItem("user_cc");
if (!userCc) {
  window.location.href = "/views/login/login.html";
}

document.addEventListener("DOMContentLoaded", async () => {
  const grid = document.getElementById("productosGrid");
  const template = document.getElementById("product-template");

  if (!grid || !template) return;

  mostrarSkeletons(grid);

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 8000);

  try {
    const response = await fetch(`${API_BASE}/product/view/data`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
      signal: controller.signal,
    });

    clearTimeout(timeoutId); 
    const result = await response.json();

    grid.innerHTML = "";

    if (
      result.success &&
      Array.isArray(result.data) &&
      result.data.length > 0
    ) {
      const fragment = document.createDocumentFragment();

      result.data.forEach((producto) => {
        const clone = template.content.cloneNode(true);

        clone.querySelector(".card-title").textContent = producto.nombre;
        clone.querySelector(".desc").textContent = producto.descripcion;
        clone.querySelector(
          ".cant"
        ).textContent = `Stock: ${producto.cantidad}`;
        clone.querySelector(".price").textContent = `${
          producto.precio}`;
        clone.querySelector(
          ".cat"
        ).textContent = `Categoría: ${producto.categoria}`;

        clone
          .querySelector(".add-to-cart-btn")
          .addEventListener("click", async () => {
            try {
              const carritoData = {
                user_cc: parseInt(userCc),
                product_id: producto.id,
                car_cantidad: 1,
              };

              const resp = await fetch(`${API_BASE}/carro/agregar`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(carritoData),
              });

              const data = await resp.json();

              if (resp.ok && data.success) {
                Swal.fire({
                  icon: "success",
                  title: "Producto agregado",
                  text: `${producto.nombre} fue agregado al carrito`,
                  timer: 1000,
                  showConfirmButton: false,
                });
              } else {
                throw new Error(data.message || "Error al agregar al carrito");
              }
            } catch (error) {
              console.error("Error agregando al carrito:", error);
              Swal.fire({
                icon: "info",
                title: "Ups...",
                text: "En este momento este producto no está disponible",
                timer: 2000,
                showConfirmButton: false,
              });
            }
          });

        fragment.appendChild(clone);
      });

      grid.appendChild(fragment);
    }
  } catch (error) {
    clearTimeout(timeoutId); 
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

document.getElementById("logoutBtn").addEventListener("click", () => {
  sessionStorage.clear();
  window.location.href = "/views/login/login.html";
});

function mostrarSkeletons(grid) {
  grid.innerHTML = `
      ${Array(12)
        .fill()
        .map(
          () => `
        <div class="col-sm-6 col-md-4 col-lg-3">
          <div class="card h-100 shadow-sm p-3">
            <div class="skeleton skeleton-card"></div>
            <div class="skeleton skeleton-text" style="width: 80%"></div>
            <div class="skeleton skeleton-text" style="width: 60%"></div>
          </div>
        </div>
      `
        )
        .join("")}
    `;
}
