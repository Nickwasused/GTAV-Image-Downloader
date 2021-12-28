#!/usr/bin/python3
# Nickwasused 2021
from json import loads
from urllib3 import PoolManager
from os import mkdir
from os.path import exists

pool = PoolManager()

# Use Dumps from here: https://github.com/DurtyFree/gta-v-data-dumps

source = [
    { "link": "https://raw.githubusercontent.com/DurtyFree/gta-v-data-dumps/master/peds.json", "object_type": "ped", "file_type": "png" },
    { "link": "https://raw.githubusercontent.com/DurtyFree/gta-v-data-dumps/master/vehicles.json", "object_type": "vehicle", "file_type": "png" },
    { "link": "https://raw.githubusercontent.com/DurtyFree/gta-v-data-dumps/master/weapons.json", "object_type": "weapon", "file_type": "png" }
]

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