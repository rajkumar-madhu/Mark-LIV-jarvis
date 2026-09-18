"""Standalone FastAPI dashboard for Kubernetes.

The PyQt6 HUD, microphone, speakers, and Gemini Live session cannot run in a
headless pod. This entrypoint serves only the remote-control HTTP UI.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

# Allow `python -m dashboard.k8s_main` from /app
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from dashboard.server import BASE_DIR, DashboardServer  # noqa: E402


def _seed_api_key_file() -> None:
    key = (os.environ.get("GEMINI_API_KEY") or "").strip()
    if not key:
        return
    cfg_dir = BASE_DIR / "config"
    cfg_dir.mkdir(parents=True, exist_ok=True)
    path = cfg_dir / "api_keys.json"
    payload = {"gemini_api_key": key, "os_system": "linux"}
    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(existing, dict):
                existing["gemini_api_key"] = key
                payload = existing
        except Exception:
            pass
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


async def _main() -> None:
    os.environ.setdefault("JARVIS_K8S", "1")
    _seed_api_key_file()

    public_host = (os.environ.get("PUBLIC_HOST") or "127.0.0.1").strip()
    server = DashboardServer()
    server._ip = public_host

    pin = server.register_static_pin(os.environ.get("DASHBOARD_PIN") or "")
    print(f"[Dashboard] Pairing PIN: {pin}")
    print(f"[Dashboard] Login: https://{public_host}/login")
    print(
        "[Dashboard] Limits: no mic, no speakers, no PyQt HUD, no Gemini Live. "
        "Commands queue in-process until a desktop session is attached."
    )
    await server.broadcast({
        "type": "sys",
        "text": "Mark LIV dashboard running in Kubernetes. Voice HUD is not available in-cluster.",
    })
    await server.serve()


def main() -> None:
    asyncio.run(_main())


if __name__ == "__main__":
    main()
