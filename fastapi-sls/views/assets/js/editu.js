const API_BASE = "http://localhost:8000";

const userCc = sessionStorage.getItem("user_cc");
if (!userCc) {
  window.location.href = "/views/login/login.html";
}

let userCcInput, usernameInput, phoneInput, emailInput, form;

document.addEventListener("DOMContentLoaded", () => {
  userCcInput = document.getElementById("user_cc");
  usernameInput = document.getElementById("username");
  phoneInput = document.getElementById("phone");
  emailInput = document.getElementById("email");
  form = document.querySelector("form");

  cargarDatosUsuario(userCc);

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    actualizarUsuario();
  });

  document.getElementById("logoutBtn").addEventListener("click", () => {
    sessionStorage.clear();
    window.location.href = "/views/login/login.html";
  });
});

async function cargarDatosUsuario(cc) {
  try {
    const resp = await fetch(`${API_BASE}/user/view/${cc}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    if (!resp.ok) throw new Error("Usuario no encontrado");

    const usuario = await resp.json();

    if (usuario.success) {
      userCcInput.value = usuario.data.user_cc;
      usernameInput.value = usuario.data.username;
      phoneInput.value = usuario.data.phone;
      emailInput.value = usuario.data.email;
    } else {
      throw new Error("Usuario no encontrado en la base de datos");
    }
  } catch (error) {


    if (error.name === "TypeError") {

      Swal.fire({
        title: "🚨 Error de conexión",
        text: "No se pudo establecer conexión. Intenta más tarde.",
        icon: "error",
        showConfirmButton: false,
        timer: 3500,
        timerProgressBar: true,
        
    });
    } else {
      Swal.fire(
        "⚠️ Error",
        "No se pudo cargar la información del usuario",
        "error"
      );
    }
  }
}


async function actualizarUsuario() {
  const usuarioActualizado = {
    user_cc: Number(userCcInput.value.trim()),
    username: usernameInput.value.trim(),
    phone: phoneInput.value.trim(),
    email: emailInput.value.trim(),
  };

  try {
    const response = await fetch(`${API_BASE}/user/update`, {
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
        text: result.message || "Datos guardados",
        timer: 1500,
        showConfirmButton: false,
      });
    } else {
      Swal.fire({
        icon: "error",
        title: "❌ Error",
        text: result.message || "No se pudo actualizar el usuario",
      });
    }
  } catch (error) {
   

    if (error.name === "TypeError") {
      Swal.fire({
        icon: "error",
        title: "🚨 Error de conexión",
        text: "No se pudo establecer conexión con el servidor. Intenta más tarde.",
      });
    } else {
      Swal.fire({
        icon: "error",
        title: "⚠️ Error inesperado",
        text: "Ocurrió un problema al actualizar el usuario",
      });
    }
  }
}
