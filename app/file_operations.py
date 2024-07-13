import os
import shutil
import zipfile

def copy_file(src, dst):
    try:
        shutil.copy2(src, dst)
        return True
    except Exception as e:
        print(f'Error copying file: {e}')
        return False

def move_file(src, dst):
    try:
        shutil.move(src, dst)
        return True
    except Exception as e:
        print(f'Error moving file: {e}')
        return False

def delete_file(path):
    try:
        os.remove(path)
        return True
    except Exception as e:
        print(f'Error deleting file: {e}')
        return False

def rename_file(src, dst):
    try:
        os.rename(src, dst)
        return True
    except Exception as e:
        print(f'Error renaming file: {e}')
        return False

def compress_file(src, dst):
    try:
        with zipfile.ZipFile(dst, 'w') as zipf:
            zipf.write(src, os.path.basename(src))
        return True
    except Exception as e:
        print(f'Error compressing file: {e}')
        return False

def decompress_file(src, dst):
    try:
        with zipfile.ZipFile(src, 'r') as zipf:
            zipf.extractall(dst)
        return True
    except Exception as e:
        print(f'Error decompressing file: {e}')
        return False
