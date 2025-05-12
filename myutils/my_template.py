import json
from string import Template


class MyTemplate(Template):
    """支持 {{var}} 和 {{ var }} 形式的双大括号模板"""
    delimiter = '{{'
    idpattern = r'[a-zA-Z][a-zA-Z0-9_]*'
    pattern = r'''
        \{\{\s*  # 左大括号和可选空格
        (?:
          (?P<escaped>\{\{) |  # 转义的 {{
          (?P<named>%s)     |  # 命名变量 {{var}}
          (?P<braced>%s)    |  # 带括号的变量 {{var}}
          (?P<invalid>)        # 无效模式
        )
        \s*\}\}  # 右大括号和可选空格
        ''' % (idpattern, idpattern)


if __name__ == '__main__':
    # d = {'instanceIds':'{{name}}', 'resolution': '720*1280', 'dpi': 240, 'fps': 60}
    # temp = MyTemplate(json.dumps(d))
    # dd1 = temp.substitute({'name':'Bob'})
    # dd2 = json.loads(dd1)
    # print(dd2, type(dd2))
    d = {'instanceIds': '$name', 'resolution': '720*1280', 'dpi': 240, 'fps': 60}
    temp = Template(json.dumps(d))
    dd1 = temp.substitute({'name': 'Bob'})
    dd2 = json.loads(dd1)
    print(dd2, type(dd2))