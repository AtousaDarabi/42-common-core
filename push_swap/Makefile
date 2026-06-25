# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: adarabi <adarabi@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/06/23 18:06:13 by adarabi           #+#    #+#              #
#    Updated: 2026/06/25 15:38:17 by adarabi          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


NAME        = push_swap

CC          = cc
CFLAGS      = -Wall -Wextra -Werror -I. -ILibft -Ift_printf

LIBFT_DIR   = Libft
LIBFT       = $(LIBFT_DIR)/libft.a

PRINTF_DIR  = ft_printf
PRINTF      = $(PRINTF_DIR)/libftprintf.a

SRCS        = push_swap.c \
               flags.c \
               parser.c \
               utils.c \
               operations.c \
               instructions.c \
               sort.c \
               sort_complex.c \
               bench.c

OBJS        = $(SRCS:.c=.o)

BONUS_NAME  = checker

BONUS_SRCS  = checker_bonus.c \
               flags.c \
               parser.c \
               utils.c \
               operations.c

BONUS_OBJS  = $(BONUS_SRCS:.c=.o)

all: $(LIBFT) $(PRINTF) $(NAME)

bonus: $(LIBFT) $(PRINTF) $(BONUS_OBJS)
	@$(CC) $(CFLAGS) $(BONUS_OBJS) $(LIBFT) $(PRINTF) -o $(BONUS_NAME)

$(LIBFT):
	@make -C $(LIBFT_DIR)

$(PRINTF): $(PRINTF_DIR)/ft_printf.c $(PRINTF_DIR)/ft_printf.h
	@$(CC) $(CFLAGS) -c $(PRINTF_DIR)/ft_printf.c -o $(PRINTF_DIR)/ft_printf.o
	@ar rcs $(PRINTF) $(PRINTF_DIR)/ft_printf.o

$(NAME): $(OBJS) $(LIBFT) $(PRINTF)
	@$(CC) $(CFLAGS) $(OBJS) $(LIBFT) $(PRINTF) -o $(NAME)

%.o: %.c push_swap.h
	@$(CC) $(CFLAGS) -c $< -o $@

clean:
	@make clean -C $(LIBFT_DIR)
	@rm -f $(PRINTF_DIR)/*.o $(OBJS)

fclean: clean
	@make fclean -C $(LIBFT_DIR)
	@rm -f $(PRINTF) $(NAME) $(BONUS_NAME) $(BONUS_OBJS)

re: fclean all

.PHONY: all bonus clean fclean re
