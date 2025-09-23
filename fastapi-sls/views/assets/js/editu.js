
const API_BASE = "http://localhost:8000";

// 1️⃣ Verificar sesión
const userCc = sessionStorage.getItem("user_cc");
if (!userCc) {
    window.location.href = "/views/login/login.html";
}

// 2️⃣ Variables globales para poder usarlas en cualquier función
let userCcInput, usernameInput, phoneInput, emailInput, form;

document.addEventListener("DOMContentLoaded", () => {
    // Asignar referencias cuando el DOM está listo
    userCcInput   = document.getElementById("user_cc");
    usernameInput = document.getElementById("username");
    phoneInput    = document.getElementById("phone");
    emailInput    = document.getElementById("email");
    form          = document.querySelector("form");

    // Cargar datos del usuario
    cargarDatosUsuario(userCc);

    // Evento para actualizar
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        actualizarUsuario();
    });

    // Cerrar sesión
    document.getElementById("logoutBtn").addEventListener("click", () => {
        sessionStorage.clear();
        window.location.href = "/views/login/login.html";
    });
});

// 3️⃣ Obtener y mostrar datos
async function cargarDatosUsuario(cc) {
    try {
        const resp = await fetch(`${API_BASE}/user/view/${cc}`);
        if (!resp.ok) throw new Error("Usuario no encontrado");
        const usuario = await resp.json();

        if (usuario.success) {
            userCcInput.value   = usuario.data.user_cc;
            usernameInput.value = usuario.data.username;
            phoneInput.value    = usuario.data.phone;
            emailInput.value    = usuario.data.email;
        } else {
            throw new Error("Usuario no encontrado en la base de datos");
        }
    } catch (error) {
        console.error("Error obteniendo usuario:", error);
        Swal.fire("⚠️ Error", "No se pudo cargar la información del usuario", "error");
    }
}

// 4️⃣ Actualizar usuario
async function actualizarUsuario() {
    const usuarioActualizado = {
        user_cc: Number(userCcInput.value.trim()),
        username: usernameInput.value.trim(),
        phone: phoneInput.value.trim(),   // como string por si lleva +
        email: emailInput.value.trim()
    };

    try {
        const response = await fetch(`${API_BASE}/user/update`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
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
        console.error("Error actualizando:", error);
        Swal.fire({
            icon: "error",
            title: "⚠️ Error inesperado",
            text: "Ocurrió un problema al actualizar el usuario",
        });
    }
}

