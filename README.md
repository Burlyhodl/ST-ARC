# ST-ARC
ST-Article Creator and AI article generator

## Prerequisites

Install the Python dependencies used by the CLI tools.

```bash
pip install openai requests
```

Export the credentials required for generation and upload (or provide them through command-line flags when running the tools).
Secrets such as your OpenAI API key and WordPress application password should **never** be
checked into version control. Store them in environment variables or a local secrets manager.

The CLIs automatically load a `.env` file located in the project root (if it exists). You can
override the location by passing `--env-file path/to/secrets.env` to any command or by setting
`ST_ARC_ENV_FILE=/path/to/secrets.env`. Values in the explicit file take precedence over the
current environment.

```bash
export OPENAI_API_KEY="sk-your-openai-key"
export WP_APPLICATION_PASSWORD="abcd efgh ijkl mnop qrst uvwx"
```

If you prefer loading credentials from a file, create a local `.env` (or use a secrets
manager like 1Password, Bitwarden, or your CI provider's secret store). The CLI commands load
`PROJECT_ROOT/.env` automatically; you can point to a different file with `--env-file`.

```bash
# .env (do not commit this file)
OPENAI_API_KEY="sk-your-openai-key"
WP_APPLICATION_PASSWORD="abcd efgh ijkl mnop qrst uvwx"

# load it for the current shell (optional if you rely on the CLI auto-loader)
set -a
source .env
set +a
```

The repository's `.gitignore` prevents `.env` files from being committed, but double-check
your Git status before pushing to make sure no secrets slip into version control. If you need
to rotate credentials, update the environment variables and regenerate the posts without
changing the README or other tracked files.

## Generate Articles

Use the `article_workflow.py` CLI to transform a reference article into a SolarTopps-branded blog post. The tool fetches the
reference content (from a URL, file, or inline text), applies the SolarTopps master prompt, and saves the generated HTML into
`content/`.

```bash
python scripts/article_workflow.py --env-file secrets/.env generate \
    "solar roi playbook" \
    --reference-url "https://aurorasolar.com/the-solar-roi-playbook-why-efficiency-is-your-new-competitive-edge/" \
    --secondary-keywords "solar sales efficiency" "roi tracking" \
    --focus-topic "Show how SolarTopps advisors keep ROI transparent" \
    --chart-data '{"labels": ["Planning", "Design", "Install"], "values": [12, 8, 6]}'
```

The script automatically stores the HTML file in `content/<slug>.html`. Supply `--output` to override the destination path.

## Upload Articles to WordPress

You can upload either with the combined workflow or by using the upload-only script:

```bash
# Upload an existing HTML file
python scripts/article_workflow.py --env-file secrets/.env publish \
    --file content/solar-roi-playbook-efficiency-strategies.html \
    --username your-wordpress-username \
    --status draft \
    --dry-run

# Or call the uploader directly
python scripts/upload_to_wordpress.py content/solar-roi-playbook-efficiency-strategies.html \
    --username your-wordpress-username \
    --status draft \
    --env-file secrets/.env
```

Add `--categories` or `--tags` with WordPress IDs to assign taxonomy terms. Remove `--dry-run` to publish the post once the
payload looks correct.

## One-Step Generate + Upload

When you provide WordPress credentials to the `generate` command, the tool automatically uploads the freshly generated HTML
after saving it locally. This is the fastest way to create and publish a new article in one step.

```bash
python scripts/article_workflow.py --env-file secrets/.env generate \
    "solar roi playbook" \
    --reference-url "https://aurorasolar.com/the-solar-roi-playbook-why-efficiency-is-your-new-competitive-edge/" \
    --username your-wordpress-username \
    --status draft
```

Use `--dry-run` alongside the credentials to verify the JSON payload before sending it to WordPress.
