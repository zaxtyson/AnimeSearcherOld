from app import app, cachedb, logger
from flask import render_template
from app.searcher import Searcher


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/search/<name>')
def search(name):
    logger.info(f"搜索 : {name}")
    result = Searcher.search(name)
    # cachedb.clear()  # 每次搜索前清空临时数据库
    result_json = []
    for video_list in result:
        cachedb.add_video_list(video_list)  # 保存结果到临时数据库
        result_json.append(video_list.json())
    logger.info(f"搜索结果: {len(result_json)} 条")
    return render_template("result.html", result=result_json)


@app.route('/playlist/<list_hash>')
def get_playlist(list_hash):
    video_list = cachedb.get_video_list(list_hash)
    if not video_list:
        return '视频不存在'
    logger.info(f"获取视频列表: {video_list.title} ({video_list.num}集) {video_list.hash}")
    video_list_json = video_list.json()['videos']
    return render_template('playlist.html', video_list=video_list_json)


@app.route('/video/<video_hash>/type')
def get_video_type(video_hash):
    """获取视频格式"""
    video = cachedb.get_video(video_hash)
    handler = video.handler(video)
    if not video.has_handled:   # 如果 Handler 还没有处理过
        video.real_url = handler.get_real_url()     # 获取真实链接
        handler.real_url = video.real_url   # 告知 handler 视频的真实链接,减少下面再重复获取一次
        video.type = handler.detect_video_type()    # 推断视频格式
        cachedb.update_video(video)     # 更新视频信息
        video.has_handled = True
        logger.info(f"视频信息处理完成: {video.name} [{video.type}] -> {video.real_url}")
    return video.type


@app.route('/video/<video_hash>/data')
def get_video_data(video_hash):
    """获取视频数据"""
    video = cachedb.get_video(video_hash)
    handler = video.handler(video)
    return handler.make_response()
