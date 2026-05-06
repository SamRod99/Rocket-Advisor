console.log("CONTENT SCRIPT CARGADO");

chrome.runtime.onMessage.addListener((msg) => {

  // eliminar banner anterior
  const existente = document.getElementById("rocket-banner");
  if (existente) existente.remove();

  let banner = document.createElement("div");
  banner.id = "rocket-banner";

  banner.style.position = "fixed";
  banner.style.top = "0";
  banner.style.left = "0";
  banner.style.width = "100%";
  banner.style.padding = "10px";
  banner.style.textAlign = "center";
  banner.style.zIndex = "9999";
  banner.style.fontWeight = "bold";

  if (msg.accion === "alerta") {
    banner.style.background = "#ff4d4d";
    banner.style.color = "white";
    banner.textContent =  msg.mensaje;
  } else {
    banner.style.background = "#4CAF50";
    banner.style.color = "white";
    banner.textContent = "Sitio seguro";
  }

  document.body.appendChild(banner);

  setTimeout(() => {
    banner.remove
  }, 3000);
});