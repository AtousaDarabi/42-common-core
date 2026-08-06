PYTHON = python3
VENV = .venv
VENV_PYTHON = $(VENV)/bin/python
MAIN = a_maze_ing.py
CONFIG = config.txt

MLX_DIR = mlx
MLX_LIB = $(MLX_DIR)/libmlx.so
MLX_SRC = mlx_init.c mlx_new_window.c mlx_pixel_put.c mlx_loop.c \
	mlx_mouse_hook.c mlx_key_hook.c mlx_expose_hook.c mlx_loop_hook.c \
	mlx_int_anti_resize_win.c mlx_int_do_nothing.c \
	mlx_int_wait_first_expose.c mlx_int_get_visual.c \
	mlx_flush_event.c mlx_string_put.c mlx_set_font.c \
	mlx_new_image.c mlx_get_data_addr.c \
	mlx_put_image_to_window.c mlx_get_color_value.c mlx_clear_window.c \
	mlx_xpm.c mlx_int_str_to_wordtab.c mlx_destroy_window.c \
	mlx_int_param_event.c mlx_int_set_win_event_mask.c mlx_hook.c \
	mlx_rgb.c mlx_destroy_image.c mlx_mouse.c mlx_screen_size.c \
	mlx_destroy_display.c

.PHONY: venv install run debug clean lint lint-strict build archive mlx

venv:
	$(PYTHON) -m venv $(VENV)

# Compiles the vendored MiniLibX C sources (mlx/) into a shared library so
# the ctypes bindings in src/mlx_bindings.py can load it (needed for the
# MLX graphical display; the ASCII display works without this). Requires
# gcc, make, and X11 dev headers (xorg, libxext-dev, libbsd-dev) -- see
# mlx/README.md.
mlx: $(MLX_LIB)

$(MLX_LIB):
	cd $(MLX_DIR) && gcc -O2 -fPIC -c $(MLX_SRC) && \
		gcc -shared -o libmlx.so *.o -lX11 -lXext -lm && rm -f *.o

install: venv
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install flake8 mypy build
	@$(MAKE) mlx || echo "Warning: could not build MiniLibX ($(MLX_DIR)/); the graphical (MLX) display will be unavailable, but the ASCII display still works. See $(MLX_DIR)/README.md for required system packages."

run: venv
	$(VENV_PYTHON) $(MAIN) $(CONFIG)

debug: venv
	$(VENV_PYTHON) -m pdb $(MAIN) $(CONFIG)

lint: install
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: install
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --strict

# Builds the reusable mazegen package (wheel + sdist archives) and copies
# them to the repo root, as required by the subject.
build: install
	$(VENV_PYTHON) -m build
	cp dist/mazegen-*.whl dist/mazegen-*.tar.gz .

archive: build

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -f $(MLX_DIR)/*.o $(MLX_LIB)
	rm -rf build dist $(VENV)
