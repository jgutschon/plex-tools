import os
import re

# File types
junk_files = [
    'txt',
    'png',
    'jpg',
    'jpeg',
    'nfo',
    'info',
    'exe',
]

sub_files = [
    'srt',
    'smi',
    'ssa',
    'ass',
    'vtt',
]

path = os.getcwd()
series_name = path.split('/')[-1]

season_regex = '(?:(?<=(Season ))\d{1,2}|(?<=([s|S]))\d{2})'
episode_regex = '(?:(?<=(Episode ))\d{1,2}|(?<=([e|E]))\d{2})'

for root, dirs, files in os.walk(path):
    for file in files:
        ext = file.split('.')[-1]

        # Clean junk files
        if ext in junk_files:
            os.remove(os.path.join(root, file))
        else:
            # Find season number
            result = re.search(season_regex, file)
            season_num = '0'
            if result:
                season_num = result.group()
                if len(season_num) == 1:
                    season_num = '0' + season_num

                # Plex formatted season name
                season_name = f"Season {season_num}"
                if not os.path.isdir(f"{path}/{season_name}"):
                    os.mkdir(f"{path}/{season_name}")

            # Find episode number
            result = re.search(episode_regex, file)
            episode_num = '0'
            if result:
                episode_num = result.group()
                if len(episode_num) == 1:
                    episode_num = '0' + episode_num

            # Rename episode
            os.rename(
                f"{os.path.join(root, file)}",
                f"{season_name}/{series_name} - s{season_num}e{episode_num}.{ext}"
            )

    # Clear out empty folders
    for dir in dirs:
        dir_path = os.path.join(root, dir)
        if len(os.listdir(dir_path)) == 0:
            os.rmdir(dir_path)
