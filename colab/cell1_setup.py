import os, sys, subprocess, pathlib

GF = "/content/GFPGAN"

# 1. Keep existing GFPGAN; clone only if missing
if os.path.isdir(os.path.join(GF, ".git")):
    print("✅ GFPGAN already exists")
else:
    print("⬇️ Cloning GFPGAN...")
    subprocess.run([
        "git", "clone", "-q",
        "https://github.com/JTripathy4/GFPGAN.git",
        GF
    ], check=True)

os.chdir(GF)

# 2. BasicSR — check first
try:
    import basicsr
    print("✅ BasicSR already installed:", basicsr.__version__)

except ImportError:
    print("⬇️ Installing BasicSR...")
    subprocess.run([
        sys.executable, "-m", "pip", "install",
        "basicsr==1.4.2"
    ], check=True)

    import basicsr
    print("✅ BasicSR installed:", basicsr.__version__)

# 3. Other required packages
for pkg, module in [
    ("facexlib", "facexlib"),
    ("realesrgan", "realesrgan")
]:
    try:
        __import__(module)
        print("✅", pkg)
    except ImportError:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-q", pkg
        ], check=True)

# 4. Fix BasicSR / torchvision compatibility
for p in pathlib.Path("/usr/local/lib").rglob("degradations.py"):
    s = p.read_text()
    s = s.replace(
        "torchvision.transforms.functional_tensor",
        "torchvision.transforms.functional"
    )
    p.write_text(s)

# 5. Google Drive — never delete anything
from google.colab import drive

DRIVE = "/content/drive"

if os.path.ismount(DRIVE):
    print("✅ Google Drive already mounted")
else:
    if os.path.exists(DRIVE) and os.listdir(DRIVE):
        DRIVE = "/content/gdrive_new"
        os.makedirs(DRIVE, exist_ok=True)

    drive.mount(DRIVE)

# 6. FINAL verification
import basicsr

print("================================")
print("✅ CELL 1 COMPLETED")
print("✅ BasicSR:", basicsr.__version__)
print("📁 GFPGAN:", GF)
print("📁 DRIVE:", DRIVE)
print("================================")
