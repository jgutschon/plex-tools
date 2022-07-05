import os
import re

path = os.getcwd()

for root, movies, things in os.walk(path):
    for movie in movies:
        for new_root, folders, files in os.walk(f"{path}/{movie}"):
            for file in files:
                ext = file.split('.')[-1]
                if ext == 'srt':
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
                    new_name = movie
                    if lang is not None:
                        new_name += f".{lang}"
                    if sdh:
                        new_name += '.sdh'
                    if forced:
                        new_name += '.forced'
                    new_name += f".{ext}"

                    # print(f"{file} -> {new_name}")
                    try:
                        os.rename(f"{movie}/{file}", f"{movie}/{new_name}")
                    except FileNotFoundError:
                        os.rename(f"{movie}/Subs/{file}", f"{movie}/{new_name}")
