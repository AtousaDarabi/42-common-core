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