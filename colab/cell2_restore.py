import os
import shutil
import glob
import subprocess
from google.colab import files

GFPGAN_FOLDER = "/content/GFPGAN"

SERVER_INPUT = os.path.join(
    GFPGAN_FOLDER, "inputs", "upload"
)

SERVER_OUTPUT = os.path.join(
    GFPGAN_FOLDER, "results_final"
)

DRIVE_FOLDER = "/content/drive/MyDrive/GFPGAN"

DRIVE_INPUT = os.path.join(
    DRIVE_FOLDER, "input"
)

DRIVE_RESULT = os.path.join(
    DRIVE_FOLDER, "result"
)

# Check GFPGAN
if not os.path.isdir(GFPGAN_FOLDER):
    raise RuntimeError("❌ GFPGAN not found. Run Cell 1 first.")

# Check Drive
if not os.path.exists("/content/drive/MyDrive"):
    raise RuntimeError("❌ Google Drive is not mounted.")

os.chdir(GFPGAN_FOLDER)

# Drive folders — never delete
os.makedirs(DRIVE_INPUT, exist_ok=True)
os.makedirs(DRIVE_RESULT, exist_ok=True)

# Server folders — clear only these
shutil.rmtree(SERVER_INPUT, ignore_errors=True)
shutil.rmtree(SERVER_OUTPUT, ignore_errors=True)

os.makedirs(SERVER_INPUT, exist_ok=True)
os.makedirs(SERVER_OUTPUT, exist_ok=True)

# Upload
print("📤 SELECT PHOTO")

uploaded = files.upload()

if not uploaded:
    raise RuntimeError("❌ No photo selected.")

# Save original
for filename in uploaded:

    server_file = os.path.join(
        SERVER_INPUT, filename
    )

    shutil.move(filename, server_file)

    shutil.copy2(
        server_file,
        os.path.join(DRIVE_INPUT, filename)
    )

    print("✅ INPUT SAVED:", filename)

# Restore
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

# Find result
restored_files = glob.glob(
    os.path.join(
        SERVER_OUTPUT,
        "restored_imgs",
        "*"
    )
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
    print("✅ RESULT SAVED TO DRIVE")
    print("================================")

    files.download(restored_files[0])

    print("⬇️ DOWNLOAD STARTED")
