from concurrent.futures import ThreadPoolExecutor, as_completed
from app.engines import jiaonang, zzfun


class Searcher(object):
    @staticmethod
    def search(keyword) -> list:
        """调用所有 engine 搜索视频"""
        result = []
        executor = ThreadPoolExecutor(max_workers=5)
        all_task = [
            executor.submit(jiaonang.Engine().search, keyword),
            executor.submit(zzfun.Engine().search, keyword)
        ]
        for task in as_completed(all_task):
            result += task.result()
        return result
