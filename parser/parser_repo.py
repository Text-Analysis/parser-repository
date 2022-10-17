import pprint

import requests
import os
from parser import ParserFile
from dotenv import load_dotenv

load_dotenv()

github_api = 'https://api.github.com/'
TOKEN = os.environ['TOKEN']


class ParserRepo:

    def __init__(self, owner: str, repo: str):

        request = '{0}repos/{1}/{2}'.format(github_api, owner, repo)
        response = requests.get(request, headers={'Authorization': 'token {0}'.format(TOKEN)})
        content = response.json()

        download_url = content["clone_url"]
        os.system("git clone {0}".format(download_url))

        root_dir = os.path.dirname(__file__)
        refactor_path = '/'.join(root_dir.split('/')[:-1])

        obj_default = {
            "dir_name": repo,
            "files": [],
            "dirs": [],
        }
        self.obj_repository = self.__craw_repository(os.path.join(refactor_path, repo), obj_default)
        self.obj_repository = self.__clear_repository_obj(self.obj_repository)
        pprint.pprint(self.obj_repository)

    def __clear_repository_obj(self, obj):
        if len(obj["dirs"]) == 0 and len(obj["files"]) == 0:
            obj["parent"]["dirs"].remove(obj)
            return self.__clear_repository_obj(obj["parent"])
        for obj_dir in obj["dirs"]:
            self.__clear_repository_obj(obj_dir)
        return obj

    def __craw_repository(self, repo_path: str, obj):

        for name_path in os.listdir(repo_path):
            path = os.path.join(repo_path, name_path)
            if os.path.isdir(path):
                obj_dir = {
                    "dir_name": name_path,
                    "files": [],
                    "dirs": [],
                    "parent": obj,
                }
                obj["dirs"].append(obj_dir)
                self.__craw_repository(path, obj_dir)
            else:
                file_name = os.path.basename(path)
                suffix = os.path.splitext(file_name)[1]
                if suffix == ".py":
                    parser_file = ParserFile(path)
                    content = parser_file.get_data()
                    obj_file = {
                        'file_name': file_name,
                        'path': path,
                        "parent": obj,
                        "content": content,
                    }
                    obj["files"].append(obj_file)
        return obj

    def get_data(self):
        return self.obj_repository
