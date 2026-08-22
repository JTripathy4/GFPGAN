import os
import shutil
import glob
import subprocess

GFPGAN = "/content/GFPGAN"
DRIVE = "/content/drive/MyDrive/GFPGAN"

UPLOAD = f"{DRIVE}/upload"
INPUT = f"{DRIVE}/input"
RESULT = f"{DRIVE}/result"

SERVER_INPUT = f"{GFPGAN}/inputs/upload"
SERVER_OUTPUT = f"{GFPGAN}/results_final"

# ------------------------------------------------------------
# CHECK PY1
# ------------------------------------------------------------

if not os.path.isdir(GFPGAN):
    raise RuntimeError("❌ Run PY1 first")

# ------------------------------------------------------------
# FOLDERS
# ------------------------------------------------------------

os.makedirs(UPLOAD, exist_ok=True)
os.makedirs(INPUT, exist_ok=True)
os.makedirs(RESULT, exist_ok=True)

# ------------------------------------------------------------
# HEIC SUPPORT
# ------------------------------------------------------------

try:
    from PIL import Image
    import pillow_heif
except ImportError:
    subprocess.run(
        ["pip", "install", "-q", "pillow-heif"],
        check=True
    )
    from PIL import Image
    import pillow_heif

pillow_heif.register_heif_opener()

# ------------------------------------------------------------
# FIND PHOTOS
# ------------------------------------------------------------

photos = []

for ext in [
    "*.jpg", "*.jpeg", "*.JPG", "*.JPEG",
    "*.heic", "*.HEIC", "*.heif", "*.HEIF",
    "*.png", "*.PNG"
]:
    photos += glob.glob(f"{UPLOAD}/{ext}")

if not photos:
    print("📂 No photos found in upload folder")
    raise SystemExit

print(f"📷 {len(photos)} photo(s) found")

# ------------------------------------------------------------
# TEMPORARY COLAB FOLDERS
# ------------------------------------------------------------

shutil.rmtree(SERVER_INPUT, ignore_errors=True)
shutil.rmtree(SERVER_OUTPUT, ignore_errors=True)

os.makedirs(SERVER_INPUT, exist_ok=True)
os.makedirs(SERVER_OUTPUT, exist_ok=True)

# ------------------------------------------------------------
# UPLOAD → INPUT
# ------------------------------------------------------------

jobs = []

for photo in photos:

    filename = os.path.basename(photo)
    name, ext = os.path.splitext(filename)

    # HEIC/HEIF becomes JPEG
    if ext.lower() in [".heic", ".heif"]:
        filename = name + ".jpg"

        image = Image.open(photo)
        image.convert("RGB").save(
            f"{INPUT}/{filename}",
            "JPEG",
            quality=100
        )

    else:
        # Keep original JPEG/PNG
        shutil.copy2(
            photo,
            f"{INPUT}/{filename}"
        )

    # --------------------------------------------------------
    # DUPLICATE NAME
    # --------------------------------------------------------

    if os.path.exists(f"{RESULT}/{filename}"):

        if name.isdigit():

            used = []

            for folder in [INPUT, RESULT]:

                for f in os.listdir(folder):

                    n, e = os.path.splitext(f)

                    if n.isdigit():
                        used.append(int(n))

            filename = f"{max(used, default=0) + 1}{os.path.splitext(filename)[1]}"

        else:

            n = 1
            base, extension = os.path.splitext(filename)

            while (
                os.path.exists(f"{INPUT}/{filename}") or
                os.path.exists(f"{RESULT}/{filename}")
            ):
                filename = f"{base}_{n}{extension}"
                n += 1

    # Copy final input to server
    shutil.copy2(
        f"{INPUT}/{filename}",
        f"{SERVER_INPUT}/{filename}"
    )

    jobs.append(filename)

    print(f"📥 {filename}")

# ------------------------------------------------------------
# RESTORE
# ------------------------------------------------------------

os.chdir(GFPGAN)

print("🔄 Restoring...")
print("⏳ Please wait...")

command = [
    "python",
    "inference_gfpgan.py",
    "-i", SERVER_INPUT,
    "-o", SERVER_OUTPUT,
    "-v", "1.4",
    "-s", "2",
    "-w", "1.0"
]

process = subprocess.run(command)

if process.returncode != 0:
    raise RuntimeError("❌ GFPGAN restoration failed")

# ------------------------------------------------------------
# SAVE RESULTS
# ------------------------------------------------------------

restored = glob.glob(
    f"{SERVER_OUTPUT}/restored_imgs/*"
)

if not restored:
    raise RuntimeError("❌ No restored images produced")

for file in restored:

    filename = os.path.basename(file)

    shutil.copy2(
        file,
        f"{RESULT}/{filename}"
    )

    print(f"✅ {filename}")

# ------------------------------------------------------------
# DONE
# ------------------------------------------------------------

print()
print("================================")
print("✅ DONE")
print("📂 INPUT :", INPUT)
print("📂 RESULT:", RESULT)
print("================================")
