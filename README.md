<p align="center"><img src="https://ae01.alicdn.com/kf/U150c6f229b47468781c941fdd80545eak.png" width="200"></p>
<h3 align="center">- AnimeSearcher -</h3>
 
# 简介  
- AnimeSearcher 是一款本地动漫搜索引擎，基于 Flask + DPlayer  

- 它支持添加规则引擎以拓展搜索结果(目前有 3 个引擎), 编写规范请查看 [Wiki](https://github.com/zaxtyson/AnimeSearcher/wiki)  

- 它允许您为每一个视频绑定 Handler，以解析更为复杂的请求

- 它作为中间代理访问远程视频资源，并将其映射到本地，对于前端播放器而言，就像在访问本地视频资源

- 它允许您在代理请求发出前修改 Headers，以绕过服务器的防盗链限制和解决前端播放器直接访问视频时出现的跨域问题

- 它允许您在代理响应返回前修改视频数据流，修改响应头，以适应前端播放器的需求

# 演示

![index.png](https://ae01.alicdn.com/kf/U34b0554a6fe34130b3dd63fa1219d8ccF.png)

![search.png](https://ae01.alicdn.com/kf/Uae60f959a38b4ab48bfefcbfccf79da9D.png)

![player.png](https://ae01.alicdn.com/kf/U7f5d5f92ac3b42e1981889c6bf47d4cfm.png)

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

# 引擎加载

- 将引擎放在 `app/engines` 目录下，程序会自动加载

- 如果想禁用某个引擎，在其文件名前加上双下划线 `__` 即可

- 引擎 `sakura` 的资源质量不错，但是搜索速度很慢(无效资源太多)。默认 `禁用` 状态，如果需要请取消其下划线

# 其它

- 有些视频 DPlayer 无法播放，提醒 `播放失败`, 但是您可以离线后使用本地播放器观看。或者可以用爱奇艺万能播放器选择从 URL 播放视频。

- 播放失败时将弹窗告知您该资源映射在本地的 URL