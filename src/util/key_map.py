from PyQt5 import QtCore


qt_key_dict = dict()


def create_key_map():
    key_map = {}
    # 遍历 QtCore.Qt 类的所有属性
    for name in dir(QtCore.Qt):
        # 筛选出所有以 "Key_" 开头的属性
        if name.startswith("Key_"):
            # 获取键名（去除前缀 "Key_"）
            key_name = name[4:]
            # 获取键值
            key_value = getattr(QtCore.Qt, name)
            # 添加到字典中
            key_map[key_name] = key_value
    return key_map


qt_key_map = create_key_map()


def key_config_init(key_dict):
    for conf, keys in key_dict.items():
        for key in [item.strip() for item in keys.split(',')]:
            if key in qt_key_map:
                if conf not in qt_key_dict:
                    qt_key_dict[conf] = list()
                qt_key_dict[conf].append(qt_key_map[key])
