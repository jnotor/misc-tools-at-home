import urllib.parse
import webbrowser


from fetcher import Fetcher

def main():
    fetcher = Fetcher()

    for x in fetcher.fetch_songs_in_playlist('hades faves'):
        yt_url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(f'{x} audio only')
        webbrowser.open_new(yt_url)

        link = input('link?')
        if link == '':
            continue

        print(link)


if __name__ == '__main__':
    main()