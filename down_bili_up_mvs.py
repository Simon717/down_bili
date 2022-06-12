import requests, math, random, re, os
import concurrent.futures
import time

start = time.time()

mid = 170028324  # 修改1，B站UP主的mid，从网址复制
video_dir = "./vid_pro"

URL = 'https://api.bilibili.com/x/space/arc/search?mid={}&ps=30&tid=0&pn={}&keyword=&order=pubdate&jsonp=jsonp'


def get_video_list():
    os.makedirs(video_dir, exist_ok=True)

    ps = int(re.findall('ps=(.*?)&', URL)[0])
    up_res = requests.get(url=URL.format(mid, 1)).json()
    total_video_counts = up_res['data']['page']['count']
    total_page_counts = math.ceil(total_video_counts / ps)
    time.sleep(0.05)

    video_list = []
    for i in range(total_page_counts):
        cur_page_res = requests.get(url=URL.format(mid, i + 1)).json()
        for item in cur_page_res['data']['list']['vlist']:
            tem_dict = {}
            tem_dict['url'] = f"https://www.bilibili.com/video/{item.get('bvid')}"
            video_list.append(tem_dict)
        time.sleep(random.uniform(0.05, 0.2))

    print(f"一共有视频 {len(video_list)}个")

    return video_list


def download_single(url):
    os.system(f"you-get -o {video_dir} {url}")


if __name__ == '__main__':
    start_time = time.time()
    video_list = get_video_list()
    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
        for item in video_list:
            executor.submit(download_single, item.get("url"))
    print('Thread pool execution in ' + str(time.time() - start_time), 'seconds')
