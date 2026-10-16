const input = document.getElementById("api");
const status = document.getElementById("status");

chrome.storage.local.get(["apiEndpoint"]).then(({ apiEndpoint }) => {
  if (apiEndpoint) input.value = apiEndpoint;
});

document.getElementById("save").addEventListener("click", async () => {
  await chrome.storage.local.set({ apiEndpoint: input.value.trim() });
  status.textContent = "Saved";
});
