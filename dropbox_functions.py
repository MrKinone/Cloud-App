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
    DROPBOX_ACCESS_TOKEN = r.text[18:161]
    print(r.text)

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


def dropbox_delete_file(dropbox_file_path):  # 22-05-2022
    name = funcs.name_convert(dropbox_file_path.rsplit('/', 1)[-1])
    dropbox_file_path = dropbox_file_path.rsplit("/", 1)[0] + "/" + name

    dbx = dropbox_connect()
    dbx.files_delete(dropbox_file_path)
    funcs.name_delete(name)

def dropbox_create_folder(dropbox_folder_path):
    dbx = dropbox_connect()
    dbx.files_create_folder_v2(dropbox_folder_path)
    
    
def retry_sharing_job(async_job_id):
    dbx = dropbox_connect()
    sharing_job = dbx.sharing_check_share_job_status(async_job_id)
    if sharing_job.is_complete():
        print("Async sharing job completed...")
        pass
    else:
        print("Async sharing job in progress")
        print("....waiting 3 seconds...")
        time.sleep(3)
        retry_sharing_job(async_job_id)
#
def creating_shared_folder(folder_path, access_level, email, message):
    dbx = dropbox_connect()
    dbx.files_create_folder(folder_path)
    # sharing_folder = dbx.sharing_share_folder(folder_path, force_async=True)
    sharing_folder = dbx.sharing_share_folder(folder_path)
    if sharing_folder.is_complete():
        sharing_folder_data = sharing_folder.get_complete()
    if sharing_folder.is_async_job_id():
        async_job_id = sharing_folder.get_async_job_id()
        # helper function will block until async sharing job completes
        retry_sharing_job(async_job_id)
        sharing_folder_job = dbx.sharing_check_share_job_status(async_job_id)
        sharing_folder_data = sharing_folder_job.get_complete()

    member = dropbox.sharing.MemberSelector.email(email)
    add_member = dropbox.sharing.AddMember(member, access_level)
    members = [add_member]
    dbx.sharing_add_folder_member(sharing_folder_data.shared_folder_id, members, custom_message=message)
    print(f"Folder successfully created and shared with {email}.")

def getusermail():
    dbx = dropbox_connect()
    account = dbx.users_get_current_account()
    print(account.email)
    return account.email