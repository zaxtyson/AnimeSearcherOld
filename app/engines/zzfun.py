import requests
from hashlib import md5
from app.models import VideoList, Video, DefaultHandler, BaseEngine
from app import logger


class Engine(BaseEngine):

    @staticmethod
    def search(name):
        """搜索接口2"""
        logger.info(f'引擎 {__name__} 正在搜索: {name}')
        result = []
        search_api = 'http://111.230.89.165:8089/android/search'
        info_api = 'http://111.230.89.165:8089/android/video/list_ios'

        req = Engine.post(search_api, data={'userid': '', 'key': name})
        if req.status_code != 200 or req.json().get('errorCode') != 0:
            return result
        video_id_list = [int(v['videoId']) for v in req.json().get('data')]  # 搜索结果: 视频 id
        for vid in video_id_list:
            req = Engine.get(info_api, {'userid': '', 'videoId': vid})
            if req.status_code != 200 or req.json().get('errorCode') != 0:
                continue
            info = req.json().get('data')  # 视频详情信息
            video_list = VideoList()
            video_list.engine = __name__
            video_list.title = info['videoName']
            video_list.cover = info['videoImg']
            video_list.desc = info['videoDoc'] or '视频简介弄丢了 (/▽＼)'
            video_list.cat = info['videoClass'].split('/')
            logger.info(f"引擎 {__name__} 正在处理: {video_list.title}")
            for video in info['videoSets'][0]['list']:
                name = f"第 {video['ji']} 集"
                video_list.add(Video(name, raw_url=video['playid'], handler=PlayIdHandler))  # playid: xxx-x-x
            result.append(video_list)
        return result


class PlayIdHandler(DefaultHandler):

    def get_real_url(self):
        """通过视频的 play_id 获取视频链接"""
        logger.info(f"PlayIdHandler 正在处理: {self.raw_url}")
        play_api = 'http://111.230.89.165:8089/android/video/play'
        play_id = self.raw_url
        secret_key = '534697'  # 这个值无法通过抓包得到,而是从客户端逆向出来的
        sing = md5((play_id + secret_key).encode('utf-8')).hexdigest()
        payload = {'playid': play_id, 'userid': '', 'apptoken': '', 'sing': sing}
        req = requests.post(play_api, data=payload)
        if req.status_code != 200 or req.json().get('errorCode') != 0:
            return ''
        real_url = req.json()['data']['videoplayurl']
        logger.info(f"PlayIdHandler return: {real_url}")
        return real_url
