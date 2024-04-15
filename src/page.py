"""
翻页
"""


from src.util import config
from loguru import logger as log


page_list = list()
text_cache = ""
text_source = None


def read_file():
    if len(text_cache) > 0:
        return True
    return read_next()


def read_next(chunk_size=1000):
    global text_cache, text_source
    if not text_source:
        text_source = list()
        try:
            # 使用with语句打开文件，确保文件最终会被关闭
            with open(f"{config.txt}", "rt", encoding="utf-8") as file:
                # 读取指定大小的字符
                cache = file.read(chunk_size)
                # 如果读取到的字符长度小于请求的长度，说明已经到了文件末尾
                while len(cache) > 0:
                    text_source.append(cache)
                    cache = file.read(chunk_size)
        except FileNotFoundError:
            log.info("文件未找到")
            return False
        except IOError:
            log.info("文件读取出错")
            return False
    if len(text_source) > 0:
        text_cache = text_source.pop(0)
        return True
    else:
        return False


def next_page():
    page_num = config.page
    while page_num + 1 >= len(page_list) and read_file():
        page_list.append(split_page())
    if page_num + 1 < len(page_list):
        page_num += 1
    config.config_save("page", page_num)
    config.page = page_num
    if page_num < len(page_list):
        return page_list[page_num]
    else:
        return "error!"


def prev_page():
    page_num = config.page
    if page_num > 0:
        page_num -= 1
    config.config_save("page", page_num)
    config.page = page_num
    if page_num < len(page_list):
        return page_list[page_num]
    else:
        return "error!"


def split_page():
    global text_cache
    part = ""
    line_num = 0
    line = ""
    char_num = 0
    max_char = int(config.width / config.font_size * 1.45)
    while line_num < config.line_num and read_file():
        while char_num < max_char and read_file():
            char = text_cache[0]
            if char == '\u0020': char = '\u3000'
            text_cache = text_cache[1:]
            if char == '\n':
                char_num += max_char
            else:
                char_num += weighted_length(char)
                line += char
        part += line + "\n"
        line_num += 1
        line = ""
        char_num = 0

    return part


def weighted_length(s):
    length = 0
    for char in s:
        if '\u4e00' <= char <= '\u9fff' or '\u3000' <= char <= '\u303F' or '\uFF01' <= char <= '\uFF5E' or '\uFFE0' <= char <= '\uFFE6':
            # 汉字范围是0x4E00到0x9FFF，全角符号范围是0xFF00到0xFFEF
            length += 2
        else:
            # 其他字符，如英文字母、数字和空格，长度加1
            length += 1
    return length

