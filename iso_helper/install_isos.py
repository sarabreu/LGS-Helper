from glob import glob
import os
import sys
from typing import List
import subprocess
import tempfile

STEAM_PATHS = [
	".local/share/Steam",
	".steam/steam",
]

SIMS_GAME_NAME = "The Sims 4"

def mount_iso_and_extract(iso_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    with tempfile.TemporaryDirectory(dir="/tmp") as mount_point:
        subprocess.run(['sudo', 'mount', '-o', 'loop', iso_path, mount_point], check=True)
        subprocess.run(['cp', '-r', f'{mount_point}/.', output_dir], check=True)
        subprocess.run(['sudo', 'umount', mount_point], check=True)


def main(iso_path: str, exclude: List[str]):
    print(iso_path, exclude)

    home_path = os.environ["HOME"]

    sims_path = ""
    for steam_path in STEAM_PATHS:
        sims_path = os.path.join(home_path, steam_path, "steamapps", "common", SIMS_GAME_NAME)
        if os.path.exists(sims_path):
            break

    print(f"Sims path: '{sims_path}'")

    iso_glob = os.path.join(iso_path, "*.iso")
    print(f"Glob: '{iso_glob}'")

    for iso_file in glob(iso_glob):
        filename = os.path.basename(iso_file).removesuffix(".iso")

        if filename in exclude:
            continue

        print(f"{iso_file} -> {sims_path}")
        mount_iso_and_extract(iso_file, sims_path)
        os.remove(iso_file)


if __name__ == "__main__":
    if sys.platform != "linux":
        raise Exception("This script is only meant to run in Linux")

    iso_path = sys.argv[1]
    exclude = sys.argv[2].split(",")
    main(iso_path, exclude)
