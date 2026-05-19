document.addEventListener("DOMContentLoaded", () => {
    
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        const tab = tabs[0];
        const urlEl = document.getElementById("url-actual");

        if (!tab || !tab.url) {
            urlEl.textContent = "No disponible";
            return;
        }

        try {
            const parsed = new URL(tab.url);
            urlEl.textContent = parsed.hostname + (parsed.pathname !== "/" ? parsed.pathname : "");
        } catch {
            urlEl.textContent = tab.url;
        }
    });

    document.getElementById("btn").addEventListener("click", () => {
        
        chrome.storage.local.get("ultimoAnalisis", (data) => {

            const res = document.getElementById("resultado");

            if (!data.ultimoAnalisis) {
                res.textContent = "No hay datos";
                res.style.color = "#cbd5e1"
                return;
            }

            const r = data.ultimoAnalisis;

            if (r.riesgo === "alto") {
                res.textContent = "Sitio peligroso"
                res.style.color = "#f87171"
            } else if(r.riesgo === "sospechoso"){
                res.textContent = "Sitio sospechoso"
                res.style.color = "#fb923c"
            }else if(r.riesgo === "bajo"){
                res.textContent = "Sitio seguro"
                res.style.color = "#4ade80"
            }else{
                el.textContent = "Riesgo desconocido: " + r.riesgo;
                el.style.color = "#cbd5e1";
            }
        });
    });

});
