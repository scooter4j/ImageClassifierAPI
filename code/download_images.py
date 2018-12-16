import argparse
import requests
import os
from os import scandir
from PIL import Image

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--urls", required=True,
                help="path to file containing image URLs")
ap.add_argument("-o", "--output", required=True,
                help="path to output directory of images")
ap.add_argument('--debug', type=bool, default=False, help='Show debug logging')
args = vars(ap.parse_args())

# grab the list of URLs from the input file, then initialize the
# total number of images downloaded thus far
rows = open(args["urls"]).read().strip().split("\n")
total = 0

# loop the URLs
for url in rows:
    try:
        # try to download the image
        r = requests.get(url, timeout=60)

        # save the image to disk
        p = os.path.sep.join([args["output"], "{}.jpg".format(
            str(total).zfill(8))])
        f = open(p, "wb")
        f.write(r.content)
        f.close()

        # update the counter
        print("[INFO] downloaded: {}".format(p))
        total += 1

    # handle if any exceptions are thrown during the download process
    except Exception as e:
        print("[INFO] error downloading {}...skipping".format(p))
        print(e)

# loop over the image paths we just downloaded
try:
    files = scandir(args["output"])
    for f in files:
        if f.is_file():
            delete = False
            # try to load the image
            try:
                image = Image.open(f.path)
                if image and args["debug"]:
                    image.show()
                # if the image is `None` then we could not properly load it
                # from disk, so delete it
                if image is None:
                    delete = True

            # if OpenCV cannot load the image then the image is likely
            # corrupt so we should delete it
            except Exception as e:
                print("Exception opening image")
                print(e)
                delete = True

            # check to see if the image should be deleted
            if delete:
                print("[INFO] deleting {}".format(f))
                os.remove(f)
except Exception as e:
    print(e)
print("All done curating images")


