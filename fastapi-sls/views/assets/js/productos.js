const API_BASE = "http://localhost:8000";

document.addEventListener("DOMContentLoaded", function () {
  cargarProductos();
  cargarCategoriasSelect("addCategory_id");
});

// 📌 CARGAR PRODUCTOS
async function cargarProductos() {
  try {
    const response = await fetch(`${API_BASE}/product/view/data`);
    const result = await response.json();

    const tbody = document.querySelector("#tablaProductos tbody");
    tbody.innerHTML = "";

    if (result.success && result.data && result.data.length > 0) {
      result.data.forEach((prod) => {
        const precio = Number(prod.precio.replace(/[^0-9.-]+/g, "")) || 0;
        const tr = document.createElement("tr");
        tr.innerHTML = `
                    <td>${prod.id}</td>
                    <td>${prod.nombre}</td>
                    <td>${prod.descripcion}</td>
                    <td>${prod.cantidad}</td>
                    <td>$${precio.toLocaleString()}</td>
                    <td>${prod.categoria}</td>
                    <td class="text-end">
                        <button class="btn btn-sm btn-warning" onclick="abrirModalEditar(${
                          prod.id
                        })">✏ Editar</button>
                        <button class="btn btn-sm btn-danger" onclick="eliminarProducto(${
                          prod.id
                        })">🗑 Eliminar</button>
                    </td>
                `;
        tbody.appendChild(tr);
      });
    } else {
      tbody.innerHTML = `<tr><td colspan="7" class="text-center text-muted">No hay productos registrados</td></tr>`;
    }
  } catch (error) {
    // console.error("Error cargando productos:", error);
    Swal.fire({
      title: "🚨 Error de conexión",
      text: "No se pudo establecer conexión. Intenta más tarde.",
      icon: "error",
      showConfirmButton: false,
      timer: 3500,
      timerProgressBar: true,
    });
  }
}

