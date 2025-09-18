document.addEventListener("DOMContentLoaded", async () => {
    const tbody = document.querySelector("tbody");

    try {
        const response = await fetch("http://localhost:8000/category/view/data");
        const result = await response.json();

        if (result.success && result.data.length > 0) {
            tbody.innerHTML = "";
            result.data.forEach(cat => {
                const row = `
          <tr>
            <td>${cat.cat_id}</td>
            <td>${cat.cat_name}</td>
            <td class="text-end">
              <button class="btn btn-sm btn-warning btn-editar"
                data-id="${cat.cat_id}"
                data-nombre="${cat.cat_name}"
                data-bs-toggle="modal"
                data-bs-target="#modalEditarCategoria">
                ✏ Editar
              </button>
              <button class="btn btn-sm btn-danger btn-eliminar" data-id="${cat.cat_id}">🗑 Eliminar</button>
            </td>
          </tr>
        `;
                tbody.insertAdjacentHTML("beforeend", row);
            });
        } else {
            tbody.innerHTML = `<tr><td colspan="3" class="text-center">No hay categorías</td></tr>`;
        }
    } catch (error) {
        console.error("Error cargando categorías:", error);
    }
});

// Crear categoría
const formCrear = document.querySelector("#modalCategoria form");

formCrear.addEventListener("submit", async (e) => {
    e.preventDefault();

    const nombre = document.querySelector("#nombreCat").value;

    try {
        const response = await fetch("http://localhost:8000/category/create", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: nombre })
        });

        const result = await response.json();

        if (result.success) {
            Swal.fire({
                icon: "success",
                title: "¡Categoría creada!",
                text: `Se agregó la categoría "${nombre}" correctamente.`,
                confirmButtonColor: "#3085d6"
            }).then(() => location.reload());
        } else {
            Swal.fire({
                icon: "error",
                title: "Error",
                text: result.message
            });
        }
    } catch (error) {
        Swal.fire({
            icon: "error",
            title: "Error en la petición",
            text: "No se pudo conectar con el servidor."
        });
    }
});

// Editar categoría - Llenar el modal con los datos
document.addEventListener("click", (e) => {
    if (e.target.classList.contains("btn-editar")) {
        const id = e.target.getAttribute("data-id");
        const nombre = e.target.getAttribute("data-nombre");

        // Llenar los campos del modal de edición con los IDs correctos
        document.querySelector("#editCategoriaId").value = id;
        document.querySelector("#editCategoriaNombre").value = nombre;

        console.log("Categoría cargada para editar - ID:", id, "Nombre:", nombre);
    }
});

// Actualizar categoría
const formEditar = document.querySelector("#modalEditarCategoria form");

formEditar.addEventListener("submit", async (e) => {
    e.preventDefault();

    const id = document.querySelector("#editCategoriaId").value;
    const nombre = document.querySelector("#editCategoriaNombre").value;

    try {
        const response = await fetch(`http://localhost:8000/category/update/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: nombre })
        });

        const result = await response.json();

        if (result.success) {
            Swal.fire({
                icon: "success",
                title: "¡Categoría actualizada!",
                text: `Se actualizó la categoría "${nombre}" correctamente.`,
                confirmButtonColor: "#3085d6"
            }).then(() => location.reload());
        } else {
            Swal.fire({
                icon: "error",
                title: "Error",
                text: result.message
            });
        }
    } catch (error) {
        Swal.fire({
            icon: "error",
            title: "Error en la petición",
            text: "No se pudo conectar con el servidor."
        });
    }
});

// Eliminar categoría
document.addEventListener("click", async (e) => {
    if (e.target.classList.contains("btn-eliminar")) {
        const id = e.target.getAttribute("data-id");

        Swal.fire({
            title: "¿Eliminar categoría?",
            text: "Esta acción no se puede deshacer.",
            icon: "warning",
            showCancelButton: true,
            confirmButtonText: "Sí, eliminar",
            cancelButtonText: "Cancelar",
            confirmButtonColor: "#d33"
        }).then(async (result) => {
            if (result.isConfirmed) {
                try {
                    const response = await fetch(`http://localhost:8000/category/update/${id}`, {
                        method: "PUT"
                    });
                    const data = await response.json();

                    if (data.success) {
                        Swal.fire({
                            icon: "success",
                            title: "Eliminado",
                            text: "La categoría fue eliminada correctamente"
                        }).then(() => location.reload());
                    } else {
                        Swal.fire({
                            icon: "error",
                            title: "Error",
                            text: "No se pudo eliminar la categoría"
                        });
                    }
                } catch (error) {
                    Swal.fire({
                        icon: "error",
                        title: "Error en la petición",
                        text: "No se pudo conectar con el servidor."
                    });
                }
            }
        });
    }
});