#!/usr/bin/python

import os
import sys

# Load ~/.config/bck/bckrc variables into a dictionary.
def load_config():
    config = {}

    # Verify config existence.
    config_dir = os.path.expanduser("~/.config/bck")
    config_rc = config_dir + "/bckrc"

    if not os.path.exists(config_rc):
        # Make config directory if needed.
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        print("Error: no config file found in ~/.config/bck.")
        sys.exit()

    # Parse config variables.
    with open(config_rc) as f:
        for line in f:
            if line[0] == '#' or line == '\n' or not line:
                continue

            # Parse key-value pair.
            data = [x.strip() for x in line.strip().split('=')]
            config[data[0]] = data[1]

    return config

# Print the allowed commands.
def print_usage():
    print("usage: bck list")
    print("       bck push <source>")
    print("       bck pull [<source>]")

# List the contents of the root bck output directory.
def list(config):
    # Handle config data.
    port = config["port"]
    target = config["user"] + "@" + config["hostname"]
    directory = config["output_dir"]

    # TODO: subdirectories.

    # Make shell command.
    cmd = "ssh -p " + port + " " + target + " ls -Apoh --color=auto " + directory
    os.system(cmd)

# Push files to the remote bck output directory.
def push(config, sources):
    for source in sources:
        if not os.path.exists(source):
            print("Error: source \"%s\" not found." % source)
            print_usage()
            sys.exit()

    # Concatenate source files into a space-separated string for passing to rsync.
    source_list = ""
    for source in sources:
        source_list += os.path.expanduser(source) + " "

    # Handle config data.
    port = config["port"]
    target = config["user"] + "@" + config["hostname"]
    output_dir = config["output_dir"]
    final_output = target + ":" + output_dir

    # Make shell command.
    cmd = "rsync -avh --progress -e 'ssh -p " + port + "' " + source_list + final_output
    os.system(cmd)

# Pull files from the remote bck output directory.
def pull(config, sources):
    port = config["port"]
    target = config["user"] + "@" + config["hostname"]
    output_dir = config["output_dir"]
    final_output = target + ":" + output_dir + "/"

    # TODO: local output directory

    # Pull entire root bck directory into the current working directory.
    if len(sys.argv) < 3:
        cmd = "rsync -avh --progress -e 'ssh -p " + port + "' " + final_output + " . "
        os.system(cmd)
        sys.exit()

    # Make shell command.
    final_output += sources[0]
    cmd = "rsync -avh --progress -e 'ssh -p " + port + "' " + final_output + " . "
    os.system(cmd)
    sys.exit()


#
# Main
#

# Input validation.
if len(sys.argv) < 2:
    print("Error: no command or source given.")
    print_usage()
    sys.exit()

command = sys.argv[1]
sources = sys.argv[2:]

# Invalid command.
if command != "list" and command != "push" and command != "pull":
    print_usage()
    sys.exit()

config = load_config()

# Handle commands.
if command == "list":
    if len(sys.argv) > 2:
        print_usage()
        sys.exit()

    list(config)
    sys.exit()

if command == "push":
    if len(sys.argv) < 3:
        print_usage()
        sys.exit()

    push(config, sources)
    sys.exit()

if command == "pull":
    if len(sys.argv) > 3:
        print_usage()
        sys.exit()

    pull(config, sources)
    sys.exit()
