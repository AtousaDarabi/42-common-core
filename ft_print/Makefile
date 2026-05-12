NAME = libftprintf.a
FLAGS = -Wall -Wextra -Werror
CC = cc
SRCS = ft_printf.c ft_helper.c

OBJS = $(SRCS:.c=.o)

all: $(NAME)
$(NAME): $(OBJS)
	make -C libft
	ar	src	$(NAME)	$(OBJS)	libft/*.o
.o: .c
	$(CC) $(FLAGS) -c $< -o $@

clean:
	rm -f $(OBJS)
	rm -f libft/*.o

fclean:
	rm -f $(NAME)
	rm -f libft/libft.a

re: fclean all
