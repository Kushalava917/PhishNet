# PhishNet Browser Extension (Skeleton)

## Privacy
- Sends only the currently navigated URL to your configured PhishNet API endpoint.
- Does **not** collect full browsing history.
- No remote telemetry by default.

## Install (Developer Mode)
1. Run local API: `uvicorn phishnet.api:app --reload`
2. Open `chrome://extensions`
3. Enable **Developer mode**
4. Click **Load unpacked** and select the `extension/` folder
5. (Optional) Open extension options and change API endpoint

## Permissions
- `webNavigation`, `tabs`, `notifications`, `storage`
- Host access for `http://localhost:8000/*` and visited web URLs (needed to evaluate page URLs before navigation completes)

## Report incorrect result
Use the extension popup and click **Report incorrect result** to open a prefilled GitHub issue.
