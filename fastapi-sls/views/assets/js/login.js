// 📄 /views/assets/js/login.js

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");

    if (!loginForm) return; // Si no existe el formulario, no hace nada

    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Capturamos los datos del formulario
        const data = {
            user_cc: document.getElementById("user_cc").value,
            password: document.getElementById("password").value
        };

        try {
            const response = await fetch("http://127.0.0.1:8000/login/sign_in", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                alert(result.message);

                // 🔑 Redirección según tipo de usuario
                if (result.message.includes("1")) {
                    window.location.href = "/views/admin/admin_usuarios.html";
                } else {
                    window.location.href = "/views/producto/producto.html";
                }
            } else {
                alert(result.message);
            }
        } catch (error) {
            console.error("Error en la conexión:", error);
            alert("Hubo un problema al iniciar sesión.");
        }
    });
});
