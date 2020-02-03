from app.models import VideoList, Video


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
        """获取一个视频列表"""
        return self._video_list_db.get(list_hash, None)

    def get_video(self, video_hash) -> Video:
        """获取一个视频"""
        return self._video_db.get(video_hash, None)

    def clear(self):
        """清空临时数据库"""
        self._video_db = {}
        self._video_list_db = {}
