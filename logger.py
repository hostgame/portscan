import logging
import logging.handlers

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

syslog_handler = logging.handlers.SysLogHandler(address='/dev/log')
syslog_handler.setLevel(logging.DEBUG)

http_logger = logging.getLogger('aiohttp.access')
http_logger.addHandler(stream_handler)
http_logger.addHandler(syslog_handler)
http_logger.setLevel(logging.DEBUG)

app_logger = logging.getLogger('portscan')
app_logger.setLevel(logging.DEBUG)

app_logger.addHandler(stream_handler)
app_logger.addHandler(syslog_handler)
