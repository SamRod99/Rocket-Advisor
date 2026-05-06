document.getElementById("btn").addEventListener("click", () => {

  chrome.storage.local.get("ultimoAnalisis", (data) => {

    if (!data.ultimoAnalisis) {
      document.getElementById("resultado").textContent = "No hay datos";
      return;
    }

    let r = data.ultimoAnalisis;

    document.getElementById("resultado").textContent =
      r.riesgo === "alto"
        ? "Sitio peligroso"
        : "Sitio seguro";
  });
});