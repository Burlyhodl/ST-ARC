# ST-ARC
ST-Article Creator and AI article generator

## Uploading Articles to WordPress

1. **Install dependencies**
   ```bash
   pip install requests
   ```

2. **Export your WordPress application password** (or supply it via `--password`).
   ```bash
   export WP_APPLICATION_PASSWORD="m4AR YqSY LW2b IhUW lPjx 1led"
   ```

3. **Run the uploader script** from the project root. Provide your WordPress username and the HTML file generated in `content/`.
   ```bash
   python scripts/upload_to_wordpress.py content/solar-roi-playbook.html \
       --username your-wordpress-username \
       --status draft
   ```

   Use `--dry-run` to inspect the payload without sending it, or `--status publish` when ready to go live. Category and tag IDs can be added with `--categories` and `--tags` respectively.
