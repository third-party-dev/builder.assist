#!/usr/bin/env python3

import sys
import subprocess
import argparse

from signal import signal, SIGINT
from time import sleep

from thirdparty.builder.assist import start_watching


def KeyboardInterrupt_handler(signum, frame):
    sys.exit(0)


def main_loop(path_to_watch, command_args):
    ctx = start_watching(path_to_watch)

    no_command = False
    cmd = " ".join(command_args).strip()
    if len(cmd) == 0:
        no_command = True

    while True:
        sleep(1)
        is_event = ctx.is_event()

        if is_event:
            if no_command:
                print("CHANGE_EVENT_OBSERVED")
            else:
                subprocess.run(cmd, stderr=sys.stderr,
                               stdin=sys.stdin, stdout=sys.stdout, shell=True)


def main():

    # This must be here for the setuptools console_script to pick it up.
    signal(SIGINT, KeyboardInterrupt_handler)

    parser = argparse.ArgumentParser(
        description='Run command when directory content changes.')
    parser.add_argument('-p', '--path', dest='path_to_watch',
                        default='.', metavar='PATH',
                        help='Path to watch')
    parser.add_argument('-c', dest='command', default='',
                        metavar='CMD', help='Command to run on path change.')
    # Note: This only exist for --help. We extract this before parse_args().
    parser.add_argument('--', dest='command_args',
                        metavar='ARG',
                        nargs='*', help='Command arguments to run on path change.')

    # Get the location of the sentinal.
    sentinal = 0
    try:
        sentinal = sys.argv.index('--')
    except:
        pass

    if sentinal >= 1:
        argv = sys.argv[1:sentinal]
    else:
        argv = sys.argv[1:]

    args = parser.parse_args(argv)

    command_args = [args.command]
    if sentinal >= 1:
        command_args.extend(sys.argv[sentinal + 1:])

    print(command_args)
    main_loop(args.path_to_watch, command_args)


if __name__ == '__main__':
    main()
