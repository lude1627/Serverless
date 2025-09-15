async function loadComponent(id, file) {
  try {
    const res = await fetch(file);
    const html = await res.text();
    document.getElementById(id).innerHTML = html;
  } catch (error) {
    console.error("Error al cargar " + file, error);
  }
}

// Cargar header y footer en la página
loadComponent("header", "/fastapi-sls/view/refence/headers_sesion.html");
loadComponent("footer", "/fastapi-sls/view/refence/footer_sesion.html");
