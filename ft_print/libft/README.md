*This project has been created as part of the 42 curriculum by adarabi.*

# Description
The **Libft** project is a foundational milestone in the 42 curriculum. Its goal is to re-create a selection of functions from the standard C library (`libc`), as well as additional utility functions that will be used throughout the rest of the program. By building our own library from scratch, we gain a deep understanding of memory management, pointer manipulation, and string handling in C.

This library serves as a versatile toolkit, providing reliable implementations of essential tools that are otherwise forbidden in later projects where we are restricted to using only our own code.

# The Library
The project is divided into several parts:
**Libc Functions:** Re-implementations of standard functions like `strlen`, `memset`, `memcpy`, `atoi`, etc.
**Additional Functions:** Utility functions for string and memory manipulation not found in the standard library, such as `ft_substr`, `ft_strjoin`, and `ft_strtrim`.
**Linked Lists:** Functions used to manipulate a linked list structure (`t_list`), including `ft_lstnew`, `ft_lstadd_front`, `ft_lstadd_back`, `ft_lstsize`, `ft_lstlast`, `ft_lstdelone`, `ft_lstclear`, `ft_lstiter`, and `ft_lstmap`. These are crucial for learning dynamic data structures.

## Technical Overview
- **Language:** C
- **Compiler:** cc/gcc
- **Flags:** -Wall -Wextra -Werror
- **Memory Management:** Manual allocation via `malloc` and `free`.
- **Standards:** All code adheres to the 42 Norm.

# Instructions

## Compilation
The project includes a `Makefile` with the following rules:
- `make`: Compiles the source files and generates the `libft.a` static library.
- `make clean`: Removes the object files (`.o`).
- `make fclean`: Removes object files and the generated `libft.a`.
- `make re`: Performs a full re-compilation.

## Installation
To use this library in your projects:
1. Clone the repository.
2. Run `make` to generate `libft.a`.
3. Include the header in your C files: `#include "libft.h"`.
4. Link the library during compilation: `gcc main.c -L. -lft`.

# Resources
- [C Library Reference (CPlusPlus)](https://cplusplus.com/reference/clibrary/) - For understanding standard function behavior.
- [Core C language constructs](https://cppreference.com/c/language) - For detailed documentation on C syntax, data types, and memory models.s

## AI Usage
AI (Large Language Models) was used in this project for the following tasks:
- **Logic Debugging:** Assisting in identifying edge cases for complex string functions like `ft_strtrim` and `ft_split`.
- **Documentation:** Structural formatting of the `README.md` to comply with specific pedagogical requirements.
- **Code Optimization:** Reviewing the logic of `ft_itoa` to ensure efficient memory usage and handling of the minimum integer value (`-2147483648`).
