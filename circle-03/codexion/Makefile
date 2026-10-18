NAME = codexion
CC = cc
CFLAGS = -Wall -Wextra -Werror -pthread
SRCS = main.c parse.c error.c utils.c log.c
OBJS = $(SRCS:.c=.o)
TEST_LOG = test/test-log

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

$(TEST_LOG): test/test-log.c log.c utils.c codexion.h
	$(CC) $(CFLAGS) test/test-log.c log.c utils.c -o $(TEST_LOG)

test-log: $(TEST_LOG)
	./$(TEST_LOG)

%.o: %.c codexion.h
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TEST_LOG)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re test-log
