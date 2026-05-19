document.addEventListener("DOMContentLoaded", () => {
    const displayPagina = document.getElementById("pagina");
    const displayResultado = document.getElementById("resultado");
    const boton = document.getElementById("btn");

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs && tabs.length > 0) {
            displayPagina.textContent = tabs[0].url;
        } else {
            displayPagina.textContent = "No disponible";
        }
    });

    boton.addEventListener("click", () => {
        chrome.storage.local.get("ultimoAnalisis", (data) => {
            
            if (!data || !data.ultimoAnalisis) {
                displayResultado.textContent = "No hay datos";
                displayResultado.style.color = "#94a3b8";
                return;
            }

            let r = data.ultimoAnalisis;

            if (r.riesgo === "alto") {
                displayResultado.textContent = "Sitio peligroso";
                displayResultado.style.color = "#f87171"; // Rojo
            } else {
                displayResultado.textContent = "Sitio seguro";
                displayResultado.style.color = "#4ade80"; // Verde
            }
        });
    });
});
