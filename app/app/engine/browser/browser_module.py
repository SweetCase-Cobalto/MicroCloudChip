import json
import os, sys
import time
import zipfile
import shutil

CATEGORY_DIRECTORY  = "directory"
CATEGORY_FILE       = "file"

DATA_NAME =     "filename"
DATA_DATE =     "modify_date"
DATA_OWNER =    "owner"
DATA_TYPE =     "type"
DATA_SIZE =     "size"
DATA_SIZE_TYPE =    "size_type"

SIZE_TYPE_FILE =    "files"
SIZE_TYPE_BYTE =    "byte"
SIZE_TYPE_KB =      "KB"
SIZE_TYPE_MB =      "MB"
SIZE_TYPE_GB =      "GB"

def get_main_root(json_root):
    data = None
    with open(json_root, 'rt') as f:
        data = json.load(f)
        data = data["root"]
    return data
    
def get_list(target_root):
    # 1. get file list
    file_list = os.listdir(target_root)
    
    only_file_list = []
    only_dir_list = []
    result_list = []

    for file_data in file_list:
        
        # Different between file and directory
        data_type = None
        file_size = None
        size_type = None

        # Common Data
        full_root = f'{target_root}/{file_data}'
        filename = file_data
        create_date = time.localtime(os.path.getctime(full_root))

        # ReMapping create_date
        create_time = {
            "year": create_date.tm_year,
            "month": create_date.tm_mon,
            "date": create_date.tm_mday,
            "hour": create_date.tm_hour,
            "min": create_date.tm_min,
            "sec": create_date.tm_sec
        }

        if os.path.isfile(full_root):
            data_type = CATEGORY_FILE
            file_size = os.path.getsize(full_root)

            # Chekcing File
            if file_size < 1000:
                size_type = SIZE_TYPE_BYTE
            elif file_size < 1000**2:
                size_type = SIZE_TYPE_KB
            elif file_size < 1000**3:
                size_type = SIZE_TYPE_MB
            else:
                size_type = SIZE_TYPE_GB
            
            only_file_list.append(
            {
                DATA_NAME: filename,
                DATA_DATE: create_time,
                DATA_OWNER: "Not Implement",
                DATA_TYPE: data_type,
                DATA_SIZE: file_size,
                DATA_SIZE_TYPE: size_type,
            })

        elif os.path.isdir(full_root):
            data_type = CATEGORY_DIRECTORY
            file_size = len(os.listdir(full_root))
            size_type = SIZE_TYPE_FILE

            only_dir_list.append(
            {
                DATA_NAME: filename,
                DATA_DATE: create_time,
                DATA_OWNER: "Not Implement",
                DATA_TYPE: data_type,
                DATA_SIZE: file_size,
                DATA_SIZE_TYPE: size_type,
            })

        result_list = only_dir_list + only_file_list
    return result_list

# Get Multiple Zip File
def get_file_archive(archive_name, directory_list, file_list, absolute_root, current_path):
    zfile = zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED)

    if (len(directory_list) == 1) and (directory_list[0] == ''):
        del directory_list[0]
    if (len(file_list) == 1) and (file_list[0] == ''):
        del file_list[0]
    
    for directory in directory_list:
        directory_full_root = absolute_root + current_path + directory
        for root, dirs, files in os.walk(directory_full_root):

            for file in files:
                zfile.write(os.path.join(root, file), os.path.join(root, file)[len(absolute_root):])

    for _file in file_list:
        file_full_root = absolute_root + current_path + _file
        with open(file_full_root, 'rb') as f:
            zfile.write(file_full_root, current_path+_file)
    zfile.close()

def get_usage_data():
    total, used, free = shutil.disk_usage("/")
    return {
        "total": total,
        "used": used,
        "free": free
    }
