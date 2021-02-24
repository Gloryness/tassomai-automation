import compress_json
import json
import os
import subprocess

from app import path
from base.common import retreive_temp_data

class Database:
    def __init__(self, folder, filename):
        self.folder = os.path.abspath(folder)
        self.filename = self.folder + f'\\{filename}'

        if not os.path.exists(self.folder): # making sure all the folders exist to avoid errors
            os.makedirs(self.folder)

        if not os.path.isfile(self.filename):
            compress_json.dump({}, self.filename)

        if self.filename == 'answers.lzma':
            subprocess.call([path('github_db.exe'), '-p', self.folder, '-g'], shell=True)
            content = retreive_temp_data(self.folder)
            compress_json.dump(content, self.filename)
        if self.filename == 'info.lzma':
            compress_json.dump({'email': '', 'password': ''})

    def _test_if_empty(self):
        try:
            compress_json.load(self.filename)
        except: # If the file is somehow 0 bytes
            compress_json.dump({}, self.filename)
            return True
        return False

    def cached(self, key):
        """
        Check if the question has already been stored.
        """
        empty = self._test_if_empty()
        if empty: return False

        data = compress_json.load(self.filename)
        if key in data.keys():
            return True
        return False

    def all(self):
        """
        Return the whole database.
        """
        empty = self._test_if_empty()
        if empty: return {}

        data = compress_json.load(self.filename)

        return data

    def store(self, dictionary):
        """
        Add to the database.
        """
        empty = self._test_if_empty()
        if empty: return {}

        data = compress_json.load(self.filename)

        data.update(dictionary)

        compress_json.dump(data, self.filename)

    def get(self, key, *keys):
        """
        Retrieve values in the database.
        :param key: A required key to get from the database
        :param keys: Optional other keys to get stacking up from the first key
        For example: get('1', '2', 3) is equal to data['1']['2'][3]
        """
        keys = list(keys)
        keys.insert(0, key)
        data = compress_json.load(self.filename)
        if not self.cached(key):
            return ""
        evalulated = 'data' + ''.join([f'[{ascii(keyy) if type(keyy) == str else keyy}]' for keyy in keys])
        return eval(evalulated)

    def clear(self):
        empty = self._test_if_empty()
        if empty: return {}

        data = json.loads('{}')
        compress_json.dump(data, self.filename)