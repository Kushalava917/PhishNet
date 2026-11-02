const API_DEFAULT = "http://localhost:8000/analyze";
const resultsByTab = new Map();

async function analyzeUrl(url) {
  const { apiEndpoint } = await chrome.storage.local.get(["apiEndpoint"]);
  const endpoint = apiEndpoint || API_DEFAULT;
  const response = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url })
  });
  if (!response.ok) {
    throw new Error(`API returned ${response.status}`);
  }
  return response.json();
}

async function analyzeTab(tabId, url, notify = false) {
  if (!url || !/^https?:\/\//i.test(url)) {
    resultsByTab.delete(tabId);
    return { status: "unsupported", url };
  }

  try {
    const result = await analyzeUrl(url);
    const entry = { status: "ready", url, result };
    resultsByTab.set(tabId, entry);
    if (result.classification === "phishing" || result.classification === "suspicious") {
      if (notify) {
        await chrome.notifications.create({
          type: "basic",
          iconUrl: "icon48.png",
          title: "PhishNet warning",
          message: `This site is ${result.classification}. Open PhishNet for details.`
        });
      }
    }
    return entry;
  } catch (error) {
    const entry = {
      status: "error",
      url,
      error: error instanceof Error ? error.message : "Unable to reach the PhishNet API."
    };
    resultsByTab.set(tabId, entry);
    return entry;
  }
}

chrome.webNavigation.onBeforeNavigate.addListener((details) => {
  if (details.frameId !== 0) return;
  void analyzeTab(details.tabId, details.url, true);
});

chrome.tabs.onRemoved.addListener((tabId) => resultsByTab.delete(tabId));

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message?.type === "get-tab-result") {
    const cached = resultsByTab.get(message.tabId);
    if (cached?.url === message.url) {
      sendResponse(cached);
      return;
    }
    analyzeTab(message.tabId, message.url).then(sendResponse);
    return true;
  }

  if (message?.type === "refresh-tab") {
    analyzeTab(message.tabId, message.url).then(sendResponse);
    return true;
  }
});
