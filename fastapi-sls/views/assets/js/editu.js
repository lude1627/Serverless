const API_BASE = "http://localhost:8000";


document.addEventListener("DOMContentLoaded", () => {
    const userCcInput   = document.getElementById("user_cc");
    const usernameInput = document.getElementById("username");
    const phoneInput    = document.getElementById("phone");
    const emailInput    = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const form          = document.querySelector("form");

    document.getElementById("btnVerDatos").addEventListener("click", () => {
    const idUsuario = document.getElementById("user_cc").value.trim();
    cargarDatosUsuario(idUsuario);
    });


// 👉 Cargar datos del usuario

async function cargarDatosUsuario(user_cc) {
    try {
        if (!user_cc) {
            Swal.fire("Atención", "Ingrese el N° de Identificación para consultar", "warning");
            return;
        }
        const resp = await fetch(`${API_BASE}/user/view/${user_cc}`);
        if (!resp.ok) throw new Error("Usuario no encontrado");

        const usuario = await resp.json();

        console.log('usuarios', usuario);

        if(usuario.success) {

            console.log('success', usuario.success);
            // Llenar inputs del formulario de perfil
            document.getElementById("user_cc").value  = usuario.data.user_cc;
            document.getElementById("username").value = usuario.data.username;
            document.getElementById("phone").value    = usuario.data.phone;
            document.getElementById("email").value    = usuario.data.email;


            document.getElementById("perfilTabsContent")

            Swal.fire("Datos cargados", "Información obtenida correctamente", "success");
        }
        else if (!usuario || !usuario.user_cc) {
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

});