# -*- coding: utf-8 -*-
from screen import out
from args import parse_args
from template import templates

import os
import re
import codecs
import json
import subprocess as sp

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
    if params.get('avr_home') is not None or params.get('sdk_home') is not None:
        if params.get('avr_home', None) is None:
            params.update(
                avr_home=os.path.sep.join([
                    params.get('sdk_home'),
                    'hardware',
                    'tools',
                    'avr'
                ])
            )

        avr_bindir = os.path.join(params.get('avr_home'), 'bin')
        avr_includedir = os.path.join(params.get('avr_home'), 'include')
        avr_libdir = os.path.join(params.get('avr_home'), 'lib')

        params.update(
            cc=search(re.compile('^(avr\-gcc|gcc)$'), [avr_bindir, '/usr/bin'], 'not found'),
            ld=search(re.compile('^(avr\-ld|ld)$'), [avr_bindir, '/usr/bin'], 'not found'),
            objcopy=search(re.compile('^(avr\-objcopy|objcopy)$'), [avr_bindir, '/usr/bin'], 'not found'),
            avr_include=avr_includedir,
            avr_lib=avr_libdir,
            ar=search(re.compile('^(avr\-ar|ar)$'), [avr_bindir, '/usr/bin'], 'not found')
        )

    return params

def expand_project_path(params):
    params.update(
        project_home=os.path.abspath(params.get('project_home'))
    )

    project_dir = params.get('project_home')

    params.update(
        source_dir=os.path.join(project_dir, 'src'),
        lib_dir=os.path.join(project_dir, 'lib'),
        bin_dir=os.path.join(project_dir, 'binary'),
        include_dir=os.path.join(project_dir, 'include'),
    )

    return params

def not_implemented(**kargs):
    out('Not implemented command %(RED)s%(BLINK)s%(command)s', **kargs)

def command_not_found(**kargs):
    out('The command %(RED)s%(BLINK)s%(command)s%(RESET)s not found!', **kargs)

def create_directory_tree(directory):
    if os.path.isdir(directory) is False:
        parent = os.path.dirname(directory)
        if parent != '/':
            create_directory_tree(parent)
        os.mkdir(directory)
        return '+'
    else:
        return 'S'

def scan_for_sources(path, basepath=None):
    is_source = lambda filename: re.match('^.*\.(c|cc|cpp|cxx)$', filename) is not None
    files = []
    basepath = basepath if basepath else path

    for attr in os.listdir(path):
        filepath = os.path.join(path, attr)
        if attr not in ('.', '..') and os.path.isdir(filepath):
            files = files + scan_for_sources(filepath, basepath)
        elif os.path.isfile(filepath) and is_source(attr):
            files.append(os.path.relpath(filepath, basepath))

    return files

def sources_to_objects(sources):
    objs = []
    for src in sources:
        src = src.replace('.cc', '.o')
        src = src.replace('.c', '.o')
        src = src.replace('.cpp', '.o')
        src = src.replace('.cxx', '.o')
        src = src.replace(os.path.sep, '-')
        objs.append(os.path.join('tmp', src))

    return objs

def ruler_for(sources):
    rulers = []

    for source in sources:
        obj = source.replace('.cc', '').replace('.c', '').replace('.cpp', '').replace('.cxx', '').replace(os.path.sep, '-') + '.o'
        rulers.append(templates.get('obj_ruler') % {
            'obj': obj,
            'source': source
        })

    return '\n\n'.join(rulers)

def create_or_update_makefile(**params):
    project_home = params.get('project_home')
    sources = scan_for_sources(params.get('source_dir'))

    params.update(
        version=__version__,
        clock_hz=long(params.get('clock') * 10 ** 6),
        project_name=project_home.split(os.path.sep)[-1],
        obj_dep=' '.join(sources_to_objects(sources)),
        obj_rulers=ruler_for(sources)
    )
    filename = os.path.join(project_home, 'Makefile')
    rst = '?'

    rst = 'U' if os.path.isfile(filename) else 'C'

    with codecs.open(filename, 'w', 'utf-8') as fd:
        fd.write(templates.get('Makefile') % params)

    return rst

def create_main(**params):
    project_home = params.get('project_home')
    params.update(
        version=__version__,
        project_name=project_home.split(os.path.sep)[-1]
    )
    filename = os.path.sep.join([project_home, 'src', 'main.cc'])

    rst = '?'

    rst = 'S' if os.path.isfile(filename) else 'C'
    if rst == 'C':
        with codecs.open(filename, 'w', 'utf-8') as fd:
            fd.write(templates.get('main.cc') % params)

    return rst

