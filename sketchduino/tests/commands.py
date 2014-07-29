from unittest import TestCase
from sketchduino import *

import os
import re


class ProjectBaseTestCase(object):

    @classmethod
    def setUpClass(cls):
        cls.conf = {
            'project_home': 'nose_test',
            'sdk_home': 'mock-toolchain'
        }

    @classmethod
    def tearDownClass(cls):
        pass


class CommandTestCase(ProjectBaseTestCase, TestCase):

    def test_create_or_update(self):
        assert True


class HelpersTestCase(ProjectBaseTestCase, TestCase):

    def test_create_directory_tree(self):
        nodes = [
            os.path.join('root', 'node1'),
            os.path.join('root', 'node2'),
            os.path.join('root', 'node3'),
        ]

        for node in nodes:
            create_directory_tree(node)

        for node in nodes:
            self.assertTrue(os.path.exists(node))


    def test_src_to_obj(self):
        assert src_to_obj('main.c') == 'main.o'
        assert src_to_obj('main.cc') == 'main.o'
        assert src_to_obj('main.cpp') == 'main.o'
        assert src_to_obj('main.cxx') == 'main.o'


    def test_src_to_asm(self):
        assert src_to_asm('main.c') == 'main.s'
        assert src_to_asm('main.cc') == 'main.s'
        assert src_to_asm('main.cpp') == 'main.s'
        assert src_to_asm('main.cxx') == 'main.s'

    def test_find_avr_toolchain(self):
        rst = find_avr_toolchain(self.conf)

        self.assertEqual(
            rst.get('cc', None),
            os.path.sep.join([
                self.conf.get('sdk_home'),
                'hardware',
                'tools',
                'avr',
                'bin',
                'avr-gcc'
            ])
        )

        self.assertEqual(
            rst.get('cxx', None),
            os.path.sep.join([
                self.conf.get('sdk_home'),
                'hardware',
                'tools',
                'avr',
                'bin',
                'avr-g++'
            ])
        )

        self.assertEqual(
            rst.get('ld', None),
            os.path.sep.join([
                self.conf.get('sdk_home'),
                'hardware',
                'tools',
                'avr',
                'bin',
                'avr-ld'
            ])
        )

        self.assertEqual(
            rst.get('objcopy', None),
            os.path.sep.join([
                self.conf.get('sdk_home'),
                'hardware',
                'tools',
                'avr',
                'bin',
                'avr-objcopy'
            ])
        )

        self.assertEqual(
            rst.get('ar', None),
            os.path.sep.join([
                self.conf.get('sdk_home'),
                'hardware',
                'tools',
                'avr',
                'bin',
                'avr-ar'
            ])
        )

        self.assertEqual(
            rst.get('avr_include', None),
            os.path.sep.join([
                self.conf.get('sdk_home'),
                'hardware',
                'tools',
                'avr',
                'include'
            ])
        )

        self.assertEqual(
            rst.get('avr_lib', None),
            os.path.sep.join([
                self.conf.get('sdk_home'),
                'hardware',
                'tools',
                'avr',
                'lib'
            ])
        )

        self.assertTrue(
            rst.get('avrdude', None) == os.path.sep.join([
                self.conf.get('sdk_home'),
                'hardware',
                'tools',
                'avr',
                'avrdude64'
            ]) or
            rst.get('avrdude', None) == os.path.sep.join([
                self.conf.get('sdk_home'),
                'hardware',
                'tools',
                'avr',
                'avrdude'
            ])
        )

    def test_search(self):
        found_re = re.compile('^(avr\-g\+\+|g\+\+)$')
        notfound_re = re.compile('^notfound$')

        conf = find_avr_toolchain(self.conf)
        avr_bindir = os.path.join(conf.get('avr_home'), 'bin')

        rst = search(found_re, avr_bindir), search(notfound_re, avr_bindir)

        self.assertEqual(rst[0], os.path.join(avr_bindir, 'avr-g++'))
        self.assertEqual(rst[1], None)

    def test_sdk_refresh(self):
        rst = sdk_refresh(self.conf)

        sdk_home = self.conf.get('sdk_home')

        self.assertEqual(
            rst.get('sdk_variant_dir', None),
            os.path.sep.join([sdk_home, 'hardware', 'arduino', 'variants'])
        )

        self.assertEqual(
            rst.get('sdk_source_dir', None),
            os.path.sep.join([sdk_home, 'hardware', 'arduino', 'cores', 'arduino'])
        )

        self.assertEqual(
            rst.get('sdk_libary_dir', None),
            os.path.sep.join([sdk_home, 'libraries'])
        )

    def test_expand_project(self):
        rst = expand_project_path(self.conf)

        self.assertEqual(
            rst.get('source_dir', None),
            os.path.join(self.conf.get('project_home'), 'src')
        )

        self.assertEqual(
            rst.get('lib_dir', None),
            os.path.join(self.conf.get('project_home'), 'lib')
        )

        self.assertEqual(
            rst.get('bin_dir', None),
            os.path.join(self.conf.get('project_home'), 'binary')
        )

        self.assertEqual(
            rst.get('include_dir', None),
            os.path.join(self.conf.get('project_home'), 'include')
        )


class HelpCommandTestCase(TestCase):
    pass
