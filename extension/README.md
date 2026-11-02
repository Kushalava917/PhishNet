# PhishNet Browser Extension

## Privacy
- Sends only the currently navigated URL to your configured PhishNet API endpoint.
- Does **not** collect full browsing history.
- No remote telemetry by default.
- Results are kept in memory per tab and are discarded when the tab closes.

## Install (Developer Mode)
1. Run local API: `uvicorn phishnet.api:app --reload`
2. Open `chrome://extensions`
3. Enable **Developer mode**
4. Click **Load unpacked** and select the `extension/` folder
5. Open the extension popup, select **Extension settings**, and change the API endpoint if needed.

## Permissions
- `webNavigation`, `tabs`, `notifications`, `storage`
- Host access for `http://localhost:8000/*` and visited web URLs (needed to evaluate page URLs before navigation completes)

## Features
- Analyzes the top-level page before navigation completes.
- Shows safe, suspicious, or phishing status with confidence and explainable indicators.
- Caches the current tab result and supports manual re-checking.
- Shows a browser notification for suspicious or phishing pages.
- Reports an incorrect result through a prefilled GitHub bug report.

The extension intentionally skips browser-internal pages such as `chrome://` and `file://`.
