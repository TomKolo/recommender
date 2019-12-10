from download.datasetSamplesDownloader import DatasetSamplesDownloader
import pandas as pd

if __name__ == '__main__':
    with open(".\\FOUND_TOTAL_UNIQUE.txt", 'r') as f:
        ids = f.readlines()
    idsWithoutNewLine = []
    for id in ids:
        idsWithoutNewLine.append(id.strip())
    idsSet = set(idsWithoutNewLine)
    #songs = pd.read_csv("./data/song_dataset.csv", encoding="Latin1")
    #ratings = pd.read_csv("./data/songs_ratings.csv", encoding="Latin1")

    #df = songs[songs['song_id'].isin(idsWithoutNewLine)]
    #df.to_csv(".\\filtered_songs_data.csv",encoding="Latin1", index=False)

    #df = ratings[ratings['song_id'].isin(idsWithoutNewLine)]
    #df.to_csv(".\\filtered_ratings.csv",encoding="Latin1", index=False)

    ratings = pd.read_csv(".\\filtered_ratings.csv", encoding="Latin1")
    print(len(ratings)) #1307803