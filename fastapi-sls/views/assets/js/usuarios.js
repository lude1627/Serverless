modalUsuario; 
let usuariosGlobal = [];

const API_BASE = "http://localhost:8000";

document.addEventListener("DOMContentLoaded", function () {
  const addModal = document.getElementById("modalUsuario");
  if (addModal) {
    addModal.addEventListener("shown.bs.modal", cargarSelectsAgregarUsuario);
  }
});

async function cargarSelectsEditarUsuario() {
  try {
    const responseTipos = await fetch("http://localhost:8000/user-types");
    const tipos = await responseTipos.json();

    const selectTipo = document.getElementById("editTipoUsuario");
    selectTipo.innerHTML = ""; 

    tipos.data.forEach(tipo => {
      const option = document.createElement("option");
      option.value = tipo.id;
      option.textContent = tipo.nombre;
      selectTipo.appendChild(option);
    });
    const estados = [
      { value: 1, text: "Activo" },
      { value: 0, text: "Inactivo" }
    ];

    const selectEstado = document.getElementById("editEstadoUsuario");
    selectEstado.innerHTML = "";

    estados.forEach(e => {
      const option = document.createElement("option");
      option.value = e.value;
      option.textContent = e.text;
      selectEstado.appendChild(option);
    });

  } catch (error) {
    console.error("Error cargando selects:", error);
  }
}
async function cargarUsuarios() {
  try {
    const response = await fetch(`${API_BASE}/user/view/all`);
    const result = await response.json();

    if (result.success && result.data) {
      usuariosGlobal = result.data;
      renderUsuarios(usuariosGlobal);
    } else {
      usuariosGlobal = [];
      renderUsuarios([]);
    }
  } catch (error) {
    Swal.fire({
      title: "🚨 Error de conexión",
      text: "No se pudo establecer conexión. Intenta más tarde.",
      icon: "error",
      showConfirmButton: false,
      timer: 3500,
      timerProgressBar: true,
    })
    usuariosGlobal = [];
    renderUsuarios([]);
  }
}

function renderUsuarios(lista) {
  const tbody = document.querySelector("#tablaUsuarios tbody");
  if (!tbody) {
    console.error("No se encontró el tbody de la tabla de usuarios");
    return;
  }

  tbody.innerHTML = "";

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

  lista.forEach((usuario) => {
    const roleBadge =
      usuario.user_type == 1
        ? '<span class="badge bg-primary"><i class="fas fa-user-shield"></i> Admin</span>'
        : '<span class="badge bg-secondary"><i class="fas fa-user"></i> Cliente</span>';

    const statusBadge =
      usuario.status == 1
        ? '<span class="badge bg-success"><i class="fas fa-check-circle"></i> Activo</span>'
        : '<span class="badge bg-danger"><i class="fas fa-times-circle"></i> Inactivo</span>';

    tbody.innerHTML += `
      <tr>
      
        <td><strong>${usuario.user_id}</strong></td>
        <td>${usuario.user_cc}</td>
        <td>${usuario.username}</td>
        <td><i class="fas fa-phone"></i> ${usuario.phone}</td>
        <td><i class="fas fa-envelope"></i> ${usuario.email}</td>
        <td>${roleBadge}</td>
        <td>${statusBadge}</td>
        <td class="text-end">
          <button class="btn btn-warning btn-sm me-1" onclick="abrirModalEditar(${usuario.user_cc})">
            ✏ Editar
          </button>
        </td>
      </tr>
    `;
  });
}

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

document.addEventListener("DOMContentLoaded", cargarUsuarios);
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
    if (isNaN(data.user_status) || ![0,1].includes(data.user_status)) {
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
      console.log(result); 

      if (result.success) {
        Swal.fire({
          title: "✅ Éxito",
          text: "Usuario agregado correctamente",
          icon: "success",
          timer: 1000,
          timerProgressBar: true,
          showConfirmButton: false,
        });
        document.getElementById("formAgregarUsuario").reset();
        const modal = bootstrap.Modal.getInstance(
          document.getElementById("modalUsuario")
        );
        if (modal) modal.hide();
        cargarUsuarios();
      } else {
        Swal.fire(
          "❌ Error",
          result.message || "No se pudo agregar el usuario",
          "error"
        );
      }
      const modal = bootstrap.Modal.getInstance(
        document.getElementById("modalUsuario")
      );
      if (modal) modal.hide();
    } catch (error) {
      console.error("Error al agregar usuario:", error);
      Swal.fire(
        "⚠️ Error inesperado",
        "No se pudo agregar el usuario",
        "error"
      );
    }
  });
async function abrirModalEditar(user_id) {
  try {
    const response = await fetch(`${API_BASE}/user/view/admin/${user_id}`);
    const result = await response.json();

    if (result.success && result.data) {
      const usuario = result.data;

      const userTypeSelect = document.getElementById("edituser_type");
      userTypeSelect.innerHTML = `
        <option value="">Seleccionar rol</option>
        <option value="1">Administrador</option>
        <option value="2">Cliente</option>
      `;
      userTypeSelect.value = usuario.user_type; 

      const statusSelect = document.getElementById("edituser_status");
      statusSelect.innerHTML = `
        <option value="">Seleccionar estado</option>
        <option value="1">Activo</option>
        <option value="0">Inactivo</option>
      `;
      statusSelect.value = usuario.user_status; 

      document.getElementById("edituser_id").value = usuario.user_id;
      document.getElementById("edituser_cc").value = usuario.user_cc;
      document.getElementById("edituser_name").value = usuario.username;
      document.getElementById("edituser_phone").value = usuario.phone;
      document.getElementById("edituser_mail").value = usuario.email;

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
document
  .getElementById("formEditarUsuario")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const user_id = parseInt(
      document.getElementById("edituser_id").value || null
    );
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
      user_id,
      user_cc,
      username,
      phone,
      email,
      user_type,
      user_status,
      password: null,
    };

    try {
      const response = await fetch(`${API_BASE}/user/admin/update/${user_id}`, {
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
          title: "✅ Éxito",
          text: "Usuario actualizado correctamente",
          icon: "success",
          timer: 1000,
          timerProgressBar: true,
          showConfirmButton: false,
        });

        const modal = bootstrap.Modal.getInstance(
          document.getElementById("modalEditarUsuario")
        );
        if (modal) modal.hide();

        cargarUsuarios();
      } else {
        Swal.fire({
          icon: "warning",
          title: "¡No se pudo completar la accion!",
          text: result.message || "No se pudo actualizar el usuario",
          timer: 3500,
          timerProgressBar: true,
          showConfirmButton: false,
        });
      }

      const modal = bootstrap.Modal.getInstance(
        document.getElementById("modalEditarUsuario")
      );
      if (modal) modal.hide();
    } catch (error) {
      console.error("Error updating user:", error);
      Swal.fire({
        icon: "error",
        title: "⚠️ Error inesperado",
        text: "Ocurrió un problema al actualizar el usuario",
      });
    }
  });

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
        Swal.fire({
          title: "✅ Éxito",
          text: "Usuario eliminado correctamente",
          icon: "success",
          timer: 1000,
          timerProgressBar: true,
          showConfirmButton: false,
      });
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
