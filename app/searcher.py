from concurrent.futures import ThreadPoolExecutor, as_completed
from os import listdir

# 自动导入和加载引擎模块
engine_modules = [e.split('.')[0] for e in listdir('app/engines') if not e.startswith('__')]
exec('\n'.join([f"from app.engines import {e}" for e in engine_modules]))
Engines = [eval(f"{e}.Engine().search") for e in engine_modules]


class Searcher(object):
    @staticmethod
    def search(keyword) -> list:
        """调用所有 engine 搜索视频"""
        result = []
        executor = ThreadPoolExecutor(max_workers=5)
        all_task = [executor.submit(engine, keyword) for engine in Engines]
        for task in as_completed(all_task):
            result += task.result()
        return result
