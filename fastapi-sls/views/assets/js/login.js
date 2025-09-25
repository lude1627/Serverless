// 📄 /views/assets/js/login.js

document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");

  if (!loginForm) return;

  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
      user_cc: document.getElementById("user_cc").value,
      password: document.getElementById("password").value,
    };

    try {
      const response = await fetch("http://localhost:8000/login/sign_in", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (result.success) {
        sessionStorage.setItem("user_cc", result.user_cc);
        Swal.fire({
          icon: "success",
          title: "¡Bienvenido!",
          text: result.message,
          showConfirmButton: false,
          timer: 2000,
          timerProgressBar: true,
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
            title: "🛑 Error de autenticación",
            text: "Usuario o contraseña incorrectos.",
            icon: "error",
            showConfirmButton: false,
            timer: 3500,
            timerProgressBar: true,
        });
      }
    } catch (error) {
      // console.error("Error en la conexión:", error);
      Swal.fire({
        title: "🚨 Error de conexión",
        text: "No se pudo establecer conexión. Intenta más tarde.",
        icon: "error",
        showConfirmButton: false,
        timer: 3500,
        timerProgressBar: true,
      });
    }
  });
});
