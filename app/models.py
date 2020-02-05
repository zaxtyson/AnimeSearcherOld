from hashlib import md5
import requests
import re
from flask import request, Response
from lxml import etree


class Video(object):
    """单个视频对象"""

    def __init__(self, name, raw_url, handler=None):
        self.name = name  # 视频名
        self.type = 'auto'  # 视频格式
        self.raw_url = raw_url  # 原始 URL
        self.real_url = None  # 真实 URL
        self.hash = md5(raw_url.encode('utf-8')).hexdigest()  # URL 的 hash,用作数据库的 key
        self.handler = DefaultHandler if not handler else handler  # 该视频对应的 Handler,进一步处理视频
        self.has_handled = False  # 记录处理状态,防止重复处理

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


class BaseEngine(object):
    """基础引擎，提供了一些工具"""
    _default_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4033.0 Safari/537.36 Edg/81.0.403.1"
    }

    @staticmethod
    def get(url, params=None, headers=None, encoding='utf-8', **kwargs):
        """封装 get 请求方法,禁用 SSL 验证"""
        if not headers:
            headers = BaseEngine._default_headers
        try:
            ret = requests.get(url, params, headers=headers, verify=False, timeout=10, **kwargs)
            ret.encoding = encoding
            return ret
        except requests.RequestException:
            return None

    @staticmethod
    def post(url, data=None, headers=None, encoding='utf-8', **kwargs):
        """"封装 post 方法"""
        if not headers:
            headers = BaseEngine._default_headers
        try:
            ret = requests.post(url, data, headers=headers, verify=False, timeout=10, **kwargs)
            ret.encoding = encoding
            return ret
        except requests.RequestException:
            return None

    @staticmethod
    def xpath(html, xpath):
        """支持 xpath 方便处理网页"""
        if not html:
            return None
        try:
            return etree.HTML(html).xpath(xpath)
        except etree.XPathError:
            return None


class DefaultHandler(object):
    """默认的视频处理器"""

    def __init__(self, Video_Obj):
        self.raw_url = Video_Obj.raw_url
        self.real_url = Video_Obj.real_url
        self.video_type = Video_Obj.type    # 视频格式
        self._chunk_size = 1024 * 512  # 代理访问时每次读取的数据流大小 bytes
        self.proxy_headers = {}  # 代理访问使用的 header

    def get_real_url(self):
        """获取视频真实链接"""
        return self.real_url or self.raw_url

    def set_proxy_headers(self):
        """设置代理访问使用的请求头"""
        self.proxy_headers = {
            'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        }

    def _get_stream_from_server(self, byte_start=0, byte_end=None) -> (dict, iter):
        """从服务器读取视频,并指定数据流起始位置"""
        self.set_proxy_headers()  # 请求数据前设置 headers
        if not byte_end:
            self.proxy_headers['Range'] = f'bytes={byte_start}-'
        else:
            self.proxy_headers['Range'] = f'bytes={byte_start}-{byte_end}'
        real_url = self.real_url if self.real_url else self.get_real_url()
        try:

            req = requests.get(real_url, stream=True, headers=self.proxy_headers, verify=False)
            return req.headers, req.iter_content(self._chunk_size)  # 返回服务器响应头, byte 数据流迭代器
        except requests.RequestException:
            return None, None

    def get_stream(self):
        """按客户端请求头中要求的 Range 获取视频流"""
        byte_start = 0
        range_header = request.headers.get('Range', None)
        if range_header:
            result = re.search(r'(\d+)-\d*', range_header)
            if result:
                byte_start = int(result.group(1))  # 客户端要求的视频流起始位置
        return self._get_stream_from_server(byte_start)

    def detect_video_type(self):
        """判断视频真正的格式"""
        type_hex = {
            'mp4': ['69736F6D', '70617663', '6D703432', '4D50454734', '4C617666'],
            'flv': ['464C56'],
            'hls': ['4558544D3355']
        }
        _, data_iter = self._get_stream_from_server(0, 512)     # 通过前 512 字节数据判断视频格式
        if not data_iter:
            return 'auto'

        mata = next(data_iter).hex().upper()
        for _type, hex_list in type_hex.items():
            for hex_sign in hex_list:
                if hex_sign in mata:
                    self.video_type = _type
                    return _type
        return 'auto'   # 未知的格式,让前端播放器自行判断

    def fix_m3u8(self, raw_data):
        """m3u8视频修复"""
        domain = '/'.join(self.real_url.split('/')[:-1])
        fixed_data = []
        for line in raw_data.splitlines():
            if line.startswith('#') or line.startswith('http'):
                fixed_data.append(line)
            elif line.endswith('.ts'):
                fixed_data.append(domain + '/' + line)
            else:
                fixed_data.append(line)
        fixed_data = '\n'.join(fixed_data)
        return fixed_data

    def make_response(self):
        """读取远程的视频流，并伪装成本地的响应返回"""
        header, data_iter = self.get_stream()
        if not data_iter:
            return Response('error', status=500)

        if self.video_type == "mp4":
            resp = Response(data_iter, status=206)  # 状态码需设置为 206,否则无法拖动进度条
            resp.content_range = header.get('Content-Range', None)
        elif self.video_type == "hls":
            raw_data = next(data_iter).decode('utf-8')      # next 读取一块数据,一般 m3u8 文件不会超过 512k
            fixed_data = self.fix_m3u8(raw_data)
            resp = Response(fixed_data, status=200)
        else:
            resp = Response(data_iter, status=200)
            resp.content_range = header.get('Content-Range', None)
            resp.content_type = header.get('Content-Type', None)
        # 设置其它响应头的信息
        # resp.content_length = header.get('Content-Length', 0)
        return resp
