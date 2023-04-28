# [Assembly101](https://assembly-101.github.io/) downloader
![model](https://github.com/assembly-101/assembly-101.github.io/blob/main/docs/assets/assembly.jpg)
Assembly101 is a new procedural activity dataset featuring 4321 videos of people assembling and disassembling 101 "take-apart" toy vehicles. Participants work without fixed instructions, and the sequences feature rich and natural variations in action ordering, mistakes, and corrections. Assembly101 is the first multi-view action dataset, with simultaneous static (8) and egocentric (4) recordings. Sequences are annotated with more than 100K coarse and 1M fine-grained action segments, and 18M 3D hand poses. We benchmark on three action understanding tasks: recognition, anticipation and temporal segmentation. Additionally, we propose a novel task of detecting mistakes. The unique recording format and rich set of annotations allow us to investigate generalization to new toys, cross-view transfer, long-tailed distributions, and pose vs. appearance. We envision that Assembly101 will serve as a new challenge to investigate various activity understanding problems.
- - -
This repository provides scripts for downloading Assembly101 from [Gdrive](https://drive.google.com/drive/folders/1nh8PHwEw04zxkkkKlfm4fsR3IPEDvLKj). Please submit an access request with your google account. Owing to concerns regarding security and server traffic overload, only one google account per individual will be provided access for an initial 14 days. If your current access expires, please request for another access mentioning "renewal" in the comments to extend it for another 14 days.

The folders present in the Gdrive are:
- `recordings`: containing all 362 recordings (12 views per recording - 8 fixed and 4 egocentric)
- `TSM_features`: containing per-frame visual features extracted by [TSM](https://openaccess.thecvf.com/content_ICCV_2019/papers/Lin_TSM_Temporal_Shift_Module_for_Efficient_Video_Understanding_ICCV_2019_paper.pdf)
- `poses@60fps`: containing 3D hand poses generated at 60fps
- `metadata.zip`: containing camera extrinsics and positions for all the 12 views

### Folder structure of the Assembly101 `recordings`:
```
recordings
├── nusar-2021_action_both_9086-c14a_9086_user_id_2021-02-16_153910
│   ├── C10095_rgb.mp4
│   ├── C10115_rgb.mp4
│   ├── C10118_rgb.mp4
│   ├── C10119_rgb.mp4
│   ├── C10379_rgb.mp4
│   ├── C10390_rgb.mp4
│   ├── C10395_rgb.mp4
│   ├── C10404_rgb.mp4
│   ├──HMC_21176875_mono10bit.mp4
│   ├──HMC_21176623_mono10bit.mp4
│   ├──HMC_21110305_mono10bit.mp4
│   ├──HMC_21179183_mono10bit.mp4
├── nusar-2021_action_both_9071-b06b_9071_user_id_2021-02-11_100739
│   ├── C10095_rgb.mp4
│   ├── .
│   ├── .
│   ├── .
.
.
.
```

## Dependencies
- Python3
- PyDrive2
- pickle, shutil, tqdm

## This repository contains the following files:
- `authenticate.py` : a python script to authenticate your google account [[Authentication](#authentication)]
- `download.py` : a python script to download the Assembly101 videos through CLI
- `file_ids.pkl` : a dictionary containing the mapping of the folder (video) names with the folder ids
- `client_secrets.json` : a dictionary containing the access credentials (submit an access request to [Gdrive](https://drive.google.com/drive/folders/1nh8PHwEw04zxkkkKlfm4fsR3IPEDvLKj) to get the `client_secret` key)
- `settings.yaml` : .yaml file to save your credentials once you authenticate
- `recording_names.txt` : .txt file containing names of all the 362 videos

Once you receive the `client_secret` key, update the `client_secrets.json` with the key.

`download.py` takes the following command-line arguments:

| Arguments | Remarks |
|-----------|---------|
|--videos    | you can selectively download any single video by its `name` or download all videos by setting the argument to be `all` (*default*) | 
|--views    | `all` downloads all the 12 views per video (*default*)<br/> `fixed` to download the 8 fixed (RGB) views per video <br/> `egocentric` to download the 4 egocentric (monochrome) views per video <br/> v`i` downloads fixed view `i` where i = 1....8 <br/> e`i` downloads egocentric view `i` where i = 1....4
|--outDir    |  main directory where you want the videos to be downloaded
|--resume    |  `True` or `False` <br/> if the downloading stopped for any reason and you want to resume from where you left off (this requires `outDir` to be identical to the previous download)

If any video fails to download it will be recorded in a `error_downloading.txt` file in the current directory.

### Which `camera_IDs` correspond to which `views` ?
```
C10095_rgb : v1
C10115_rgb : v2
C10118_rgb : v3
C10119_rgb : v4
C10379_rgb : v5
C10390_rgb : v6
C10395_rgb : v7
C10404_rgb : v8

HMC_84346135_mono10bit or HMC_21176875_mono10bit : e1
HMC_84347414_mono10bit or HMC_21176623_mono10bit : e2
HMC_84355350_mono10bit or HMC_21110305_mono10bit : e3
HMC_84358933_mono10bit or HMC_21179183_mono10bit : e4
```

### Egocentric views camera ID mapping:
For some videos the camera ID for egocentric (monochrome) views starts with `HMC_8...` and for some they start with `HMC_2...`. This occurs to the usage of different cameras for some of the videos. The camera ID mapping is as follows:

```
HMC_84346135_mono10bit : HMC_21176875_mono10bit
HMC_84347414_mono10bit : HMC_21176623_mono10bit
HMC_84355350_mono10bit : HMC_21110305_mono10bit
HMC_84358933_mono10bit : HMC_21179183_mono10bit
```

## Authentication
Google requires you to authenticate your google account (the account which already has access to the drive) at least once through a browser to access the contents of the drive through CLI. If you are working from a remote/headless machine with no browser, run the `authenticate.py` once on your local machine with an accessible browser to generate a `credentials.json`. Once this `credentials.json` is created you can move this file to your working directory in the remote/headless machine. For people working from a machine with an accesible browser, this step is not required to perform.

**Note:** Before proceeding with the above authentication protocol, please update the `client_secrets.json` file with the `client_secret` key provided with GDrive access.

# License
Assembly101 is licensed by us under the Creative Commons Attribution-NonCommerial 4.0 International License, found [here](https://creativecommons.org/licenses/by-nc/4.0/). The terms are :
- **Attribution** : You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- **NonCommercial** : You may not use the material for commercial purposes.
