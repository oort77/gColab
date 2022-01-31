# -*- coding: utf-8 -*-
#  File: gdrive.py
#  Project: 'gColab'
#  Created by Gennady Matveev (gm@og.ly) on 30-01-2022.
#  Copyright 2022. All rights reserved.

# Import libraries
import os
import os.path
import tomli
import pyperclip as pc
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Import secrets
script_path = os.path.realpath(__file__)
secrets_toml = script_path.rsplit("/", 2)[0]+"/config/.secrets.toml"
with open(secrets_toml, "rb") as f:
    secrets = tomli.load(f)

# Authorize with gDrive
gauth = GoogleAuth(settings_file=secrets["settings_file"])
GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = secrets["secrets_file"]
GoogleAuth.DEFAULT_SETTINGS['save_credentials_file'] = secrets["save_credentials_file"]
drive = GoogleDrive(gauth)

# Get current directory:
work_dir = os.getcwd()

# Datasets folder in Google Drive
folder_id = secrets["folder_id"]

# Get list of zip files
def file_info(dir_name: str):
    file_list = {}
    for i in os.listdir(dir_name):
        if secrets["file_type"] in i:
            a = os.stat(os.path.join(dir_name, i))
            file_list[i] = a.st_ctime
    return file_list


# Get last zip
def get_last_zip(dir_name: str):
    # Get all
    zips = file_info(dir_name)
    # Get the last one
    return max(zips, key=zips.get)


# Send last zip to gDrive
def send_zip(dir_name: str):
    last_zip = get_last_zip(dir_name)
    gfile = drive.CreateFile({'parents': [{'id': folder_id}]})
    # Read file and set it as the content of this instance
    gfile.SetContentFile(last_zip)
    gfile.Upload()  # Upload the file
    permission = gfile.InsertPermission({
                                        'type': 'anyone',
                                        'value': 'anyone',
                                        'role': 'reader'})
    return gfile


def main():
    try:
        file = send_zip(work_dir)
        output = f'''
# Download data from Google Drive
import gdown
!mkdir ../data
url = "https://drive.google.com/uc?export=download&id={file["id"]}"
data = pd.read_csv(gdown.download(url, output="../data/{file["title"]}",  
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tquiet=True), compression="zip")
data.head()'''
    # Place text on clipboard
        pc.copy(output)
        print("Snippet copied to clipboard")
        print(file["id"], file["title"])

    except:
        print('''
              Usage:
              $ cd path/to/archive/folder
              $ gdrive
              ''')


if __name__ == "__main__":
    main()
