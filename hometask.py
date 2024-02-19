import threading
import multiprocessing
import asyncio
import aiohttp
import requests
import os
from time import time
import logging
import argparse



"""
Задание

Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск. 
Каждое изображение должно сохраняться в отдельном файле, 
название которого соответствует названию изображения в URL-адресе.
Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
— Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
— Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
— Программа должна выводить в консоль информацию о времени скачивания каждого изображения
 и общем времени выполнения программы.
"""


urls = ["https://wallpaperaccess.com/full/4958480.jpg",
 "https://www.wallpapers13.com/nature-lake-bled-desktop-background-image/",
 "https://www.imagelighteditor.com/img/bg-after.jpg"]
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_image(url):
    logger.info("get_image launched")
    responce = requests.get(url)
    name = url.replace("/", " ").split()[-1]
    if not os.path.exists("urls_folder"):
        os.mkdir("urls_folder")

    with open(f"urls_folder/{name}", "wb") as f:
        f.write(responce.content)

########    THREADING ###############
threads = []
def get_image_thr(urls):
    logger.info("get_image_thr has launched")
    for i in urls:
        thr = threading.Thread(target=get_image, args=(i, ))
        threads.append(thr)
        thr.start()
    for i in threads:
        i.join()



########    MULTIPROCESSING ###############
processes = []
def get_image_prc(urls):
    logger.info("get_image_prc has launched")
    for i in urls:
        thr = multiprocessing.Process(target=get_image, args=(i, ))
        processes.append(thr)
        thr.start()
    for i in threads:
        i.join()



########    ASYNCIO ###############
async def download(url):
    logger.info("download has launched")

    async with aiohttp.ClientSession() as f:
        async with f.get(url) as responce:
            res = await responce.read()
            name = url.replace("/", " ").split()[-1]
            if not os.path.exists("urls_folder"):
                os.mkdir("urls_folder")
            with open(f"urls_folder/{name}", "wb" ) as f:
                f.write(res)

asyn_list = []
async def get_image_asyn(urls):
    logger.info("get_image_asyn has launched")

    tasks = [download(url) for url in urls]
    await asyncio.gather(*tasks)




def arg_pars():
    parse = argparse.ArgumentParser(description="doenload images from urls")
    parse.add_argument("-u", "--urls",nargs="*")
    return parse.parse_args()

if __name__ == "__main__":
    start_time = time()
    pars = arg_pars()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_image_asyn(pars.urls))
    
    logger.info(f"time: {round(time()  - start_time, 2)}")