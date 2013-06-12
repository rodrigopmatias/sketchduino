# -*- coding: utf-8 -*-
from argparse import ArgumentParser

def parse_args():
    parse = ArgumentParser(description='The Arduino Sketch utiliter')

    parse.add_argument(
        '--processor',
        dest='mcu',
        help='The name of Microcontroler Unit.',
        required=True
    )

    parse.add_argument(
        '--clock',
        dest='clock',
        help='The clock of Microcontroler Unit in MHz.',
        required=True,
        type=float
    )

    parse.add_argument(
        '--sdk',
        dest='SDK_HOME',
        help='The path for SDK of arduino.',
        required=True
    )

    parse.add_argument(
        '--avr',
        dest='AVR_HOME',
        help='The path for AVR/GNU compiler.',
    )

    parse.add_argument(
        '--cmd',
        dest='command',
        help='The command for Sketch utility.',
        required=True
    )

    parse.add_argument(
        '--project',
        dest='PROJECT_HOME',
        help='The home directory for project.',
        required=True
    )

    return parse.parse_args().__dict__