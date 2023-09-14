#  ▄████▄    ██████ 
# ▒██▀ ▀█  ▒██    ▒ 
# ▒▓█    ▄ ░ ▓██▄   
# ▒▓▓▄ ▄██▒  ▒   ██▒
# ▒ ▓███▀ ░▒██████▒▒ by ftp
# ░ ░▒ ▒  ░▒ ▒▓▒ ▒ ░
#   ░  ▒   ░ ░▒  ░ ░
# ░        ░  ░  ░  
# ░ ░            ░  
# ░ 
import sys,os,subprocess
import datetime
import argparse
import hashlib
import re
import json
import uuid

# Local imports
from lib.colors import *
from lib.args import *

# ==== Variables ====

# Configuration
Config = {}

# Get current path
data_directory  = os.path.join(os.path.expanduser("~"), "Documents", "csdata")
config_file     = os.path.join(data_directory, "config.json")
notes_file      = os.path.join(data_directory, "nots.txt")
preservation_directory = os.path.join(data_directory, "preserved")

# ==== FUNCTIONS ====
def ok():
    print(Color.GREEN + Config["messages"]["success"] + Color.RESET)

def fail():
    print(Color.RED + Config["messages"]["fail"] + Color.RESET)

def done():
    print(Color.CYAN + Config["messages"]["done"] + Color.RESET)

# Return true/false if this is or isn't a file
def is_file(path):
    # Check if the path exists
    if not os.path.exists(path):
        return False
    
    # Check if the path is a file (not a directory)
    return os.path.isfile(path)

# Write configuration function
def write_config():
    # This function takes the modified Config{} variable and writes it to the configuration file.
    with open(config_file, "w") as json_file:
        json.dump(Config, json_file)
        json_file.close()

def create_directory(directory_name):
    # This function checks to make sure a directory exists
    if not os.path.exists(directory_name):
        # Create a new dir if it doesn't exist already
        os.makedirs(directory_name)

# Generate random "Linux safe" filenames with custom extensions
# + hidden file ability
def random_filename_with_extension(extension=".c", hidden=False):
    unique_id = uuid.uuid4()
    prefix = ""
    if hidden:
        prefix = "."
    filename = prefix + str(unique_id) + extension
    return filename

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

# ==== Main ====

# Ensure required directories exist
create_directory(data_directory)
create_directory(preservation_directory)

if not os.path.exists(config_file):
    Config = {
        "USER": "user",
        "GROUP": "",
        "EMAIL": "user@student.42.fr",
        "NOTES_PATH": notes_file,
        "messages": {
            "success": "✅ OK!",
            "fail": "🟥 FAIL",
            "done": "👍 DONE"
        },
        "preserved": []
    }
    # Write the default json
    write_config()

# Load configuration from config.json file because it already exists
with open(config_file, "r") as config_data_file:
    Config = json.load(config_data_file)
    config_data_file.close()

# Clear the screen
if args.clear:
    os.system("clear||cls")

# Check if we should hide the banner
if not args.nobanner:
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
    grading_file_1 = random_filename_with_extension(extension=".bin", hidden=True)
    grading_file_2 = random_filename_with_extension(extension=".bin", hidden=True)
    grading_output_file_1 = random_filename_with_extension(extension=".out", hidden=True)
    grading_output_file_2 = random_filename_with_extension(extension=".out", hidden=True)
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


# Preserve subcommand
if args.subcommand == "preserve":
    # Preserve this file
    if is_file(args.file):

        # Create a new preservation filename
        output_filename = random_filename_with_extension(extension="") + "-" + args.file
        output_md5sum   = md5sum(open(args.file, "rb").read())

        # Ensure this exact file (with matching md5sum) hasn't been saved already (duplicate entry)
        for entry in Config["preserved"]:
            if entry["hash"] == output_md5sum:
                # This file was already preserved! Exit!
                ok()
                sys.exit(0)
        
        # Save this file to the database
        Config["preserved"].append({
            "og_name": args.file,
            "file": output_filename,
            "hash": output_md5sum,
            "time": timestamp()
        })

        # Update the config file
        write_config()

        # Copy this file
        run_command(["cp", args.file, os.path.join(preservation_directory, output_filename)])

        # Return status
        ok()
    else:
        # Invalid file source
        fail()

# Restore
if args.subcommand == "restore":
    # Preserve this file
    if is_file(args.file):

        # Loop through each entry in the config file
        # (Reverse the Preserved list to ensure newest files are displayed first)
        for entry in Config["preserved"]:
            if args.view or args.latest:
                # Select file to view by hash
                # args.view should equal the start of a hash
                if not args.view:
                    args.view = "NOT SET"

                if entry["hash"].startswith(args.view) or entry["hash"] == args.view or args.latest:
                    # Open the file
                    run_command(["pygmentize", "-g", "-O", "style=colorful,linenos=1", os.path.join(preservation_directory, entry["file"])])
            else:
                # Don't do anything, just list the preserved files
                print("📄 " + entry["og_name"] + Color.GREEN + " (" + entry["time"] + ")" + Color.RESET + Color.CYAN + " [" + entry["hash"][:10] + "]" + Color.RESET)

    else:
        # Invalid file source
        fail()