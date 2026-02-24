import argparse
import music_tag
import os
import string
import re

parser = argparse.ArgumentParser("format_albums")
parser.add_argument("-p", "--path", help="Path of folder containing albums", default=".")
parser.add_argument("-o", "--output", help="Path of folder to sort to", default="./sorted_albums")
parser.add_argument("-v", "--verbose", action='store_true')
args = parser.parse_args()

path:str        = args.path
output_path:str = args.output
verbose:str     = args.verbose


def main():
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    folders: list(str) = list_folders(path)
    for album in folders:
        print(f"Processing: {capitalise_string(album)}")
        album_path = os.path.join(args.path, album)

        possible_artists_list = []
        possible_albums_list = []

        possible_years_list = []
        match = re.match(r'.*([1-2][0-9]{3})', album)
        if match is not None:
            try:
                possible_years_list.append(int(match.group(1)[:4]))
            except:
                pass
        songs: list(str) = list_songs(album_path)
        track_index = 1
        if songs:
            for song in songs:
                song_path = os.path.join(album_path, song)
                f = music_tag.load_file(song_path)
                track_title = capitalise_string(str(f['tracktitle']))
                print(f"  Track {track_index}: {track_title}")

                this_artist = capitalise_string(str(f['artist']))
                this_albumartist = capitalise_string(str(f['albumartist']))
                this_album = capitalise_string(str(f['album']))
                try:
                    this_year = int(str(f['year'])[:4])
                except:
                    this_year = 0
                                                
                if len(this_artist) > 1 and this_artist not in possible_artists_list:
                    possible_artists_list.append(this_artist)
                    print_debug(f"    Adding artist: {this_artist}")
                if len(this_albumartist) > 1 and this_albumartist not in possible_artists_list:
                    possible_artists_list.append(this_albumartist)
                    print_debug(f"    Adding albumartist: {this_albumartist}")
                if len(this_album) > 1 and this_album not in possible_albums_list:
                    possible_albums_list.append(this_album)
                    print_debug(f"    Adding album: {this_album}")
                if this_year > 0 and this_year not in possible_years_list:
                    possible_years_list.append(this_year)
                    print_debug(f"    Adding year: {this_year}")

                track_index += 1

            print_debug(f"Possible artists: {possible_artists_list}")
            if len(possible_artists_list) == 1:
                chosen_artist = possible_artists_list[0]
            else:
                print(f"Pick an artist name for this album from one of these or 0 for text input")
                possible_artist_index = 1
                for possible_artist in possible_artists_list:
                    print(f"{possible_artist_index}: {possible_artist}")
                    possible_artist_index += 1
                while True:
                    choice = input()
                    try:
                        int_choice = int(choice)
                        if int_choice == 0:
                            chosen_artist = input("Enter album name: ")
                            break
                        chosen_artist = possible_artists_list[int_choice - 1]
                        break
                    except:
                        print("Try again, you muppet.")
            print(f"Artist name: {chosen_artist}")

            print_debug(f"Possible albums: {possible_albums_list}")
            if len(possible_albums_list) == 1:
                chosen_album = possible_albums_list[0]
            else:
                print(f"Pick an album name for this album from one of these or 0 for text input")
                possible_album_index = 1
                for possible_album in possible_albums_list:
                    print(f"{possible_album_index}: {possible_album}")
                    possible_album_index += 1
                while True:
                    choice = input()
                    try:
                        int_choice = int(choice)
                        if int_choice == 0:
                            chosen_album = input("Enter album name: ")
                            break
                        chosen_album = possible_albums_list[int_choice - 1]
                        break
                    except:
                        print("Try again, you muppet.")
            print(f"Album name: {chosen_album}")

            print_debug(f"Possible years: {possible_years_list}")
            if len(possible_years_list) == 1:
                chosen_year:int = possible_years_list[0]
            else:
                print(f"Pick an year for this album from one of these or 0 for text input")
                possible_year_index = 1
                for possible_year in possible_years_list:
                    print(f"{possible_year_index}: {possible_year}")
                    possible_year_index += 1
                while True:
                    choice = input()
                    try:
                        int_choice = int(choice)
                        if int_choice == 0:
                            chosen_year = input("Enter year: ")
                            break
                        chosen_year = possible_years_list[int_choice - 1]
                        break
                    except:
                        print("Try again, you muppet.")
            print(f"Year: {chosen_year}")

            track_index:int = 1
            for song in songs:
                song_path = os.path.join(album_path, song)
                f = music_tag.load_file(song_path)
                extension = os.path.splitext(song_path)[1]

                track_title = capitalise_string(str(f['tracktitle']))

                print(f"New track name: {chosen_artist} - {chosen_album} - {track_index} - {track_title}{extension}")

                track_index += 1     
        else:
            print("No files, skipping...")
        print("\n")
             
def list_folders(path: str):
    return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]

def list_files(path: str):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def list_songs(path: str):
    return [f for f in os.listdir(path) 
            if os.path.isfile(os.path.join(path, f)) and 
               is_audio_file(os.path.join(path, f))]

def is_audio_file(file: str):
    return file.endswith(".mp3") or file.endswith(".flac") or file.endswith(".wav")

def capitalise_string(phrase: str):
    exceptions = ["I'm", "'s", "'t", "'ll", "'re", "'ve", "II", "III", "IV", "VI", "VII", "VIII", "IX"]
    fixed_phrase = phrase.replace("_", " ")
    wordList = fixed_phrase.split(" ")
    newWordList = []
    for word in wordList:
        isException = False
        for exception in exceptions:
            if word.endswith(exception):
                isException = True
        if isException:
            newWordList.append(word)
        else:
            newWordList.append(str.title(word))
    return " ".join(newWordList)

def print_debug(phrase: str):
    if verbose:
        print(phrase)
    
if __name__ == "__main__":
    main()

