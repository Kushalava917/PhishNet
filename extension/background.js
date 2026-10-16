const API_DEFAULT = "http://localhost:8000/analyze";

async function analyzeUrl(url) {
  const { apiEndpoint } = await chrome.storage.local.get(["apiEndpoint"]);
  const endpoint = apiEndpoint || API_DEFAULT;
  const response = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url })
  });
  if (!response.ok) {
    return null;
  }
  return response.json();
}

chrome.webNavigation.onBeforeNavigate.addListener(async (details) => {
  if (details.frameId !== 0) return;
  if (!details.url.startsWith("http")) return;

  try {
    const result = await analyzeUrl(details.url);
    if (!result) return;
    if (result.classification === "phishing" || result.classification === "suspicious") {
      await chrome.notifications.create({
        type: "basic",
        iconUrl: "icon48.png",
        title: "PhishNet warning",
        message: `This site is ${result.classification}. Open extension popup to report if incorrect.`
      });
    }
  } catch {
    // Fail closed: extension skips warning if local API is unavailable.
  }
});
