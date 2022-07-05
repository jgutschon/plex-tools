# Plex Tools

This repo contains scripts used to automate tasks for a Plex server and maintaining torrents with the `transmission-remote` BitTorrent client.

## Scripts

### `download-complete.sh`

Upon finishing a download, this script is ran automatically. This deletes the .torrent files, moves completed downloads to the Plex directory, and changes the permissions of the resulting video files so they are owned by the `plex` user.

### `movie-rename.py`

This script is ran at the root folder of a movie torrent, and renames the video and subtitle files to the Plex naming format. This also deletes all junk files (.txt, .png, etc).

### `series-rename.py`

This script is ran at the root folder of a series torrent directory, and renames all episodes and seasons to the Plex naming format. Use with caution, this doesn't cover all naming schemes.
