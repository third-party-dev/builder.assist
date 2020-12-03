#!/usr/bin/env python3

"""
Pre-requisite: pip install inotify

Brief: Use this script to launch a build script when source changes.

Usage: python assist.py <path to watch> <command to run>

Inotify (i.e. inotifywait) and other file change notification systems will
send many events all at once about how the file is being accessed or changed.
You can't you these raw events to trigger a build because you'd start running
the build prematurely.

This script is designed to watch for only mutation events (i.e. it ignores
opens, accesses, and close with nowrite). When using an editor like VSCode,
it is constantly accessing file meta data to determine if it needs to reread
files. We should not build everytime VSCode merely reads the metadata of a
file path.

The script waits for the inotify events to settle before running the build
again. For example, you may run a formatter that modifies many files in the
source directory. You don't want the build command to be executed after only
the first file has been written, you need to wait until all files have been
touched. This settlement is detected with a simple timeout. It waits for a
given duration of no events after an event before running the given reaction
command.

The script will not queue commands to run while changes are incoming. If the
given command takes a while to run, changes might be made to the source
while the command is running. The last change time is recorded and this is
checked against the last time the command was executed. If the difference is
greater than the given settlement duration it'll rerun the command.

The script has a signal handler to catch Ctrl-C. Ctrl-C is the expected way
to exit the watcher.py while its waiting for updates. I don't know what the
behavior of the system is if you Ctrl-C/SIGINT while the given user command
is being executed.

"""

import inotify.adapters
from threading import Thread, Lock
from time import monotonic

SETTLE_DURATION_DEFAULT = 1


class Context(object):
    def __init__(self, settle_duration=SETTLE_DURATION_DEFAULT):
        self._settle_duration = settle_duration

        self._event_lock = Lock()
        self._prev_time = 0
        self._last_checked = 0
        self._cur_time = 0

    @property
    def prev_time(self):
        return self._prev_time

    def update(self):
        self._event_lock.acquire()
        self._prev_time = monotonic()
        self._event_lock.release()

    def is_event(self):
        is_event = False
        self._event_lock.acquire()
        self._cur_time = monotonic()
        if self._prev_time != self._last_checked and self._cur_time - self._prev_time >= self._settle_duration:
            self._last_checked = self._prev_time
            is_event = True
        self._event_lock.release()
        return is_event


def inotifywait(ctx, path_to_watch):
    global prev_time
    i = inotify.adapters.InotifyTree(path_to_watch)

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event

        # IGNORE: access, close_nowrite, open
        # WATCH: modify, attrib, close_write, close, moved_to, moved_from, move,
        #        move_self, create, delete, delete_self, unmount
        ignored_events = ['IN_ACCESS', 'IN_CLOSE_NOWRITE', 'IN_OPEN']
        for event_type in type_names:
            if event_type in ignored_events:
                break
        else:
            ctx.update()


def start_watching(path_to_watch, settle_duration=SETTLE_DURATION_DEFAULT):
    ctx = Context(settle_duration=settle_duration)

    inotify_thread = Thread(target=inotifywait, args=(
        ctx, path_to_watch), daemon=True)
    inotify_thread.start()

    return ctx
