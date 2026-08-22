import os
import shutil
import glob
import subprocess

# ============================================================
# PATHS
# ============================================================

DRIVE = "/content/drive/MyDrive/GFPGAN"

GFPGAN = f"{DRIVE}/software/GFPGAN"
MODEL = f"{DRIVE}/models/GFPGANv1.4.pth"

UPLOAD = f"{DRIVE}/upload"
INPUT = f"{DRIVE}/input"
RESULT = f"{DRIVE}/result"

SERVER_INPUT = "/content/gfpgan_input"
SERVER_OUTPUT = "/content/gfpgan_output"


# ============================================================
# CHECK SETUP
# ============================================================

if not os.path.isdir(GFPGAN):
    raise RuntimeError("❌ GFPGAN setup not found in Drive. Run PY1.")

if not os.path.isfile(MODEL):
    raise RuntimeError("❌ GFPGAN V1.4 model not found. Run PY1.")


# ============================================================
# CREATE PHOTO FOLDERS
# ============================================================

os.makedirs(UPLOAD, exist_ok=True)
os.makedirs(INPUT, exist_ok=True)
os.makedirs(RESULT, exist_ok=True)


# ============================================================
# HEIC SUPPORT
# ============================================================

try:
    from PIL import Image
    import pillow_heif

    pillow_heif.register_heif_opener()

except ImportError:

    subprocess.run(
        ["pip", "install", "-q", "pillow-heif"],
        check=True
    )

    from PIL import Image
    import pillow_heif

    pillow_heif.register_heif_opener()


# ============================================================
# FIND PHOTOS IN UPLOAD
# ============================================================

photos = []

for ext in [
    "*.jpg", "*.jpeg", "*.JPG", "*.JPEG",
    "*.heic", "*.HEIC", "*.heif", "*.HEIF",
    "*.png", "*.PNG"
]:
    photos.extend(
        glob.glob(f"{UPLOAD}/{ext}")
    )


if not photos:

    print("📂 Upload folder is empty.")
    print(f"📁 {UPLOAD}")

    raise SystemExit


print(f"📷 {len(photos)} photo(s) found")


# ============================================================
# FIND AVAILABLE NAME
# ============================================================

def get_filename(original):

    name, ext = os.path.splitext(original)

    # HEIC/HEIF will become JPG
    if ext.lower() in [".heic", ".heif"]:
        ext = ".jpg"

    candidate = name + ext

    # Keep uploaded name whenever possible
    if (
        not os.path.exists(f"{INPUT}/{candidate}")
        and
        not os.path.exists(f"{RESULT}/{candidate}")
    ):
        return candidate

    # Numeric filename
    if name.isdigit():

        numbers = []

        for folder in [INPUT, RESULT]:

            for file in os.listdir(folder):

                n, e = os.path.splitext(file)

                if n.isdigit():
                    numbers.append(int(n))

        return f"{max(numbers, default=0) + 1}{ext}"

    # Normal filename
    number = 1

    while True:

        candidate = f"{name}_{number}{ext}"

        if (
            not os.path.exists(f"{INPUT}/{candidate}")
            and
            not os.path.exists(f"{RESULT}/{candidate}")
        ):
            return candidate

        number += 1


# ============================================================
# CLEAR ONLY TEMPORARY COLAB FOLDERS
# ============================================================

shutil.rmtree(SERVER_INPUT, ignore_errors=True)
shutil.rmtree(SERVER_OUTPUT, ignore_errors=True)

os.makedirs(SERVER_INPUT, exist_ok=True)
os.makedirs(SERVER_OUTPUT, exist_ok=True)


# ============================================================
# UPLOAD → INPUT → COLAB
# ============================================================

for photo in photos:

    original = os.path.basename(photo)
    filename = get_filename(original)

    if filename != original:
        print(f"🔄 {original} → {filename}")

    input_file = f"{INPUT}/{filename}"

    # HEIC / HEIF → JPEG
    if original.lower().endswith(
        (".heic", ".heif")
    ):

        image = Image.open(photo)

        image.convert("RGB").save(
            input_file,
            "JPEG",
            quality=100
        )

    else:

        shutil.copy2(
            photo,
            input_file
        )

    # Copy to temporary Colab folder
    shutil.copy2(
        input_file,
        f"{SERVER_INPUT}/{filename}"
    )

    print(f"📥 {filename}")


# ============================================================
# FORCE CPU
# ============================================================

os.environ["CUDA_VISIBLE_DEVICES"] = ""

print()
print("🖥️ MODE: CPU")
print("🔄 Restoring...")
print("⏳ Please wait...")


# ============================================================
# RUN GFPGAN
# ============================================================

os.chdir(GFPGAN)

command = [
    "python",
    "inference_gfpgan.py",

    "-i", SERVER_INPUT,
    "-o", SERVER_OUTPUT,

    "-v", "1.4",
    "-s", "2",
    "-w", "1.0"
]

process = subprocess.run(
    command,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

print(process.stdout)


# ============================================================
# CHECK
# ============================================================

if process.returncode != 0:

    raise RuntimeError(
        f"❌ GFPGAN failed. Return code: {process.returncode}"
    )


# ============================================================
# FIND RESULTS
# ============================================================

restored = glob.glob(
    f"{SERVER_OUTPUT}/restored_imgs/*"
)

if not restored:

    raise RuntimeError(
        "❌ No restored images produced."
    )


# ============================================================
# RESULT → DRIVE
# ============================================================

for file in restored:

    filename = os.path.basename(file)

    result_file = f"{RESULT}/{filename}"

    # Safety: don't overwrite
    if os.path.exists(result_file):

        name, ext = os.path.splitext(filename)

        if name.isdigit():

            numbers = []

            for folder in [INPUT, RESULT]:

                for f in os.listdir(folder):

                    n, e = os.path.splitext(f)

                    if n.isdigit():
                        numbers.append(int(n))

            filename = (
                f"{max(numbers, default=0) + 1}"
                f"{ext}"
            )

        else:

            number = 1

            while os.path.exists(
                f"{RESULT}/{name}_{number}{ext}"
            ):
                number += 1

            filename = f"{name}_{number}{ext}"

        result_file = f"{RESULT}/{filename}"

    shutil.copy2(
        file,
        result_file
    )

    print(f"✅ {filename}")


# ============================================================
# COMPLETE
# ============================================================

print()
print("================================")
print("✅ ALL PHOTOS COMPLETED")
print("================================")
print(f"📂 Upload : {UPLOAD}")
print(f"📂 Input  : {INPUT}")
print(f"📂 Result : {RESULT}")
print("================================")
