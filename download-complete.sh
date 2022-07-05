#!/bin/bash

SERVER="localhost:9091 -n transmission:transmission"
DONE_STATES=("Seeding" "Stopped" "Finished" "Idle")

TORRENT_LIST=$(transmission-remote $SERVER -l | sed -e '1d' -e '$d' | awk '{print $1}' | sed -e 's/[^0-9]*//g')

for TORRENT_ID in $TORRENT_LIST; do
    INFO=$(transmission-remote $SERVER --torrent "$TORRENT_ID" --info)
    NAME=$(echo "$INFO" | sed -n 's/.*Name: \(.*\)/\1/p')
    
    PROGRESS=$(echo "$INFO" | sed -n 's/.*Percent Done: \(.*\)%.*/\1/p')
    STATE=$(echo "$INFO" | sed -n 's/.*State: \(.*\)/\1/p')

    # check if torrent is 100% done and state is none of the done states
    if [[ "$PROGRESS" == "100" ]] && [[ "${DONE_STATES[@]}" =~ "$STATE" ]]; then
        # remove torrent
        transmission-remote $SERVER --torrent "$TORRENT_ID" --remove

        PLEX_DL="/opt/plexmedia/downloads"

        # move completed download to plex downloads location
        sudo mv "/var/lib/transmission-daemon/downloads/$NAME" "$PLEX_DL"
        sudo chown -R plex:plex "$PLEX_DL/$NAME"
        sudo chmod o+w "$PLEX_DL/$NAME"
    else
        echo "Torrent #$TORRENT_ID is $PROGRESS% done with state \"$STATE\". Ignoring."
    fi    
done
