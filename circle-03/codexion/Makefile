NAME		= codexion
CC			= cc
CFLAGS		= -Wall -Wextra -Werror -pthread

SRC_MAIN	= main.c parse.c
SRC_LOG		= utils.c log.c
SRC_HEAP	= heap.c heap_ops.c
SRC_DONGLE	= dongle_init.c dongle_wait.c dongle.c
SRC_CODER	= coder_init.c coder_utils.c coder.c run.c setup.c
SRC_MONITOR	= monitor.c

SRCS		= $(SRC_MAIN) $(SRC_LOG) $(SRC_HEAP) $(SRC_DONGLE) \
				$(SRC_CODER) $(SRC_MONITOR)
OBJS		= $(SRCS:.c=.o)
OBJ_LOG		= $(SRC_LOG:.c=.o)
OBJ_HEAP	= $(SRC_HEAP:.c=.o)
OBJ_DONGLE	= $(SRC_DONGLE:.c=.o)
OBJ_CODER	= $(SRC_CODER:.c=.o)
OBJ_MONITOR	= $(SRC_MONITOR:.c=.o)

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

%.o: %.c codexion.h
	$(CC) $(CFLAGS) -c $< -o $@

# make test_heap / test_dongle / test_coder / test_monitor
test_heap: $(OBJ_HEAP)
	$(CC) $(CFLAGS) tests/test_heap.c $(OBJ_HEAP) -o test_heap.out
	./test_heap.out

test_dongle: $(OBJ_LOG) $(OBJ_HEAP) $(OBJ_DONGLE)
	$(CC) $(CFLAGS) tests/test_dongle.c $(OBJ_LOG) $(OBJ_HEAP) \
		$(OBJ_DONGLE) -o test_dongle.out
	./test_dongle.out

test_coder: parse.o $(OBJ_LOG) $(OBJ_HEAP) $(OBJ_DONGLE) $(OBJ_CODER) \
		$(OBJ_MONITOR)
	$(CC) $(CFLAGS) tests/test_coder.c parse.o $(OBJ_LOG) $(OBJ_HEAP) \
		$(OBJ_DONGLE) $(OBJ_CODER) $(OBJ_MONITOR) -o test_coder.out
	sh tests/run_coder_tests.sh ./test_coder.out

test_monitor: $(NAME)
	sh tests/run_monitor_tests.sh ./$(NAME)

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME) test_heap.out test_dongle.out test_coder.out

re: fclean all

.PHONY: all clean fclean re test_heap test_dongle test_coder test_monitor
