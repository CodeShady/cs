#     ___                                          __      
#    /   |  _________ ___  ______ ___  ___  ____  / /______
#   / /| | / ___/ __ `/ / / / __ `__ \/ _ \/ __ \/ __/ ___/
#  / ___ |/ /  / /_/ / /_/ / / / / / /  __/ / / / /_(__  ) 
# /_/  |_/_/   \__, /\__,_/_/ /_/ /_/\___/_/ /_/\__/____/  
#             /____/                                       
                                                                                
import argparse

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

# Preservation mode
mode_preserve = subparsers.add_parser("preserve", help="Select a file to preserve")
mode_preserve.add_argument("file", help="Choose a file to preserve for later", metavar="FILE")

# Restore a preserved file mode
mode_preserve = subparsers.add_parser("history", help="View the history of a preserved file")
mode_preserve.add_argument("file", help="Choose a file to restore", metavar="FILE")
mode_preserve.add_argument("--latest", "-l", action="store_true", help="View the latest version of the preserved file")
mode_preserve.add_argument("--hash", "-s", help="View a specific version of a preserved file by selecting a hash", metavar="HASH")
mode_preserve.add_argument("--pretty", "-p", action="store_true", help="Pretty-print the output (with color)")

# Grading Mode
mode_match = subparsers.add_parser("grade", help="Simulate grading your C code")
mode_match.add_argument("file", help="Your C file", metavar="mycode.c")
mode_match.add_argument("--answer", "-a", help="Correct C file", metavar="correct_code.c", required=True)
mode_match.add_argument("--diff", "-d", action="store_true", help="Show the difference between your output and the correct output")

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

parser.add_argument("--nobanner", action="store_true", help="Hide the banner")
parser.add_argument("--note", "-n", action="store_true", help="Access your personal notes")
parser.add_argument("--clear", action="store_true", help="Clear the screen before displaying the output")
parser.add_argument("--install", action="store_true", help="Install cs")

# Parse arguments
args = parser.parse_args()