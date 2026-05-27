*This project has been created as part of the 42 curriculum by adarabi.*

# Description

`get_next_line` is a C programming project.

The goal of the project is to create a function that reads and returns one line at a time from a file descriptor. The function must work efficiently with different buffer sizes and handle multiple calls correctly while managing memory safely.

The project focuses on:

- File descriptor manipulation
- Dynamic memory allocation
- Static variables
- Efficient string handling
- Buffer management
- Memory leak prevention

The mandatory function prototype is:

```c
char	*get_next_line(int fd);
```

Each call to `get_next_line()` returns:
- the next line from the file descriptor
- including the newline character (`\n`) if it exists
- or `NULL` when the end of file is reached or an error occurs

**Algorithm**

The function uses a static array of pointers `str[4096]` — one slot per possible file descriptor. Between calls, any unprocessed bytes read from the fd are kept in `str[fd]`.

Each call works in three steps:
1. ***Read***: fill `str[fd]` by reading BUFFER_SIZE bytes at a time into a temporary buffer, joining each chunk onto `str[fd]`, stopping as soon as a `\n` is found in the buffer or EOF is reached.
2. ***Extract***: scan `str[fd]` up to the first `\n` (or end of string), copy that as the return value.
3. ***Trim***: store whatever comes after the `\n` back into `str[fd]` for the next call. If nothing remains, set `str[fd]` to NULL.

This approach was chosen because it reads as little as possible per call, avoids re-reading already-buffered data, and handles any BUFFER_SIZE correctly without changing logic.


# Instructions

**Compilation**

Compile with:

```bash
cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 get_next_line.c get_next_line_utils.c main.c
```

You can replace `42` with any buffer size:

```bash
-D BUFFER_SIZE=1
```

or:

```bash
-D BUFFER_SIZE=1000
```

**Usage**

Example:

```c
#include <fcntl.h>
#include <stdio.h>
#include "get_next_line.h"

int	main(void)
{
	int		fd;
	char	*line;

	fd = open("example.txt", O_RDONLY);
	if (fd < 0)
		return (1);

	while ((line = get_next_line(fd)) != NULL)
	{
		printf("%s", line);
		free(line);
	}

	close(fd);
	return (0);
}
```

**Memory Leak Check**

Using Valgrind:

```bash
valgrind --leak-check=full --show-leak-kinds=all ./a.out
```

Expected result:

```txt
All heap blocks were freed -- no leaks are possible
```

# Resources

**Official Documentation**
- C Standard Library
- `read()` man page
- `malloc()` man page
- `free()` man page
- `open()` man page


**AI Assistance**
Artificial Intelligence tools were used during the development of this project as supportive learning and debugging resources.
AI assistance was mainly used for:
- Understanding the project requirements and expected behavior
- Clarifying concepts related to:
- Debugging segmentation faults and timeout issues
- Identifying memory leaks and improving memory safety

**Testing Tools**

```bash
norminette
```

```bash
paco
```

```bash
paco --strict
```

```bash
valgrind --leak-check=full ./a.out
```