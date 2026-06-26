# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jukohler <jukohler@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/06/12 18:40:00 by jukohler          #+#    #+#              #
#    Updated: 2026/06/25 16:19:46 by jukohler         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME        := libft.a

CC          := cc
CFLAGS      := -Wall -Wextra -Werror -I.

SRCS        := ft_bzero.c \
               ft_memset.c \
               ft_putstr_fd.c \
               ft_atoi.c \
			   ft_strcmp.c

OBJS        := $(SRCS:.c=.o)

all: $(NAME)

$(NAME): $(OBJS)
	@ar rcs $(NAME) $(OBJS)

%.o: %.c libft.h
	@$(CC) $(CFLAGS) -c $< -o $@

clean:
	@rm -f $(OBJS)

fclean: clean
	@rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
