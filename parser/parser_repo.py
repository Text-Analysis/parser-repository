import requests
import os
from typing import Dict
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
        self.list_paths = self.__craw_repository(os.path.join(refactor_path, repo))

    def __craw_repository(self, repo_path: str, list_paths: list[Dict[str, str]] = None) -> list[Dict[str, str]]:
        if list_paths is None:
            list_paths = []

        for lists in os.listdir(repo_path):
            path = os.path.join(repo_path, lists)
            if os.path.isdir(path):
                self.__craw_repository(path, list_paths)
            else:
                file_name = os.path.basename(path)
                suffix = os.path.splitext(file_name)[1]
                if suffix == ".py":
                    obj = {
                        'file_name': file_name,
                        'path': path,
                    }
                    list_paths.append(obj)
        return list_paths

    def get_data(self) -> list:
        data = []
        for obj_path in self.list_paths:
            file_name = obj_path.get('file_name')
            path = obj_path.get('path')
            parser_file = ParserFile(path)
            content = parser_file.get_data()
            data.append({
                'file_name': file_name,
                "content": content
            })
        return data
