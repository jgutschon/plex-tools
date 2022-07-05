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
title = path.split('/')[-1]

for root, dirs, files in os.walk(path):
    for file in files:
        ext = file.split('.')[-1]

        # Clean junk files
        if ext in junk_files:
            os.remove(file)

        # Organize subtitles
        elif ext in sub_files:
            # Check for either English, German, Spanish subs
            lang = None
            en_lang_re = '([E|e][N|n]|[E|e]nglish|ENG|[E|e]ng)(?=\.|-| |\]|\))'
            de_lang_re = '([D|d][E|e]|[D|d]eutsch|DEU|[D|d]eu)(?=\.|-| |\]|\))'
            es_lang_re = '([E|e][S|s]|[S|s]panish|SPA|[S|s]pa)(?=\.|-| |\]|\))'
            if re.search(en_lang_re, file):
                lang = 'eng'
            elif re.search(de_lang_re, file):
                lang = 'deu'
            elif re.search(es_lang_re, file):
                lang = 'spa'

            # Check for CC subs
            sdh = False
            sdh_re = '(SDH|[S|s]dh)(?=\.|-| |\]|\))'
            if re.search(sdh_re, file):
                sdh = True

            # Check for forced subs
            forced = False
            forced_re = '(FORCED|[F|f]orced)(?=\.|-| |\]|\))'
            if re.search(forced_re, file):
                forced = True

            # Generate new name
            new_name = title
            if lang is not None:
                new_name += f".{lang}"
            if sdh:
                new_name += '.sdh'
            if forced:
                new_name += '.forced'
            new_name += f".{ext}"

            try:
                os.rename(file, new_name)
            except FileNotFoundError:
                os.rename(f"Subs/{file}", new_name)

        # Organize movies
        else:
            name = f"{title}.{ext}"

            # Check for junk video files
            if os.path.exists(name):
                if os.path.getsize(file) < os.path.getsize(name):
                    os.remove(file)
                else:
                    os.remove(name)
                    os.rename(file, name)
            else:
                os.rename(file, name)
