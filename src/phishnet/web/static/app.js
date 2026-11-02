const form = document.getElementById("analyze-form");
const inputType = document.getElementById("input-type");
const value = document.getElementById("value");
const result = document.getElementById("result");

function escapeHtml(text) {
  return String(text).replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  }[character]));
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  result.className = "";
  result.textContent = "Analyzing...";

  const payload = inputType.value === "url" ? { url: value.value } : { message: value.value };

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) {
      result.textContent = data.detail || "Analysis failed";
      return;
    }

    const items = data.indicators
      .map((item) => `<li><strong>${escapeHtml(item.name)}</strong>: ${escapeHtml(item.evidence)}</li>`)
      .join("");
    result.className = data.classification;
    result.innerHTML = `
      <h2>${escapeHtml(data.classification.toUpperCase())}</h2>
      <p>Confidence: ${escapeHtml(data.confidence)}</p>
      <p>Model version: ${escapeHtml(data.model_version)}</p>
      <p>${escapeHtml(data.summary)}</p>
      <ul>${items || "<li>No suspicious indicators detected.</li>"}</ul>
    `;
  } catch {
    result.textContent = "Network error";
  }
});
