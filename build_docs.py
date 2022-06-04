import os, subprocess, glob, shutil
from checkit.utils import working_directory

with working_directory("viewer"):
    print("building viewer...")
    subprocess.run("npm run build".split(" "))

for f in glob.glob("docs/demo/assets/index.*.*"):
    print(f"removing {f}")
    os.remove(f)

print("copying viewer")
shutil.copytree("viewer/dist","docs/demo",dirs_exist_ok=True)

print("copying bank")
shutil.copyfile("demo-bank/docs/bank.json", "docs/demo/bank.json")
