"""
loguru 配置项
"""


from loguru import logger
import sys


def custom_console_format(record):
    # 处理 line，固定占4格，右对齐
    record["extra"]["line"] = f"{record['line']:>4}"

    # 拼接 name.function
    name = record["name"]
    short_name = name.split('.')[-1] if '.' in name else name
    function = record["function"]
    name_function = f"{short_name}.{function}"
    name_function_length = len(name_function) + (4 - len(name_function) % 4) % 4
    name_function_length = 24 if name_function_length < 24 else name_function_length

    # 获取线程名
    thread_name = record["thread"].name
    thread_name = thread_name.split(' (')[0] if ' (' in thread_name else thread_name
    thread_name = f"{thread_name.split('-')[0]}-{thread_name.split('-')[1].zfill(3)}" if '-' in thread_name else thread_name

    # name_length = len(short_name) + (4 - len(short_name) % 4) % 4
    # function_length = len(function) + (4 - len(function) % 4) % 4

    # if len(short_name) > 4 and len(function) > 12:
    #     name_length = 8 if name_length < 8 else name_length
    #     function_length = 16 if function_length < 16 else function_length
    # elif len(short_name) <= 4 and len(function) > 16:
    #     name_length = 4 if name_length < 4 else name_length
    #     function_length = 20 if function_length < 20 else function_length
    # elif len(short_name) > 8 and len(function) <= 12:
    #     name_length = 12 if name_length < 12 else name_length
    #     function_length = 12 if function_length < 12 else function_length

    # record["extra"]["name"] = f"{short_name: >{name_length}}"
    # record["extra"]["function"] = f"{function: >{function_length}}"

    record["extra"]["thread_name"] = thread_name
    record["extra"]["name_function"] = f"{name_function: >{name_function_length}}"

    # 转义message中的大括号
    # 将单个大括号替换为双大括号，以避免被视为格式化标记
    record["message"] = record["message"].replace("{", "{{").replace("}", "}}")

    # 定义自定义的日志格式
    custom_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<magenta>{extra[thread_name]}</magenta>: <cyan>{extra[name_function]}</cyan>:<cyan>{extra[line]}</cyan> - <level>{message}</level>\n"
    )
    return custom_format.format(**record)


def setup_logger(log_title):

    file_format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"

    logger.remove()

    logger.add(
        "/mnt/logs/ChatRoom/" + log_title + "-{time:YYYY-MM-DD}.log",  # 日志文件名格式
        level="INFO",
        rotation="1 day",  # 每天轮转
        retention="100 days",  # 保留100天的日志文件
        compression="zip",
        format=file_format  # 自定义日志格式
    )

    logger.add(
        sys.stdout,
        level="DEBUG",
        format=custom_console_format
    )

