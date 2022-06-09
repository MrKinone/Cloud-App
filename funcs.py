from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os
import csv

def get_path(array):
    folder_paths=[]
    for folder in range(len(array)):
        path_display = array[folder]["path_display"]
        ext = path_display.split("/")[1:]
        folder_paths.append(ext)
    return folder_paths

def get_client_modified(array):
    client_modified_list = []
    for folder in range(len(array)):
        client_modified = array[folder]["client_modified"]
        date_time = client_modified.strftime("%m/%d/%Y, %H:%M:%S")
        client_modified_list.append(date_time)
    return client_modified_list


def get_child_control(files, folders):
    items = []
    files_paths = get_path(files)
    folder_paths = get_path(folders)
    client_modified_list = get_client_modified(files)
    while True:
        if not folder_paths:
            break
        elif 1 == len(folder_paths[0]):
            item = QTreeWidgetItem([folder_paths[0][0], "folder"])
            folder_paths.remove(folder_paths[0])
            item.setIcon(0, QIcon('images/folder.ico'))
            items.append(item)
        elif 2 <= len(folder_paths[0]):
            dir_len = len(folder_paths[0])
            items = found_child_folder(items, folder_paths[0], dir_len)
            folder_paths.remove(folder_paths[0])



    while True:
        if not files_paths:
            break
        if 1 == len(files_paths[0]):
            item = QTreeWidgetItem([name_convert(files_paths[0][0]), "file", client_modified_list[0]])
            files_paths.remove(files_paths[0])
            items.append(item)
        elif 2 <= len(files_paths[0]):
            dir_len = len(files_paths[0])
            items = found_child_file(items, files_paths[0], dir_len, client_modified_list)
            files_paths.remove(files_paths[0])
        client_modified_list.remove(client_modified_list[0])
    return items


def found_child_file(items, folder_paths, dir_len, client_modified_list):
    new_dir_len = dir_len-1
    if dir_len >= 3:
        for i in range(len(items)):
            if items[i].text(0) == folder_paths[0]:
                child_count = items[i].childCount()
                childs = []
                for j in range(child_count):
                    childs.append(items[i].child(j))
                if childs:
                    childs = found_child_file(childs, folder_paths[1:], new_dir_len, client_modified_list)
                for j in range(len(childs)):
                    items[i].addChild(childs[j])
                return items
    elif dir_len == 2:
        for i in range(len(items)):
            if items[i].text(0) == folder_paths[0]:
                item = found_child_file(items, folder_paths[1:], new_dir_len, client_modified_list)
                items[i].addChild(item)
                return items
    else:
        childs = QTreeWidgetItem([name_convert(folder_paths[0]), "file", client_modified_list[0]])
        folder_paths.remove(folder_paths[0])
        return childs


def found_child_folder(items, folder_paths, dir_len):
    new_dir_len = dir_len-1
    if dir_len >= 3:
        for i in range(len(items)):
            if items[i].text(0) == folder_paths[0]:
                child_count = items[i].childCount()
                childs = []
                for j in range(child_count):
                    childs.append(items[i].child(j))
                if childs:
                    childs = found_child_folder(childs, folder_paths[1:], new_dir_len)
                for j in range(len(childs)):
                    items[i].addChild(childs[j])
                return items
    elif dir_len == 2:
        for i in range(len(items)):
            if items[i].text(0) == folder_paths[0]:
                item = found_child_folder(items, folder_paths[1:], new_dir_len)
                items[i].addChild(item)
                return items
    else:
        childs = QTreeWidgetItem([folder_paths[0], "folder"])
        childs.setIcon(0, QIcon('images/folder.ico'))
        return childs


def folder_check(DIR):
    if not os.path.isdir(DIR):
        folder_check(DIR.rsplit("/", 1)[0])
        os.mkdir(DIR)
        print("Directory '% s' created" % DIR)
    return

def str2binary(text):
    textbinary = ''.join(format(ord(i), '08b') for i in text)
    textbinary += '00000000'
    return textbinary


def binary2str(textbinary):
    line = textbinary
    n = 8
    binary_values = [line[i:i + n] for i in range(0, len(line), n)]
    ascii_string = ""
    for binary_value in binary_values:
        an_integer = int(binary_value, 2)
        ascii_character = chr(an_integer)
        ascii_string = ascii_string + ascii_character
    return ascii_string


def decimal2Binary(decimal):
    binary =''
    for i in range(8):
        if decimal%2==1:
            binary = str(1)+binary
        else:
            binary = str(0)+binary
        decimal = int(decimal / 2)
    return binary


def name_convert(str):
    try:
        with open('name.csv', 'r', encoding='UTF8') as f:
            reader = csv.reader(f)
            names = []
            for name in reader:
                if name != []:
                    names.append(name)

        for i in range(len(names)):
            if str == names[i][0]:
                return names[i][1]
            elif str == names[i][1]:
                return names[i][0]
    except:
        print("file not found")


def name_delete(name):

    lines = list()

    imp = open('name.csv', 'r')
    for row in csv.reader(imp):
        if len(row)==0:
            continue
        elif row[0] == name:
            continue
        else:
            lines.append(row)
    imp.close()

    with open('name.csv', 'w') as writeFile:
        for num in range(len(lines)):
            writeFile.write(lines[num][0]+","+(lines[num][1]+"\n"))
