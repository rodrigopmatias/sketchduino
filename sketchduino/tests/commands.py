from unittest import TestCase

import subprocess as sp

class CreateCommandTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cmd_args = [
            'sketchduino',
            '--cmd', 'create',
            '--project', 'nose_test',
            '--processor', 'atmega8',
            '--clock', '16',
            '--variant', 'standard',
            '--sdk', 'mock-toolchain',
        ]

        cls.fd = sp.Popen(
            ' '.join(cmd_args),
            shell=True,
            stdout=sp.PIPE,
            stderr=sp.PIPE
        )

    @classmethod
    def tearDownClass(cls):
        pass

    def test_call(self):
        self.fd.wait()
        self.assertEqual(self.fd.returncode, 0)

    def test_structure(self):
        pass

    def test_makefile(self):
        pass

class HelpCommandTestCase(TestCase):

    def test_show(self):
        with sp.Popen('sketchduino -h', shell=True, stdout=sp.PIPE, stderr=sp.PIPE) as fd:
            fd.wait()

            self.assertEqual(fd.returncode, 0)
            assert len(fd.stdout.read()) > 0
            assert len(fd.stderr.read()) == 0

    def test_command_show(self):
        with sp.Popen('sketchduino --cmd help', shell=True, stdout=sp.PIPE, stderr=sp.PIPE) as fd:
            fd.wait()

            self.assertEqual(fd.returncode, 0)
            assert len(fd.stdout.read()) > 0
            assert len(fd.stderr.read()) == 0

