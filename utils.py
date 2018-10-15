# -*- coding: utf-8 -*-
"""
Some useful function.
"""


def readlines(sock, buffer_size=2048, delim='\n'):
    """
    Read data from socket until connection is closed,
    and supply a generator interface.
    """
    buf = ''
    data = True
    while data:
        data = sock.recv(buffer_size)
        buf += data.decode()

        while buf.find(delim) != -1:
            line, buf = buf.split('\n', 1)
            yield line
    return
