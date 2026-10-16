document.getElementById("report").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const issueUrl = new URL("https://github.com/Kushalava917/PhishNet/issues/new");
  issueUrl.searchParams.set("template", "feature_request.yml");
  issueUrl.searchParams.set("title", "[Incorrect detection] " + (tab?.url || "URL"));
  issueUrl.searchParams.set("body", `The extension flagged or missed this URL:\n\n${tab?.url || "unknown"}`);
  chrome.tabs.create({ url: issueUrl.toString() });
});