// 📌 CARGAR CATEGORÍAS EN SELECT
async function cargarCategoriasSelect(selectId, selectedValue = null) {
  try {
    const response = await fetch(`${API_BASE}/category/view/data`);
    const result = await response.json();

    const select = document.getElementById(selectId);
    if (!select) {
      Swal.fire("❌ Error", "El select de categorías no fue encontrado", "error");
      return;
    }

    // Limpiar opciones anteriores y mostrar carga
    select.innerHTML =
      '<option value="" disabled selected>Cargando categorías...</option>';

    if (
      result.success &&
      Array.isArray(result.data) &&
      result.data.length > 0
    ) {
      // Limpiar y agregar opción por defecto
      select.innerHTML = "";
      const optionDefault = document.createElement("option");
      optionDefault.value = "";
      optionDefault.textContent = "-- Selecciona una categoría --";
      optionDefault.disabled = true;
      optionDefault.selected = !selectedValue;
      select.appendChild(optionDefault);

      // Iterar sobre el array de categorías
      result.data.forEach((cat) => {
        const option = document.createElement("option");
        option.value = cat.cat_id;
        option.textContent = cat.cat_name;
        if (selectedValue && String(selectedValue) === String(cat.cat_id)) {
          option.selected = true;
        }
        select.appendChild(option);
      });
    } else {
      select.innerHTML =
        '<option value="" disabled>No hay categorías disponibles</option>';
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
    // console.error("Error cargando categorías:", error);
    // Mostrar mensaje de error en el select
    const select = document.getElementById(selectId);
    if (select) {
      select.innerHTML =
        '<option value="" disabled>Error cargando categorías</option>';
    }
  }
}

document
  .getElementById("modalProducto")
  .addEventListener("shown.bs.modal", function () {
    cargarCategoriasSelect("addCategory_id");
  });

// 📌 CREAR PRODUCTO
document
  .getElementById("formAgregarProducto")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
      name: document.getElementById("addName").value,
      description: document.getElementById("addDescription").value,
      cant: parseInt(document.getElementById("addCant").value),
      price: parseFloat(document.getElementById("addPrice").value),
      category_id: parseInt(document.getElementById("addCategory_id").value),
    };

    if (!data.name.trim()) {
      Swal.fire("⚠️ Error", "El nombre es requerido", "error");
      return;
    }
    if (!data.description.trim()) {
      Swal.fire("⚠️ Error", "La descripción es requerida", "error");
      return;
    }
    if (isNaN(data.cant) || data.cant < 0) {
      Swal.fire("⚠️ Error", "La cantidad debe ser un número válido", "error");
      return;
    }
    if (isNaN(data.price) || data.price < 0) {
      Swal.fire("⚠️ Error", "El precio debe ser un número válido", "error");
      return;
    }
    if (isNaN(data.category_id) || !data.category_id) {
      Swal.fire("⚠️ Error", "Selecciona una categoría válida", "error");
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/product/create`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (result.success) {
        Swal.fire({
          title: "✅ Éxito",
          text: "Producto agregado correctamente",
          icon: "success",
          timer: 1000,
          timerProgressBar: true,
          showConfirmButton: false,
        }).then(() => {
          const modal = bootstrap.Modal.getInstance(
            document.getElementById("modalProducto")
          );
          modal.hide();

          document.getElementById("formAgregarProducto").reset();

          location.reload();
        });
      } else {
        Swal.fire(
          "⚠️ Error",
          result.message || "No se pudo agregar el producto",
          "error"
        );
      }
    } catch (error) {
      Swal.fire({
        title: "❌ Error",
        text: "No se pudo conectar al servidor",
        icon: "error"
    });
      // console.error("Error creando producto:", error);
    }
  });

// 📌 ABRIR MODAL EDITAR
async function abrirModalEditar(id) {
  try {
    const response = await fetch(`${API_BASE}/product/get_product/${id}`);
    const producto = await response.json();

    if (!producto || !producto.product_id) {
      throw new Error("Producto no encontrado");
    }

    // Llenar inputs del modal editar
    document.getElementById("editProductoId").value = producto.product_id;
    document.getElementById("editProductoIdVisible").value =
      producto.product_id;
    document.getElementById("editName").value = producto.product_name;
    document.getElementById("editDescription").value =
      producto.product_description;
    document.getElementById("editPrice").value = producto.product_price;
    document.getElementById("editCant").value = producto.product_cant;

    await cargarCategoriasSelect("editCategory_id", producto.category_id);

    const modal = new bootstrap.Modal(
      document.getElementById("modalEditarProducto")
    );
    modal.show();
  } catch (error) {
    console.error("Error obteniendo producto:", error);
    Swal.fire("⚠️ Error", "No se pudo cargar el producto", "error");
  }
}

// 📌 EDITAR PRODUCTO
document
  .getElementById("formEditarProducto")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    // 🔎 1. Obtener valores y validar antes de enviar
    const id = document.getElementById("editProductoId").value;
    const name = document.getElementById("editName").value.trim();
    const description = document.getElementById("editDescription").value.trim();
    const price = parseFloat(document.getElementById("editPrice").value);
    const cant = parseInt(document.getElementById("editCant").value);
    const category_id = parseInt(
      document.getElementById("editCategory_id").value
    );

    if (
      !name ||
      !description ||
      isNaN(price) ||
      isNaN(cant) ||
      isNaN(category_id)
    ) {
      Swal.fire(
        "⚠️ Campos incompletos",
        "Por favor llena todos los campos correctamente",
        "warning"
      );
      return;
    }

    const productoActualizado = {
      id,
      name,
      description,
      price,
      cant,
      category_id,
    };

    try {
      const response = await fetch(`${API_BASE}/product/edit/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(productoActualizado),
      });

      const result = await response.json();

      if (!response.ok || result.success === false) {
        throw new Error(result.message || "Error al actualizar el producto");
      }

      Swal.fire({
        title: "✅ Éxito",
        text: "Producto agregado correctamente",
        icon: "success",
        timer: 1000,
        timerProgressBar: true,
        showConfirmButton: false,
      });

      const modal = bootstrap.Modal.getInstance(
        document.getElementById("modalEditarProducto")
      );
      if (modal) modal.hide();

      if (typeof cargarProductos === "function") {
        cargarProductos();
      }
    } catch (error) {
      console.error("Error editando producto:", error);
      Swal.fire(
        "❌ Error",
        error.message || "No se pudo actualizar el producto",
        "error"
      );
    }
  });

// 📌 ELIMINAR PRODUCTO
async function eliminarProducto(id) {
  Swal.fire({
    title: "¿Estás seguro?",
    text: "Este producto se eliminará",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#d33",
    cancelButtonColor: "#3085d6",
    confirmButtonText: "Sí, eliminar",
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        const response = await fetch(`${API_BASE}/product/delete/${id}`, {
          method: "PUT",
        });

        const result = await response.json();

        if (result.success) {
          Swal.fire({
          title: "✅ Éxito",
          text: "Producto eliminado correctamente",
          icon: "success",
          timer: 100,
          timerProgressBar: true,
          showConfirmButton: false,
        }).then(() => location.reload());
        } else {
          Swal.fire(
            "⚠️ Error",
            result.message || "No se pudo eliminar",
            "error"
          );
        }
      } catch (error) {
        console.error("Error eliminando producto:", error);
        Swal.fire("❌ Error", "No se pudo conectar al servidor", "error");
      }
    }
  });
}
