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
from sketchduino.screen import out
from sketchduino.args import parse_args
from sketchduino.template import templates

import os
import re
import codecs
import json
import subprocess as sp

__version__ = '0.5.3'


def sdk_refresh(params):
    sdk_home = params.get('sdk_home', None)

    params.update(
        sdk_variant_dir=os.path.sep.join([sdk_home, 'hardware', 'arduino', 'variants']) if sdk_home else '',
        sdk_source_dir=os.path.sep.join([sdk_home, 'hardware', 'arduino', 'cores', 'arduino']) if sdk_home else '',
        sdk_libary_dir=os.path.sep.join([sdk_home, 'libraries']) if sdk_home else '',
    )

    if sdk_home is not None:
        sdk_version = '000'
        with open(os.path.sep.join([sdk_home, 'lib', 'version.txt'])) as fd:
            sdk_version = fd.read().replace('.', '')

        params.update(sdk_version=sdk_version)

    return params


def search(patterns, directory, notfound=None):
    directories = tuple([directory]) if not isinstance(directory, (tuple, list)) else directory
    patterns = tuple([patterns]) if not isinstance(patterns, (tuple, list)) else patterns
    rst = notfound

    for pattern in patterns:
        compiled = re.compile(pattern)
        rst = search_for_pattern(compiled, directories, notfound)

        if rst != notfound:
            break

    return rst


def search_for_pattern(pattern, directories, notfound):
    flag = False

    for dirpath in directories:
        for filename in os.listdir(dirpath):
            if pattern.match(filename):
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

        avr_home = params.get('avr_home')
        avr_bindir = os.path.join(avr_home, 'bin')
        avr_includedir = os.path.join(avr_home, 'include')
        avr_libdir = os.path.join(avr_home, 'lib')

        params.update(
            cxx=search((r'^avr\-g\+\+$', r'^g\+\+$'), [avr_bindir, '/usr/bin'], 'not found'),
            cc=search((r'^avr\-gcc$', r'^gcc$'), [avr_bindir, '/usr/bin'], 'not found'),
            ld=search((r'^avr\-ld$', r'^ld$'), [avr_bindir, '/usr/bin'], 'not found'),
            objcopy=search((r'^avr\-objcopy$', r'^objcopy$'), [avr_bindir, '/usr/bin'], 'not found'),
            size=search((r'^avr\-size$', r'^size$'), [avr_bindir, '/usr/bin'], 'not found'),
            avr_include=avr_includedir,
            avr_lib=avr_libdir,
            ar=search((r'^avr\-ar$', r'^ar$'), [avr_bindir, '/usr/bin'], 'not found'),
            asm=search((r'^avr\-as$', r'^as$'), [avr_bindir, '/usr/bin'], 'not found'),
            avrdude=search('^avrdude(|64)$', [avr_home, '/usr/bin'], 'not found')
        )

    return params


def expand_project_path(params):
    params.update(
        project_home=os.path.abspath(params.get('project_home'))
    )

    project_home = params.get('project_home')

    params.update(
        source_dir=os.path.join(project_home, 'src'),
        lib_dir=os.path.join(project_home, 'lib'),
        bin_dir=os.path.join(project_home, 'binary'),
        include_dir=os.path.join(project_home, 'include'),
    )

    return params


def not_implemented(**kargs):
    '''
    Comando não implementado até o momento.
    '''
    out('Not implemented command %(RED)s%(BLINK)s%(command)s', **kargs)


def command_not_found(**kargs):
    '''
    Commando não encontrado.
    '''
    out('The command %(RED)s%(BLINK)s%(command)s%(RESET)s not found!', **kargs)


def create_directory_tree(directory):
    if os.path.isdir(directory) is False:
        parent = os.path.dirname(directory)
        if parent not in ('/', '.', '..', ''):
            create_directory_tree(parent)
        os.mkdir(directory)
        return '+'
    else:
        return 'S'


