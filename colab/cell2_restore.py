from google.colab import files
import os, shutil, glob, subprocess

%cd /content/GFPGAN

# SERVER
SERVER_IN = "inputs/upload"
SERVER_OUT = "results_final"

# DRIVE
DRIVE_IN = f"{DRIVE}/MyDrive/GFPGAN/input"
DRIVE_OUT = f"{DRIVE}/MyDrive/GFPGAN/result"

# Clear SERVER files only
shutil.rmtree(SERVER_IN, ignore_errors=True)
shutil.rmtree(SERVER_OUT, ignore_errors=True)

os.makedirs(SERVER_IN, exist_ok=True)
os.makedirs(SERVER_OUT, exist_ok=True)

# Keep all existing Drive files
os.makedirs(DRIVE_IN, exist_ok=True)
os.makedirs(DRIVE_OUT, exist_ok=True)

# Upload
print("📤 SELECT PHOTO")
uploaded = files.upload()

for name in uploaded:
    src = os.path.join(SERVER_IN, name)

    shutil.move(name, src)
    shutil.copy2(src, os.path.join(DRIVE_IN, name))

print("✅ INPUT SAVED TO DRIVE")
print("🔄 RESTORING WITH GFPGAN V1.4...")

# GFPGAN V1.4
r = subprocess.run([
    "python",
    "inference_gfpgan.py",
    "-i", SERVER_IN,
    "-o", SERVER_OUT,
    "-v", "1.4",
    "-s", "2",
    "-w", "1.0"
])

# Find result
results = glob.glob(
    os.path.join(SERVER_OUT, "restored_imgs", "*")
)

if r.returncode == 0 and results:

    for result in results:
        name = os.path.basename(result)
        shutil.copy2(
            result,
            os.path.join(DRIVE_OUT, name)
        )

    print("================================")
    print("✅ GFPGAN COMPLETED")
    print("✅ RESULT SAVED TO DRIVE")
    print("================================")

    # Download first result
    files.download(results[0])

    print("⬇️ DOWNLOAD STARTED")

else:
    print("================================")
    print("❌ GFPGAN FAILED")
    print("================================")