def create_or_update_command(command=None, **kargs):
    params = expand_project_path(find_avr_toolchain(kargs))
    project_home = kargs.get('project_home')
    temp_dir = os.path.join(project_home, 'tmp')
    out('Creating sketch in %(CYAN)s%(project_home)s', endline='%(RESET)s ', **params)

    out(create_directory_tree(project_home), endline='')
    out(create_directory_tree(temp_dir), endline='')
    out(create_directory_tree(kargs.get('source_dir')), endline='')
    out(create_directory_tree(kargs.get('lib_dir')), endline='')
    out(create_directory_tree(kargs.get('bin_dir')), endline='')
    out(create_directory_tree(kargs.get('include_dir')), endline='')
    out(create_main(**kargs), endline='')
    out(create_or_update_makefile(**kargs), endline='')

    with codecs.open(os.path.join(project_home, 'sketch.json'), 'w', 'utf-8') as fd:
        json.dump(params, fd, indent=4)

    out('', **params)

def show_command(command=None, project_dir=None, **kargs):
    out(project_dir)

def load_sketch_conf(project_home):
    params = None

    try:
        with codecs.open(os.path.join(project_home, 'sketch.json'), 'r', 'utf-8') as fd:
            params = json.load(fd)
    except:
        params = {}

    return params

def apply_if(a, b):
    for key, value in b.items():
        if a.get(key, None) is None:
            a.update({key: value})

    return a

def rebuild_command(project_home, **params):
    sp.call('cd %s && make clean && make' % project_home, shell=True)

def build_command(project_home, **params):
    sp.call('cd %s && make' % project_home, shell=True)

def clean_command(project_home, **params):
    sp.call('cd %s && make clean' % project_home, shell=True)

def show_command(**params):
    params = expand_project_path(params)

    out('%(CYAN)s%(BOLD)sMCU name%(RESET)s: %(mcu)s', **params)
    out('%(CYAN)s%(BOLD)sMCU clock%(RESET)s: %(clock)0.2f MHz', **params)
    out('%(CYAN)s%(BOLD)sArduino SDK%(RESET)s: %(sdk_home)s', **params)
    out('%(CYAN)s%(BOLD)sAVR Compiler%(RESET)s: %(avr_home)s', **params)
    out(' - %(CYAN)s%(BOLD)scc%(RESET)s: %(cc)s', **params)
    out(' - %(CYAN)s%(BOLD)sLD%(RESET)s: %(ld)s', **params)
    out(' - %(CYAN)s%(BOLD)sobjcopy%(RESET)s: %(objcopy)s', **params)
    out(' - %(CYAN)s%(BOLD)sAR%(RESET)s: %(ar)s', **params)
    out(' - %(CYAN)s%(BOLD)sINCLUDE%(RESET)s: %(avr_include)s', **params)
    out(' - %(CYAN)s%(BOLD)sLIB%(RESET)s: %(avr_lib)s', **params)
    out('%(CYAN)s%(BOLD)sProject Path%(RESET)s: %(project_home)s', **params)
    out(' - %(CYAN)s%(BOLD)sSources%(RESET)s: %(source_dir)s', **params)
    out(' - %(CYAN)s%(BOLD)sLibrary%(RESET)s: %(lib_dir)s', **params)
    out(' - %(CYAN)s%(BOLD)sBinary%(RESET)s: %(bin_dir)s', **params)
    out(' - %(CYAN)s%(BOLD)sInclude%(RESET)s: %(include_dir)s', **params)

def main():
    params = parse_args()
    apply_if(params, load_sketch_conf(params.get('project_home')))

    out('%(GRAY)s%(BOLD)sStart of Arduino Sketch Utility.')
    out('%(BOLD)s-------')
    CMD_MAP = {
        'create': create_or_update_command,
        'update': create_or_update_command,
        'build': build_command,
        'rebuild': rebuild_command,
        'clean': clean_command,
        'deploy': not_implemented,
        'show': show_command,
    }

    cmd = params.get('command')
    CMD_MAP.get(cmd, command_not_found)(**params)
    out('%(BOLD)s-------')
    out('%(GRAY)s%(BOLD)sEnd of Arduino Sketch Utility.')

if __name__ == '__main__':
    main()
