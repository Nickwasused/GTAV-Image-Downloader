#!/usr/bin/python3
# Nickwasused 2021
import argparse
from urllib3 import PoolManager

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--option", help="fetch | zip | both", default="fetch")
parser.add_argument("-r", "--remote", help="alt:V | alt:V2 | rage | fivem", default="alt:V")
args = parser.parse_args()

pool = PoolManager()

# Use Dumps from here: https://github.com/DurtyFree/gta-v-data-dumps

source = [
    { "link": "https://raw.githubusercontent.com/DurtyFree/gta-v-data-dumps/master/peds.json", "object_type": "ped" },
    { "link": "https://raw.githubusercontent.com/DurtyFree/gta-v-data-dumps/master/vehicles.json", "object_type": "vehicle" },
    { "link": "https://raw.githubusercontent.com/DurtyFree/gta-v-data-dumps/master/weapons.json", "object_type": "weapon" }
]

def retrieve_file_paths(dirName):
    from os import walk
    from os.path import join
    # setup file paths variable
    filePaths = []

    # Read all directory, subdirectories and file lists
    for root, directories, files in walk(dirName):
        for filename in files:
            # Create the full filepath by using os module.
            filePath = join(root, filename)
            filePaths.append(filePath)
       
    # return all paths
    return filePaths

def fetch_handler():
    if args.remote == "alt:V":
        getremoteimages_modern_docs("https://docs.altv.mp/gta/images/{}/models/{}.{}", "alt:V", "png")
    elif args.remote == "alt:V2":
        getremoteimages_old_wiki("https://wiki.altv.mp/wiki/File:{}.png", "https://wiki.altv.mp{}", "alt:V", "png")
    elif args.remote == "rage":
        getremoteimages_old_wiki("https://wiki.rage.mp/index.php?title=File:{}.png", "https://wiki.rage.mp{}", "rage", "png")
    elif args.remote == "fivem":
        getremoteimages_modern_docs("https://docs.fivem.net/{}/{}.{}", "https://docs.fivem.net{}", "fivem", "webp")

def check_directories():
    from os.path import exists
    from os import mkdir
    # check directories
    if (exists("./images") == False):
        mkdir("./images")

    for source_object in source:
        directory = "./images/{}".format(source_object["object_type"])
        if (exists(directory) == False):
            mkdir(directory)

def check_data(data, source_object, file_type):
    from os.path import exists
    return_array = []
    for data_object in data:
        name = data_object["Name"].lower()
        filename = "./images/{}/{}.{}".format(source_object["object_type"], name, file_type)

        if (exists(filename) == False):
            return_array.append(data_object)
    
    return return_array

def getremoteimages_modern_docs(remote_url, special_flag, file_type):
    from json import loads
    from os.path import exists

    check_directories()

    # download or skip
    for source_object in source:
        if special_flag == "fivem" and source_object["object_type"] != "ped":
            print("Downloading {} is not supported on Fivem!".format(source_object["object_type"]))
            continue

        data_request = pool.request('GET', source_object["link"])
        data = loads(data_request.data.decode('utf-8'))

        filtered_data = check_data(data, source_object, file_type)

        for data_object in filtered_data:
            name = data_object["Name"].lower()
            if special_flag == "fivem":
                link = remote_url.format(source_object["object_type"] + "s", name, file_type)
            else:
                link = remote_url.format(source_object["object_type"], name, file_type)
            filename = "./images/{}/{}.{}".format(source_object["object_type"], name, file_type)

            print("Downloading: {}:{}".format(source_object["object_type"], name))
            image_request = pool.request('GET', link, preload_content=False)
            with open(filename, "wb") as image_file:
                for chunk in image_request.stream(1024):
                    image_file.write(chunk)

            image_request.release_conn()

def getremoteimages_old_wiki(remote_url, base_remote_url, weapon_fetch_type, file_type):
    from os.path import exists
    from os import mkdir
    from re import compile
    from json import loads
    from bs4 import BeautifulSoup

    check_directories()

    regexraw = r"\/images\/[0-9a-zA-Z_]{1,}\/[a-zA-Z0-9_]{2}\/.{1,}.png"
    regex = compile(regexraw)

    for source_object in source:
        data_request = pool.request('GET', source_object["link"])
        data = loads(data_request.data.decode('utf-8'))

        filtered_data = check_data(data, source_object, file_type)

        for data_object in filtered_data:
            name = data_object["Name"].lower()
            filename = "./images/{}/{}.{}".format(source_object["object_type"], name, file_type)


            print("Downloading: {}:{}".format(source_object["object_type"], name))
            if source_object["object_type"] == "weapon" and weapon_fetch_type == "alt:V":
                link = remote_url.format(data_object["Name"].replace("WEAPON_", "").replace("_", "-").capitalize().replace("mk2", "Mk2") + "-icon")
            elif source_object["object_type"] == "weapon" and weapon_fetch_type == "rage" or source_object["object_type"] == "ped" and weapon_fetch_type == "rage":
                print("Downloading Weapons from Rage is not supported!")
                break
            else:
                link = remote_url.format(data_object["Name"].capitalize())
            response = pool.request('GET', link)
            decoded_html = response.data.decode("utf-8", errors='ignore')
            soup = BeautifulSoup(decoded_html, 'html.parser')
            links = soup.find_all("a", href=True)

            for link in links:
                result = regex.match(link["href"])
                if (result != None):
                    filelink = base_remote_url.format(link["href"])
                    image_request = pool.request('GET', filelink, preload_content=False)
                    with open(filename, "wb") as image_file:
                        for chunk in image_request.stream(1024):
                            image_file.write(chunk)
                    image_request.release_conn()
                    break

def zipimages():
    from os import mkdir, remove
    from os.path import exists, basename
    import zipfile

    if (exists("./zips") == False):
        mkdir("./zips")

    for source_object in source:
        zip_file = "./zips/{}.zip".format(source_object["object_type"])
        if (exists(zip_file) == True):
            remove(zip_file)

    for source_object in source:
        directory = "./images/{}".format(source_object["object_type"])
        zip_file_path = "./zips/{}.zip".format(source_object["object_type"])
        filePaths = retrieve_file_paths(directory)
        print("Compressing: {} with {} Files".format(source_object["object_type"], len(filePaths)))

        zip_file = zipfile.ZipFile(zip_file_path, 'w')
        with zip_file:
            for file in filePaths:
                zip_file.write(file, basename(file))

        zip_file.close()


if __name__ == "__main__":
    if args.option == "fetch":
        fetch_handler()
    elif args.option == "zip":
        zipimages()
    else:
        fetch_handler()
        zipimages()