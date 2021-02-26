import os

__title__ = 'app'
__author__ = 'Gloryness'
__license__ = 'MIT License'
__version__ = '2021.02.26'
__module__ = os.getcwd()

if not __module__.endswith("app"):
    __module__ = __module__+'\\'
    github_db = __module__+'github_db.exe'
    if not os.path.isfile(github_db):
        github_db = 'github_db.exe'
    is_executable = True
else:
    __module__ = __module__.replace("app", "").replace("/", "\\")
    github_db = __module__+'app\\github_db.exe'
    is_executable = False

path = lambda *p: __module__+'\\'.join(p)