import os
import sys
import subprocess
import pathlib

GF = "/content/GFPGAN"

# =========================
# GFPGAN
# =========================
if os.path.isdir(GF):
    print("✅ GFPGAN already exists")
else:
    print("⬇️ Cloning GFPGAN...")
    subprocess.run([
        "git", "clone", "-q",
        "https://github.com/JTripathy4/GFPGAN.git",
        GF
    ], check=True)

os.chdir(GF)

# =========================
# BASICSR
# =========================
try:
    import basicsr
    print("✅ BasicSR already installed:", basicsr.__version__)

except ImportError:

    print("⬇️ Installing BasicSR fixed version...")

    subprocess.run([
        sys.executable, "-m", "pip", "install", "-q",
        "basicsr-fixed==1.4.2"
    ], check=True)

    import basicsr
    print("✅ BasicSR installed:", basicsr.__version__)

# =========================
# OTHER DEPENDENCIES
# =========================
for package in ["facexlib", "realesrgan"]:

    try:
        __import__(package)
        print("✅", package, "ready")

    except ImportError:
        subprocess.run([
            sys.executable, "-m", "pip",
            "install", "-q", package
        ], check=True)

# =========================
# BASICSR / TORCHVISION FIX
# =========================
for p in pathlib.Path("/usr/local/lib").rglob("degradations.py"):

    text = p.read_text()

    text = text.replace(
        "torchvision.transforms.functional_tensor",
        "torchvision.transforms.functional"
    )

    p.write_text(text)

# =========================
# GOOGLE DRIVE
# =========================
from google.colab import drive

DRIVE = "/content/drive"

if os.path.ismount(DRIVE):

    print("✅ Google Drive already mounted")

else:

    if os.path.exists(DRIVE) and os.listdir(DRIVE):

        DRIVE = "/content/gdrive_new"
        os.makedirs(DRIVE, exist_ok=True)

    drive.mount(DRIVE)

# =========================
# FINAL CHECK
# =========================
import basicsr

print("================================")
print("✅ CELL 1 COMPLETED")
print("✅ BasicSR:", basicsr.__version__)
print("📁 GFPGAN:", GF)
print("📁 DRIVE:", DRIVE)
print("================================")
