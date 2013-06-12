# -*- coding: utf-8 -*-
import sys

CODERS = {
    'BLACK': '\e[30m',
    'RED': '\e[31m',
    'BROW': '\e[32m',
    'GREEN': '\e[33m',
    'BROW': '\e[34m',
    'CYAN': '\e[35m',
    'MAGENTA': '\e[36m',
    'GRAY': '\e[37m',
    'RESET': '\e[0m',
    'BOLD': '\e[1m',
    'LINE': '\e[4m',
    'BLINK': '\e[5m',
}


def out(message, fd=sys.stdout, endline='\n', **params):
    message = message if isinstance(message, str) else str(message)
    params.update(CODERS)

    fd.write(message % params)
    fd.write(endline)
    fd.flush()