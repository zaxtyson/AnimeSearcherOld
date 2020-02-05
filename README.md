<p align="center"><img src="http://img03.sogoucdn.com/app/a/100520146/798A9149A43079106F96F2AE7F314779" width="200"></p>
<h3 align="center">- AnimeSearcher -</h3>
 
# 简介  
- AnimeSearcher 是一款本地动漫搜索引擎，基于 Flask + DPlayer  

- 它支持添加规则引擎以拓展搜索结果(目前有 3 个引擎), 编写规范请查看 [Wiki](https://github.com/zaxtyson/AnimeSearcher/wiki)  

- 它允许您为每一个视频绑定 Handler，以解析更为复杂的请求

- 它作为中间代理访问远程视频资源，并将其映射到本地，对于前端播放器而言，就像在访问本地视频资源

- 它允许您在代理请求发出前修改 Headers，以绕过服务器的防盗链限制和解决前端播放器直接访问视频时出现的跨域问题

- 它允许您在代理响应返回前修改视频数据流，设置响应头，以满足前端播放器的需求

# TODO
- [ ] Bilibili 分段 FLV 视频合并播放 (目前只能播放其中一段)
- [ ] 爱奇艺视频解析 (参数的算法貌似挺复杂) 

# 演示

![index.png](http://img03.sogoucdn.com/app/a/100520146/332EEC17EBAAE98F698BA8822A36CC39)

![search.png](http://img04.sogoucdn.com/app/a/100520146/38D1C370026C5B3E0C44C9ACCAFE192D)

![player.png](http://img01.sogoucdn.com/app/a/100520146/22BD2AEA7D16A0045465AB2C0AD38D82)

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

# 引擎加载

- 将引擎放在 `app/engines` 目录下，程序会自动加载
- 如果想禁用某个引擎，在其文件名前加上双下划线 `__` 即可
- 引擎 `sakura` 的资源质量不错，但是搜索速度很慢(无效资源太多)。默认 `禁用` 状态，如果需要请取消其下划线