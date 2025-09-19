const API_BASE = "http://localhost:8000";

// 1️⃣ Verificar sesión
const userCc = sessionStorage.getItem("user_cc");
if (!userCc) {
    window.location.href = "/views/login/login.html";
}

// 2️⃣ Cuando el DOM esté listo, cargar datos del usuario automáticamente
document.addEventListener("DOMContentLoaded", () => {
    const userCcInput   = document.getElementById("user_cc");
    const usernameInput = document.getElementById("username");
    const phoneInput    = document.getElementById("phone");
    const emailInput    = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const form          = document.querySelector("form");

    // 👉 Llamar a la función directamente usando el id guardado en sesión
    cargarDatosUsuario(userCc);
});

// 3️⃣ Función para obtener y mostrar datos del usuario
async function cargarDatosUsuario(user_Cc) {
    try {
        const resp = await fetch(`${API_BASE}/user/view/${user_Cc}`);
        if (!resp.ok) throw new Error("Usuario no encontrado");

        const usuario = await resp.json();
        console.log("usuarios", usuario);

        if (usuario.success) {
            // Rellenar los inputs del formulario de perfil
            document.getElementById("user_cc").value  = usuario.data.user_cc;
            document.getElementById("username").value = usuario.data.username;
            document.getElementById("phone").value    = usuario.data.phone;
            document.getElementById("email").value    = usuario.data.email;

       
        } else {
            throw new Error("Usuario no encontrado en la base de datos");
        }

    } catch (error) {
        console.error("Error obteniendo usuario:", error);
        Swal.fire("⚠️ Error", "No se pudo cargar la información del usuario", "error");
    }
}


form.addEventListener("submit", (e) => {
    e.preventDefault();
    actualizarUsuario();
});



async function actualizarUsuario() {
    // 👉 Tomar los valores actuales de los campos del formulario
    const usuarioActualizado = {
        user_cc: Number(userCcInput.value.trim()),      
        username: usernameInput.value.trim(),         
        phone: Number(phoneInput.value.trim()),        
        email: emailInput.value.trim()
    };

    console.log("Sending update data:", usuarioActualizado);

    try {
        const response = await fetch(`${API_BASE}/user/update`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
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
}
document.getElementById("logoutBtn").addEventListener("click", () => {
    sessionStorage.clear();
    window.location.href = "/views/login/login.html";
});
