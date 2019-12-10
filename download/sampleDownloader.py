import os, requests

class SampleDownloader:
    def __init__(self):
        self.testUrl = "https://cdns-preview-9.dzcdn.net/stream/c-92d5bbb148445d41dc7be319744f1691-4.mp3"

        self.apiKeyHeaderKey = "x-rapidapi-key"
        self.apiKeyHeaderValue = "b5264b2c71mshf1c19fd9fd30ba4p17b725jsna13beb3023ee"
        self.hostHeaderKey = "x-rapidapi-host"
        self.hostHeaderValue =  "deezerdevs-deezer.p.rapidapi.com"
        self.searchUrl = "https://deezerdevs-deezer.p.rapidapi.com/search"
        self.searchQueryKey = "q"
        self.samplesDirectory = "./data/samples"

    def __download(self, url, filePath):
        get_response = requests.get(url, stream=True)
        with open(filePath, 'wb') as f:
            for chunk in get_response.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    def __findSampleUrl(self, title, artist):
        params = {self.searchQueryKey : "{} {}".format(title, artist)}
        headers = {self.hostHeaderKey : self.hostHeaderValue, self.apiKeyHeaderKey : self.apiKeyHeaderValue}
        response = requests.get(self.searchUrl, params=params, headers=headers)
        try:
            jsonResponse = response.json()
        
            if 'data' in jsonResponse and jsonResponse['data']:
                collection = jsonResponse['data']
                for item in collection: 
                    if item['duration'] > 200:
                        return item['preview'];
                return None
            else:
                #raise Exception("Song {} of artist {} was not found".format(title, artist))
            #print("Song {} of artist {} was not found".format(title, artist))
                return None
        except:
            print('Empty json response exception occurred')
            return None

    def downloadSong(self, title, artist, songId):
        sampleUrl = self.__findSampleUrl(title, artist)
        if sampleUrl:
            filePath = "{}/{}.mp3".format(self.samplesDirectory, songId)
            self.__download(sampleUrl, filePath)
            return True
        else:
            return False

    def checkIfSongIsAvailable(self, title, artist, songId):
        sampleUrl = self.__findSampleUrl(title, artist)
        if sampleUrl:
            return True
        else:
            return False