def scan_for_sources(path, basepath=None):
    is_source = lambda filename: re.match('^.*\.(c|cc|cpp|cxx)$', filename) is not None
    files = []
    basepath = basepath if basepath else path

    if os.path.isdir(path) is True:
        for attr in os.listdir(path):
            filepath = os.path.join(path, attr)
            if attr not in ('.', '..') and os.path.isdir(filepath):
                files = files + scan_for_sources(filepath, basepath)
            elif os.path.isfile(filepath) and is_source(attr):
                files.append(os.path.relpath(filepath, basepath))

    return files


def src_to_obj(src):
    return re.sub('\/', '-', re.sub('\.(c|cc|cpp|hpp|cxx)$', '.o', src))


def src_to_asm(src):
    return re.sub('\/', '-', re.sub('\.(c|cc|cpp|hpp|cxx)$', '.s', src))


def sources_to_objects(sources, prefix=''):
    objs = []
    for src in sources:
        src = src_to_obj(src)
        src = src.replace(os.path.sep, '-')
        src = '-'.join([prefix, src])

        objs.append(os.path.join('tmp', src))

    return objs


def sources_to_asm(sources, prefix=''):
    objs = []
    for src in sources:
        src = src_to_asm(src)
        src = src.replace(os.path.sep, '-')
        src = '-'.join([prefix, src])

        objs.append(os.path.join('tmp', src))

    return objs


def asm_ruler_for(sources, source_dir='', obj_dir='', prefix=''):
    rulers = []

    for source in sources:
        obj = src_to_asm(source)
        if re.match(r'^.*\.c$', source):
            rulers.append(templates.get('c_asm_ruler') % {
                'obj': os.path.join(obj_dir, '-'.join([prefix, obj])),
                'source': os.path.join(source_dir, source)
            })
        else:
            rulers.append(templates.get('cxx_asm_ruler') % {
                'obj': os.path.join(obj_dir, '-'.join([prefix, obj])),
                'source': os.path.join(source_dir, source)
            })

    return '\n\n'.join(rulers)


def ruler_for(sources, source_dir='', obj_dir='', prefix=''):
    rulers = []

    for source in sources:
        obj = src_to_asm(source)
        if re.match(r'^.*\.c$', source):
            rulers.append(templates.get('c_asm_ruler') % {
                'obj': os.path.join(obj_dir, '-'.join([prefix, obj])),
                'source': os.path.join(source_dir, source)
            })
        else:
            rulers.append(templates.get('cxx_asm_ruler') % {
                'obj': os.path.join(obj_dir, '-'.join([prefix, obj])),
                'source': os.path.join(source_dir, source)
            })

    return '\n\n'.join(rulers)


def obj_ruler_for(sources, source_dir='', obj_dir='', prefix=''):
    rulers = []

    for source in sources:
        obj = src_to_obj(source)
        rulers.append(templates.get('asm_obj_ruler') % {
            'obj': os.path.join(obj_dir, '-'.join([prefix, obj])),
            'source': os.path.join(obj_dir, '-'.join([prefix, src_to_asm(source)]))
        })

    return '\n\n'.join(rulers)


def core_ruler(sources, prefix, obj_dir, library):
    rst = []

    for src in sources:
        obj = os.path.join(obj_dir, '-'.join([prefix, src_to_obj(src)]))
        rst.append(templates.get('static_link') % {
            'obj': obj,
            'lib': os.path.join('binary', library)
        })

    return rst


def gen_pgr_extra(serial=None, baudrate=None, **params):
    params = []

    if serial:
        params.append('-P')
        params.append(serial)

    if baudrate:
        params.append('-b')
        params.append(baudrate)

    return ' '.join(params)


def detect_libraries(lib_dir, **kwargs):
    rst = {}

    for name in [item for item in os.listdir(lib_dir) if item not in ['.', '..']]:
        path = os.path.join('lib', name)
        if os.path.isdir(path):
            sources = scan_for_sources(path)
            rst.update({
                name: {
                    'path': path,
                    'asm_dep': sources_to_asm(sources, prefix=name),
                    'obj_dep': sources_to_objects(sources, prefix=name),
                    'obj_rulers': obj_ruler_for(sources, path, 'tmp', name),
                    'asm_rulers': asm_ruler_for(sources, path, 'tmp', name)
                }
            })

    return rst


