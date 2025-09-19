// aquí guardaremos todos los usuarios
let usuariosGlobal = [];

// API_BASE esté definido
const API_BASE = "http://localhost:8000";

// Cargar opciones de selección
document.addEventListener("DOMContentLoaded", function () {
  const addModal = document.getElementById("modalUsuario");
  if (addModal) {
    addModal.addEventListener("shown.bs.modal", cargarSelectsAgregarUsuario);
  }
});

// ✅ Cargar usuarios (única función)
async function cargarUsuarios() {
  try {
    const response = await fetch(`${API_BASE}/user/view/all`);
    const result = await response.json();

    if (result.success && result.data) {
      usuariosGlobal = result.data; // 🔑 Guardar globalmente
      renderUsuarios(usuariosGlobal);
    } else {
      usuariosGlobal = [];
      renderUsuarios([]);
    }
  } catch (error) {
    console.error("Error cargando usuarios:", error);
    usuariosGlobal = [];
    renderUsuarios([]);
  }
}

// ✅ Renderizar usuarios
function renderUsuarios(lista) {
  const tbody = document.querySelector("#tablaUsuarios tbody");
  if (!tbody) {
    console.error("No se encontró el tbody de la tabla de usuarios");
    return;
  }

  tbody.innerHTML = ""; // Limpiar tabla

  if (lista.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="8" class="text-center text-muted">
          No se encontraron usuarios
        </td>
      </tr>
    `;
    return;
  }

  lista.forEach((usuario, index) => {
    const roleBadge =
      usuario.user_type == 1
        ? '<span class="badge bg-primary"><i class="fas fa-user-shield"></i> Admin</span>'
        : '<span class="badge bg-success"><i class="fas fa-user"></i> Cliente</span>';

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
}

// ✅ Filtro por rol
document.getElementById("filtroRol").addEventListener("change", (e) => {
  const filtro = e.target.value;
  let filtrados = usuariosGlobal;

  if (filtro === "cliente") {
    filtrados = usuariosGlobal.filter((u) => u.user_type != 1);
  } else if (filtro === "admin") {
    filtrados = usuariosGlobal.filter((u) => u.user_type == 1);
  }

  console.log("🔎 Filtro:", filtro, "| Resultado:", filtrados.length);
  renderUsuarios(filtrados);
});

// ✅ Cargar usuarios al iniciar
document.addEventListener("DOMContentLoaded", cargarUsuarios);

// Registrar usuario panel admin
document
  .getElementById("formAgregarUsuario")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
      user_cc: parseInt(document.getElementById("adduser_cc").value),
      username: document.getElementById("adduser_name").value.trim(),
      phone: parseInt(document.getElementById("adduser_phone").value),
      email: document.getElementById("adduser_mail").value.trim(),
      user_type: parseInt(document.getElementById("adduser_type").value),
      user_status: parseInt(document.getElementById("adduser_status").value),
    };

    // Validaciones
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
    if (isNaN(data.user_status) || data.user_status < -1) {
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
      console.log(result); // Para depuración

      if (result.success) {
        Swal.fire({
          icon: "success",
          title: "✅ Usuario agregado",
          timer: 1500,
          showConfirmButton: false,
        });

        // Limpia el formulario
        document.getElementById("formAgregarUsuario").reset();

        // Cierra modal de forma segura
        const modalEl = document.getElementById("modalAgregarUsuario");
        if (modalEl) {
          let modalInstance = bootstrap.Modal.getInstance(modalEl);
          if (modalInstance) modalInstance.hide();
        }

        // Recarga usuarios
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
    const response = await fetch(`${API_BASE}/user/view/${user_cc}`);
    const result = await response.json();

    if (result.success) {
      const usuario = result.data;

      await cargarSelectsEditarUsuario();

      document.getElementById("editusuarioId").value = usuario.user_id;
      document.getElementById("edituser_cc").value = usuario.user_cc;
      document.getElementById("edituser_name").value = usuario.username;
      document.getElementById("edituser_phone").value = usuario.phone;
      document.getElementById("edituser_mail").value = usuario.email;
      document.getElementById("edituser_type").value = usuario.user_type;
      document.getElementById("edituser_status").value = usuario.status;

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
    const userTypeSelect = document.getElementById("edituser_type");
    if (userTypeSelect) {
      userTypeSelect.innerHTML = `
        <option value="">Seleccionar rol</option>
        <option value="1">Administrador</option>
        <option value="2">Cliente</option>
      `;
    }

    const statusSelect = document.getElementById("edituser_status");
    if (statusSelect) {
      statusSelect.innerHTML = `
       <option value="">Seleccionar estado</option>
        <option value="1">Activo</option>
        <option value="0">Inactivo</option>
      `;
    }
  } catch (error) {
    console.error("Error loading select options:", error);
  }
}

// formulario de usuario (editar)
document
  .getElementById("formEditarUsuario")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const user_cc = parseInt(document.getElementById("edituser_cc").value);
    const username = document.getElementById("edituser_name").value.trim();
    const phone = parseInt(document.getElementById("edituser_phone").value);
    const email = document.getElementById("edituser_mail").value.trim();
    const user_type = parseInt(document.getElementById("edituser_type").value);
    const user_status = parseInt(document.getElementById("edituser_status").value);

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
      user_cc,
      username,
      phone,
      email,
      user_type,
      user_status,
      password: null,
    };

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

        const modal = bootstrap.Modal.getInstance(
          document.getElementById("modalEditarUsuario")
        );
        if (modal) modal.hide();

        cargarUsuarios();
      } else {
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

// Cargar opciones de selección para agregar
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
        cargarUsuarios();
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
