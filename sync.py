import hashlib
import shutil
from pathlib import Path
import os
from typing import Dict, Generator, Union

BLOCKSIZE = 65536


def sync(source: str, dest: str):
    # imperative shell step 1, gather inputs
    source_hashes = read_paths_and_hashes(source)  # (1)
    dest_hashes = read_paths_and_hashes(dest)  # (1)

    # step 2: call functional core
    actions = determine_actions(source_hashes, dest_hashes, source, dest)  # (2)

    # imperative shell step 3, apply outputs
    for action, *paths in actions:
        if action == "copy":
            shutil.copyfile(*paths)
        if action == "move":
            shutil.move(*paths)
        if action == "delete":
            os.remove(paths[0])


def read_paths_and_hashes(root: str) -> Dict:
    hashes = {}
    for folder, _, files in os.walk(root):
        for fn in files:
            hashes[hash_file(Path(folder) / fn)] = fn
    return hashes


def determine_actions(src_hashes: Dict, dst_hashes: Dict, src_folder: Union[Path, str], dst_folder: Union[Path, str]) -> Generator:
    for sha, filename in src_hashes.items():
        if sha not in dst_hashes:
            sourcepath = Path(src_folder) / filename
            destpath = Path(dst_folder) / filename
            yield "copy", sourcepath, destpath

        elif dst_hashes[sha] != filename:
            olddestpath = Path(dst_folder) / dst_hashes[sha]
            newdestpath = Path(dst_folder) / filename
            yield "move", olddestpath, newdestpath

    for sha, filename in dst_hashes.items():
        if sha not in src_hashes:
            yield "delete", dst_folder / filename


def hash_file(path: Path) -> str:
    hasher = hashlib.sha1()
    with path.open("rb") as file:
        buf: bytes = file.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf: bytes = file.read(BLOCKSIZE)
    return hasher.hexdigest()
