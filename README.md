<h3 align="center">- AnimeSearcher -</h3>

# 简介  
- AnimeSearcher 是一款本地动漫搜索引擎，基于 Flask + DPlayer  

- 它支持添加规则引擎以拓展搜索结果(目前有 2 个引擎), 编写规范请查看 [Wiki](https://github.com/zaxtyson/AnimeSearcher/wiki)  

- 它允许您为每一个视频绑定 Handler，以解析更为复杂的请求

- 它作为中间代理访问远程视频资源，并将其映射到本地，对于前端播放器而言，就像在访问本地视频资源

- 它允许您在代理请求发出前修改 Headers，以绕过服务器的防盗链限制和解决前端播放器直接访问视频时出现的跨域问题

- 它允许您在代理响应返回前修改视频数据流，设置响应头，以满足前端播放器的需求

# TODO
- [ ] Bilibili 分段 FLV 视频合并播放 (目前只能播放其中一段)
- [ ] 爱奇艺视频解析 (参数的算法貌似挺复杂) 

# 演示

![index.png](https://www.6000tu.com/images/2020/02/03/index.png)

![search.png](https://www.6000tu.com/images/2020/02/03/search.png)

![player.png](https://www.6000tu.com/images/2020/02/03/player.png)

# 使用

- Windows 用户可下载打包完成的: [点我下载](https://www.lanzous.com/b0f19w6aj)

- Linux 用户需安装依赖后执行 `run.py`
```
pip install -r requirement.txt
```

- 打开浏览器访问
```
127.0.0.1:5000
```