// 📄 /views/assets/js/login.js

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");

    if (!loginForm) return;

    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = {
            user_cc: document.getElementById("user_cc").value,
            password: document.getElementById("password").value
        };

        try {
            const response = await fetch("http://localhost:8000/login/sign_in", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                Swal.fire({
                    icon: "success",
                    title: "¡Bienvenido!",
                    text: result.message,
                    showConfirmButton: false,
                    timer: 2000
                }).then(() => {
                    // Redirigir según tipo de usuario

                    if (result.user_type === 1) {

                        window.location.href = "/views/admin/admin_usuarios.html";
                    } else {
                        window.location.href = "/views/producto/producto.html";
                    }
                });
            } else {
                Swal.fire({
                    icon: "error",
                    title: "Error",
                    text: result.message,
                    confirmButtonColor: "#d33"
                });
            }
        } catch (error) {
            console.error("Error en la conexión:", error);
            Swal.fire({
                icon: "error",
                title: "Problema de conexión",
                text: "No se pudo contactar al servidor. Intenta de nuevo.",
                confirmButtonColor: "#d33"
            });
        }
    });
});