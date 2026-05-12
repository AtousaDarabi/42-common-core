NAME = libftprintf.a
FLAGS = -Wall -Wextra -Werror
CC = cc
SRCS = ft_printf.c ft_helper.c

OBJS = $(SRCS:.c=.o)

all: $(NAME)
$(NAME): $(OBJS)
	ar	src	$(NAME)	$(OBJS)
%.o: %.c
	$(CC) $(FLAGS) -c $< -o $@

clean:
	rm -f *.o $(OBJS) 

fclean:
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
