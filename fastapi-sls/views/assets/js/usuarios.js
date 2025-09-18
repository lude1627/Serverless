// API_BASE esté definido
const API_BASE = "http://localhost:8000";

// Cargar opciones de selección
document.addEventListener("DOMContentLoaded", function () {
  const addModal = document.getElementById("modalUsuario");
  if (addModal) {
    addModal.addEventListener("shown.bs.modal", cargarSelectsAgregarUsuario);
  }
});

// Registrar usuarido panel admin
document
  .getElementById("formAgregarUsuario")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
      user_cc: parseInt(document.getElementById("adduser_cc").value),
      username: document.getElementById("adduser_name").value.trim(),
      phone: parseInt(document.getElementById("adduser_phone").value),
      email: document.getElementById("adduser_mail").value.trim(),
      user_type: parseInt(document.getElementById("addtuser_type").value),
      user_status: parseInt(document.getElementById("adduser_status").value),
    };

    // validar
    if (isNaN(data.user_cc) || data.user_cc <= 0) {
      Swal.fire(
        "⚠️ Error",
        "La cédula es requerida y debe ser un número válido",
        "error"
      );
      return;
    }

    if (!data.username) {
      Swal.fire("⚠️ Error", "El nombre de usuario es requerido", "error");
      return;
    }

    if (isNaN(data.phone) || data.phone <= 0) {
      Swal.fire(
        "⚠️ Error",
        "El teléfono es requerido y debe ser un número válido",
        "error"
      );
      return;
    }

    if (!data.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
      Swal.fire("⚠️ Error", "El correo electrónico no es válido", "error");
      return;
    }

    if (isNaN(data.user_type) || data.user_type < 1) {
      Swal.fire("⚠️ Error", "Selecciona un tipo de usuario válido", "error");
      return;
    }

    if (isNaN(data.user_status) || data.user_status < 0) {
      Swal.fire("⚠️ Error", "Selecciona un estado válido", "error");
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/user/admin/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (result.success) {
        Swal.fire({
          icon: "success",
          title: "✅ Usuario agregado",
          timer: 1500,
          showConfirmButton: false,
        });

        // Limpia el formulario y cierra modal
        document.getElementById("formAgregarUsuario").reset();
        const modal = bootstrap.Modal.getInstance(
          document.getElementById("modalAgregarUsuario")
        );
        modal.hide();

        // Recargar la lista de usuarios
        cargarUsuarios();
      } else {
        Swal.fire(
          "❌ Error",
          result.message || "No se pudo agregar el usuario",
          "error"
        );
      }
    } catch (error) {
      console.error("Error al agregar usuario:", error);
      Swal.fire(
        "⚠️ Error inesperado",
        "No se pudo agregar el usuario",
        "error"
      );
    }
  });

// Modal editar
async function abrirModalEditar(user_cc) {
  try {
    // Petición al backend para traer datos de un usuario
    const response = await fetch(`${API_BASE}/user/view/${user_cc}`);
    const result = await response.json();

    if (result.success) {
      const usuario = result.data;

      // Cargar opciones de selección
      await cargarSelectsEditarUsuario();

      // Rellenar campos de formulario
      document.getElementById("editusuarioId").value = usuario.user_id;
      document.getElementById("edituser_cc").value = usuario.user_cc;
      document.getElementById("edituser_name").value = usuario.username;
      document.getElementById("edituser_phone").value = usuario.phone;
      document.getElementById("edituser_mail").value = usuario.email;

      // Establecer rol y estado
      document.getElementById("edituser_type").value = usuario.user_type;
      document.getElementById("edituser_status").value = usuario.status;

      console.log("User data loaded:", usuario);
      console.log("Role from backend:", usuario.user_type);
      console.log("Status from backend:", usuario.status);

      const modal = new bootstrap.Modal(
        document.getElementById("modalEditarUsuario")
      );
      modal.show();
    } else {
      Swal.fire("Error", result.message || "Usuario no encontrado", "error");
    }
  } catch (error) {
    console.error("Error loading user:", error);
    Swal.fire("Error", "No se pudo cargar el usuario", "error");
  }
}

// Cargar opciones de selección
async function cargarSelectsEditarUsuario() {
  try {
    // Cargar tipos de usuarios (roles)
    const userTypeSelect = document.getElementById("edituser_type");
    if (userTypeSelect) {
      userTypeSelect.innerHTML = `
        <option value="1">Administrador</option>
        <option value="2">Cliente</option>
      `;
    }

    // Opciones de estado
    const statusSelect = document.getElementById("edituser_status");
    if (statusSelect) {
      statusSelect.innerHTML = `
        <option value="1">Activo</option>
        <option value="0">Inactivo</option>
      `;
    }

    console.log("Select options loaded successfully");
  } catch (error) {
    console.error("Error loading select options:", error);
  }
}

