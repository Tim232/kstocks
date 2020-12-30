import asyncio
import re
from concurrent.futures import ThreadPoolExecutor

import aiohttp
from scrapy.selector import Selector


class Performance:
    """Performance Module
    - run_in_threadpool
    """

    def __init__(self, max_threads: int = 4):
        """
        ```
        Performance(max_threads: int)
        max_threads:
            Default 4
        ```
        """
        self.running_threads = 0  # Fixed value
        self.max_threads = max_threads

    async def run_in_threadpool(self, function):
        """run_in_threadpool Usage:
        ```
        ...
        async def main():
            data = await run_in_threadpool(lambda: function())
            return data
        ```
        """
        global running_threads

        while self.running_threads >= self.max_threads:
            await asyncio.sleep(1)

        with ThreadPoolExecutor(max_workers=1) as thread_pool:
            running_threads = self.running_threads + 1

            loop = asyncio.get_event_loop()
            result = loop.run_in_executor(thread_pool, function)
            try:
                result = await result
            except Exception as e:
                raise e
            finally:
                running_threads = running_threads - 1
                thread_pool.shutdown(wait=True)
            return result


class Stocks:
    def __init__(self):
        self.loop = Performance()
        self.url = "https://m.stock.naver.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10.0.0; SM-G988NZKAKOO) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.101 Mobile Safari/537.36"
        }

    async def cleanText(self, text):
        loop = Performance()
        # cleanT = await loop.run_in_executor(None, re.sub, "<.+?>", "", str(text), 0, re.I|re.S)
        cleanT = await loop.run_in_threadpool(
            lambda: re.sub("<.+?>", "", str(text), 0, re.I | re.S)
        )
        return cleanT

    async def Request(self):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url=self.url) as resp:
                if resp.status != 200:
                    raise Exception("404 Not Found")
                html = await resp.text()
        soup = await self.loop.run_in_threadpool(lambda: Selector(text=html))
        return soup

    async def KOSPI(self):
        """코스피"""
        soup = await self.Request()

        kospi = await self.loop.run_in_threadpool(
            lambda: soup.xpath(
                '//*[@id="mflick"]/div/div[1]/div/ul/li[1]/a/div[1]/span'
            )
        )
        u_kospi = await self.loop.run_in_threadpool(
            lambda: soup.xpath('//*[@id="mflick"]/div/div[1]/div/ul/li[1]/a/div[1]/div')
        )

        _kospi = await self.loop.run_in_threadpool(lambda: kospi.getall()[0])
        _u_kospi = await self.loop.run_in_threadpool(lambda: u_kospi.getall()[0])

        clean = await self.cleanText(_kospi)

        clean2 = await self.cleanText(
            _u_kospi.strip()
            .replace('<span class="gap_rate">', "^")
            .replace("</em>", "^")
        )

        return f"코스피: {clean.strip()},    {clean2.strip().replace('^', '   ')}"

    async def KOSDAQ(self):
        """코스닥"""
        soup = await self.Request()

        kosdaq = await self.loop.run_in_threadpool(
            lambda: soup.xpath(
                '//*[@id="mflick"]/div/div[1]/div/ul/li[2]/a/div[1]/span'
            )
        )
        u_kosdaq = await self.loop.run_in_threadpool(
            lambda: soup.xpath('//*[@id="mflick"]/div/div[1]/div/ul/li[2]/a/div[1]/div')
        )

        _kosdaq = await self.loop.run_in_threadpool(lambda: kosdaq.getall()[0])
        _u_kosdaq = await self.loop.run_in_threadpool(lambda: u_kosdaq.getall()[0])

        clean = await self.cleanText(_kosdaq)
        clean2 = await self.cleanText(
            _u_kosdaq.strip()
            .replace('<span class="gap_rate">', "^")
            .replace("</em>", "^")
        )

        return f"코스닥: {clean.strip()},    {clean2.strip().replace('^', '   ')}"
