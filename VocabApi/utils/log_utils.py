from loguru import logger

from configs import log


logger.add(
    log.LOG_FILE_PATH,
    rotation="1 days",
    format=log.LOG_MSG_FORMAT,
    level=log.LOG_LEVEL,
    encoding="utf8")


# Errorログ出力用
# def put_error(file: str, method: str, line: str, code: str, message: str, other: str):
#     output = {}
#     output["CLASS"]   = file
#     output["METHOD"]  = method
#     output["LINE"]    = line
#     output["CODE"]    = code
#     output["MESSAGE"] = message
#     output["OTHER"]   = other

#     logger.error(output)

def put_error(message: str):
    logger.error(message)