# -*- coding: utf-8 -*-
from argparse import ArgumentParser

def parse_args():
    parse = ArgumentParser(description='The Arduino Sketch utiliter')

    parse.add_argument(
        '--processor',
        dest='mcu',
        help='The name of Microcontroler Unit.'
    )

    parse.add_argument(
        '--clock',
        dest='clock',
        help='The clock of Microcontroler Unit in MHz.',
        type=float
    )

    parse.add_argument(
        '--sdk',
        dest='sdk_home',
        help='The path for SDK of arduino.'
    )

    parse.add_argument(
        '--avr',
        dest='avr_home',
        help='The path for AVR/GNU compiler.'
    )

    parse.add_argument(
        '--cmd',
        dest='command',
        help='The command for Sketch utility.',
        required=True
    )

    parse.add_argument(
        '--project',
        dest='project_home',
        help='The home directory for project.',
        default=''
    )

    parse.add_argument(
        '--variant',
        dest='variant',
        help='The variante of your arduino.'
    )

    return parse.parse_args().__dict__