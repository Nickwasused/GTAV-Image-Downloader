#!/usr/bin/python3
# Nickwasused 2021
import argparse
from urllib3 import PoolManager

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--option", help="fetch | zip | both", default="fetch")
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

def download_file(download_object):
    image_request = pool.request('GET', download_object["link"], preload_content=False)
    if (image_request.status != 200):
        return
    with open(download_object["filename"], "wb") as image_file:
        for chunk in image_request.stream(1024):
            image_file.write(chunk)
    image_request.release_conn()
    return

def getremoteimages_modern_docs(remote_url, special_flag, file_type):
    from multiprocessing.pool import ThreadPool
    from multiprocessing import cpu_count
    from json import loads
    from os.path import exists

    check_directories()

    download_urls = []

    # download or skip
    for source_object in source:
        data_request = pool.request('GET', source_object["link"])
        data = loads(data_request.data.decode('utf-8'))

        filtered_data = check_data(data, source_object, file_type)
        print("Found {} images for {}".format(len(filtered_data), source_object["object_type"]))
        for data_object in filtered_data:
            name = data_object["Name"].lower()
            link = remote_url.format(source_object["object_type"], name, file_type)
            filename = "./images/{}/{}.{}".format(source_object["object_type"], name, file_type)

            download_urls.append({
                "link": link,
                "filename": filename
            })

    print("Downloading {} images".format(len(download_urls)))
    results = ThreadPool(cpu_count()).imap_unordered(download_file, download_urls)
    # do this or the images won´t be saved !
    for r in results:
        pass

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

def add_watermark(file):
    # https://betterprogramming.pub/add-copyright-or-watermark-to-photos-using-python-a3773c71d431
    # https://www.geeksforgeeks.org/how-to-add-text-on-an-image-using-pillow-in-python/
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont

    photo = Image.open(file, formats=["PNG"])

    #Store image width and height
    w, h = photo.size

    drawing = ImageDraw.Draw(photo)
    font = ImageFont.truetype("Roboto-Light.ttf", round(w/20))

    text = "alt:V Multiplayer"
    text_w, text_h = drawing.textsize(text, font)
    pos = w - text_w, (h - text_h)

    drawing.text(((w - text_w) - 5, (h - text_h) - 5), text, font=font)
    photo.save(file)

def watermark():
    print("Adding Watermarks...")
    from multiprocessing import Pool
    from os import walk
    from os.path import join

    images = []

    for root, dirs, files in walk("./images"):
        for file in files:
            images.append(join(root, file))

    pool = Pool()
    pool.map(add_watermark, images)
    pool.close()

if __name__ == "__main__":
    if args.option == "fetch":
        getremoteimages_modern_docs("https://docs.altv.mp/gta/images/{}/models/{}.{}", "alt:V", "png")
        watermark()
    elif args.option == "zip":
        zipimages()
    else:
        getremoteimages_modern_docs("https://docs.altv.mp/gta/images/{}/models/{}.{}", "alt:V", "png")
        watermark()
        zipimages()