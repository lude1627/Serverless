document.addEventListener("DOMContentLoaded", async () => {
  const tbody = document.querySelector("tbody");

  try {
    const response = await fetch("http://localhost:8000/category/view/data");
    const result = await response.json();

    if (result.success && result.data.length > 0) {
      tbody.innerHTML = "";
      result.data.forEach((cat) => {
        const row = `
          <tr>
  <td>${cat.cat_id}</td>
  <td>${cat.cat_name}</td>
  <td>
    ${
      cat.cat_status === "1"
        ? '<span class="badge bg-success">Activo</span>'
        : '<span class="badge bg-secondary">Inactivo</span>'
    }
  </td>
  <td class="text-end">
    <button class="btn btn-sm btn-warning btn-editar"
      data-id="${cat.cat_id}"
      data-nombre="${cat.cat_name}"
      data-estado="${cat.cat_status}"
      data-bs-toggle="modal"
      data-bs-target="#modalEditarCategoria">
      ✏ Editar
    </button>
    <button class="btn btn-sm btn-danger btn-eliminar" data-id="${
      cat.cat_id
    }">🗑 Eliminar</button>
  </td>
</tr>

        `;
        tbody.insertAdjacentHTML("beforeend", row);
      });
    } else {
      tbody.innerHTML = `<tr><td colspan="3" class="text-center">No hay categorías</td></tr>`;
    }
  } catch (error) {
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

const formCrear = document.querySelector("#modalCategoria form");

formCrear.addEventListener("submit", async (e) => {
  e.preventDefault();

  const nombre = document.querySelector("#nombreCat").value;

  try {
    const response = await fetch("http://localhost:8000/category/create", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: nombre }),
    });

    const result = await response.json();

    if (result.success) {
      Swal.fire({
        title: "¡Categoría creada!",
        text: `Se creó la categoría "${nombre}" correctamente.`,
        icon: "success",
        timer: 1500,
        showConfirmButton: false,
      }).then(() => location.reload());
    } else {
      Swal.fire({
        icon: "error",
        title: "Error",
        text: "No se pudo crear la categoría",
        timer: 2000,
        showConfirmButton: false,
        timerProgressBar: true,
      });
    }
  } catch (error) {
    Swal.fire({
      icon: "error",
      title: "Error en la petición",
      text: "No se pudo conectar con el servidor.",
    });
  }
});

document.addEventListener("click", (e) => {
  if (e.target.classList.contains("btn-editar")) {
    const id = e.target.getAttribute("data-id");
    const name = e.target.getAttribute("data-nombre");
    const status = e.target.getAttribute("data-estado");

    document.querySelector("#editCategoriaId").value = id;
    document.querySelector("#editCategoriaNombre").value = name;
    document.querySelector("#editCategoriaEstado").value = status;

    console.log("Categoría cargada para editar - ID:", id, "Nombre:", name);
  }
});


const formEditar = document.querySelector("#modalEditarCategoria form");

formEditar.addEventListener("submit", async (e) => {
  e.preventDefault();

  const id = document.querySelector("#editCategoriaId").value;
  const nombre = document.querySelector("#editCategoriaNombre").value;
  const estado = document.querySelector("#editCategoriaEstado").value;

  try {
    const response = await fetch(
      `http://localhost:8000/category/update/${id}`,
      {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: nombre, status: estado }),
      }
    );

    const result = await response.json();

    if (result.success) {
      Swal.fire({
        title: "¡Categoría actualizada!",
        text: `Se actualizó la categoría a "${nombre}" correctamente.`,
        icon: "success",
        timer: 1500,
        showConfirmButton: false,
      }).then(() => location.reload());
    } else {
      Swal.fire({
        icon: "error",
        title: "Error",
        text: result.message,
      });
    }
  } catch (error) {
    Swal.fire({
      icon: "error",
      title: "Error en la petición",
      text: "No se pudo conectar con el servidor.",
    });
  }
});

document.addEventListener("click", async (e) => {
  if (e.target.classList.contains("btn-eliminar")) {
    const id = e.target.getAttribute("data-id");

    Swal.fire({
      title: "¿Estás seguro?",
      text: "Esta acción no se puede deshacer.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "Sí, eliminar",
      cancelButtonText: "Cancelar",
    }).then(async (result) => {
      if (result.isConfirmed) {
        try {
          const response = await fetch(
            `http://localhost:8000/category/delete/${id}`,
            {
              method: "put",
            }
          );
          const data = await response.json();

          if (data.success) {
            Swal.fire({
              title: "¡Categoría eliminada!",
              text: "La categoría fue eliminada correctamente.",
              icon: "success",
              timer: 1500,
              showConfirmButton: false,
            }).then(() => location.reload());
          } else {
            Swal.fire({
              icon: "error",
              title: "Error",
              text: "No se pudo eliminar la categoría",
            });
          }
        } catch (error) {
          Swal.fire({
            icon: "error",
            title: "Error en la petición",
            text: "No se pudo conectar con el servidor.",
          });
        }
      }
    });
  }
});
