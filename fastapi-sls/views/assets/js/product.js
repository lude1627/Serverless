document.addEventListener("DOMContentLoaded", async () => {
    const container = document.querySelector("main.container");
    const template = document.getElementById("product-template");

    if (!container || !template) return;

    try {
        const response = await fetch("http://localhost:8000/product/view/data", {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });

        const result = await response.json();

        if (result.success && Array.isArray(result.data) && result.data.length > 0) {
            const fragment = document.createDocumentFragment();

            result.data.forEach(producto => {
                // Clonar el template
                const clone = template.content.cloneNode(true);

                // Asignar datos
                clone.querySelector(".card-title").textContent = producto.nombre;
                clone.querySelector(".desc").textContent = producto.descripcion;
                clone.querySelector(".cant").textContent = producto.cantidad;
                clone.querySelector(".price").textContent = producto.precio;
                clone.querySelector(".cat").textContent = `Categoría: ${producto.categoria}`;

                // Opcional: agregar funcionalidad al botón
                clone.querySelector(".add-to-cart-btn").addEventListener("click", () => {
                    console.log(`Agregando al carrito: ${producto.nombre}`);
                    try {
                        // Aquí tomas el ID del usuario desde la sesión o storage
                        const userCc = sessionStorage.getItem("user_cc");
                        if (!userCc) {
                            alert("Debes iniciar sesión para agregar productos");
                            return;
                        }

                        const payload = {
                            user_cc: Number(userCc),          // ID del usuario
                            product_id: producto.id,          // Debe venir en el JSON de backend
                            cantidad: 1                       // o un valor elegido por el usuario
                        };

                        const resp = await fetch("http://localhost:8000/carro/agregar", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify(payload)
                        });

                        const data = await resp.json();
                        if (!resp.ok || !data.success) {
                            throw new Error(data.message || "No se pudo agregar");
                        }

                        alert(`Producto "${producto.nombre}" agregado al carrito`);
                        // aquí puedes actualizar un contador del carrito en el header, etc.
                    } catch (err) {
                        console.error(err);
                        alert("Error al agregar al carrito");
                    }
                });

                fragment.appendChild(clone);
            });

            container.appendChild(fragment);
        } else {
            container.innerHTML += `<p class="text-center">No hay productos disponibles.</p>`;
        }
    } catch (error) {
        console.error("Error al cargar productos:", error);
        container.innerHTML += `<p class="text-center text-danger">Error de conexión con el servidor.</p>`;
    }
});
