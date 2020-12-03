# thirdparty.builder.assist

Tool for automatically building code on save.

## Usage Synopsis

```
assist -p <path to watch> -- <command to run>
```

## Overview

Inotify (i.e. inotifywait) and other file change notification systems will send many events all at once about how a file is being accessed or changed. You can't you these raw events to trigger a build because you'd start running the build prematurely.

This script is designed to watch for only mutation events (i.e. it ignores opens, accesses, and close with nowrite). When using an editor like VSCode, it is constantly accessing file meta data to determine if it needs to reread files. We should not build everytime VSCode merely reads the metadata of a file path.

The script waits for the inotify events to settle before running the build again. For example, you may run a formatter that modifies many files in the source directory. You don't want the build command to be executed after only the first file has been written, you need to wait until all files have been touched. This settlement is detected with a simple timeout. It waits for a given duration of no events after an event before running the given reaction command.

The script will not queue commands to run while changes are incoming. If the given command takes a while to run, changes might be made to the source while the command is running. The last change time is recorded and this is checked against the last time the command was executed. If the difference is greater than the given settlement duration it'll rerun the command.

The script has a signal handler to catch Ctrl-C. Ctrl-C is the expected way to exit the watcher.py while its waiting for updates. I don't know what the behavior of the system is if you Ctrl-C/SIGINT while the given user command is being executed.

## Install

```
python3 -m pip install --upgrade thirdparty-builder-assist
```

## CLI Usage

Thirdparty Builder Assist includes a console script `assist`. The intended use for this is to run a file watcher for a source directory and automatically run a build and/or test command after there have been no changes to any files for 1 second.

If your current working directory is `/project`, and this project is a make project will all source stored in `/project/src`, you can use `assist` to automatically run `make` using a command like the following:

```
assist -p src -- make
```

## API Usage

Thirdparty Builder Assist comes with an API that allows your code to react to inotify events the same way the `assist` console script does. Using the same example above, here is an example Python snippet prints a message when change events are detected.

```
from thirdparty.builder.assist import start_watching
from time import sleep

# Fire up builder.assist thread.
assist_context = start_watching('/project/src')

while True:
    sleep(0.1)
    if assist_context.is_event():
        print("Detected changes.")
```

## Contributing

Any contributions and feature requests are welcome! Please submit all contributions for thirdparty.builder.assist as an issue or pull-request (PR) on [thirdparty.builder.assist's Github Page](https://github.com/third-party-dev/builder.assist).

## License

```
MIT License

Copyright (c) 2020 third-party-dev

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```
