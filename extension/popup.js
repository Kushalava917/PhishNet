const elements = {
  status: document.getElementById("status"),
  url: document.getElementById("url"),
  details: document.getElementById("details"),
  confidence: document.getElementById("confidence"),
  summary: document.getElementById("summary"),
  indicators: document.getElementById("indicators"),
  error: document.getElementById("error"),
  refresh: document.getElementById("refresh"),
  report: document.getElementById("report")
};

let activeTab;

function setLoading() {
  elements.status.className = "status loading";
  elements.status.textContent = "Checking this page...";
  elements.details.hidden = true;
  elements.error.hidden = true;
}

function renderResult(entry) {
  elements.url.textContent = entry.url || "";
  elements.refresh.disabled = false;
  elements.report.disabled = entry.status !== "ready";

  if (entry.status === "unsupported") {
    elements.status.className = "status neutral";
    elements.status.textContent = "This page cannot be analyzed";
    elements.error.hidden = false;
    elements.error.textContent = "PhishNet analyzes regular HTTP and HTTPS pages.";
    return;
  }
  if (entry.status === "error") {
    elements.status.className = "status error";
    elements.status.textContent = "Analysis unavailable";
    elements.error.hidden = false;
    elements.error.textContent = "Check that the PhishNet API is running and the endpoint is configured correctly.";
    return;
  }

  const { result } = entry;
  elements.status.className = `status ${result.classification}`;
  elements.status.textContent = result.classification.toUpperCase();
  elements.confidence.textContent = `Confidence: ${Math.round(result.confidence * 100)}%`;
  elements.summary.textContent = result.summary;
  elements.indicators.replaceChildren();
  for (const indicator of result.indicators) {
    const item = document.createElement("li");
    item.textContent = `${indicator.name}: ${indicator.evidence}`;
    elements.indicators.append(item);
  }
  elements.details.hidden = false;
}

async function loadResult(refresh = false) {
  if (!activeTab?.id || !activeTab.url) return;
  setLoading();
  elements.refresh.disabled = true;
  const response = await chrome.runtime.sendMessage({
    type: refresh ? "refresh-tab" : "get-tab-result",
    tabId: activeTab.id,
    url: activeTab.url
  });
  renderResult(response);
}

elements.refresh.addEventListener("click", () => void loadResult(true));

elements.report.addEventListener("click", async () => {
  const issueUrl = new URL("https://github.com/Kushalava917/PhishNet/issues/new");
  issueUrl.searchParams.set("template", "bug_report.yml");
  issueUrl.searchParams.set("title", "[Incorrect detection] " + (activeTab?.url || "URL"));
  issueUrl.searchParams.set(
    "body",
    `PhishNet analyzed this URL:\n\n${activeTab?.url || "unknown"}\n\nPlease describe the incorrect result and expected classification.`
  );
  await chrome.tabs.create({ url: issueUrl.toString() });
});

chrome.tabs.query({ active: true, currentWindow: true }).then(([tab]) => {
  activeTab = tab;
  void loadResult();
});
