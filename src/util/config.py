"""
服务端配置项
"""


import configparser
from pathlib import Path


filename = "config.ini"
# 默认配置
x = 300
y = 300
height = 200
width = 600
line_num = 4
page = 0
txt = "kt-fx.txt"
font_size = 13


def save_all():
    config = configparser.ConfigParser()
    config_file = get_config_file(filename)
    config.read(config_file)
    config['main']['x'] = f"{x}"
    config['main']['y'] = f"{y}"
    config['main']['height'] = f"{height}"
    config['main']['width'] = f"{width}"
    config['main']['page'] = f"{page}"
    config['main']['font_size'] = f"{font_size}"
    config['main']['txt'] = f"{txt}"
    config['main']['line_num'] = f"{txt}"

    # 写入到配置文件
    with config_file.open("w") as file:
        config.write(file)


def config_save(conf, value):
    config = configparser.ConfigParser()
    config_file = get_config_file(filename)
    config.read(config_file)
    config['main'][conf] = f"{value}"

    # 写入到配置文件
    with config_file.open("w") as file:
        config.write(file)


# 读取配置项
def get_config(config, section, option, default_value, is_int=False):
    try:
        value = config[section][option]
        if value is None and default_value is None and is_int:
            return 0
        if value is None and default_value is None and not is_int:
            return None
        if value is None and default_value is not None:
            value = default_value
        if is_int:
            return int(value)
        return value
    except KeyError or TypeError or ValueError:
        try:
            if is_int:
                return int(default_value)
            return default_value
        except TypeError or ValueError:
            return 0


def get_config_file(config_filename):
    config_file = Path(config_filename)
    if not config_file.exists():
        config_file = Path(f"../{config_filename}")
    if not config_file.exists():
        config_file = Path(f"../../{config_filename}")
    if not config_file.exists():
        raise FileNotFoundError(f"配置文件不存在！")
    return config_file


# 读取配置
def config_init(config_filename="config.ini"):
    # 加载配置文件
    config = configparser.ConfigParser()
    config_file = get_config_file(config_filename)
    global filename
    filename = config_filename
    config.read(config_file)

    global x, y, height, width, page, font_size, txt, line_num

    x = get_config(config, 'main', 'x', default_value=x, is_int=True)
    y = get_config(config, 'main', 'y', default_value=y, is_int=True)
    height = get_config(config, 'main', 'height', default_value=height, is_int=True)
    width = get_config(config, 'main', 'width', default_value=width, is_int=True)
    line_num = get_config(config, 'main', 'line_num', default_value=line_num, is_int=True)
    page = get_config(config, 'main', 'page', default_value=page, is_int=True)
    font_size = get_config(config, 'main', 'font_size', default_value=font_size, is_int=True)
    txt = get_config(config, 'main', 'txt', default_value=txt)


if __name__ == '__main__':
    config_init()