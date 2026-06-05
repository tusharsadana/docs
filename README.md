# Hercules External API — Developer Portal

The public documentation site for the **Hercules External API**, built with
[Mintlify](https://mintlify.com). It combines narrative guides with an
interactive API reference generated from the service's OpenAPI specification.

## Structure

```
docs.json                     # Site config: branding + navigation (Guides + API Reference tabs)
index.mdx                     # Landing page
quickstart.mdx                # End-to-end first integration
guides/                       # Narrative guides
  authentication.mdx
  uploading-files.mdx
  polling-status.mdx
  discovering-results.mdx
  exporting-results.mdx
  webhooks.mdx
  errors-and-rate-limits.mdx
api-reference/
  openapi.json                # Generated spec — drives the API Reference tab
scripts/
  export_openapi.py           # Regenerates api-reference/openapi.json from the live app
```

## Local preview

Install the [Mintlify CLI](https://www.npmjs.com/package/mint) and run from the
repo root (where `docs.json` lives):

```bash
npm i -g mint
mint dev                 # preview at http://localhost:3000
mint broken-links        # validate internal links
```

## Updating the API reference

`api-reference/openapi.json` is generated from the External API's FastAPI app, so
it stays accurate without a running service. Regenerate it after any route change.

The script imports the app, so it must run inside the Hercules monorepo's Python
environment (not this repo's). `app.openapi()` only introspects routes — no
database or network — but importing the app validates two secrets, so pass
throwaway-but-valid values:

```bash
EXTAPI_AUTH__JWT_SECRET_KEY="$(openssl rand -hex 32)" \
EXTAPI_WEBHOOKS__SECRET_ENCRYPTION_KEY="$(python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')" \
uv run --project /path/to/hercules-framework/framework/apps/external_api \
  python /path/to/this-repo/scripts/export_openapi.py
```

Commit the regenerated `api-reference/openapi.json`.

## Publishing

This repo is connected to Mintlify via its GitHub app. **Pushing to `main`
deploys to production automatically** (~30s). Pull requests get preview deploys.

To put the site on a custom domain (e.g. `developers.hercules.ai`), configure the
domain in the Mintlify dashboard and add the provided CNAME record in Cloudflare
DNS. (Custom domains require a paid Mintlify plan.)
