const input = document.getElementById("api");
const status = document.getElementById("status");

chrome.storage.local.get(["apiEndpoint"]).then(({ apiEndpoint }) => {
  if (apiEndpoint) input.value = apiEndpoint;
});

document.getElementById("save").addEventListener("click", async () => {
  const endpoint = input.value.trim();
  try {
    const parsed = new URL(endpoint);
    if (!["http:", "https:"].includes(parsed.protocol)) {
      throw new Error("Unsupported protocol");
    }
    await chrome.storage.local.set({ apiEndpoint: endpoint });
    status.className = "safe";
    status.textContent = "Settings saved.";
  } catch {
    status.className = "error";
    status.textContent = "Enter a valid HTTP or HTTPS endpoint.";
  }
});
