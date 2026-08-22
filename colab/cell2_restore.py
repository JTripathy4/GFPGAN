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


# ============================================================
# CHECK
# ============================================================

if not os.path.isdir(GFPGAN):
    raise RuntimeError("❌ Run PY1 first")


# ============================================================
# CREATE FOLDERS
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
# FIND PHOTOS
# ============================================================

photos = []

for ext in [
    "*.jpg", "*.jpeg",
    "*.JPG", "*.JPEG",
    "*.heic", "*.HEIC",
    "*.heif", "*.HEIF",
    "*.png", "*.PNG"
]:
    photos += glob.glob(f"{UPLOAD}/{ext}")


if not photos:

    print("📂 No photos found")
    print("📁", UPLOAD)

    raise SystemExit


print(f"📷 {len(photos)} photo(s) found")


# ============================================================
# GET AVAILABLE NAME
# ============================================================

def get_name(filename):

    name, ext = os.path.splitext(filename)

    # HEIC → JPG
    if ext.lower() in [".heic", ".heif"]:
        ext = ".jpg"

    candidate = name + ext

    # Original name available
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

            for f in os.listdir(folder):

                n, e = os.path.splitext(f)

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
# TEMPORARY SERVER FOLDERS
# ============================================================

shutil.rmtree(
    SERVER_INPUT,
    ignore_errors=True
)

shutil.rmtree(
    SERVER_OUTPUT,
    ignore_errors=True
)

os.makedirs(
    SERVER_INPUT,
    exist_ok=True
)

os.makedirs(
    SERVER_OUTPUT,
    exist_ok=True
)


# ============================================================
# PREPARE EACH PHOTO
# ============================================================

for photo in photos:

    original_name = os.path.basename(photo)

    final_name = get_name(original_name)

    if final_name != original_name:

        print(
            f"🔄 {original_name} → {final_name}"
        )


    # --------------------------------------------------------
    # CREATE INPUT FILE
    # --------------------------------------------------------

    input_file = f"{INPUT}/{final_name}"


    # HEIC / HEIF → JPEG
    if original_name.lower().endswith(
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


    # --------------------------------------------------------
    # COPY INPUT → COLAB
    # --------------------------------------------------------

    shutil.copy2(
        input_file,
        f"{SERVER_INPUT}/{final_name}"
    )

    print(
        f"📥 {final_name}"
    )


# ============================================================
# FORCE CPU
# ============================================================

os.environ["CUDA_VISIBLE_DEVICES"] = ""

os.chdir(GFPGAN)

print()
print("🖥️ MODE: CPU")
print("🔄 Restoring...")
print("⏳ Please wait...")


# ============================================================
# GFPGAN
# ============================================================

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
# SAVE RESULTS
# ============================================================

restored = glob.glob(
    f"{SERVER_OUTPUT}/restored_imgs/*"
)


if not restored:

    raise RuntimeError(
        "❌ No restored images produced"
    )


for file in restored:

    filename = os.path.basename(file)

    shutil.copy2(
        file,
        f"{RESULT}/{filename}"
    )

    print(
        f"✅ {filename}"
    )


# ============================================================
# DONE
# ============================================================

print()
print("================================")
print("✅ ALL PHOTOS COMPLETED")
print("================================")
print("📂 Upload :", UPLOAD)
print("📂 Input  :", INPUT)
print("📂 Result :", RESULT)
print("================================")