def linker_ruler_for(objs, out=''):
    rulers = []

    for obj in objs:
        rulers.append(templates.get('static_link') % {
            'obj': obj,
            'lib': out
        })

    return '\n'.join(rulers)


def lib_ruler_for(name, conf):
    tpl = '''binary/%(name)s.a: %(obj_deps)s%(linker)s

%(obj_rulers)s

%(asm_rulers)s
'''

    return tpl % {
        'name': name,
        'obj_deps': ' '.join(conf.get('obj_dep')),
        'linker': linker_ruler_for(conf.get('obj_dep'), 'binary/%s.a' % name),
        'obj_rulers': conf.get('obj_rulers'),
        'asm_rulers': conf.get('asm_rulers')
    }


def create_or_update_makefile(sdk_source_dir, **params):
    project_home = params.get('project_home')
    sources = scan_for_sources(params.get('source_dir'))
    core_sources = scan_for_sources(sdk_source_dir)

    libs = detect_libraries(**params)

    params.update(
        libs_rulers=''.join([lib_ruler_for(name, conf) for name, conf in libs.items()]),
        lib_deps=' '.join(['binary/%s.a' % name for name in libs.keys()]),
        pgrextra=gen_pgr_extra(**params),
        version=__version__,
        clock_hz=int((params.get('clock', 0) or 0) * 10 ** 6),
        project_name=project_home.split(os.path.sep)[-1],
        core_obj_dep=' '.join(
            sources_to_objects(core_sources, prefix='core')
        ),
        core_ruler=''.join(core_ruler(core_sources, 'core', 'tmp', 'core.a')),
        obj_dep=' '.join(
            sources_to_objects(sources, prefix='sketch')
        ),
        asm_dep=' '.join(
            sources_to_asm(sources, prefix='sketch')
        ),
        asm_rulers=asm_ruler_for(sources, 'src', 'tmp', 'sketch'),
        obj_rulers=obj_ruler_for(sources, 'src', 'tmp', 'sketch'),
        core_asm_rulers=asm_ruler_for(core_sources, sdk_source_dir, 'tmp', 'core'),
        core_obj_rulers=obj_ruler_for(core_sources, sdk_source_dir, 'tmp', 'core'),
    )
    filename = os.path.join(project_home, 'Makefile')
    rst = '?'

    rst = 'U' if os.path.isfile(filename) else 'C'

    with codecs.open(filename, 'w', 'utf-8') as fd:
        fd.write(templates.get('Makefile' if params.get('variant') != 'avr' else 'avr-Makefile') % params)

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
            fd.write(templates.get('main.cc' if params.get('variant') != 'avr' else 'avr-main.cc') % params)

    return rst


def create_or_update_command(command=None, **kargs):
    '''
    Manipula o projeto.
    '''
    params = expand_project_path(
        sdk_refresh(
            find_avr_toolchain(kargs)
        )
    )

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
    '''
    Executa a limpeza do cache de compilação e realiza uma nova compilação completa.
    '''
    sp.call('cd %s && make clean && make' % project_home, shell=True)


def build_command(project_home, **params):
    '''
    Executa a compilação do projeto de acordo com as configurações, somente compila
    o que foi modificado desde a ultima compilação se houver cache.
    '''
    sp.call('cd %s && make' % project_home, shell=True)


def clean_command(project_home, **params):
    '''
    Executa limpeza da ultima compilação.
    '''
    sp.call('cd %s && make clean' % project_home, shell=True)


