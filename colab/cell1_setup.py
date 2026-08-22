import os
import sys
import subprocess
from pathlib import Path

GFPGAN = "/content/GFPGAN"

# ============================================================
# GFPGAN REPOSITORY
# ============================================================

if os.path.isdir(GFPGAN):

    print("✅ GFPGAN already exists")

else:

    print("⬇️ Cloning GFPGAN...")

    subprocess.run([
        "git", "clone", "-q",
        "https://github.com/JTripathy4/GFPGAN.git",
        GFPGAN
    ], check=True)

    print("✅ GFPGAN cloned")

os.chdir(GFPGAN)


# ============================================================
# BASICSR
# ============================================================

try:

    import basicsr

    print(
        "✅ BasicSR already installed:",
        basicsr.__version__
    )

except ImportError:

    print("⬇️ Installing BasicSR...")

    subprocess.run([
        sys.executable,
        "-m",
        "pip",
        "install",
        "-q",
        "basicsr-fixed==1.4.2"
    ], check=True)

    import basicsr

    print(
        "✅ BasicSR installed:",
        basicsr.__version__
    )


# ============================================================
# TORCHVISION / BASICSR COMPATIBILITY FIX
# ============================================================

print("🔧 Checking BasicSR compatibility...")

fixed = False

for base in [
    "/usr/local/lib/python3.11/site-packages",
    "/usr/local/lib/python3.11/dist-packages"
]:

    path = Path(base)

    if not path.exists():
        continue

    for file in path.rglob("degradations.py"):

        text = file.read_text()

        old = "torchvision.transforms.functional_tensor"
        new = "torchvision.transforms.functional"

        if old in text:

            file.write_text(
                text.replace(old, new)
            )

            fixed = True

            print(
                "✅ BasicSR torchvision compatibility fixed"
            )


if not fixed:

    print("✅ BasicSR compatibility already correct")


# ============================================================
# FACEXLIB
# ============================================================

try:

    import facexlib

    print("✅ facexlib already installed")

except ImportError:

    print("⬇️ Installing facexlib...")

    subprocess.run([
        sys.executable,
        "-m",
        "pip",
        "install",
        "-q",
        "facexlib"
    ], check=True)

    print("✅ facexlib installed")


# ============================================================
# REALESRGAN
# ============================================================

try:

    import realesrgan

    print("✅ realesrgan already installed")

except ImportError:

    print("⬇️ Installing realesrgan...")

    subprocess.run([
        sys.executable,
        "-m",
        "pip",
        "install",
        "-q",
        "realesrgan"
    ], check=True)

    print("✅ realesrgan installed")


# ============================================================
# V1.4 MODEL
# ============================================================

MODEL_DIR = os.path.join(
    GFPGAN,
    "experiments",
    "pretrained_models"
)

MODEL = os.path.join(
    MODEL_DIR,
    "GFPGANv1.4.pth"
)

MODEL_URL = (
    "https://github.com/TencentARC/GFPGAN/releases/"
    "download/v1.3.0/GFPGANv1.4.pth"
)

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)

if os.path.isfile(MODEL):

    print("✅ GFPGAN V1.4 MODEL already exists")

else:

    print("⬇️ Downloading GFPGAN V1.4 MODEL...")

    subprocess.run([
        "wget",
        "-q",
        "--show-progress",
        MODEL_URL,
        "-O",
        MODEL
    ], check=True)

    print("✅ GFPGAN V1.4 MODEL downloaded")


# ============================================================
# FINAL
# ============================================================

print()
print("========================================")
print("✅ CELL 1 COMPLETED")
print("========================================")
print("📁 GFPGAN :", GFPGAN)
print("✅ BasicSR :", basicsr.__version__)
print("✅ V1.4 MODEL : READY")
print("========================================")
