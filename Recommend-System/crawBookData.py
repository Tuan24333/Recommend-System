import asyncio
import aiohttp
from bs4 import BeautifulSoup
import csv
import time
import json
import aiocsv
import aiofiles
import time

lastBook = 0
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def get_book_info(session, book_url, indexBook):
    try:
        await asyncio.sleep(2)
        html = await fetch(session, book_url)
        soup = BeautifulSoup(html, "lxml") ## html.parser
        await asyncio.sleep(1)
        arr = [None]*16
        ## json
        jsonData = soup.find('script', {'type': 'application/json'}).get_text()
        jsonData = json.loads(jsonData)
        testNest = jsonData["props"]["pageProps"]["apolloState"]
        searchKey = ["Book:", "Work:", "Contributor:"]
        keyBook = [key for key, val in testNest.items() if searchKey[0] in key]
        keyWork = [key for key, val in testNest.items() if searchKey[1] in key]
        keyContributor = [key for key, val in testNest.items() if searchKey[2] in key]
        ## 
        keyDetails = testNest[keyBook[-1]]["details"]
        ##
        # title
        # arr[0] = soup.find("h1", class_="Text Text__title1").text.strip()
        arr[0] = book_url
        # book name
        arr[1] = testNest[keyBook[-1]]["title"]
        # author name
        arr[2] = testNest[keyContributor[0]]["name"]
        # publisher
        arr[3] = keyDetails["publisher"]
        # numPages
        arr[4] = keyDetails["numPages"]
        # format
        arr[5] = keyDetails["format"]
        # public date
        arr[6] = keyDetails["publicationTime"]
        # language
        arr[7] = keyDetails["language"]["name"]
        ## stats
        keyStats = testNest[keyWork[0]]["stats"]
        ##
        # ratings count
        arr[8] = keyStats["ratingsCount"]   
        # text reviewing counts
        arr[9] = keyStats["textReviewsCount"]  
        # genres
        listGenre = [genre["genre"]["name"] for genre in testNest[keyBook[-1]]["bookGenres"]]
        arr[10] = listGenre[0]
        # awards
        listAward = [award["name"] for award in testNest[keyWork[0]]["details"]["awardsWon"]]
        arr[11] = "@".join(listAward)
        # number of books
        arr[12] = testNest[keyContributor[0]]["works"]["totalCount"]
        # number of followers 
        arr[13] = testNest[keyContributor[0]]["followers"]["totalCount"]
        # ratings
        arr[14] = keyStats["averageRating"]
        # image url
        arr[15] = testNest[keyBook[0]]["imageUrl"]

        with open('dataset.csv', 'a') as f:
            # create the csv writer
            writer = csv.writer(f)

            # write a row to the csv file
            writer.writerow(arr)
        print(indexBook)
    except Exception as e:
        print("error",indexBook, book_url)
        print("-----------------------")
        print(e)
        print("-----------------------")

async def mainCrawl(start, stop):
    async with aiohttp.ClientSession(trust_env=True) as session:
        # response = await session.get("https://www.goodreads.com/genres/most_read/comics")
        # html = await response.text()
        # soup = BeautifulSoup(html, "html.parser")

        with open('url.txt', 'r') as f:
            # create the csv writer
            book_urls = f.read().splitlines()
            tasks = []
        
            for i in range(start, stop):
                tasks.append(asyncio.ensure_future(get_book_info(session, book_urls[i], i)))
            await asyncio.gather(*tasks)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mainCrawl(9000,9800))
