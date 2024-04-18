"""
服务端配置项
"""


import configparser
from pathlib import Path
from loguru import logger as log


__filename__ = "config.ini"
# 默认配置
x = 300
y = 300
height = 200
width = 600
line_num = 4
page = 0
txt = "kt-fx.txt"
font_size = 13
key_pageUp = "W,A,Left"
key_pageDown = "S,D,Right"
key_pageHide = "Q,Down"
key_pageShow = "E,Up"
key_pageExit = "Escape"


def save_all():
    config = configparser.ConfigParser()
    config_file = get_config_file(__filename__)
    config.read(config_file)

    # 获取所有全局变量
    global_vars = {k: v for k, v in globals().items() if not k.startswith("__") and not callable(v)}
    for var_name, var_value in global_vars.items():
        config['main'][var_name] = f"{var_value}"

    with config_file.open("w") as file:
        config.write(file)


def config_save(conf, value):
    # 获取所有全局变量
    global_vars = {k: v for k, v in globals().items() if not k.startswith("__") and not callable(v)}
    if conf not in global_vars:
        log.error(f"保存配置{conf}失败，没有找到对应的配置项！")
        return

    config = configparser.ConfigParser()
    config_file = get_config_file(__filename__)
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
    global __filename__
    __filename__ = config_filename
    config.read(config_file)

    # 获取所有全局变量
    global_vars = {k: v for k, v in globals().items() if not k.startswith("__") and not callable(v)}
    for var_name, var_value in global_vars.items():
        globals()[var_name] = get_config(config, 'main', var_name, default_value=var_value, is_int=isinstance(var_value, int))

if __name__ == '__main__':
    config_init()