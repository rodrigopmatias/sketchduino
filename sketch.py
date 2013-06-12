# -*- coding: utf-8 -*-
from screen import out
from args import parse_args

import os
import re

__version__ = '0.0.2'

def search(regexp, directory, notfound=None):
    directories = [directory] if isinstance(directory, (tuple, list)) is False else directory
    flag = False

    for dirpath in directories:
        for filename in os.listdir(dirpath):
            if regexp.match(filename):
                notfound = os.path.join(dirpath, filename)
                flag = True
            if flag is True:
                break
        if flag is True:
            break
    return notfound

def find_avr_toolchain(params):
    if params.get('AVR_HOME', None) is None:
        params.update(
            AVR_HOME=os.path.sep.join([
                params.get('SDK_HOME'),
                'hardware',
                'tools',
                'avr'
            ])
        )

    avr_bindir = os.path.join(params.get('AVR_HOME'), 'bin')
    avr_includedir = os.path.join(params.get('AVR_HOME'), 'include')
    avr_libdir = os.path.join(params.get('AVR_HOME'), 'lib')

    params.update(
        CC=search(re.compile('^(avr\-gcc|gcc)$'), [avr_bindir, '/usr/bin'], 'not found'),
        LD=search(re.compile('^(avr\-ld|ld)$'), [avr_bindir, '/usr/bin'], 'not found'),
        OBJCOPY=search(re.compile('^(avr\-objcopy|objcopy)$'), [avr_bindir, '/usr/bin'], 'not found'),
        AVR_INCLUDE=avr_includedir,
        AVR_LIB=avr_libdir,
        AR=search(re.compile('^(avr\-ar|ar)$'), [avr_bindir, '/usr/bin'], 'not found')
    )

    return params

def expand_project_path(params):
    params.update(
        PROJECT_HOME=os.path.abspath(params.get('PROJECT_HOME'))
    )

    project_dir = params.get('PROJECT_HOME')

    params.update(
        SOURCE_DIR=os.path.join(project_dir, 'src'),
        LIB_DIR=os.path.join(project_dir, 'lib'),
        BINARY_DIR=os.path.join(project_dir, 'binary'),
        INCLUDE_DIR=os.path.join(project_dir, 'include'),
    )

    return params

def not_implemented(**kargs):
    out('Not implemented command %(RED)s%(BLINK)s%(command)s', **kargs)

def command_not_found(**kargs):
    out('The command %(RED)s%(BLINK)s%(command)s%(RESET)s not found!', **kargs)

def create_command(**kargs):
    pass

def main():
    params = expand_project_path(
        find_avr_toolchain(
            parse_args()
        )
    )

    out('%(GRAY)s%(BOLD)sStart of Arduino Sketch Utility.')
    out('%(CYAN)s%(BOLD)sMCU name%(RESET)s: %(mcu)s', **params)
    out('%(CYAN)s%(BOLD)sMCU clock%(RESET)s: %(clock)0.2f MHz', **params)
    out('%(CYAN)s%(BOLD)sArduino SDK%(RESET)s: %(SDK_HOME)s', **params)
    out('%(CYAN)s%(BOLD)sAVR Compiler%(RESET)s: %(AVR_HOME)s', **params)
    out(' - %(CYAN)s%(BOLD)sCC%(RESET)s: %(CC)s', **params)
    out(' - %(CYAN)s%(BOLD)sLD%(RESET)s: %(LD)s', **params)
    out(' - %(CYAN)s%(BOLD)sOBJCOPY%(RESET)s: %(OBJCOPY)s', **params)
    out(' - %(CYAN)s%(BOLD)sAR%(RESET)s: %(AR)s', **params)
    out(' - %(CYAN)s%(BOLD)sINCLUDE%(RESET)s: %(AVR_INCLUDE)s', **params)
    out(' - %(CYAN)s%(BOLD)sLIB%(RESET)s: %(AVR_LIB)s', **params)
    out('%(CYAN)s%(BOLD)sProject Path%(RESET)s: %(PROJECT_HOME)s', **params)
    out(' - %(CYAN)s%(BOLD)sSources%(RESET)s: %(SOURCE_DIR)s', **params)
    out(' - %(CYAN)s%(BOLD)sLibrary%(RESET)s: %(LIB_DIR)s', **params)
    out(' - %(CYAN)s%(BOLD)sBinary%(RESET)s: %(BINARY_DIR)s', **params)
    out(' - %(CYAN)s%(BOLD)sInclude%(RESET)s: %(INCLUDE_DIR)s', **params)
    out('%(BOLD)s-------')
    CMD_MAP = {
        'create': create_command,
        'update': not_implemented,
        'build': not_implemented,
        'deploy': not_implemented,
    }

    cmd = params.get('command')
    CMD_MAP.get(cmd, command_not_found)(**params)
    out('%(BOLD)s-------')
    out('%(GRAY)s%(BOLD)sEnd of Arduino Sketch Utility.')

if __name__ == '__main__':
    main()
