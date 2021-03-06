<p align="center"><img src="https://ae01.alicdn.com/kf/U150c6f229b47468781c941fdd80545eak.png" width="200"></p>
<h3 align="center">- AnimeSearcher -</h3>

# 本项目不再继续维护, 转到 [AnimeSearcher](https://github.com/zaxtyson/AnimeSearcher)
 
# 简介  
- 这是一款动漫搜索工具，基于 Flask + DPlayer  

- 真 • 无广告，无需下载，在线看番

- 自动匹配哔哩哔哩的弹幕~

- 可扩展，支持添加资源引擎

- 给个 star 嘛 (/ω＼*)

# 演示

![index.png](https://ae01.alicdn.com/kf/U34b0554a6fe34130b3dd63fa1219d8ccF.png)

![search.png](https://ae01.alicdn.com/kf/Uae60f959a38b4ab48bfefcbfccf79da9D.png)

![player.png](https://ae01.alicdn.com/kf/U7f5d5f92ac3b42e1981889c6bf47d4cfm.png)

![danmaku.png](https://s2.ax1x.com/2020/02/11/1o2PMQ.png)

# 下载和使用

- Windows 用户可下载打包完成的文件: [点我下载](https://www.lanzous.com/b0f19w6aj)

- Linux 用户需安装依赖后执行 `run.py`
```
pip install -r requirement.txt
```

- 打开浏览器访问
```
127.0.0.1:5000
```

# 资源引擎

- 将引擎放在 `app/engines` 目录下，程序会自动加载

- 如果想禁用某个引擎，在其文件名前加上双下划线 `__` 即可

- 引擎 `sakura` (樱花动漫)的资源质量不错，但是搜索速度很慢(无效资源太多)。默认 `禁用` 状态，如果需要请取消其下划线

- 如果您想编写自己的资源引擎，请查看 [Wiki](https://github.com/zaxtyson/AnimeSearcher/wiki)  


# 其它

- 有些视频 DPlayer 无法播放，提醒 `播放失败`, 但是您可以离线后使用本地播放器观看。或者可以用爱奇艺万能播放器选择从 URL 播放视频。

- 播放失败时将弹窗告知您该资源映射在本地的 URL
