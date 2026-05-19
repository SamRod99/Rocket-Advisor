const ventanaEnAnalisis = new Set();
const ultimaUrlPorVentana = new Map();

function analizarURL(url, tabId) {
  ultimaUrlPorVentana.set(tabId, url); // ← gaudarmos la url antes del fetch

  fetch("http://localhost:5000/analizar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url: url })
  })
  .then(res => res.json())
  .then(data => {
    let resultado = { url, tabId, timestamp: Date.now(), riesgo: data.riesgo };
    chrome.storage.local.set({ ultimoAnalisis: resultado });
    console.log("[Rocket Advisor]", resultado);

    if (ultimaUrlPorVentana.get(tabId) !== url) return; 

    if (resultado.riesgo === "alto") {
      chrome.tabs.sendMessage(tabId, {
        accion: "alerta",
        mensaje: "Sitio malicioso detectado"
      }, () => { if (chrome.runtime.lastError) console.warn("[Rocket Advisor]", chrome.runtime.lastError.message); });

    } else if (resultado.riesgo === "sospechoso") {
      chrome.tabs.sendMessage(tabId, {
        accion: "sospechoso",
        mensaje: "Sitio sospechoso detectado"
      }, () => { if (chrome.runtime.lastError) console.warn("[Rocket Advisor]", chrome.runtime.lastError.message); });

    } else if(resultado.riesgo === "bajo"){
      chrome.tabs.sendMessage(tabId,{
        accion: "seguro",
        mensaje: "Sitio seguro"
      }, () => { if (chrome.runtime.lastError) console.warn("[Rocket Advisor]", chrome.runtime.lastError.message); });
    }
  })
  .catch(err => console.error("[Rocket Advisor] Error conectando con backend:", err));
}

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url) {
    if (tab.url.startsWith("chrome://") || tab.url.startsWith("brave://")) return;

    ventanaEnAnalisis.add(tabId);
    analizarURL(tab.url, tabId);
    setTimeout(() => ventanaEnAnalisis.delete(tabId), 1000);
  }
});

chrome.tabs.onActivated.addListener(({ tabId }) => {
  if (ventanaEnAnalisis.has(tabId)) {
    ventanaEnAnalisis.delete(tabId);
    return;
  }

  chrome.tabs.get(tabId, (tab) => {
    if (chrome.runtime.lastError || !tab || !tab.url) return;
    if (tab.url.startsWith("chrome://") || tab.url.startsWith("brave://")) return;

    analizarURL(tab.url, tabId);
  });
});