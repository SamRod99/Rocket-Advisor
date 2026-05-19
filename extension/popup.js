document.addEventListener("DOMContentLoaded", () => {
    
    document.getElementById("btn").addEventListener("click", () => {
        
        chrome.storage.local.get("ultimoAnalisis", (data) => {

            if (!data.ultimoAnalisis) {
                document.getElementById("resultado").textContent = "No hay datos";
                document.getElementById("resultado").style.color = "#cbd5e1";
                return;
            }

            let r = data.ultimoAnalisis;


            if (r.riesgo === "alto") {
                document.getElementById("resultado").textContent = "Sitio peligroso";
                document.getElementById("resultado").style.color = "#f87171";
            } else {
                document.getElementById("resultado").textContent = "Sitio seguro";
                document.getElementById("resultado").style.color = "#4ade80";
            }
        });
    });

});
