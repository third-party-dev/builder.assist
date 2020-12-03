import os
import tempfile
from pathlib import PurePath
from thirdparty.builder.assist import start_watching, SETTLE_DURATION_DEFAULT
from time import sleep


def test_noevents_with_noactions():

    # Create a temporary directory to work in
    path_to_watch = PurePath(tempfile.mkdtemp())

    # Fire up builder.assist thread.
    ctx = start_watching(str(path_to_watch))

    # We need to poll to give the VFS time to trigger the event.
    tries = 0
    event_count = 0
    while tries < 30:
        sleep(0.1)
        is_event = ctx.is_event()
        if is_event == True:
            event_count += 1
        tries += 1

    assert event_count == 0


def test_events_with_file_open_write_close():

    # Create a temporary directory to work in
    path_to_watch = PurePath(tempfile.mkdtemp())

    # Fire up builder.assist thread.
    ctx = start_watching(str(path_to_watch))
    event_count = 0

    # Should get 1 event from this open, write, and close.
    with open(path_to_watch.joinpath("testfile"), "w") as fobj:
        fobj.write("stuff")

    # We need to poll to give the VFS time to trigger the event.
    tries = 0
    while tries < 30:
        sleep(0.1)
        is_event = ctx.is_event()
        if is_event == True:
            event_count += 1
        tries += 1

    assert event_count == 1


def test_events_with_file_open_access_nowrite():

    # Create a temporary directory to work in.
    path_to_watch = PurePath(tempfile.mkdtemp())

    # Create file to read from.
    with open(path_to_watch.joinpath("testfile"), "w") as fobj:
        fobj.write("stuff")

    # Fire up builder.assist thread.
    ctx = start_watching(str(path_to_watch))

    # Events generated from this read should be ignored.
    with open(path_to_watch.joinpath("testfile"), "r") as fobj:
        data = fobj.read()
    assert data == "stuff"

    # We need to poll to give the VFS time to trigger the event.
    tries = 0
    event_count = 0
    while tries < 30:
        sleep(0.1)
        is_event = ctx.is_event()
        if is_event == True:
            event_count += 1
        tries += 1

    assert event_count == 0


def test_events_with_many_file_open_write_close():

    # Create a temporary directory to work in
    path_to_watch = PurePath(tempfile.mkdtemp())

    # Fire up builder.assist thread.
    ctx = start_watching(str(path_to_watch))

    # Should get 1 event from these 10 opens, writes, and closes.
    for i in range(0, 10):
        with open(path_to_watch.joinpath("testfile%d" % i), "w") as fobj:
            fobj.write("stuff%d" % i)

    # We need to poll to give the VFS time to trigger the event.
    tries = 0
    event_count = 0
    while tries < 30:
        sleep(0.1)
        is_event = ctx.is_event()
        if is_event == True:
            event_count += 1
        tries += 1

    assert event_count == 1


def test_events_with_set_of_many_file_open_write_close():

    # Create a temporary directory to work in
    path_to_watch = PurePath(tempfile.mkdtemp())

    # Fire up builder.assist thread.
    ctx = start_watching(str(path_to_watch))
    event_count = 0

    # Should get 1st event from these 10 opens, writes, and closes.
    for i in range(0, 10):
        with open(path_to_watch.joinpath("testfile%d" % i), "w") as fobj:
            fobj.write("stuff%d" % i)

    # We need to poll to give the VFS time to trigger the event.
    tries = 0
    while tries < 30:
        sleep(0.1)
        is_event = ctx.is_event()
        if is_event == True:
            event_count += 1
        tries += 1

    sleep(SETTLE_DURATION_DEFAULT)

    # Should get 2nd event from these 10 opens, writes, and closes.
    for i in range(0, 10):
        with open(path_to_watch.joinpath("testfile%d" % i), "w") as fobj:
            fobj.write("stuff%d" % i)

    # We need to poll to give the VFS time to trigger the event.
    tries = 0
    while tries < 30:
        sleep(0.1)
        is_event = ctx.is_event()
        if is_event == True:
            event_count += 1
        tries += 1

    assert event_count == 2
