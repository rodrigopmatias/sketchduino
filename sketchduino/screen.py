# -*- coding: utf-8 -*-
'''
Copyright 2012 Rodrigo Pinheiro Matias <rodrigopmatias@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
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
