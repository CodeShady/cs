# `cs` - CodeShady's 42 Tool
42 Helper Script!

## Setup

**First, ensure you have the following Python packages installed:**
```
$ pip3 install c_formatter_42
```

To start using this tool, grab the main `csverify.py` file and edit the `Config` variable in the csverify.py file to your preference. These settings are used by the program later.

```
Config  = {
    "USER":  "myusername",
    "GROUP":  "",
    "EMAIL":  "user@student.42.fr",
    "NOTES_PATH":  "/mnt/nfs/homes/user/my-notes.txt"
}
```

Next, create an alias for easy usage in your `.zshrc` or `.bashrc` depending on which shell you're using.

**(~/.zshrc)**
```
alias cs="python3 ~/path/to/csverify.py"
```
Open a new shell or run `source ~/.zshrc` to update the changes to your shell session.

## Using `cs`
Run `cs` in your terminal to get a list of cool tools you can use.
```
usage: csverify.py [-h] {...} ...

options:
  -h, --help            show this help message and exit
  --banner              Show the banner
  --note, -n            Access your personal notes
  --clear               Clear the screen before displaying the output
  ...

Sub-Commands:
  ...
```

## Guide

### 👉 C Tools

#### Help
Use the `c` mode to select "C programming mode".
```
$ cs c --help
```
#### C File Template (with 42 Header)
Create a new C program with the required 42 header.
```
$ cs c --new my_new_program.c
```
#### Compile & Run your code
Compile and run your C code with the recommended compiler flags: `-Wall -Wextra -Werror`
```
$ cs c --run my_code.c
```
#### C File Template (with 42 Header)
Compile your C code into `a.out` with the recommended compiler flags: `-Wall -Wextra -Werror`
```
$ cs c --compile my_code.c
```
#### Norminette Check
Check your code with the `norminette`
```
$ cs c --norm my_code.c
```
#### Norminette Auto Formatter
Format your C code automatically for the `norminette`
```
$ cs c --format my_code.c
```
#### Simulate Moulinette Code Grading 
If you have C code that prints the correct **output** that has successfully passed the Moulinette, use the `grade` mode to check whether the output of your code matches the correct output.

Use `--answer` followed by a C program to specify the code previously graded by the Moulinette.
```
$ cs grade my_own_code.c --answer test.c
```

### 👉 Git
#### Add, commit, push (all-in-one)
The tool below adds all changed files, commits them, and then pushes them to your git repository.
```
$ cs git --push
```
#### Just Commit
To add all changed files and commit them automatically **without pushing to your repository**, use the following:
```
$ cs git --commit
```
#### Log
Log your git history
```
$ cs git --log
```
