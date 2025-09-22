const API_BASE = "http://localhost:8000";

const userCc = sessionStorage.getItem("user_cc");
if (!userCc) {
    window.location.href = "/views/login/login.html";
}



document.addEventListener("DOMContentLoaded", async () => {
    const container = document.querySelector("main.container");
    const template = document.getElementById("product-template");

    if (!container || !template) return;

    try {
        const response = await fetch(`${API_BASE}/product/view/data`, {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });

        const result = await response.json();

        if (result.success && Array.isArray(result.data) && result.data.length > 0) {
            const fragment = document.createDocumentFragment();

            result.data.forEach(producto => {
               
                const clone = template.content.cloneNode(true);

              
                clone.querySelector(".card-title").textContent = producto.nombre;
                clone.querySelector(".desc").textContent = producto.descripcion;
                clone.querySelector(".cant").textContent = producto.cantidad;
                clone.querySelector(".price").textContent = producto.precio;
                clone.querySelector(".cat").textContent = `Categoría: ${producto.categoria}`;


                
                clone.querySelector(".add-to-cart-btn").addEventListener("click", async () => {
                    try {
                        
                        const carritoData = {
                            user_cc: parseInt(userCc),    
                            product_id: producto.id,      
                            car_cantidad: 1                   
                        };

                        const resp = await fetch(`${API_BASE}/carro/agregar`, {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify(carritoData)
                        });

                        const data = await resp.json();

                        if (resp.ok && data.success) { 
                            Swal.fire({
                                icon: "success",
                                title: "Producto agregado",
                                text: `${producto.nombre} fue agregado al carrito`,
                                timer: 1500,
                                showConfirmButton: false
                            });
                        } else {
                            throw new Error(data.message || "Error al agregar al carrito");
                        }
                    } catch (error) {
                        console.error("Error agregando al carrito:", error);
                        Swal.fire({
                            icon: "error",
                            title: "Error",
                            text: "No se pudo agregar el producto al carrito"
                        });
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

document.getElementById("logoutBtn").addEventListener("click", () => {
    sessionStorage.clear();
    window.location.href = "/views/login/login.html";
});