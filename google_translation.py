# coding=utf-8
import requests
import re
from HandleJs import Py4Js


def translate(tk, content):
    if len(content) > 4891:
        print("翻译的长度超过限制！！！")
        return

    param = {'tk': tk, 'q': content}

    result = requests.get("""http://translate.google.cn/translate_a/single?client=t&sl=en 
        &tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss 
        &dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1&srcrom=0&ssel=0&tsel=0&kc=2""", params=param)

    # 返回的结果为Json，解析为一个嵌套列表
    RE = (result.json()[0])
    return result_handler(RE)


def result_handler(RE):
    result = ""
    for i in RE:
        if type(i[0]) == type("i"):
            result += i[0].split()[0].strip("\n")
    print(type(result))
    return "111"


def translation_tool(content):
    js = Py4Js()
    tk = js.getTk(content)
    if len(content) > 4891:
        print("翻译的长度超过限制！！！")
        return

    param = {'tk': tk, 'q': content}

    result = requests.get("""http://translate.google.cn/translate_a/single?client=t&sl=en 
        &tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss 
        &dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1&srcrom=0&ssel=0&tsel=0&kc=2""", params=param)

    # 返回的结果为Json，解析为一个嵌套列表
    RE = (result.json()[0])
    result = ""
    for i in RE:
        if type(i[0]) == type("i"):
            result += i[0].split()[0].strip("\n")
    print(type(result))
    return result

if __name__ == '__main__':
    content = """Beautiful is better than ugly. 
        Explicit is better than implicit. 
        Simple is better than complex. 
        Complex is better than complicated. 
        Flat is better than nested. 
        Sparse is better than dense. 
        Readability counts. 
        Special cases aren't special enough to break the rules. 
        Although practicality beats purity. 
        Errors should never pass silently. 
        Unless explicitly silenced. 
        In the face of ambiguity, refuse the temptation to guess. 
        There should be one-- and preferably only one --obvious way to do it. 
        Although that way may not be obvious at first unless you're Dutch. 
        Now is better than never. 
        Although never is often better than *right* now. 
        If the implementation is hard to explain, it's a bad idea. 
        If the implementation is easy to explain, it may be a good idea. 
        Namespaces are one honking great idea -- let's do more of those!
    """
    result = (translation_tool(content))
    print(result)
