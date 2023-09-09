# 
# CS, by ftp
# 
import sys,os,subprocess
import datetime
import argparse
import hashlib

# Configuration
Config = {
    "USER": "ftower-p",
    "GROUP": "",
    "EMAIL": "ftower-p@student.42.fr",
    "STORAGE_PATH": "~/Documents/cs_storage/",
    "NOTES_PATH": "/mnt/nfs/homes/ftower-p/Documents/notes.txt"
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
    print(Color.GREEN + "✅ OK!" + Color.RESET)

def fail():
    print(Color.RED + "🟥 FAIL" + Color.RESET)

def done():
    print(Color.CYAN + "👍 DONE" + Color.RESET)


def run_command(command=[], successful_output_settings={}, show_output=True):
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
    if show_output:
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
    
    # Return the status code for use with other code
    return console_command.returncode

def show_banner():
    print(Color.RED + """ ▄▄· .▄▄ · 
▐█ ▌▪▐█ ▀. 
██ ▄▄▄▀▀▀█▄
▐███▌▐█▄▪▐█
·▀▀▀  ▀▀▀▀""" + Color.RESET)

def timestamp():
    current_datetime = datetime.datetime.now()
    formatted_timestamp = current_datetime.strftime("%Y/%m/%d %H:%M:%S")
    return formatted_timestamp

def md5sum(data):
    return hashlib.md5(data).hexdigest()

# ==== SCRIPT ====
# Set up arguments
parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(title="Sub-Commands", dest="subcommand")

# C Language Mode
mode_c = subparsers.add_parser("c", help="Use C language mode")
mode_c.add_argument("--norm", "--norminette", help="Test your code with the Norminette", metavar="FILE")
mode_c.add_argument("--new", "-n", help="Create a new template file for the selected language", metavar="FILE")
mode_c.add_argument("--run", "-r", help="Compile & run your program", metavar="FILE")
mode_c.add_argument("--compile", "-c", help="Compile your program", metavar="FILE")
mode_c.add_argument("--format", "-f", help="Show formatted version your program", metavar="FILE")
mode_c.add_argument("--expect", help="OK is determined by whether the output is X", metavar="'value'")
mode_c.add_argument("--contains", help="OK is determined by whether the output contains X", metavar="'value'")

# mode_c.add_argument("--file", "-f", help="Select a target file")

# Output verification/matching
mode_match = subparsers.add_parser("match", help="Use match mode")
mode_match.add_argument("command")
mode_match.add_argument("--contains", "-c", help="Check if output contains a value", metavar="'value'")

# File checksum mode
mode_match = subparsers.add_parser("checksum", help="Use checksum mode")
mode_match.add_argument("file1")
mode_match.add_argument("file2")
mode_match.add_argument("--diff", "-d", action="store_true", help="Show the difference between the files")

# # Lookup mode (Helpful resources from Google)
# mode_lookup = subparsers.add_parser("lookup", help="Use lookup mode")
# mode_match.add_argument("--ascii-table", help="Show the C ascii table")

# Git Mode
mode_git = subparsers.add_parser("git", help="Use git mode")
mode_git.add_argument("--commit", "-c", action="store_true", help="Adds all changed files and commits them quickly!")
mode_git.add_argument("--log", "-l", action="store_true", help="Shows git commit history")
mode_git.add_argument("--savegame", "-s", action="store_true", help="Save your game? (adds and pushes files to git)")

parser.add_argument("--banner", action="store_true", help="Show the banner")
parser.add_argument("--note", "-n", action="store_true", help="Access your personal notes")
parser.add_argument("--clear", action="store_true", help="Clear the screen before displaying the output")

# Parse arguments
args = parser.parse_args()

# Clear the screen
if args.clear:
    os.system("clear||cls")

# Check if we should hide the banner
if args.banner:
    show_banner()

# Automatically show help when no arguments are passed
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

# Matching mode selection
if args.subcommand == "match":
    # Check if a command was supplied
    if args.contains:
        run_command([args.command], {"contains": args.contains}, show_output=False)

# Checksum mode selection
if args.subcommand == "checksum":
    # Check if we should show the difference between the files
    if args.diff:
        os.system(f"diff --color {args.file1} {args.file2}")

    # Check if a command was supplied
    if md5sum(open(args.file1, "rb").read()) == md5sum(open(args.file2, "rb").read()):
        ok()
    else:
        fail()

# # Lookup mode
# if args.subcommand == "lookup":
#     # Check which lookup was passed


# Programming Language selection
if args.subcommand == "c":
    # C compiling
    if args.compile:
        # Just compile C code
        run_command(["cc", "-Wall", "-Wextra", "-Werror", args.compile])
    
    if args.run:
        # Compile and run C code
        if run_command(["cc", "-Wall", "-Wextra", "-Werror", args.run]) == 0:
            # Check if successful output is based on status code or --expect flag
            if args.expect:
                # A output value is expected to return OK!
                run_command(["./a.out"], {"output": args.expect})
            elif args.contains:
                # A output value that contains X is expected to return OK!
                run_command(["./a.out"], {"output": args.contains})
            else:
                run_command(["./a.out"])
        else:
            fail()

    # C code test with "the norminette/the norm"
    elif args.norm:
        run_command(["norminette", "-R", "CheckForbiddenSourceHeader", args.norm], {
            "contains": ": OK!"
        })
    
    # 42 C Code Formatter
    elif args.format:
        run_command(["python3", "-m", "c_formatter_42", args.format])
    
    # Create a new file with template data (42 specific)
    elif args.new:
        with open(args.new, "a+") as newfile:
            newfile.write(f"""/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   {args.new + (" " * (51 - len(args.new))) }:+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: {Config["USER"]} <{Config["EMAIL"]}>{(" " * (40 - (len(Config["USER"])+len(Config["EMAIL"]))))}+#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: {timestamp()} by {Config["USER"] + (" " * (17 - len(Config["USER"])))} #+#    #+#             */
/*   Updated: 2023/09/06 17:04:41 by {Config["USER"] + (" " * (16 - len(Config["USER"])))} ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */
\n\n""")
            newfile.close()
        done()

# Open notes
if args.note:
    os.system(f"vim '{Config['NOTES_PATH']}'")

# Git
if args.subcommand == "git":
    if args.savegame:
        # Funny joke to "save the game"
        run_command(["git", "add", "--all"])
        run_command(["git", "commit", "-m", "CS Automatic Push (" + str(timestamp()) + ")"])
        run_command(["git", "push"], {"status_code": 0})
    
    if args.commit:
        run_command(["git", "add", "--all"])
        run_command(["git", "commit", "-m", "CS Automatic Push (" + str(timestamp()) + ")"], {"status_code": 0})

    if args.log:
        os.system("git log --stat")
