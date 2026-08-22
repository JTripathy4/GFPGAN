import os
import sys
import subprocess

# ============================================================
# DRIVE PATHS
# ============================================================

DRIVE = "/content/drive/MyDrive/GFPGAN"

SOFTWARE = f"{DRIVE}/software"
GFPGAN = f"{SOFTWARE}/GFPGAN"
MODEL_DIR = f"{DRIVE}/models"

MODEL = f"{MODEL_DIR}/GFPGANv1.4.pth"

# ============================================================
# CHECK DRIVE
# ============================================================

if not os.path.exists("/content/drive/MyDrive"):
    raise RuntimeError("❌ Google Drive is not mounted.")

os.makedirs(DRIVE, exist_ok=True)
os.makedirs(SOFTWARE, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

print("✅ Google Drive ready")


# ============================================================
# GFPGAN REPOSITORY
# ============================================================

if os.path.isdir(GFPGAN):

    print("✅ GFPGAN already exists in Drive")

else:

    print("⬇️ Cloning GFPGAN to Drive...")

    subprocess.run([
        "git",
        "clone",
        "-q",
        "https://github.com/JTripathy4/GFPGAN.git",
        GFPGAN
    ], check=True)

    print("✅ GFPGAN cloned to Drive")


# ============================================================
# BASICSR
# ============================================================

try:

    import basicsr

    print(
        "✅ BasicSR already available:",
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
# BASICSR / TORCHVISION FIX
# ============================================================

basicsr_path = os.path.dirname(basicsr.__file__)

degradation_file = os.path.join(
    basicsr_path,
    "data",
    "degradations.py"
)

if os.path.isfile(degradation_file):

    with open(degradation_file, "r") as f:
        text = f.read()

    old = (
        "from torchvision.transforms.functional_tensor "
        "import rgb_to_grayscale"
    )

    new = (
        "from torchvision.transforms.functional "
        "import rgb_to_grayscale"
    )

    if old in text:

        text = text.replace(old, new)

        with open(degradation_file, "w") as f:
            f.write(text)

        print("✅ BasicSR compatibility fixed")

    else:

        print("✅ BasicSR compatibility already fixed")


# ============================================================
# FACEXLIB
# ============================================================

try:

    import facexlib

    print("✅ facexlib already available")

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

    print("✅ realesrgan already available")

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
# GFPGAN V1.4 MODEL
# ============================================================

MODEL_URL = (
    "https://github.com/TencentARC/GFPGAN/releases/"
    "download/v1.3.0/GFPGANv1.4.pth"
)

if os.path.isfile(MODEL):

    print("✅ GFPGAN V1.4 model already exists in Drive")

else:

    print("⬇️ Downloading GFPGAN V1.4 model...")

    subprocess.run([
        "wget",
        "-q",
        "--show-progress",
        MODEL_URL,
        "-O",
        MODEL
    ], check=True)

    print("✅ GFPGAN V1.4 model saved to Drive")


# ============================================================
# DRIVE FOLDERS FOR PHOTOS
# ============================================================

for folder in [
    "upload",
    "input",
    "result"
]:

    os.makedirs(
        f"{DRIVE}/{folder}",
        exist_ok=True
    )


# ============================================================
# FINAL
# ============================================================

print()
print("========================================")
print("✅ PERSISTENT GFPGAN SETUP COMPLETED")
print("========================================")
print("📁 GFPGAN :", GFPGAN)
print("📁 MODEL  :", MODEL)
print("📁 DRIVE  :", DRIVE)
print("========================================")
