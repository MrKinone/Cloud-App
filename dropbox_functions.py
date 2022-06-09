import os
import pathlib
import encrypt, decrypt
import dropbox
from dropbox.exceptions import AuthError
import funcs, requests

def setToken(authorization_code):
    app_key = "e1iey9lzp2uu6jq"
    app_secret = "8ohqk4mtdff1yos"
    token_url = "https://api.dropboxapi.com/oauth2/token"
    params = {
        "code": authorization_code,
        "grant_type": "authorization_code",
        "client_id": app_key,
        "client_secret": app_secret
    }
    r = requests.post(token_url, data=params)
    global DROPBOX_ACCESS_TOKEN
    DROPBOX_ACCESS_TOKEN = r.text[18:156]
    print(DROPBOX_ACCESS_TOKEN)

def dropbox_connect():
    """Create a connection to Dropbox."""
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    except AuthError as e:
        print('Error connecting to Dropbox with access token: ' + str(e))
    return dbx


def dropbox_upload_file(local_file_path, dropbox_file_path):
    enc_local_file_path = encrypt.encrypt_file(local_file_path)

    dropbox_file_path = dropbox_file_path + enc_local_file_path.rsplit("/", 1)[-1]
    print(dropbox_file_path)

    enc_local_file_path = pathlib.Path(enc_local_file_path)

    try:
        dbx = dropbox_connect()

        with enc_local_file_path.open("rb") as f:
            meta = dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"))

        os.remove(enc_local_file_path)
        return meta
    except Exception as e:
        os.remove(enc_local_file_path)
        print('Error uploading file to Dropbox: ' + str(e))


def dropbox_download_file(dropbox_file_path, local_file_path):  # 22-05-2022

    funcs.folder_check(local_file_path)
    name = funcs.name_convert(dropbox_file_path.rsplit('/', 1)[-1])
    enc_local_file_path = local_file_path + "/" + name
    dropbox_file_path = dropbox_file_path.rsplit("/", 1)[0] + "/" + name
    try:
        dbx = dropbox_connect()

        with open(enc_local_file_path, "wb") as f:
            metadata, res = dbx.files_download(path=dropbox_file_path)
            f.write(res.content)

    except Exception as e:
        print('Error downloading file to Dropbox: ' + str(e))
        os.remove(enc_local_file_path)

    decrypt.decrypt_file(enc_local_file_path, local_file_path)

    os.remove(enc_local_file_path)


def dropbox_list_files(path):
    dbx = dropbox_connect()

    try:
        files = dbx.files_list_folder(path).entries
        files_list = []
        folder_list = []
        for file in files:
            if isinstance(file, dropbox.files.FileMetadata):
                metadata = {
                    'name': file.name,
                    'path_display': file.path_display,
                    'client_modified': file.client_modified,
                    'server_modified': file.server_modified
                }
                files_list.append(metadata)
            else:
                metadata = {
                    'name': file.name,
                    'path_display': file.path_display
                }
                folder_list.append(metadata)
        for i in range(len(folder_list)):
            path_display = (folder_list[i]["path_display"])
            sub_files, sub_folders = dropbox_list_files(path_display)

            if sub_files:
                for j in range(len(sub_files)):
                    files_list.append(sub_files[j])

            if sub_folders:
                for j in range(len(sub_folders)):
                    folder_list.append(sub_folders[j])

        return files_list, folder_list
    except Exception as e:
        print('Error getting list of files from Dropbox: ' + str(e))


def dropbox_delete_file(dropbox_file_path):  # 22-05-2022
    name = funcs.name_convert(dropbox_file_path.rsplit('/', 1)[-1])
    dropbox_file_path = dropbox_file_path.rsplit("/", 1)[0] + "/" + name
    try:
        dbx = dropbox_connect()
        dbx.files_delete(dropbox_file_path)
        funcs.name_delete(name)
    except Exception as e:
        print('Error deleting file from Dropbox: ' + str(e))
