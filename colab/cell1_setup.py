import os
import sys
import subprocess
import pathlib

GFPGAN_FOLDER = "/content/GFPGAN"

# =========================
# GFPGAN REPOSITORY
# =========================

if os.path.isdir(GFPGAN_FOLDER):
    print("✅ GFPGAN already exists")
else:
    print("⬇️ Cloning GFPGAN...")
    subprocess.run([
        "git", "clone", "-q",
        "https://github.com/JTripathy4/GFPGAN.git",
        GFPGAN_FOLDER
    ], check=True)
    print("✅ GFPGAN cloned")

os.chdir(GFPGAN_FOLDER)


# =========================
# BASICSR
# =========================

try:
    import basicsr
    print("✅ BasicSR already installed:", basicsr.__version__)

except ImportError:
    print("⬇️ Installing BasicSR...")

    subprocess.run([
        sys.executable, "-m", "pip", "install", "-q",
        "basicsr-fixed==1.4.2"
    ], check=True)

    import basicsr
    print("✅ BasicSR installed:", basicsr.__version__)


# =========================
# FACEXLIB
# =========================

try:
    import facexlib
    print("✅ facexlib already installed")

except ImportError:
    print("⬇️ Installing facexlib...")

    subprocess.run([
        sys.executable, "-m", "pip", "install", "-q",
        "facexlib"
    ], check=True)


# =========================
# REALESRGAN
# =========================

try:
    import realesrgan
    print("✅ Real-ESRGAN already installed")

except ImportError:
    print("⬇️ Installing Real-ESRGAN...")

    subprocess.run([
        sys.executable, "-m", "pip", "install", "-q",
        "realesrgan"
    ], check=True)


# =========================
# BASICSR / TORCHVISION FIX
# =========================

for file_path in pathlib.Path("/usr/local/lib").rglob(
    "degradations.py"
):

    text = file_path.read_text()

    old = "torchvision.transforms.functional_tensor"
    new = "torchvision.transforms.functional"

    if old in text:
        file_path.write_text(text.replace(old, new))
        print("✅ BasicSR compatibility fixed")


# =========================
# FINAL CHECK
# =========================

import basicsr
import facexlib
import realesrgan

print()
print("================================")
print("✅ SOFTWARE SETUP COMPLETED")
print("================================")
print("📁 GFPGAN :", GFPGAN_FOLDER)
print("✅ BasicSR :", basicsr.__version__)
print("================================")
