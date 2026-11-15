from common import log

log("[STEP 2] Dev Container Started")

for pkg in ("requests", "ncclient"):
    try:
        __import__(pkg)
        log(f"PKG_OK: {pkg}")
    except ImportError:
        log(f"PKG_FAIL: {pkg}")
