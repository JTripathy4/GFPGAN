import os
import shutil
import glob
import subprocess
import time
from google.colab import files

# ============================================================
# PATHS
# ============================================================

GFPGAN_FOLDER = "/content/GFPGAN"

SERVER_INPUT = os.path.join(
    GFPGAN_FOLDER, "inputs", "upload"
)

SERVER_OUTPUT = os.path.join(
    GFPGAN_FOLDER, "results_final"
)

DRIVE_FOLDER = "/content/drive/MyDrive/GFPGAN"
DRIVE_INPUT = os.path.join(DRIVE_FOLDER, "input")
DRIVE_RESULT = os.path.join(DRIVE_FOLDER, "result")

MODEL_FILE = os.path.join(
    GFPGAN_FOLDER,
    "experiments",
    "pretrained_models",
    "GFPGANv1.4.pth"
)

# ============================================================
# CHECK PY1 SETUP
# ============================================================

if not os.path.isdir(GFPGAN_FOLDER):
    raise RuntimeError("❌ Run PY1 first.")

if not os.path.isfile(MODEL_FILE):
    raise RuntimeError("❌ V1.4 model missing. Run PY1 first.")

if not os.path.exists("/content/drive/MyDrive"):
    raise RuntimeError("❌ Google Drive is not mounted.")

os.chdir(GFPGAN_FOLDER)

# ============================================================
# DRIVE — NEVER DELETE
# ============================================================

os.makedirs(DRIVE_INPUT, exist_ok=True)
os.makedirs(DRIVE_RESULT, exist_ok=True)

# ============================================================
# SERVER — CLEAR ONLY TEMPORARY FILES
# ============================================================

shutil.rmtree(SERVER_INPUT, ignore_errors=True)
shutil.rmtree(SERVER_OUTPUT, ignore_errors=True)

os.makedirs(SERVER_INPUT, exist_ok=True)
os.makedirs(SERVER_OUTPUT, exist_ok=True)

# ============================================================
# UPLOAD
# ============================================================

print("📤 Select photo")

uploaded = files.upload()

if not uploaded:
    raise RuntimeError("❌ No photo selected.")

# ============================================================
# SAVE INPUT
# ============================================================

for filename in uploaded:

    source = os.path.join("/content", filename)
    server_file = os.path.join(SERVER_INPUT, filename)

    shutil.move(source, server_file)

    shutil.copy2(
        server_file,
        os.path.join(DRIVE_INPUT, filename)
    )

print("✅ Photo saved to Drive")

# ============================================================
# RESTORE
# ============================================================

print("🔄 Restoring...")

command = [
    "python",
    "inference_gfpgan.py",
    "-i", SERVER_INPUT,
    "-o", SERVER_OUTPUT,
    "-v", "1.4",
    "-s", "2",
    "-w", "1.0"
]

start_time = time.time()

process = subprocess.Popen(
    command,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

# Live elapsed-time indicator
while process.poll() is None:

    elapsed = int(time.time() - start_time)

    print(
        f"\r⏳ Processing: {elapsed}s",
        end="",
        flush=True
    )

    time.sleep(2)

return_code = process.wait()

print()

# ============================================================
# FIND RESULT
# ============================================================

restored_files = glob.glob(
    os.path.join(
        SERVER_OUTPUT,
        "restored_imgs",
        "*"
    )
)

# ============================================================
# SAVE RESULT
# ============================================================

if return_code != 0 or not restored_files:

    raise RuntimeError(
        "❌ Restoration failed. Check the GFPGAN error above."
    )

for restored_file in restored_files:

    filename = os.path.basename(restored_file)

    shutil.copy2(
        restored_file,
        os.path.join(DRIVE_RESULT, filename)
    )

# ============================================================
# DOWNLOAD
# ============================================================

print("✅ Restoration completed")
print("💾 Result saved to Drive")

files.download(restored_files[0])

print("⬇️ Download started")
