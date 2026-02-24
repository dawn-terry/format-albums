import argparse
import music_tag
import os
import string

parser = argparse.ArgumentParser("format_albums")
parser.add_argument("-p", "--path", help="Path of folder containing albums", default=".")
parser.add_argument("-o", "--output", help="Path of folder to sort to", default="./sorted_albums")
args = parser.parse_args()

path:str = args.path
output_path:str = args.output


def main():
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    folders: list(str) = list_folders(path)
    for album in folders:
        print(f"Processing {capitalise_string(album)}")
        album_path = os.path.join(args.path, album)
        try:
            possible_artists_set.clear()
        except:
            possible_artists_set = set()
        try:
            possible_albums_set.clear()
        except:
            possible_albums_set = set()
        songs: list(str) = list_songs(album_path)
        album_index = 1
        if songs:
            for song in songs:
                song_path = os.path.join(album_path, song)
                f = music_tag.load_file(song_path)
                track_title = capitalise_string(str(f['tracktitle']))
                print(f"  Track {album_index}: {track_title}")

                if len(str(f['artist'])) > 1:
                    possible_artists_set.add(capitalise_string(str(f['artist'])))
                if len(str(f['albumartist'])) > 1:
                    possible_artists_set.add(capitalise_string(str(f['album artist'])))
                if len(str(f['album'])) > 1:
                    possible_albums_set.add(capitalise_string(str(f['album'])))
                album_index += 1

            print(f"Possible artists: {possible_artists_set}")
            possible_artists_list = list(possible_artists_set)
            if len(possible_artists_list) == 1:
                artist = possible_artists_list[0]
            else:
                print(f"Pick an artist name for this album from one of these or 0 for text input")
                possible_artist_index = 1
                for possible_artist in possible_artists_list:
                    print(f"{possible_artist_index}: {possible_artist}")
                    possible_artist_index += 1
                choice = input()

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
    exceptions = ["I'm", "'s", "'t", "'ll", "'re", "'ve"]
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

if __name__ == "__main__":
    main()

