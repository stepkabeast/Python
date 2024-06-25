import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from urllib.request import urlopen
import os
import ffmpeg

def get_tiktok_video_id(url):
    match = re.search(r'/video/(\d+)', url)
    if match:
        return match.group(1)
    return None

def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def process_video(input_video, output_video):
    # Временные файлы для промежуточных этапов
    slow_video_path = "videos/temp_slow.mp4"
    resized_video_path = "videos/temp_resized.mp4"
    temp_audio_path = "videos/temp_audio.aac"

    # Уменьшение скорости видео и применение фильтра setpts
    ffmpeg.input(input_video).output(slow_video_path, vf="setpts=1.1*PTS").run(overwrite_output=True)

    # Получение информации о видео
    video_info = ffmpeg.probe(slow_video_path)
    width = int(video_info['streams'][0]['width'])
    height = int(video_info['streams'][0]['height'])
    duration = float(video_info['format']['duration'])

    # Уменьшение разрешения на 90%
    new_width = int(width * 0.9)
    new_height = int(height * 0.9)

    # Если высота не делится на 2, уменьшим ее на 1
    if new_height % 2 != 0:
        new_height -= 1

    # Изменение размера видео
    ffmpeg.input(slow_video_path).output(resized_video_path, vf=f"scale={new_width}:{new_height}").run(overwrite_output=True)

    # Извлечение аудио из исходного видео
    ffmpeg.input(input_video).output(temp_audio_path, **{'c:a': 'aac', 'b:a': '192k'}).run(overwrite_output=True)

    # Комбинирование отфильтрованного видео и новой звуковой дорожки с обрезкой аудио до длительности видео
    video_stream = ffmpeg.input(resized_video_path)
    audio_stream = ffmpeg.input('never_gonna_give_you_up.mp3', t=duration)
    ffmpeg.concat(video_stream, audio_stream, v=1, a=1).output(output_video, acodec='aac', shortest=None).run(overwrite_output=True)

def download_video(link, id):
    print(f"Downloading video {id} from: {link}")

    cookies = {
        '_ga': 'GA1.1.854060230.1719229499',
        '_ga_ZSF3D6YSLC': 'GS1.1.1719229498.1.1.1719229926.0.0.0',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'ru,en;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'hx-current-url': 'https://ssstik.io/en-1',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://ssstik.io/en-1',
        'sec-ch-ua': '"Chromium";v="124", "YaBrowser";v="24.6", "Not-A.Brand";v="99", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'QjNubVQ2',
    }

    print("STEP 4: Getting the download link")
    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)

    if response.status_code != 200:
        print(f"Failed to get download link. Status code: {response.status_code}")
        return

    downloadSoup = BeautifulSoup(response.text, "html.parser")

    downloadLink = downloadSoup.find("a", href=True)["href"]
    videoTitle = downloadSoup.find("p").getText().strip()
    sanitizedTitle = sanitize_filename(videoTitle)

    print("STEP 5: Saving the video :)")
    os.makedirs("videos", exist_ok=True)
    mp4File = urlopen(downloadLink)
    temp_file = f"videos/temp-{id}.mp4"
    output_file = f"videos/{id}-{sanitizedTitle}.mp4"
    with open(temp_file, "wb") as output:
        while True:
            data = mp4File.read(4096)
            if data:
                output.write(data)
            else:
                break

    process_video(temp_file, output_file)
    os.remove(temp_file)

print("STEP 1: Open Chrome browser")
options = Options()
options.add_argument("start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
driver = webdriver.Chrome(options=options)
# Измените ссылку TikTok
driver.get("https://www.tiktok.com/@russian_lesson")

# Если вы получаете CAPTCHA TikTok, измените здесь TIMEOUT
# на 60 секунд, достаточно времени для того, чтобы вы могли выполнить CAPTCHA самостоятельно.
time.sleep(1)

scroll_pause_time = 1
screen_height = driver.execute_script("return window.screen.height;")
i = 1

print("STEP 2: Scrolling page")
while True:
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    if (screen_height) * i > scroll_height:
        break

print("STEP 2.5")
className = "css-x6y88p-DivItemContainerV2 e19c29qe8"

script = """
let l = [];
Array.from(document.getElementsByClassName("%s")).forEach(item => { 
    let a = item.querySelector('a');
    if (a) {
        l.push(a.href);
    }
});
return l;
""" % className

urlsToDownload = driver.execute_script(script)

print(f"STEP 3: Time to download {len(urlsToDownload)} videos")
for index, url in enumerate(urlsToDownload):
    print(f"Downloading video: {index}")
    download_video(url, index)
    time.sleep(10)