def show_command(**params):
    '''
    Mostra informações da configuração atual do projeto.
    '''
    params = expand_project_path(params)

    if params.get('clock', None) is None:
        params.update(clock=0)

    tpl = [
        '%(CYAN)s%(BOLD)sMCU name%(RESET)s: %(mcu)s',
        '%(CYAN)s%(BOLD)sMCU clock%(RESET)s: %(clock)0.2f MHz',
        '%(CYAN)s%(BOLD)sVariant%(RESET)s: %(variant)s',
        '%(CYAN)s%(BOLD)sArduino SDK%(RESET)s: %(sdk_home)s',
        ' - %(CYAN)s%(BOLD)sVariants%(RESET)s: %(sdk_variant_dir)s',
        ' - %(CYAN)s%(BOLD)sLibraries%(RESET)s: %(sdk_libary_dir)s',
        ' - %(CYAN)s%(BOLD)sSources%(RESET)s: %(sdk_source_dir)s',
        ' - %(CYAN)s%(BOLD)sProgramer%(RESET)s: %(programer)s',
        ' - %(CYAN)s%(BOLD)sSerial port%(RESET)s: %(serial)s',
        '%(CYAN)s%(BOLD)sAVR Compiler%(RESET)s: %(avr_home)s',
        ' - %(CYAN)s%(BOLD)sCC%(RESET)s: %(cc)s',
        ' - %(CYAN)s%(BOLD)sLD%(RESET)s: %(ld)s',
        ' - %(CYAN)s%(BOLD)sOBJCOPY%(RESET)s: %(objcopy)s',
        ' - %(CYAN)s%(BOLD)sAR%(RESET)s: %(ar)s',
        ' - %(CYAN)s%(BOLD)sASM%(RESET)s: %(asm)s',
        ' - %(CYAN)s%(BOLD)sSIZE%(RESET)s: %(size)s',
        ' - %(CYAN)s%(BOLD)sINCLUDE%(RESET)s: %(avr_include)s',
        ' - %(CYAN)s%(BOLD)sLIB%(RESET)s: %(avr_lib)s',
        '%(CYAN)s%(BOLD)sProject Path%(RESET)s: %(project_home)s',
        ' - %(CYAN)s%(BOLD)sSources%(RESET)s: %(source_dir)s',
        ' - %(CYAN)s%(BOLD)sLibrary%(RESET)s: %(lib_dir)s',
        ' - %(CYAN)s%(BOLD)sBinary%(RESET)s: %(bin_dir)s',
        ' - %(CYAN)s%(BOLD)sInclude%(RESET)s: %(include_dir)s'
    ]

    out('\n'.join(tpl), **params)


def variant_list(sdk_variant_dir, variant, **params):
    '''
    Mostra a lista de variantes reconhecida pela SDK do arduino.
    '''
    pathname = "avr"
    if variant == pathname:
        out(' %(GREEN)s%(BOLD)s%(pathname)s', pathname=pathname)
    else:
        out(' %(GREEN)s%(pathname)s', pathname=pathname)
        if sdk_variant_dir is not None and os.path.isdir(sdk_variant_dir) is True:
            for pathname in os.listdir(sdk_variant_dir):
                path = os.path.join(sdk_variant_dir, pathname)
                if os.path.isdir(path) and variant == pathname:
                    out(' %(GREEN)s%(BOLD)s%(pathname)s', pathname=pathname)
                elif os.path.isdir(path):
                    out(' %(GREEN)s%(pathname)s', pathname=pathname)


def version_cmd(*args, **kwargs):
    '''
    Mostra a versão do sketchduino.
    '''
    out('Sketchduino version %(BOLD)s%(GREEN)s%(version)s', version=__version__)

def main():
    params = parse_args()

    if params.get('project_home', '') == '':
        params.update(project_home=os.getcwd())

    apply_if(params, load_sketch_conf(params.get('project_home')))

    # print(json.dumps(params, indent=4))

    out('%(GRAY)s%(BOLD)sStart of Arduino Sketch Utility.')
    out('%(BOLD)s-------')
    CMD_MAP = {
        'create': create_or_update_command,
        'update': create_or_update_command,
        'build': build_command,
        'rebuild': rebuild_command,
        'clean': clean_command,
        'deploy': not_implemented,
        'variant-list': variant_list,
        'library-list': not_implemented,
        'show': show_command,
        'version': version_cmd,
    }

    cmd = params.get('command')
    if cmd == 'help':
        for command, method in CMD_MAP.items():
            out(
                ' %(GRAY)s%(BOLD)s%(command)s%(RESET)s%(doc)s',
                command=command,
                doc=method.__doc__
            )
    else:
        CMD_MAP.get(cmd, command_not_found)(**params)

    out('%(BOLD)s-------')
    out('%(GRAY)s%(BOLD)sEnd of Arduino Sketch Utility.')

if __name__ == '__main__':
    main()
