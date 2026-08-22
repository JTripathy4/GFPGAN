import os
import sys
import subprocess

GFPGAN = "/content/GFPGAN"

# ============================================================
# GFPGAN
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
    print("✅ BasicSR already installed:", basicsr.__version__)

except ImportError:
    print("⬇️ Installing BasicSR...")

    subprocess.run([
        sys.executable, "-m", "pip", "install", "-q",
        "basicsr-fixed==1.4.2"
    ], check=True)

    import basicsr
    print("✅ BasicSR installed:", basicsr.__version__)


# ============================================================
# FIX BASICSR / TORCHVISION
# ============================================================

print("🔧 Checking BasicSR compatibility...")

basicsr_path = os.path.dirname(basicsr.__file__)

degradation_file = os.path.join(
    basicsr_path,
    "data",
    "degradations.py"
)

if not os.path.isfile(degradation_file):
    raise RuntimeError(
        "❌ BasicSR degradations.py not found"
    )

with open(degradation_file, "r") as f:
    text = f.read()

old = "from torchvision.transforms.functional_tensor import rgb_to_grayscale"
new = "from torchvision.transforms.functional import rgb_to_grayscale"

if old in text:

    text = text.replace(old, new)

    with open(degradation_file, "w") as f:
        f.write(text)

    print("✅ BasicSR torchvision fix applied")

else:

    print("✅ BasicSR torchvision fix already applied")


# ============================================================
# FACEXLIB
# ============================================================

try:
    import facexlib
    print("✅ facexlib already installed")

except ImportError:
    print("⬇️ Installing facexlib...")

    subprocess.run([
        sys.executable, "-m", "pip",
        "install", "-q", "facexlib"
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
        sys.executable, "-m", "pip",
        "install", "-q", "realesrgan"
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

os.makedirs(MODEL_DIR, exist_ok=True)

if os.path.isfile(MODEL):

    print("✅ GFPGAN V1.4 MODEL already exists")

else:

    print("⬇️ Downloading GFPGAN V1.4 MODEL...")

    subprocess.run([
        "wget", "-q", "--show-progress",
        MODEL_URL,
        "-O", MODEL
    ], check=True)

    print("✅ GFPGAN V1.4 MODEL downloaded")


# ============================================================
# FINAL
# ============================================================

print()
print("========================================")
print("✅ CELL 1 COMPLETED")
print("================================")
print("📁 GFPGAN :", GFPGAN)
print("✅ BasicSR :", basicsr.__version__)
print("✅ V1.4 MODEL : READY")
print("========================================")
