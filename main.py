import os

import requests as req


class YaUploader:
    
    base_url = 'https://cloud-api.yandex.net/v1/disk/'
    
    def __init__(self, token: str):
        self.token = token
    
    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def upload(self, file_path: str):
        """Метод загружает файл, путь к которому указан в file_path, на яндекс диск"""
        url_to_get_upload_url = YaUploader.base_url + 'resources/upload'
        file_name = os.path.basename(file_path)
        upload_url = req.get(url_to_get_upload_url, params={'path': file_name, 'overwrite': True}, headers=self.get_headers())
        if upload_url.status_code != 200:
            return f'Ошибка при получении url для загрузки:\n {upload_url}!\n{upload_url.json()}'
        upload_href = upload_url.json()['href']
        res = req.put(upload_href, data=open(file_path, 'rb'))
        if res.status_code == 201:
            return 'Файл успешно загружен'
        else:
            return f'Ошибка при загрузке файла:\n {res}!'


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    path_to_file = input('Введите путь к файлу для загрузки на Яндекс.Диск: ')
    token = input('Введите токен для обращения к Яндекс.Диску: ')
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file)
    print(result)