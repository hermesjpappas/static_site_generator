import os
import shutil


def copy_files(src_path, dest_path):
    if not os.path.exists(src_path):
        raise Exception("Source path does not exist")

    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)

    os.mkdir(dest_path)

    source_files = os.listdir(src_path)

    for file in source_files:
        new_src = os.path.join(src_path, file)
        new_dest = os.path.join(dest_path, file)
        if os.path.isfile(new_src):
            print("Copying from", new_src, "to", new_dest)
            shutil.copy(new_src, new_dest)
        else:
            copy_files(new_src, new_dest)
