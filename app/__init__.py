from flask import Flask
import logging
from app.config import Config
from app.cachedb import CacheDB
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

cachedb = CacheDB()  # 临时的对象数据库,保存搜索结果

app = Flask(__name__)
app.config.from_object(Config)
app.logger.handlers.clear()

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(
    logging.Formatter("%(asctime)s [%(filename)s:L%(lineno)d] %(threadName)s %(levelname)s - %(message)s")
)

app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)
disable_warnings(InsecureRequestWarning)  # 禁用日志输出SSL警告

logger = app.logger

from app import app, routes
