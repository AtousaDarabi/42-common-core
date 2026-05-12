*This project has been created as part of the 42 curriculum by adarabi*

# ft_printf #

## Description ##
`ft_printf` is a C library that reimplements the standard `printf()` function from libc.
The goal is to produce a function with the following prototype:
```
int ft_printf(const char *format, ...);
```
It handles a variable number of arguments using C's variadic function mechanism `stdarg.h` and supports the following format conversions:

| Specifier  | Output                           |
| ---------- |:--------------------------------:|
| %c         | Single character                 |
| %s         | String                           |
| %p         | Pointer address in hexadecimal   |
| %d         | Decimal integer (base 10)        |
| %i         | Integer (base 10)                |
| %u         | Unsigned decimal integer         |
| %x         | Hexadecimal (base 16, lowercase) |
| %X         | Hexadecimal (base 16, uppercase) |
| %%         | Literal percent sign             |   

## Instructions ##
### Compilation ###
Clone the repository and run:
`make`
This produces `libftprintf.a` at the root of the repository.
#### Makefile rules ####
| Rule                  | Effect                                    |
| --------------------- |:-----------------------------------------:|
| `make` / `make all`   | Compile the library                       |
| `make clean`          | Remove object files                       |
| `make fclean`         | Remove object files and `libftprintf.a`   |
| `make re`             | Full recompilation                        |

## Resources ##
* C `printf` man page
* C `stdarg.h` / variadic functions — cppreference
* 42 Norm

## algorithm and data structure ##

### Main algorithm (`ft_printf`)

It's a simple **single-pass string parser**. You iterate character by character over the format string. When you hit a `%`, you look at the next character and dispatch to the appropriate handler, then skip ahead by one extra. Otherwise you write the character directly. This is the same strategy the real `printf` uses internally — no buffering, no lookahead beyond one character.

### Conversion handlers (`ft_helper.c`)

Each handler uses a specific sub-algorithm:

- **`ft_print_number` / `ft_print_hex_helper`** — recursive digit extraction. You divide by the base repeatedly until you reach a single digit, then write on the way back up the call stack. This naturally produces digits in the correct left-to-right order without needing a temporary string buffer or reversing.
- **`ft_print_pointer`** — a thin wrapper that casts `void *` to `unsigned long`, handles the `NULL` edge case (`(nil)`), prepends `0x`, then delegates to the hex printer.

### Data structures used

There are no complex data structures in this project — and that's worth saying explicitly. The key one is **`va_list`** from `<stdarg.h>`, which is an opaque type that the compiler uses to walk variadic arguments on the stack. You advance through it with `va_arg`, and the type you pass to `va_arg` must match what the caller actually passed — that's why `%c` uses `int` (C promotes `char` to `int` in variadic calls) and `%p` uses `void *`.

### Design choices

The recursive approach for number printing avoids `malloc` entirely, keeping the code simple and leak-free. The tradeoff is stack depth proportional to the number of digits (at most ~20 for a 64-bit number), which is acceptable. An iterative approach would need a local char array and a reverse step — more code for no real benefit at this scale.