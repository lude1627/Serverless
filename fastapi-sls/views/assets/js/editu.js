

document.addEventListener("DOMContentLoaded", () => {
    const userCcInput   = document.getElementById("user_cc");
    const usernameInput = document.getElementById("username");
    const phoneInput    = document.getElementById("phone");
    const emailInput    = document.getElementById("email");
    const passwordInput = document.getElementById("password");

    const btnVerDatos   = document.getElementById("btnVerDatos");
    const form          = document.querySelector("form");

    // 👉 Cargar datos del usuario
    btnVerDatos.addEventListener("click", async () => {
        try {
            const user_cc = userCcInput.value.trim();
            if (!user_cc) {
                Swal.fire("Atención", "Ingrese el N° de Identificación para consultar", "warning");
                return;
            }

            const resp = await fetch(`/user/view/${user_cc}`);
            if (!resp.ok) throw new Error("No se pudo obtener la información");

            const data = await resp.json();

            
            usernameInput.value = data.user_name || "";
            phoneInput.value    = data.phone     || "";
            emailInput.value    = data.email     || "";

            Swal.fire("Datos cargados", "Información obtenida correctamente", "success");
        } catch (err) {
            console.error(err);
            Swal.fire("Error","No fue posible cargar los datos", "error");
        }
    });

    // 👉 Actualizar datos del usuario
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        try {
            const payload = {
                user_cc:  userCcInput.value.trim(),
                user_name: usernameInput.value,
                phone:     phoneInput.value,
                email:     emailInput.value,
                password:  passwordInput.value
            };

            const resp = await fetch(`/user/update`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!resp.ok) throw new Error("Error al actualizar");
            const result = await resp.json();

            Swal.fire("Éxito", result.message || "Datos actualizados correctamente", "success");
        } catch (err) {
            console.error(err);
            Swal.fire("Error", "No fue posible actualizar los datos", "error");
        }
    });
});
