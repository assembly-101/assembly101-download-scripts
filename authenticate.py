import os
import shutil
import pickle as pkl
from tqdm import tqdm
from argparse import ArgumentParser
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

gauth = GoogleAuth()

# if accessing from a remote server
if "SSH_CONNECTION" in os.environ:
	print('Remote server detected!! Authenticating from remote server not possible.')
	print('Please run [authentication.py] from a local machine where you can access the browser.')
	exit()

drive = GoogleDrive(gauth)

folder = '1nh8PHwEw04zxkkkKlfm4fsR3IPEDvLKj'
file_list = drive.ListFile({'q' : f"'{folder}' in parents and trashed=false"}).GetList()