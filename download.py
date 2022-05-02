import os
import shutil
import pickle as pkl
from tqdm import tqdm
from argparse import ArgumentParser
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

with open('file_ids.pkl', 'rb') as f:
	video_ids = pkl.load(f)

# mapping of views with camera ID
view_dict = {
			'v1': 'C10095_rgb',
			'v2': 'C10115_rgb',
			'v3': 'C10118_rgb',
			'v4': 'C10119_rgb',
			'v5': 'C10379_rgb',
			'v6': 'C10390_rgb',
			'v7': 'C10395_rgb',
			'v8': 'C10404_rgb',
			'e1': ['HMC_84346135_mono10bit', 'HMC_21176875_mono10bit'],
			'e2': ['HMC_84347414_mono10bit', 'HMC_21176623_mono10bit'],
			'e3': ['HMC_84355350_mono10bit', 'HMC_21110305_mono10bit'],
			'e4': ['HMC_84358933_mono10bit', 'HMC_21179183_mono10bit']
			}

parser = ArgumentParser(description="Download Assembly101")
parser.add_argument('--videos', type=str, default='all', choices=list(video_ids.keys())+['all'],
                    help = 'whether to download specific videos for all of them.')
parser.add_argument('--views', type=str, default='all', choices=list(view_dict.keys())+['all', 'fixed', 'egocentric'],
                    help = 'whether to download all views or only fixed (RGB) or egocentric (monochrome) views.')
parser.add_argument('--outDir', type=str, default='downloads')
parser.add_argument('--resume', type=bool, default=False)

args = parser.parse_args()
print(f'........Downloading videos: {args.videos}')
print(f'........Downloading views: {args.views}')

master_dict = {}
''' structure of master_dict after filling:
{
	video_name1: 
	{
		view_name1.mp4 : pydrive_file}
		view_name2.mp4 : pydrive_file}
		.
		.
		.
	}
	video_name2:
	{
		.
		.
		.
	} 
	.
	.
	.
}
'''

# authenticate your google account
gauth = GoogleAuth()
drive = GoogleDrive(gauth)


def getAllFiles(video_name, video_id):
	file_list = drive.ListFile({'q' : f"'{video_id}' in parents and trashed=false"}).GetList()
	
	for file in file_list:
		master_dict[f"{video_name}/{file['title']}"] = file


def download_file(out_path, file_name, file):
	if not os.path.exists(out_path):		
		os.makedirs(out_path)
	try:
		file.GetContentFile(file['title'])
		os.rename(f'{file_name}', f'{out_path}/{file_name}')
	except:
		# if any video fails to download completely, its name will be stored in error_downloading.txt
		with open('./error_downloading.txt', 'a') as f:
			f.write(f'{out_path}/{file_name}\n')
		os.remove(f'{file_name}')


if __name__ == '__main__':
	if args.videos == 'all':
		# if 'all' videos need to be downloaded
		for folder_name, folder_id in tqdm(video_ids.items(), 'Loading files from the server', total=len(video_ids)):
			getAllFiles(folder_name, folder_id)
	else:
		# if a single video by their name needs to be downloaded
		folder_name, folder_id = args.videos, video_ids[args.videos]
		getAllFiles(folder_name, folder_id)

	if not args.views == 'all':
		# if all views need to be downloaded for each video
		to_delete = []
		for x in master_dict:
			if args.views in {'egocentric', 'fixed'}:
				if (x.split('/')[-1][0] == 'C') and (args.views == 'egocentric'):
					to_delete.append(x)
				elif (x.split('/')[-1][0] == 'H') and (args.views == 'fixed'):
					to_delete.append(x)
			else:
				views = view_dict[args.views]
				if not isinstance(views, list):
					views = [views]
				if not x.split('/')[-1][:-4] in views:
					to_delete.append(x)

		for x in to_delete:
			del master_dict[x]

	if args.resume:
		# resuming from a previously expired download.py session
		# check 'outDir' for all the videos that have already been downloaded
		to_delete = []
		for x in tqdm(master_dict, 'Checking downloaded files'):
			if os.path.exists(f'{args.outDir}/{x}'):
				to_delete.append(x)
		print(f'#videos already downloaded = {len(to_delete)}')
		print(f'#videos remaining = {len(master_dict)-len(to_delete)}')
		for x in to_delete:
			del master_dict[x]
		print('........Resuming download')

	for video_path in tqdm(master_dict, 'Downloading'):
		path_lis = video_path.split('/')
		video_name = path_lis[-1]
		out_path = ('/').join(path_lis[:-1])
		out_path = f'{args.outDir}/{out_path}'

		video_file = master_dict[video_path]
		download_file(out_path, video_name, video_file)