#!/usr/bin/python3
# Nickwasused 2021
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--option", help="fetch | zip | both", default="fetch")
args = parser.parse_args()

# Use Dumps from here: https://github.com/DurtyFree/gta-v-data-dumps

source = [
    { "link": "https://raw.githubusercontent.com/DurtyFree/gta-v-data-dumps/master/peds.json", "object_type": "ped", "file_type": "png" },
    { "link": "https://raw.githubusercontent.com/DurtyFree/gta-v-data-dumps/master/vehicles.json", "object_type": "vehicle", "file_type": "png" },
    { "link": "https://raw.githubusercontent.com/DurtyFree/gta-v-data-dumps/master/weapons.json", "object_type": "weapon", "file_type": "png" }
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

def getremoteimages():
    from json import loads
    from urllib3 import PoolManager
    from os import mkdir
    from os.path import exists

    pool = PoolManager()

    # check directories
    if (exists("./images") == False):
        mkdir("./images")

    for source_object in source:
        directory = "./images/{}".format(source_object["object_type"])
        if (exists(directory) == False):
            mkdir(directory)

    # download or skip
    for source_object in source:
        data_request = pool.request('GET', source_object["link"])
        data = loads(data_request.data.decode('utf-8'))

        for data_object in data:
            name = data_object["Name"].lower()
            link = "https://docs.altv.mp/gta/images/{}/models/{}.{}".format(source_object["object_type"], name, source_object["file_type"])
            filename = "./images/{}/{}.{}".format(source_object["object_type"], name, source_object["file_type"])

            if (exists(filename)):
                print("SKIPPING: {}:{}".format(source_object["object_type"], name))
                continue
            else:
                print("Downloading: {}:{}".format(source_object["object_type"], name))
                image_request = pool.request('GET', link, preload_content=False)
                with open(filename, "wb") as image_file:
                    for chunk in image_request.stream(1024):
                        image_file.write(chunk)

                image_request.release_conn()

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
        getremoteimages()
    elif args.option == "zip":
        zipimages()
    else:
        getremoteimages()
        zipimages()