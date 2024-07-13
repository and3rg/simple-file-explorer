import os

def get_storage_usage(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def get_file_details(path):
    try:
        return {
            'size': os.path.getsize(path),
            'last_modified': os.path.getmtime(path)
        }
    except Exception as e:
        print(f'Error getting file details: {e}')
        return None
