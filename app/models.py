from hashlib import md5
import requests
import re
from flask import request, Response


class Video(object):
    """单个视频对象"""

    def __init__(self, name, raw_url, type='mp4', handler=None):
        self.name = name  # 视频名
        self.type = type  # 视频格式: mp4 hls flv ...
        self.raw_url = raw_url  # 原始 URL
        self.hash = md5(raw_url.encode('utf-8')).hexdigest()  # URL 的 hash,用作数据库的 key
        self.handler = DefaultHandler if not handler else handler  # 该视频对应的 Handler,进一步处理视频

    def __repr__(self):
        return f'<Video {self.name}>'

    def json(self):
        """视频对象转 json 格式"""
        return {
            'name': self.name,
            'type': self.type,
            'hash': self.hash
        }


class VideoList(object):
    """视频列表对象(一部动漫)"""

    def __init__(self, title='', cover='', cat=None, desc=''):
        self.title = title  # 动漫名
        self.cover = cover  # 封面 URL
        self.cat = cat or []  # 分类
        self.desc = desc  # 描述
        self.hash = ''  # 用作数据库的 key
        self.videos = []  # 包含的 Video 对象列表
        self.num = 0  # 视频集数
        self.engine = ''  # 调用的引擎名

    def __repr__(self):
        return f'<VideoList {self.title}>'

    def add(self, video: Video):
        """添加一个 Video 对象"""
        self.videos.append(video)
        self.num += 1
        _all_hash = ''.join([v.hash for v in self.videos])
        self.hash = md5(_all_hash.encode('utf-8')).hexdigest()  # 通过所有 Video 对象的 hash 计算 VideoList 的 hash

    def json(self):
        """VideoList 对象转 json"""
        return {
            'title': self.title,
            'cover': self.cover,
            'cat': ' | '.join(self.cat),
            'desc': self.desc,
            'hash': self.hash,
            'num': self.num,
            'engine': self.engine,
            'videos': [v.json() for v in self.videos]
        }


class DefaultHandler(object):
    """默认的视频处理器"""

    def __init__(self, raw_url, type='mp4'):
        self.raw_url = raw_url  # 视频原始地址
        self.type = type  # 视频格式
        self._chunk_size = 1024 * 512  # 代理访问时每次读取的数据流大小 bytes
        self.proxy_headers = {}  # 代理访问使用的 header


    def get_real_url(self):
        """获取视频真实链接"""
        return self.raw_url

    def set_proxy_headers(self):
        """设置代理访问使用的请求头"""
        self.proxy_headers = {
            'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        }

    def _get_stream_from_server(self, real_url, byte_start=0) -> (dict, iter):
        """从服务器读取视频,并指定数据流起始位置"""
        self.set_proxy_headers()  # 请求数据前设置 headers
        self.proxy_headers['Range'] = f'bytes={byte_start}-'
        req = requests.get(real_url, stream=True, headers=self.proxy_headers, verify=False)
        return req.headers, req.iter_content(self._chunk_size)  # 返回服务器响应头, byte 数据流迭代器

    def get_stream(self):
        """按客户端请求头中要求的 Range 获取视频流"""
        real_url = self.get_real_url()
        byte_start = 0
        range_header = request.headers.get('Range', None)
        if range_header:
            result = re.search(r'(\d+)-\d*', range_header)
            if result:
                byte_start = int(result.group(1))  # 客户端要求的视频流起始位置
        return self._get_stream_from_server(real_url, byte_start)

    def make_response(self):
        """读取远程的视频流，并伪装成本地的响应返回"""
        header, data_iter = self.get_stream()
        if self.type == "hls":
            resp = Response(data_iter, status=200)
        elif self.type == "mp4":
            resp = Response(data_iter, status=206)  # 状态码需设置为 206,否则无法拖动进度条
            resp.content_range = header.get('Content-Range', None)
        else:
            resp = Response(data_iter, status=200)
            resp.content_type = header.get('Content-Type', None)
        # 设置其它响应头的信息
        resp.content_length = header.get('Content-Length', None)
        return resp
