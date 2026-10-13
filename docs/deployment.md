# Running the prototype

1. Download or clone the repository.
2. Open `index.html` in a modern browser.
3. Use fictional demonstration records only.
4. Export records for backup and test re-import.

The browser prototype can work without a deployed server. Local browser storage is not a durable shared database. The optional Flask and Power Automate connections require separate setup and security review.

For a local HTTP server, run `python3 -m http.server 8000` in the repository directory and open `http://localhost:8000`.
