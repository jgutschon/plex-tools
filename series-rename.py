import os
import re

path = os.getcwd()
series_name = path.split('/')[-1]

season_regex = '(?:(?<=(Season ))\d{1,2}|(?<=([s|S]))\d{2})'
episode_regex = '(?:(?<=(Episode ))\d{1,2}|(?<=([e|E]))\d{2})'

for root, seasons, files in os.walk(os.getcwd()):
    for season in seasons:
        # Find season number
        result = re.search(season_regex, season)
        season_num = '0'
        if result:
            season_num = result.group()
            if len(season_num) == 1:
                season_num = '0' + season_num
        
            # Rename season
            os.rename(season, f"Season {season_num}")

        for root, seasons, episodes in os.walk(f"{os.getcwd()}/Season {season_num}"):
            for episode in episodes:
                # Find episode number
                result = re.search(episode_regex, episode)
                episode_num = '0'
                if result:
                    episode_num = result.group()
                    if len(episode_num) == 1:
                        episode_num = '0' + episode_num

                # Find episode title and extension
                title = episode.split(' - ')[-1].split('.')[0].split('(')[0].strip(' ')
                ext = episode.split('.')[-1]

                # Rename episode
                os.rename(
                    f"Season {season_num}/{episode}",
                    f"Season {season_num}/{series_name} - s{season_num}e{episode_num} - {title}.{ext}"
                )
