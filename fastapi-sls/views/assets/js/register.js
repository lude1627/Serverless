// 📄 /views/assets/js/login.js

document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("formRegistro");

    if (!registerForm) return;

    registerForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = {
            user_cc: document.getElementById("user_cc").value,
            username: document.getElementById("username").value,
            phone: document.getElementById("phone").value,
            email: document.getElementById("email").value,
            password: document.getElementById("password").value
        };

        try {
            const response = await fetch("http://localhost:8000/user/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                Swal.fire({
                    icon: "success",
                    title: "Registro Exitoso",
                    text: result.message,
                    showConfirmButton: false,
                    timer: 2000
                }).then(() => {
                
                        window.location.href = "/views/login/login.html";
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