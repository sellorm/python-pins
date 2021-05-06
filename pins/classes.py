"""
Hadley notes
---
board = board_rsconnect()
board.search("sales") (array of pins)

x = [1, 2, 3]
pin = board.pin(x, "hadley/sales") 
board.pin_get("hadley/sales")
board.pin_meta("hadley/sales")
"""
import requests as req
import os
import yaml
from dotenv import load_dotenv
import tempfile
import pandas
import shutil
import ntpath
import json

load_dotenv(os.getcwd() + "/.env")


class Board:
    # Fields -- https://github.com/rstudio/pins/blob/master/R/board.R
    # methods - browse, desc, pin_get, pin_remove, pin_find

    def __init__(self, board, cache, versions):
        self.board = board

        if cache is None:
            cache = tempfile.TemporaryDirectory()
        self.cache = cache
        self.versions = versions

    def parse_meta(self, meta_path):
        with open(meta_path) as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    def write_data_txt(loc, metadata):
        with open(loc + "/data.txt", "w") as data_file:
            yaml.dump(metadata, data_file)

class Board_Rsconnect(
    Board
):  # https://github.com/rstudio/pins/blob/master/R/board_rsconnect.R
    def __init__(
        self,
        server=os.getenv("CONNECT_SERVER"),
        key=os.getenv("CONNECT_API_KEY"),
        cache=None,
        versions=False,
    ):
        if server is None:
            raise IOError("No server arg provided")

        if key is None:
            raise IOError("No key arg provided")

        super().__init__("rsconnect", cache, versions)
        self.server = server
        self.__auth = {"Authorization": "Key " + key}  

    def pin_download(self, name, version = None, hash = None):
        meta = self.pin_meta(name)
        if meta is not None:
            return self.__download(meta["url"], meta['file'])

    def pin_get(self, name, version=None, hash=None):
        meta = self.pin_meta(name)
        # get solo URL of content
        # note -- meta called again, good way to solve?
        path = self.pin_download(name, version, hash)

        if path is not None:
            ret = path
            if meta['type'] == "csv":
                ret = pandas.read_csv(path)

            return ret

    def __download(self, content_url, name):
        dest_file = self.cache.name + "/" + name

        if not os.path.exists(dest_file):
            pin = self.rsc_GET(content_url + "/" + name)
            with open(dest_file, "wb") as file:
                file.write(pin.content)

        return dest_file

    def pin_meta(self, name):
        pin_dat = self.search(name)
        if len(pin_dat) > 0:
            pin_dat = pin_dat[0]
            meta_path = self.__download(pin_dat["content_url"], "data.txt")

            meta = self.parse_meta(meta_path)
            meta["url"] = pin_dat["content_url"]

            return meta

    def search(self, name=None):
        if name is not None:
            name = {"name": name}

        content = self.find_rsc_content(name)
        return [x for x in content if x["content_category"] == "pin"]

    def find_rsc_content(self, name):
        return self.rsc_GET(self.api_v1("content"), {"name":name}).json()

    def pin_upload(self, name, path, metadata=None, access_type="acl"):
        #TODO: check access type

        # Find/create content item
        description = ""
        if metadata is not None and "description" in metadata.keys():
            description = metadata['description']
             
        content = self.check_content(name, access_type, description)
        guid = content['guid']

        # Make bundle including data.txt, index.html, and data from path
        bndl_dir = tempfile.TemporaryDirectory().name
        self.make_bundle(bndl_dir, path, metadata)
        bndl_tar = self.make_tarfile(bndl_dir)

        # Upload Bundle
        #TODO: make it accept a file
        bndl = self.rsc_POST(api_v1("/".join(["content",guid, "deploy"])), bndl_tar).json()

        # Deploy
        task = self.rsc_POST(api_va("/".join(["content",guid,"deploy"])), {"bundle_id": bndl['bundle_id']})

        # TODO: clean up old versions
        # What to return?

    def make_tarfile(self, dir, filename):
        tf = tempfile.NamedTemporaryFile().name
        with tarfile.open(tf, "w:gz") as tar:
            tar.add(dir, arcname=os.path.basename(dir))
        
        return(tf)

    def make_bundle(self, bndl_dir, path, metadata):
        filename = ntpath.basename(path)
        filepath = bndl_dir + "/" + filename
        # TODO: WHY DOESN'T THIS WORK????
        shutil.copy(path, filepath)

        self.write_data_txt(bndl_dir + "/data.txt")
        self.write_preview(bndl_dir)
        self.write_manifest(bndl_dir, filename)

    def write_manifest(self, loc, filename):
        manifest = {"version": 1,
        "locale": "en_US",
        "platform": "3.5.1",
        "metadata": {
            "appmode": "static",
            "primary_rmd": None,
            "primary_html": "index.html",
            "content_category": "pin",
            "has_parameters": False,
        },
        "packages": None,
        "files": ["data.txt", "index.html", filename],
        "users": None}

        with open(loc + "/manifest.json", "w") as manifest_loc:
            json.dump(manifest, manifest_loc)

    def write_preview(self, loc):
        #TODO: customize to pin
        lines = ["<h1>Python Pin", "\n"]
        with open(loc + "\index.html", "w") as index:
            for line in lines:
                index.write(line)

    def check_content(self, name, access_type, description):
        content = self.find_rsc_content(name)
        if content:
            return content[0]
        else:
            return create_rsc_content(name, access_type, description)

    def create_rsc_content(self, name, access_type, description):
        data = {"name": name, "title": name, "access_type": access_type, "description":description}
        return self.rsc_POST(self.api_v1("content"), data).json()

    def api_v1(self, endpoint):
        return self.server + "/__api__/v1/" + endpoint

    def rsc_GET(self, url, params=None):
        return req.get(
            url,
            headers=self.__auth,
            params=params,
        )

    def rsc_POST(self, url, data):
        return req.post(url, headers = self.__auth, json = data)


board = Board_Rsconnect()
#board.search("diamonds")
#board.pin_meta("diamonds")
#board.pin_get("diamonds")
#board.pin_get("cars_test")
board.pin_upload("python_pins_test", '/Users/alexkgold/rstudio/python-pins/cars.csv')


