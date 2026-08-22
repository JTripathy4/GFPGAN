import os
import sys
import subprocess

# ============================================================
# PATHS
# ============================================================

GFPGAN_FOLDER = "/content/GFPGAN"

MODEL_FOLDER = os.path.join(
    GFPGAN_FOLDER,
    "experiments",
    "pretrained_models"
)

MODEL_FILE = os.path.join(
    MODEL_FOLDER,
    "GFPGANv1.4.pth"
)

MODEL_URL = (
    "https://github.com/TencentARC/GFPGAN/releases/"
    "download/v1.3.0/GFPGANv1.4.pth"
)


# ============================================================
# GFPGAN REPOSITORY
# ============================================================

if os.path.isdir(GFPGAN_FOLDER):

    print("✅ GFPGAN already exists")

else:

    print("⬇️ Cloning GFPGAN...")

    subprocess.run([
        "git",
        "clone",
        "-q",
        "https://github.com/JTripathy4/GFPGAN.git",
        GFPGAN_FOLDER
    ], check=True)

    print("✅ GFPGAN cloned")


os.chdir(GFPGAN_FOLDER)


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
# GFPGAN V1.4 MODEL
# ============================================================

os.makedirs(
    MODEL_FOLDER,
    exist_ok=True
)

if os.path.isfile(MODEL_FILE):

    print("✅ GFPGAN V1.4 MODEL already exists")

else:

    print("⬇️ Downloading GFPGAN V1.4 MODEL...")

    subprocess.run([
        "wget",
        "-q",
        "--show-progress",
        MODEL_URL,
        "-O",
        MODEL_FILE
    ], check=True)

    print("✅ GFPGAN V1.4 MODEL downloaded")


# ============================================================
# FINAL VERIFICATION
# ============================================================

if not os.path.isfile(MODEL_FILE):

    raise RuntimeError(
        "❌ GFPGAN V1.4 model is missing"
    )


print()
print("========================================")
print("✅ CELL 1 COMPLETED")
print("========================================")
print("📁 GFPGAN :", GFPGAN_FOLDER)
print("✅ BasicSR :", basicsr.__version__)
print("✅ V1.4 MODEL : READY")
print("========================================")
