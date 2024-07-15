"""
翻页
"""


from src.util import config
from loguru import logger as log
import chardet


page_list = list()
text_cache = ""
text_source = None
begin = True


# 判断是否有后续文本，缓存存在或者可以读入新缓存则返回True。
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
            with open(f"{config.txt}", "rt", encoding=detect_encoding(f"{config.txt}")) as file:
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


# 检查文本编码，自动判断使用对应编码(测试中功能)
code = None
def detect_encoding(file_path):
    if code is not None:
        return code
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        return encoding


# 预加载页面，使第一次翻页无需等待时间。
def init_page():
    next_page()
    global begin
    begin = True


# 查找文本，返回查找到的页面文本内容
def search_word(word):

    # 空内容则不翻页
    if word is None or len(word) == 0:
        return next_page(step=0)

    # 从第0页开始查找
    page_search = 0
    while read_file():
        temp_text = ""
        while page_search + 1 >= len(page_list) and read_file():
            page_list.append(split_page())
        if page_search < len(page_list):
            temp_text += page_list[page_search]
        if page_search + 1 < len(page_list):
            temp_text += page_list[page_search + 1]
        if word in temp_text:
            if word not in page_list[page_search]:
                page_search += 1
            config.save_conf("page", page_search)
            config.page = page_search
            return page_list[page_search]
        page_search += 1
    return next_page(step=0)


# 向后翻页，返回翻页后当前页文本内容
def next_page(step=1):
    global begin
    page_num = config.page
    # 判断要读取的页码是否已经生成，未生成则继续生成，直到页码存在或者文本末尾。
    while page_num + step >= len(page_list) and read_file():
        page_list.append(split_page())
    if page_num + step < len(page_list) and not begin:
        page_num += step
    else:
        begin = False
    config.save_conf("page", page_num)
    config.page = page_num
    if page_num < len(page_list):
        return page_list[page_num]
    else:
        return "page_num error!"


# 向前翻页，返回翻页后当前页文本内容
def prev_page():
    global begin
    page_num = config.page
    # 首次启动时不翻页
    if page_num > 0 and not begin:
        page_num -= 1
    else:
        begin = False
    # 判断要读取的页码是否已经生成，未生成则继续生成，直到页码存在或者文本末尾。
    while page_num >= len(page_list) and read_file():
        page_list.append(split_page())
    # 更新当前页码配置
    config.save_conf("page", page_num)
    config.page = page_num
    if page_num < len(page_list):
        return page_list[page_num]
    else:
        return "page_num error!"


# 按显示行数分割缓存文本，返回最新一页内容。
def split_page():
    global text_cache
    part = ""
    line_num = 0
    line = ""
    char_num = 0
    max_char = int(config.width / config.fontSize * 1.5)
    while line_num < config.lineNum and read_file():
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
        if '\u4E00' <= char <= '\u9FFF' or '\u3000' <= char <= '\u303F' or '\uFF01' <= char <= '\uFF5E' or '\uFFE0' <= char <= '\u2000' or '' <= char <= '\u206F':
            # 汉字范围是0x4E00到0x9FFF，全角符号范围是0xFF00到0xFFEF
            length += 2
        else:
            # 其他字符，如英文字母、数字和空格，长度加1
            length += 1
    return length

