import os, subprocess, glob, shutil, tempfile
from checkit.utils import working_directory

def main():
    with working_directory("../demo-bank"):
        print("building bank...")
        subprocess.run("python -m checkit generate".split(" "))

    with working_directory("../viewer"):
        print("building viewer...")
        subprocess.run("npm run build".split(" "))

    print('zipping up viewer')
    with tempfile.TemporaryDirectory() as temporary_directory:
        copied_directory = shutil.copytree(
            os.path.join('..','viewer','dist'),
            temporary_directory,
            dirs_exist_ok=True,
        )
        os.remove(os.path.join(temporary_directory,"assets","bank.json"))
        shutil.make_archive(
            os.path.join('checkit','static','viewer'),
            'zip',
            temporary_directory,
        )

if __name__ == "__main__":
    main()