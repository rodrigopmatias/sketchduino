# -*- coding: utf-8 -*-
import sys

CODERS = {
    'BLACK': '\033[30m',
    'RED': '\033[31m',
    'GREEN': '\033[32m',
    'BROW': '\033[33m',
    'BLUE': '\033[34m',
    'MAGENTA': '\033[35m',
    'CYAN': '\033[36m',
    'GRAY': '\033[37m',
    'RESET': '\033[0m',
    'BOLD': '\033[1m',
    'LINE': '\033[4m',
    'BLINK': '\033[5m',
}


def out(message, fd=sys.stdout, endline='%(RESET)s\n', **params):
    message = message if isinstance(message, str) else str(message)
    params.update(CODERS)

    fd.write(message % params)
    fd.write(endline % params)
    fd.flush()