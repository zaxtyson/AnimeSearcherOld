from app.models import VideoList, Video, Danmaku


class CacheDB(object):
    """临时对象数据库"""

    def __init__(self):
        self._video_list_db = {}
        self._video_db = {}

    def add_video_list(self, video_list: VideoList):
        """存入一个视频列表"""
        self._video_list_db.setdefault(video_list.hash, video_list)
        for video in video_list.videos:
            self._video_db.setdefault(video.hash, video)

    def get_video_list(self, list_hash) -> VideoList:
        """获取一部番剧的信息"""
        return self._video_list_db.get(list_hash, None)

    def get_video(self, video_hash) -> Video:
        """获取一个视频"""
        return self._video_db.get(video_hash, None)

    def update_video(self, video: Video):
        """更新处理后的视频"""
        self._video_db[video.hash] = video

    def update_video_list(self, vl: VideoList):
        """更新番剧信息"""
        self._video_list_db[vl.hash] = vl

    def clear(self):
        """清空临时数据库"""
        self._video_db = {}
        self._video_list_db = {}
