NAME = libftprintf.a
FLAGS = -Wall -Wextra -Werror
CC = cc
SRCS = ft_printf.c

OBJS = $(SRCS: .c=.o)

all = $(NAME)
$(NAME) = $(OBJS)
	ar src $(NAME) $(OBJS)
%.o:%.c
	$(CC) $(FLAGS) -c $< -o $@

clean:
	rm -f *.o $(OBJS) 

fclean:
	rm -f $(NAME)

re: fclean all

so:
	$(CC) -nostartfiles -fPIC $(CFLAGS) $(SRCS)
	gcc -nostartfiles -shared -o libft.so $(OBJS)

.PHONY: all clean fclean re
