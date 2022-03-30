import os
import requests


class YaUploader:
    def __init__(self, token_: str):
        self.token = token_

    def get_headers(self) -> dict:
        """Метод формирует словарь заголовков"""

        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_files_list(self) -> dict:
        """Метод получает данные о файлах, уже хранящихся на диске"""

        url = "https://cloud-api.yandex.net/v1/disk/resources/files"
        headers = self.get_headers()
        response = requests.get(url, headers=headers, timeout=5)
        print(headers)

        return response.json()

    def get_uplooad_link(self, y_disc_file_path: str) -> dict:
        """Метод получает ссылку на загрузку файла на яндекс диск"""

        up_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": y_disc_file_path, "overwrite": "true"}
        responce = requests.get(up_url, headers=headers, params=params)

        return responce.json()

    def upload(self, file_path: str, yd_path: str) -> str:
        """Метод загружает файлы по списку file_list на яндекс диск"""

        file_name_ = os.path.basename(file_path)
        href_json = self.get_uplooad_link(y_disc_file_path=yd_path)
        href = href_json['href']
        response = requests.put(href, data=open(file_path, 'rb'))
        # response.raise_for_status()

        if response.status_code < 300:
            return f"File '{file_name_}' successfully loaded to Yandex Disc."
        else:
            return f"Error code: {response.status_code}"


if __name__ == '__main__':

    path_to_file = input("Input full path to file directory ('c'- to choose a current one): \t")
    if path_to_file == 'c':
        path_to_file = os.path.abspath(os.curdir)

    file_name = input("Input your file name:\t")

    path_to_file = os.path.abspath(os.path.join(path_to_file, file_name))

    token = input("Input API token: \t")
    # token = TOKEN

    uploader = YaUploader(token)

    yd_path_to_file = input("Input a Yandex Disc directory name: \t")

    yd_path_to_file = yd_path_to_file + "/" + file_name

    print(uploader.upload(path_to_file, yd_path_to_file))