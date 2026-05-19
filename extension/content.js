console.log("[Rocket Advisor] Content script cargado");

chrome.runtime.onMessage.addListener((msg) => {

  if (msg.accion !== "alerta" && msg.accion !== "sospechoso" && msg.accion !== "seguro") return;

  // Eliminar banner anterior si existe
  const existente = document.getElementById("rocket-banner");
  if (existente) existente.remove();

  const banner = document.createElement("div");
  banner.id = "rocket-banner";

  Object.assign(banner.style, {
    position:   "fixed",
    top:        "0",
    left:       "0",
    width:      "100%",
    padding:    "12px",
    textAlign:  "center",
    zIndex:     "2147483647", 
    fontWeight: "bold",
    fontSize:   "15px",
    cursor:     "pointer"
  });

  if (msg.accion === "alerta") {
    banner.style.background = "#ff4d4d";
    banner.style.color      = "white";
    banner.textContent      = msg.mensaje;
  } else if (msg.accion === "sospechoso") {
    banner.style.background = "#ffcc00";
    banner.style.color      = "black";
    banner.textContent      =  msg.mensaje;
  }else if(msg.accion == "seguro"){
    banner.style.background = "#20c000";
    banner.style.color      = "black";
    banner.textContent      =  msg.mensaje;
  }

  banner.addEventListener("click", () => banner.remove());

  document.body.appendChild(banner);

  //cierre de banner automatico 5s para alto, 4s para sospechoso
  const duracion = msg.accion === "alerta" ? 5000 : msg.accion === "sospechoso" ? 4000 : 3000;
  setTimeout(() => banner.remove(), duracion);
});