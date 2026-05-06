const blacklist = [
  "roblox.com",
  "netflix.com",
  "youtube.com"
];

//esto extrae y compara con la lisna negra de arriba
function obtenerDominio(url) {
  try {
    return new URL(url).hostname;
  } catch {
    return "";
  }
}

function esURLPeligrosa(url) {
  const dominio = obtenerDominio(url);

  return blacklist.some(sitio =>
    dominio === sitio || dominio.endsWith("." + sitio)
  );
}


chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {


  if (changeInfo.status === "complete" && tab.url) {
    const url = tab.url;


    if (url.startsWith("chrome://") || url.startsWith("brave://")) return;

    console.log("[Rocket Advisor] URL detectada:", url);
    
    analizarURL(url, tabId);
  }
});

chrome.tabs.onActivated.addListener(({ tabId }) => {
  chrome.tabs.get(tabId, (tab) => {
    if (chrome.runtime.lastError || !tab.url) return;
    if (tab.url.startsWith("chrome://") || tab.url.startsWith("brave://")) return;

    console.log("[Rocket Advisor] Pestaña activa cambiada:", tab.url);
    analizarURL(tab.url, tabId);
  });
});

function analizarURL(url, tabId) {
  let resultado = {
    url: url,
    tabId: tabId,
    timestamp: Date.now(),
    esPeligrosa: false,   
    razon: null
  };


  resultado.esPeligrosa = esURLPeligrosa(url);
  //cambie esto para que funcione con la lista negra y poder enseñarlo al profe


  chrome.storage.local.set({ ultimoAnalisis: resultado }, () => {
    console.log("[Rocket Advisor] Análisis guardado:", resultado);
  });
}

function esURLSospechoso(url) {
  const patronesSospechosos = [
    /paypa1\.com/i,          // typosquatting clasico
    /secure.*login.*\./i,    // subdominios engañosos
    /\.xyz$|\.tk$|\.ml$/i,   // tlds de alto riesgo
    /[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/  // IP directa en URL
  ];

  return patronesSospechosos.some(patron => patron.test(url));
}