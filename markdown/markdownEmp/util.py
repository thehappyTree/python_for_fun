# -*- coding:utf-8 -*-


def lines(file):
    """
     生成器，在文本最后一行加空格 ？
    """
    for line in file:yield line
    yield '\n'

def blocks(file):
    """
    生成器，生成单独文本快
    :param file:
    :return:
    """
    block = []
    for line in lines(file):
        if line.strip():
            block.append(line)




