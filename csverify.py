# 
# CS, by ftp
# 
import sys,os,subprocess
import datetime
import argparse
import hashlib
import re
import json

# Configuration
Config = {}

# Get current path
data_directory  = os.path.join(os.path.expanduser("~"), "Documents", "csdata")
config_file     = os.path.join(data_directory, "config.json")

if not os.path.exists(data_directory):
    # Create a new config folder if it doesn't exist already
    os.makedirs(data_directory)

if not os.path.exists(config_file):
    Config = {
        "USER": "user",
        "GROUP": "",
        "EMAIL": "user@student.42.fr",
        "NOTES_PATH": os.path.join(data_directory, "notes.txt"),
        "messages": {
            "success": "✅ OK!",
            "fail": "🟥 FAIL",
            "done": "👍 DONE"
        }
    }
    # Write the default json
    with open(config_file, "w") as json_file:
        json.dump(Config, json_file)
        json_file.close()

# Load configuration from config.json file because it already exists
with open(config_file, "r") as config_file:
    Config = json.load(config_file)
    config_file.close()

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
    print(Color.GREEN + Config["messages"]["success"] + Color.RESET)

def fail():
    print(Color.RED + Config["messages"]["fail"] + Color.RESET)

def done():
    print(Color.CYAN + Config["messages"]["done"] + Color.RESET)


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

# Grading Mode
mode_match = subparsers.add_parser("grade", help="Simulate grading your C code")
mode_match.add_argument("file", help="Your C file", metavar="file.c")
mode_match.add_argument("--answer", help="Correct C file", metavar="correct_code.c", required=True)

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
mode_git.add_argument("--push", "-p", action="store_true", help="Add, commit, and push files automatically, all in one command!")

parser.add_argument("--banner", action="store_true", help="Show the banner")
parser.add_argument("--note", "-n", action="store_true", help="Access your personal notes")
parser.add_argument("--clear", action="store_true", help="Clear the screen before displaying the output")
parser.add_argument("--install", action="store_true", help="Install cs")

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

# Grade mode
if args.subcommand == "grade":
    # Grade / Compare the output of a correctly programmed C file against
    # your C code, essentially grading your program.
    grading_file_1 = ".tmp-grading-file-1"
    grading_file_2 = ".tmp-grading-file-2"
    grading_output_file_1 = ".grading-output-file-1"
    grading_output_file_2 = ".grading-output-file-2"
    # shared_main_func_file = ".tmp-main-func-file.h"

    # # Find the int main() function in the attempt file, so we can copy it
    # with open(args.file, "r") as attempt_file:
    #     main_function = re.search(r'\bint main\(\) \{([\s\S]*?)\}', attempt_file.read())
        
    #     # Write the int main() function
    #     with open(shared_main_func_file, "w") as main_func_file:
    #         main_func_file.write(main_function.group(0))
    #         main_func_file.close()

    # Compile your code first
    if run_command(["cc", "-Wall", "-Wextra", "-Werror", args.file, "-o", grading_output_file_1]) == 0:
        os.system(f"./{grading_output_file_1} > {grading_file_1}")
    else:
        fail()
        sys.exit(1)

    # Compile correct code
    if run_command(["cc", "-Wall", "-Wextra", "-Werror", args.answer, "-o", grading_output_file_2]) == 0:
        os.system(f"./{grading_output_file_2} > {grading_file_2}")
    else:
        fail()
        sys.exit(1)

    # Compare both .tmp-grading-file-1 and .tmp-grading-file-2
    if md5sum(open(grading_file_1, "rb").read()) == md5sum(open(grading_file_2, "rb").read()):
        ok()
    else:
        fail()
    
    # Cleanup
    os.remove(grading_file_1)
    os.remove(grading_file_2)
    os.remove(grading_output_file_1)
    os.remove(grading_output_file_2)

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
    if args.push:
        # Funny joke to "save the game"
        run_command(["git", "add", "--all"], {"status_code": 0})
        run_command(["git", "commit", "-m", "CS Automatic Push (" + str(timestamp()) + ")"], {"status_code": 0})
        run_command(["git", "push"], {"status_code": 0})
    
    if args.commit:
        run_command(["git", "add", "--all"], {"status_code": 0})
        run_command(["git", "commit", "-m", "CS Automatic Push (" + str(timestamp()) + ")"], {"status_code": 0})

    if args.log:
        os.system("git log --stat")