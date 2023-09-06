# 
# CS, by ftp
# 
import sys,os,subprocess
import datetime
import argparse

# Configuration
Config = {
    "USER": "ftower-p",
    "GROUP": "",
    "MAIL": "",
    "STORAGE_PATH": "~/Documents/cs_storage/",
    "NOTE_FILE": "cs_notes.txt"
}

# ==== Colors ====
class Color:
    BLACK   = '\033[30m'
    RED     = '\033[31m'
    GREEN   = '\033[32m'
    YELLOW  = '\033[33m'
    BLUE    = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN    = '\033[36m'
    WHITE   = '\033[37m'
    RESET   = '\033[39m'

# ==== FUNCTIONS ====
def ok():
    print(Color.GREEN + "\n✅ OK!" + Color.RESET)

def fail():
    print(Color.RED + "\n🟥 FAIL" + Color.RESET)

def done():
    print(Color.CYAN + "\n👍 DONE" + Color.RESET)


def run_command(command=[], successful_output_settings={}):
    """
    Successful output options example:
    {
        "output": "Successfully compiled code.",
        "contains": "OK!",
        "status_code": 0,
        ...
    }
    """

    # Successful command flag
    show_status_message = True
    successful_command  = False

    # Run the console command
    console_command = subprocess.run(command, stdout=subprocess.PIPE)
    command_output  = console_command.stdout.decode("utf-8")

    # Print the output
    print(command_output, end="")

    # Check if the result was successful
    if "output" in successful_output_settings:
        if successful_output_settings["output"] == command_output:
            successful_command = True
    
    elif "contains" in successful_output_settings:
        if successful_output_settings["contains"] in command_output:
            successful_command = True
    
    elif "status_code" in successful_output_settings:
        if successful_output_settings["status_code"] == console_command.returncode:
            successful_command = True
    else:
        # No "success" examples were passed, this must mean we shouldn't
        # display any status messages
        show_status_message = False
    
    # Show status message
    if show_status_message:
        if successful_command:
            ok()
        else:
            fail()

def timestamp():
    current_datetime = datetime.datetime.now()
    formatted_timestamp = current_datetime.strftime("%Y/%m/%d %H:%M:%S")
    return formatted_timestamp

# ==== SCRIPT ====
# Set up arguments
parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(title="Sub-Commands", dest="subcommand")
# language_selection = parser.add_subparsers("--lang", "-l", type=str, help="Select your target programming language", choices=["c"])
# language_selection = parser.add_subparsers("--lang", "-l", type=str, help="Select your target programming language", choices=["c"])

c_language = subparsers.add_parser("c", help="Use the C language")
c_language.add_argument("--norm", "--norminette", action="store_true", help="Compile your program")
c_language.add_argument("--newfile", help="Create a new template file for the selected language")
c_language.add_argument("--compile", action="store_true", help="Compile your program")
c_language.add_argument("--file", "-f", help="Select a target file")

parser.add_argument("--nobanner", action="store_true", help="Hide the banner")
# parser.add_argument("--note", "-n", action="store_true", help="Access your personal notes")

# Git
parser.add_argument("--savegame", action="store_true", help="Save your game? (adds and pushes files to git)")

# Parse arguments
args = parser.parse_args()

# Check if we should hide the banner
# Banner
if not args.nobanner:
    print(Color.RED + """ ▄▄· .▄▄ · 
▐█ ▌▪▐█ ▀. 
██ ▄▄▄▀▀▀█▄
▐███▌▐█▄▪▐█
·▀▀▀  ▀▀▀▀""" + Color.RESET)

# Automatically show help when no arguments are passed
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

# Programming Language selection
if args.subcommand == "c":
    # C compiling
    if args.compile:
        # Compile and run C code
        run_command(["cc", "-Wall", "-Wextra", "-Werror", args.file])
        run_command(["./a.out"], {"status_code": 0})

    # C code test with "the norminette/the norm"
    elif args.norm:
        run_command(["norminette", "-R", "CheckForbiddenSourceHeader", args.file], {
            "contains": ": OK!"
        })
    
    # Create a new file with template data (42 specific)
    elif args.newfile:
        with open(args.newfile, "a+") as newfile:
            newfile.write(f"""/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   {args.newfile + (" " * (51 - len(args.newfile))) }:+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: {Config["USER"]} <marvin@42.fr>{(" " * (28 - len(Config["USER"])))}+#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: {timestamp()} by {Config["USER"] + (" " * (17 - len(Config["USER"])))} #+#    #+#             */
/*   Updated: 2023/09/06 17:04:41 by {Config["USER"] + (" " * (16 - len(Config["USER"])))} ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
#include <unistd.h>\n\n""")
            newfile.close()
        done()

# # Open notes
# if args.note:
#     run_command(["vim", os.path.join(Config["STORAGE_PATH"], Config["NOTE_FILE"])])

# Git
if args.savegame:
    # Funny joke to "save the game"
    # TODO TODO TODO
    pass
    # run_command("git add --all")
    # run_command("git commit -m 'CS Automatic Push (" + str(timestamp()) + ")'")
    # run_command("git push")