import os
import shutil
import glob
import subprocess
from google.colab import files

# =========================
# PATHS
# =========================

GFPGAN_FOLDER = "/content/GFPGAN"

SERVER_INPUT = f"{GFPGAN_FOLDER}/inputs/upload"
SERVER_OUTPUT = f"{GFPGAN_FOLDER}/results_final"

DRIVE_FOLDER = "/content/drive/MyDrive/GFPGAN"
DRIVE_INPUT = f"{DRIVE_FOLDER}/input"
DRIVE_RESULT = f"{DRIVE_FOLDER}/result"


# =========================
# CHECK
# =========================

if not os.path.exists(GFPGAN_FOLDER):
    raise RuntimeError("❌ GFPGAN not found. Run Cell 1 first.")

if not os.path.exists("/content/drive/MyDrive"):
    raise RuntimeError("❌ Google Drive is not mounted.")


os.chdir(GFPGAN_FOLDER)


# =========================
# FOLDERS
# =========================

os.makedirs(DRIVE_INPUT, exist_ok=True)
os.makedirs(DRIVE_RESULT, exist_ok=True)

# SERVER ONLY — DELETE OLD TEMP FILES
shutil.rmtree(SERVER_INPUT, ignore_errors=True)
shutil.rmtree(SERVER_OUTPUT, ignore_errors=True)

os.makedirs(SERVER_INPUT, exist_ok=True)
os.makedirs(SERVER_OUTPUT, exist_ok=True)


# =========================
# UPLOAD
# =========================

print("📤 SELECT PHOTO")

uploaded = files.upload()

if not uploaded:
    raise RuntimeError("❌ No photo selected.")


# =========================
# SAVE ORIGINAL
# =========================

for filename in uploaded:

    server_file = os.path.join(
        SERVER_INPUT,
        filename
    )

    shutil.move(filename, server_file)

    shutil.copy2(
        server_file,
        os.path.join(DRIVE_INPUT, filename)
    )

    print("✅ INPUT SAVED:", filename)


# =========================
# RESTORE
# =========================

print("🔄 RESTORING WITH GFPGAN V1.4...")

process = subprocess.run([
    "python",
    "inference_gfpgan.py",
    "-i", SERVER_INPUT,
    "-o", SERVER_OUTPUT,
    "-v", "1.4",
    "-s", "2",
    "-w", "1.0"
])


# =========================
# RESULT
# =========================

restored_files = glob.glob(
    f"{SERVER_OUTPUT}/restored_imgs/*"
)

if process.returncode != 0 or not restored_files:

    print("================================")
    print("❌ GFPGAN RESTORATION FAILED")
    print("RETURN CODE:", process.returncode)
    print("================================")

else:

    for restored_file in restored_files:

        filename = os.path.basename(restored_file)

        shutil.copy2(
            restored_file,
            os.path.join(DRIVE_RESULT, filename)
        )

        print("✅ RESULT SAVED:", filename)

    print("================================")
    print("✅ GFPGAN COMPLETED")
    print("📁 RESULT SAVED TO DRIVE")
    print("================================")

    files.download(restored_files[0])

    print("⬇️ DOWNLOAD STARTED")