// formulario de usuario
document
  .getElementById("formEditarUsuario")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    // Get form values
    const user_cc = parseInt(document.getElementById("edituser_cc").value);
    const username = document.getElementById("edituser_name").value.trim();
    const phone = parseInt(document.getElementById("edituser_phone").value);
    const email = document.getElementById("edituser_mail").value.trim();
    const user_type = parseInt(document.getElementById("edituser_type").value);
    const user_status = parseInt(
      document.getElementById("edituser_status").value
    );

    // Basic validation
    if (!user_cc || user_cc <= 0) {
      Swal.fire("Error", "La cédula debe ser un número válido", "error");
      return;
    }
    if (!username) {
      Swal.fire("Error", "El nombre es obligatorio", "error");
      return;
    }
    if (!phone || phone <= 0) {
      Swal.fire("Error", "El teléfono debe ser un número válido", "error");
      return;
    }
    if (!email || !email.includes("@")) {
      Swal.fire("Error", "El correo electrónico no es válido", "error");
      return;
    }

    const usuarioActualizado = {
      user_cc: user_cc,
      username: username,
      phone: phone,
      email: email,
      user_type: user_type,
      user_status: user_status,
      password: null, // La contraseña es opcional
    };

    console.log("Sending update data:", usuarioActualizado);

    try {
      const response = await fetch(`${API_BASE}/user/admin/update`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify(usuarioActualizado),
      });

      const result = await response.json();

      if (response.ok && result.success) {
        Swal.fire({
          icon: "success",
          title: "✅ Usuario actualizado",
          text: result.message,
          timer: 1500,
          showConfirmButton: false,
        });

        // Close modal
        const modal = bootstrap.Modal.getInstance(
          document.getElementById("modalEditarUsuario")
        );
        if (modal) {
          modal.hide();
        }

        // Reload table
        if (typeof cargarUsuarios === "function") {
          cargarUsuarios();
        }
      } else {
        console.error("Update failed:", result);
        Swal.fire({
          icon: "error",
          title: "❌ Error",
          text: result.message || "No se pudo actualizar el usuario",
        });
      }
    } catch (error) {
      console.error("Error updating user:", error);
      Swal.fire({
        icon: "error",
        title: "⚠️ Error inesperado",
        text: "Ocurrió un problema al actualizar el usuario",
      });
    }
  });

// Función de carga de usuarios
async function cargarUsuarios() {
  try {
    const response = await fetch(`${API_BASE}/user/view/all`);
    const result = await response.json();

    const tbody = document.querySelector("#tablaUsuarios tbody");
    if (!tbody) return;

    if (result.success && result.data) {
      tbody.innerHTML = "";
      result.data.forEach((usuario, index) => {
        // 🎨 Badge de tipo de usuario (rol)
        const roleBadge =
          usuario.user_type == 1
            ? '<span class="badge bg-primary"><i class="fas fa-user-shield"></i>Admin</span>'
            : '<span class="badge bg-success"><i class="fas fa-user"></i> Cliente</span>';

        // 🎨 Badge de estado
        const statusBadge =
          usuario.status == 1
            ? '<span class="badge bg-success"><i class="fas fa-check-circle"></i> Activo</span>'
            : '<span class="badge bg-danger"><i class="fas fa-times-circle"></i> Inactivo</span>';

        tbody.innerHTML += `
          <tr>
            <td><strong>${index + 1}</strong></td>
            <td>${usuario.user_cc}</td>
            <td>${usuario.username}</td>
            <td><i class="fas fa-phone"></i> ${usuario.phone}</td>
            <td><i class="fas fa-envelope"></i> ${usuario.email}</td>
            <td>${roleBadge}</td>
            <td>${statusBadge}</td>
            <td class="text-end">
              <button class="btn btn-warning btn-sm me-1" onclick="abrirModalEditar(${
                usuario.user_cc
              })">
                ✏ Editar
              </button>
            </td>
          </tr>
        `;
      });
    } else {
      tbody.innerHTML = `
        <tr>
          <td colspan="8" class="text-center text-muted">
            ${result.message || "No hay usuarios registrados"}
          </td>
        </tr>
      `;
    }
  } catch (error) {
    console.error("Error loading users:", error);
    const tbody = document.querySelector("#tablaUsuarios tbody");
    if (tbody) {
      tbody.innerHTML = `
        <tr>
          <td colspan="8" class="text-center text-danger">
            Error al cargar usuarios
          </td>
        </tr>
      `;
    }
  }
}

//Cargar usuarios
document.addEventListener("DOMContentLoaded", function () {
  cargarUsuarios();
});

// Cargar opciones de selección
async function cargarSelectsAgregarUsuario() {
  try {
    const userTypeSelect = document.getElementById("adduser_type");
    if (userTypeSelect) {
      userTypeSelect.innerHTML = `
        <option value="">Seleccionar rol</option>
        <option value="1">Administrador</option>
        <option value="2">Cliente</option>
      `;
    }

    const statusSelect = document.getElementById("adduser_status");
    if (statusSelect) {
      statusSelect.innerHTML = `
        <option value="">Seleccionar estado</option>
        <option value="1">Activo</option>
        <option value="0">Inactivo</option>
      `;
    }
  } catch (error) {
    console.error("Error loading add user select options:", error);
  }
}

// 📌 ELIMINAR USUARIO
async function eliminarUsuario(user_cc) {
  const confirmacion = await Swal.fire({
    title: "¿Estás seguro?",
    text: "Esta acción no se puede deshacer",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Sí, eliminar",
    cancelButtonText: "Cancelar",
  });

  if (confirmacion.isConfirmed) {
    try {
      const response = await fetch(`${API_BASE}/user/delete/${user_cc}`, {
        method: "DELETE",
      });
      const result = await response.json();

      if (result.success) {
        Swal.fire(
          "Eliminado",
          result.message || "Usuario eliminado",
          "success"
        );
        cargarUsuarios(); // recargar la tabla
      } else {
        Swal.fire(
          "Error",
          result.message || "No se pudo eliminar el usuario",
          "error"
        );
      }
    } catch (error) {
      console.error("Error eliminando usuario:", error);
      Swal.fire("Error", "No se pudo eliminar el usuario", "error");
    }
  }
}
