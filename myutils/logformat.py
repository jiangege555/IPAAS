import logging, time, threading, queue
from logging.handlers import QueueHandler, QueueListener

# 创建一个队列
# log_queue = queue.Queue(-1)  # -1 表示队列大小无限
# # 单例模式
# class MyLogger:
#     logger = None
#     _is_init = False
#     _instance = None
#
#     def __new__(cls, *args, **kwargs):
#         if cls._instance is None:
#             # cls._instance = super(SingletonClass, cls).__new__(cls)  # python2.x中，super()函数的使用语法格式
#             cls._instance = super().__new__(cls)  # python3.x中，super()函数的使用语法格式
#         return cls._instance
#
#     def __init__(self):
#         if self._is_init is False:
#             if self.logger is None:
#                 fh = logging.FileHandler(f'log/log_{time.strftime("%Y_%m_%d")}.log', mode='a', encoding='utf8')
#                 sh = logging.StreamHandler()
#                 fm = logging.Formatter('[%(asctime)s] %(filename)s %(levelname)s: line[%(lineno)d] %(message)s',
#                                        '%Y/%m/%d/%X')
#                 fh.setFormatter(fm)
#                 sh.setFormatter(fm)
#                 self.logger = logging.getLogger()
#                 self.logger.setLevel(logging.INFO)
#                 self.logger.addHandler(fh)
#                 self.logger.addHandler(sh)
#             self._is_init = True


# # 非单例模式，每个包单独创建logger对象，用于多线程写入日志--实测不成功，报告中日志依旧有混合显示
class MyLogger:
    logger = None

    def __init__(self, title):
        fh = logging.FileHandler(f'log/log_{time.strftime("%Y_%m_%d")}_{title}.log', mode='a', encoding='utf8')
        sh = logging.StreamHandler()
        fm = logging.Formatter('[%(asctime)s] %(filename)s %(levelname)s: line[%(lineno)d] %(message)s',
                               '%Y/%m/%d/%X')
        fh.setFormatter(fm)
        sh.setFormatter(fm)
        sh.encoding = 'utf-8'
        self.logger = logging.getLogger(title)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(fh)
        self.logger.addHandler(sh)
        # queue_handler = QueueHandler(log_queue)
        # self.logger.addHandler(queue_handler)
        # listener = QueueListener(log_queue, queue_handler)
        # listener.start()


# # 创建logger
# lock = threading.Lock()
# with lock:
#     logger = MyLogger().logger
