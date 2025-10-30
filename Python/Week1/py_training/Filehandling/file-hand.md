30/10/25



### **OS MODULE ->>> File handling /  Command args / Xml file \& REGEX in py / NUMP**





Regex in Python (short for Regular Expression) is basically a pattern-matching tool for strings. Think of it like search + filter + extractor all rolled into one messy but powerful feature.



Here’s the breakdown:



What it does: Finds or replaces specific patterns in text.



Module used: re (you have to import it).



How it works: You define a pattern (like "a\[0-9]+"), and regex scans your text for anything that fits that rule.



| Pattern | Meaning                               | Example Match                         |      |                               |

| ------- | ------------------------------------- | ------------------------------------- | ---- | ----------------------------- |

| `\\d`    | Any digit (0–9)                       | `7`                                   |      |                               |

| `\\D`    | Any non-digit                         | `A`, `#`                              |      |                               |

| `\\w`    | Any word character (A–Z, a–z, 0–9, \_) | `hello\_123`                           |      |                               |

| `\\W`    | Any non-word character                | `@`, `#`, `!`                         |      |                               |

| `\\s`    | Any whitespace (space, tab, newline)  | `" "`                                 |      |                               |

| `\\S`    | Any non-whitespace                    | `a`, `5`                              |      |                               |

| `^`     | Start of string                       | `^H` matches “Hello”                  |      |                               |

| `$`     | End of string                         | `end$` matches “the end”              |      |                               |

| `.`     | Any character except newline          | `a.c` matches “abc”, “axc”            |      |                               |

| `\*`     | 0 or more repeats                     | `go\*d` → `gd`, `good`, `goood`        |      |                               |

| `+`     | 1 or more repeats                     | `go+d` → `good`, `goood` but not `gd` |      |                               |

| `{n,m}` | Between n and m repeats               | `\\d{2,4}` → 2 to 4 digits             |      |                               |

| `\[]`    | Set of allowed chars                  | `\[A-Za-z]` → any letter               |      |                               |

| `       | `                                     | OR                                    | `cat | dog` → matches “cat” or “dog” |

| `()`    | Group                                 | `(\\d{2})-(\\d{2})` → captures “12-34”  |      |                               |













## OS MODULE->>>





The os module in Python is basically your backstage pass to the operating system. It lets Python scripts interact with the system just like a human fumbling through folders, renaming files, or checking environment variables — but without the human errors and coffee breaks.



Here’s the serious part:



Definition



os stands for Operating System.

The module provides functions to perform OS-level operations like file handling, directory management, and process control.









| Task                          | Function                  | Example                                |

| ----------------------------- | ------------------------- | -------------------------------------- |

| Get current working directory | `os.getcwd()`             | `print(os.getcwd())`                   |

| Change directory              | `os.chdir("path")`        | `os.chdir("C:/Users/Rajdeep/Desktop")` |

| List all files/folders        | `os.listdir()`            | `print(os.listdir())`                  |

| Create new folder             | `os.mkdir("folder\_name")` | Creates a new folder                   |

| Remove folder                 | `os.rmdir("folder\_name")` | Deletes an empty folder                |

| Run system command            | `os.system("command")`    | `os.system("cls")` clears console      |

| Access environment variables  | `os.environ`              | `print(os.environ\['PATH'])`            |

| Join paths correctly          | `os.path.join()`          | `os.path.join("folder", "file.txt")`   













## NUMPY--->>>>>>





What is NumPy?



NumPy (Numerical Python) is a Python library used for fast mathematical and array operations. It’s built in C (which is why it’s fast — unlike Python, which likes to nap mid-calculation).



You use it for:



Handling large datasets efficiently



Performing matrix, linear algebra, and statistical operations



Replacing slow Python loops with fast vectorized operations





numpy / arrays / 





































