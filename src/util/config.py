"""
配置项
"""


import configparser as __configparser
from pathlib import Path
from loguru import logger as __log


__filename = "config.ini"
conf_dict = dict()
# 默认配置
x = 300
y = 300
height = 200
width = 600
lineNum = 4
page = 0
txt = "kt-fx.txt"
fontSize = 13
key_prevPage = "W,A,Left"
key_nextPage = "S,D,Right"
key_hide = "Q,Down"
key_show = "E,Up"
key_exit = "Escape"
key_search = "F"


def save_all():
    config = __configparser.ConfigParser()
    config_file = get_config_file(__filename)
    config.read(config_file)

    # 获取所有全局变量
    global_vars = {k: v for k, v in globals().items() if not k.startswith("__") and not callable(v) and not isinstance(v, dict)}
    for var_name, var_value in global_vars.items():
        split_save(config, var_name, var_value)

    with config_file.open("w") as file:
        config.write(file)

    config_init()


def save_conf(var_name, var_value):
    # 获取所有全局变量
    global_vars = {k: v for k, v in globals().items() if not k.startswith("__") and not callable(v)}
    if var_name not in global_vars:
        __log.error(f"保存配置{var_name}失败，没有找到对应的配置项！")
        return

    config = __configparser.ConfigParser()
    config_file = get_config_file(__filename)
    config.read(config_file)
    split_save(config, var_name, var_value)

    # 写入到配置文件
    with config_file.open("w") as file:
        config.write(file)


def split_save(config, var_name, var_value):
    if len(var_name.split('_')) > 1:
        conf = var_name.split('_', 1)[0]
        key = var_name.split('_', 1)[1]
    else:
        conf = "default"
        key = var_name
    if conf not in config:
        config.add_section(conf)
    config[conf][key] = f"{var_value}"


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
    config = __configparser.ConfigParser()
    config_file = get_config_file(config_filename)
    global __filename
    __filename = config_filename
    config.read(config_file)

    # 获取所有全局变量
    global_vars = {k: v for k, v in globals().items() if not k.startswith("__") and not callable(v)}
    for var_name, var_value in global_vars.items():
        if len(var_name.split('_')) > 1:
            conf = var_name.split('_', 1)[0]
            key = var_name.split('_', 1)[1]
        else:
            conf = "default"
            key = var_name
        globals()[var_name] = get_config(config, conf.lower(), key.lower(), default_value=var_value, is_int=isinstance(var_value, int))
        if conf not in conf_dict:
            conf_dict[conf] = dict()
        conf_dict[conf][key] = globals()[var_name]


if __name__ == '__main__':
    config_init()