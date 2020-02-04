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
    cachedb.clear()  # 每次搜索前清空临时数据库
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


@app.route('/video/<video_hash>')
def get_video(video_hash):
    video = cachedb.get_video(video_hash)
    handler = video.handler(video.raw_url, video.type)
    logger.info(f"请求 : {video.name} {video.type}")
    return handler.make_response()
