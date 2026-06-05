"""Export the Hercules External API OpenAPI spec to ``api-reference/openapi.json``.

This script imports the live FastAPI app and serialises its generated OpenAPI
document. ``app.openapi()`` only introspects the registered routes — it performs
no database or network I/O — but importing the app evaluates
``external_api.settings`` at module load, which validates two secrets. Provide
throwaway-but-valid values for them; they are never used by the export itself.

Run it from inside the Hercules monorepo (the app lives there, not in this docs
repo):

    EXTAPI_AUTH__JWT_SECRET_KEY="$(openssl rand -hex 32)" \\
    EXTAPI_WEBHOOKS__SECRET_ENCRYPTION_KEY="$(python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')" \\
    uv run --project /path/to/hercules-framework/framework/apps/external_api \\
      python /path/to/docs/scripts/export_openapi.py

The output is committed to this repo so Mintlify can render the API Reference
without a running service. Re-run after changing any External API route to keep
the published spec in sync.
"""

from __future__ import annotations

import json
from pathlib import Path

from external_api.app import app

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "api-reference" / "openapi.json"


def main() -> None:
    spec = app.openapi()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")

    paths = sorted(spec.get("paths", {}))
    print(f"Wrote {OUTPUT_PATH} ({len(paths)} paths, version {spec.get('info', {}).get('version')})")
    for path in paths:
        print(f"  {path}")


if __name__ == "__main__":
    main()
