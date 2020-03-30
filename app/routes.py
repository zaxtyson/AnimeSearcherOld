from app import app, cachedb, logger
from flask import render_template, request, make_response
from app.searcher import Searcher
from app.danmaku import BiliBiliDanmaku


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/search/<name>')
def search(name):
    logger.info(f"搜索 : {name}")
    result = Searcher.search(name)
    result_json = []
    for video_list in result:
        cachedb.add_video_list(video_list)  # 保存结果到临时数据库
        result_json.append(video_list.json())
    logger.info(f"搜索结果: {len(result_json)} 条")
    return render_template("_result.html", result=result_json)


@app.route('/playlist/<list_hash>')
def get_playlist(list_hash):
    video_list = cachedb.get_video_list(list_hash)
    if not video_list:
        return '番剧列表不存在'
    logger.info(f"获取番剧列表: {video_list.title} (共{video_list.num}集) {video_list.hash}")
    resp = make_response(render_template('playlist.html', video_list=video_list))
    resp.set_cookie('video_list', list_hash)
    return resp


@app.route('/danmaku_list/<list_hash>')
def get_danmaku_list(list_hash):
    """获取可选的弹幕列表"""
    vl = cachedb.get_video_list(list_hash)
    if not vl:
        return '番剧列表不存在'
    if not vl.danmaku_list:
        for dmk in BiliBiliDanmaku.search_danmaku(vl.title):
            # 弹幕库的视频集数与番剧集数相差 4 以上丢弃
            if abs(vl.num - dmk.num) < 4:
                logger.info(f"匹配弹幕库: {dmk.title} DMK:{dmk.num}, VL:{vl.num}")
                vl.add_danmaku(dmk)
            else:
                logger.info(f"丢弃弹幕库: {dmk.title} DMK:{dmk.num}, VL:{vl.num}")
        cachedb.update_video_list(vl)
    max_num = max([ep.num for ep in vl.danmaku_list]) if vl.danmaku_list else 0  # 最多的集数
    return render_template('_danmaku_list.html', dmk_list=vl.danmaku_list, max_num=max_num)


@app.route('/video/<video_hash>/type')
def get_video_type(video_hash):
    """获取视频格式"""
    video = cachedb.get_video(video_hash)
    handler = video.handler(video)
    if not video.has_handled:  # 如果 Handler 还没有处理过
        video.real_url = handler.get_real_url()  # 获取真实链接
        handler.real_url = video.real_url  # 告知 handler 视频的真实链接,减少下面再重复获取一次
        video.type = handler.detect_video_type()  # 推断视频格式
        cachedb.update_video(video)  # 更新视频信息
        video.has_handled = True
        logger.info(f"视频信息处理完成: {video.name} [{video.type}] -> {video.real_url}")
    return video.type


@app.route('/video/<video_hash>/data')
def get_video_data(video_hash):
    """获取视频数据"""
    video = cachedb.get_video(video_hash)
    handler = video.handler(video)
    return handler.make_response()


@app.route('/video/danmaku/v3/', methods=['GET', 'POST'])
def get_video_danmaku():
    """尝试从哔哩哔哩获取视频弹幕"""
    cid = request.args.get('id')
    return BiliBiliDanmaku.get_danmaku(int(cid))
