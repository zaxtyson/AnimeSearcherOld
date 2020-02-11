from app.models import Video, VideoList, BaseEngine, DefaultHandler
from app import logger
import re
from concurrent.futures import ThreadPoolExecutor, as_completed


class Engine(BaseEngine):
    """这个引擎资源质量不错，就是搜索慢了点(无效资源实在是太多)"""
    @staticmethod
    def search(name):
        result = []
        page = 1
        while page < 3:  # 资源太多就返回前 3 页
            has_next, ret = Engine.search_one_page(name, page)
            result += ret
            page += 1
            if not has_next:
                break
        return result

    @staticmethod
    def search_one_page(name, page):
        result = []
        api = 'https://www.imomoe.in/search.asp'
        params = {'searchword': name.encode('gb2312'), 'page': page}
        ret = Engine.post(api, params, encoding='gb2312')  # 关键字和结果都必须是 gb2312 编码

        if not ret:
            logger.error(f"引擎 {__name__} 搜索失败: {name} {ret.status_code} {ret.text}")
            return False, result
        if '没有找到任何记录' in ret.text:
            logger.error(f"引擎 {__name__} 搜索失败: {name} 服务器未返回结果")
            return False, result

        page_info = Engine.xpath(ret.text, "//div[@class='pages']/span/text()")[0]  # 共n条数据 页次:1/2页
        now_page, total_page = re.search(r".+(\d+)/(\d+)页", page_info).groups()  # 1, 2
        has_next = (int(now_page) < int(total_page))  # 是否存在下一页
        logger.info(f"引擎 {__name__} 正在搜索: {name} ({now_page}/{total_page})")
        item_list = Engine.xpath(ret.text, "//div[@class='fire l']//div[@class='pics']//li")  # 每一个 item 都是一部动漫
        executor = ThreadPoolExecutor(max_workers=10)  # 服务器响应太慢，多开几个线程
        all_task = [executor.submit(Engine.get_video_list, item) for item in item_list]
        for task in as_completed(all_task):
            ret = task.result()
            if ret is not None:
                result.append(ret)
        return has_next, result

    @staticmethod
    def get_video_list(item):
        video_list = VideoList()
        video_list.engine = __name__
        video_list.title = item.xpath("h2/a/text()")[0]  # 标题
        video_list.cover = item.xpath("a/img/@src")[0]  # 封面链接
        cat_str = item.xpath("span/text()")[1]  # '12全集+OVA 类型：搞笑 校园'
        video_list.cat = cat_str.split('：')[-1].split()  # ['搞笑', '校园']
        video_list.desc = item.xpath("p/text()")[0]  # 简介
        part_url = item.xpath("a/@href")[0]  # /view/569.html
        logger.info(f"引擎 {__name__} 正在处理: {video_list.title}")
        ret = Engine._get_videos(part_url)  # 视频列表
        if not ret:
            return None
        for video in ret:
            video_list.add_video(video)
        return video_list

    @staticmethod
    def _get_videos(part_url):
        """通过部分页面参数获取视频"""
        result = []
        video_id = part_url.split('/')[-1].split('.')[0]  # '569'
        first_video_url = f"http://www.imomoe.in/player/{video_id}-0-0.html"  # 线路1-第一集的 URL
        ret = Engine.get(first_video_url, encoding='gb2312')

        if not ret:
            logger.error(f"引擎 {__name__} 解析失败: {first_video_url}")
            return result

        js_path = Engine.xpath(ret.text, "//div[@class='player']/script/@src")[0]  # /playdata/57/569.js?81281.56
        js_url = "http://www.imomoe.in" + js_path  # 视频直链在 js 文件中
        ret = Engine.get(js_url, encoding="gb2312")

        if not ret:
            logger.error(f"引擎 {__name__} 加载 js 失败: {js_url}")
            return result

        source_list = re.search(r".+?(\[.+\]).+", ret.text).group(1)  # 一个二维列表，[ ['名称', [地址列表]], ...]
        source_list = [i[1] for i in eval(source_list)]  # [['第x集$url$flv', '第x集$url$flv', ...], [...], ...]
        # 一部动漫通常有多个来源，但是一些源可能是无效的(甚至全部无效)，我们获取第一个有效的源即可
        ret = {}
        for source in source_list:
            for item in source:
                name, url, _type = item.split('$')[:3]
                if _type in ['flv', 'mp4', 'm3u8', 'zw'] \
                        and 'jiningwanjun' not in url:  # 此时这些资源才是有效的
                    ret.setdefault(name, url)
                    if 'gss3.baidu.com' in url:
                        ret[name] = url  # 优质资源,优先使用

        ret = sorted(ret.items())  # [('name', 'url'), ...]
        result = [Video(n, u, VideoHandler) for n, u in ret]
        # for v in result:
        #     print(v.name, v.raw_url)
        return result


class VideoHandler(DefaultHandler):
    def _get_real_url(self):
        ret = Engine.get(self.raw_url)
        if not ret or ret.status_code != 200:
            logger.error(f"{__name__} 处理失败: {self.raw_url}")
            return self.raw_url
        ret = re.search(r"url:\s*'(http.+?)',", ret.text)
        if not ret:
            logger.error(f"{__name__} 处理失败: {self.raw_url}")
        return ret.group(1)  # 真正的直链(m3u8)

    def get_real_url(self):
        # https://ck-qq.com/v/ZyB3mLew 这类视频需要进一步提取链接
        if '-qq.com' in self.raw_url:
            return self._get_real_url()
        else:
            return self.raw_url
