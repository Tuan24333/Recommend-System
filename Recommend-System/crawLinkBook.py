import asyncio
import aiohttp
from bs4 import BeautifulSoup
import csv
import time
import json

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def get_link_book_a_page(session, book_url):
    try:
        html = await fetch(session, book_url)
        soup = BeautifulSoup(html, "lxml") ## html.parser
        book_urls = [f"https://www.goodreads.com{x['href']}" for x in soup.select("a.bookTitle")]
        with open('url.txt', 'a') as f:
            # create the csv writer
            for url in book_urls:
                f.write(url+"\n")
        print(book_url)
    except Exception as e:
        print("error:", book_url)
        print(e)
        pass

async def main():
    async with aiohttp.ClientSession() as session:
        book_urls = []
        for i in range(100):
            book_urls.append("https://www.goodreads.com/list/show/1938.What_To_Read_Next?page="+str(i+1))
        tasks = []
        for book_url in book_urls:
            tasks.append(asyncio.ensure_future(get_link_book_a_page(session, book_url)))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
