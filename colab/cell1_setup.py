import os
import sys
import subprocess

GFPGAN_FOLDER = "/content/GFPGAN"
GFPGAN_REPO = "https://github.com/JTripathy4/GFPGAN.git"

# GFPGAN
if os.path.isdir(GFPGAN_FOLDER):
    print("✅ GFPGAN already exists")
else:
    print("⬇️ Cloning GFPGAN...")
    subprocess.run([
        "git", "clone", "-q",
        GFPGAN_REPO,
        GFPGAN_FOLDER
    ], check=True)
    print("✅ GFPGAN cloned")

os.chdir(GFPGAN_FOLDER)

# BasicSR
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

# facexlib
try:
    import facexlib
    print("✅ facexlib ready")
except ImportError:
    print("⬇️ Installing facexlib...")
    subprocess.run([
        sys.executable, "-m", "pip", "install", "-q",
        "facexlib"
    ], check=True)

# realesrgan
try:
    import realesrgan
    print("✅ realesrgan ready")
except ImportError:
    print("⬇️ Installing realesrgan...")
    subprocess.run([
        sys.executable, "-m", "pip", "install", "-q",
        "realesrgan"
    ], check=True)

print("================================")
print("✅ CELL 1 COMPLETED")
print("📁 GFPGAN:", GFPGAN_FOLDER)
print("================================")
