# Chess coaching site

Single file: `index.html`. Edit the `SITE` block near the bottom (batches, venues, price, announcements, testimonials).

## Publish on GitHub Pages (.github.io)
1. Create a repo named `<your-username>.github.io` (or any repo, then Settings > Pages).
2. Put `index.html` at the repo root, push, and enable Pages from the main branch.
3. Live at `https://<your-username>.github.io/`.

## Demo / call requests
- Default: opens WhatsApp with the form details pre-filled.
- Better: create a free Formspree form, paste its URL into `formEndpoint`; requests then arrive by email.

## Store registrations in a Google Sheet
1. Create a Google Sheet (e.g. "Chessopia registrations").
2. Extensions > Apps Script. Paste the contents of `apps-script/Code.gs` over the default code. Optionally set `NOTIFY_EMAIL`.
3. Deploy > New deployment > type **Web app**. Execute as: **Me**. Who has access: **Anyone**. Deploy and authorize.
4. Copy the web-app URL and paste it into `sheetUrl` in the `SITE` block of `index.html`.
5. Submit a test registration: a row appears in the `Registrations` tab (columns include Status for your follow-up).
6. After editing the script later, use Deploy > Manage deployments > edit > New version, or the site keeps using the old code.

The sheet holds children's names and parents' phone numbers: keep it private and do not publish its link.
