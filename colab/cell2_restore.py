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

os.makedirs(UPLOAD, exist_ok=True)
os.makedirs(INPUT, exist_ok=True)
os.makedirs(RESULT, exist_ok=True)


# ============================================================
# HEIC SUPPORT
# ============================================================

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


# ============================================================
# FIND PHOTOS
# ============================================================

photos = []

for ext in [
    "*.jpg", "*.jpeg", "*.JPG", "*.JPEG",
    "*.heic", "*.HEIC", "*.heif", "*.HEIF",
    "*.png", "*.PNG"
]:
    photos += glob.glob(f"{UPLOAD}/{ext}")

if not photos:
    print("📂 No photos found in:")
    print(UPLOAD)
    raise SystemExit

print(f"📷 {len(photos)} photo(s) found")


# ============================================================
# TEMPORARY FOLDERS
# ============================================================

shutil.rmtree(SERVER_INPUT, ignore_errors=True)
shutil.rmtree(SERVER_OUTPUT, ignore_errors=True)

os.makedirs(SERVER_INPUT, exist_ok=True)
os.makedirs(SERVER_OUTPUT, exist_ok=True)


# ============================================================
# PREPARE INPUT
# ============================================================

def get_name(filename):

    name, ext = os.path.splitext(filename)

    if ext.lower() in [".heic", ".heif"]:
        ext = ".jpg"

    candidate = name + ext

    if (
        not os.path.exists(f"{INPUT}/{candidate}")
        and
        not os.path.exists(f"{RESULT}/{candidate}")
    ):
        return candidate

    if name.isdigit():

        numbers = []

        for folder in [INPUT, RESULT]:

            for f in os.listdir(folder):

                n, e = os.path.splitext(f)

                if n.isdigit():
                    numbers.append(int(n))

        return f"{max(numbers, default=0) + 1}{ext}"

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


for photo in photos:

    original_name = os.path.basename(photo)
    filename = get_name(original_name)

    if filename != original_name:
        print(f"🔄 {original_name} → {filename}")

    input_file = f"{INPUT}/{filename}"

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

    shutil.copy2(
        input_file,
        f"{SERVER_INPUT}/{filename}"
    )

    print(f"📥 {filename}")


# ============================================================
# IMPORTANT TORCHVISION COMPATIBILITY FIX
# ============================================================

print("🔧 Preparing torchvision compatibility...")

compatibility_file = "/content/torchvision_functional_fix.py"

with open(compatibility_file, "w") as f:

    f.write("""
import sys
import types

try:
    from torchvision.transforms.functional import rgb_to_grayscale

    module = types.ModuleType(
        "torchvision.transforms.functional_tensor"
    )

    module.rgb_to_grayscale = rgb_to_grayscale

    sys.modules[
        "torchvision.transforms.functional_tensor"
    ] = module

except Exception as e:
    print("Torchvision compatibility error:", e)
    raise
""")


# ============================================================
# FORCE CPU
# ============================================================

os.environ["CUDA_VISIBLE_DEVICES"] = ""

print("🖥️ MODE: CPU")
print("🔄 Restoring...")
print("⏳ Please wait...")


# ============================================================
# RUN GFPGAN WITH COMPATIBILITY MODULE PRELOADED
# ============================================================

os.chdir(GFPGAN)

command = [
    "python",
    "-c",
    f"""
import sys
sys.path.insert(0, "/content")

exec(open("{compatibility_file}").read())

sys.argv = [
    "inference_gfpgan.py",
    "-i", "{SERVER_INPUT}",
    "-o", "{SERVER_OUTPUT}",
    "-v", "1.4",
    "-s", "2",
    "-w", "1.0"
]

exec(open("inference_gfpgan.py").read())
"""
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

    print(f"✅ {filename}")


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
