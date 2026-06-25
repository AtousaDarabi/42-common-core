*This project has been created as part of the 42 curriculum by jukohler, adarabi.*

---

# push_swap

## Description

**push_swap** is a sorting algorithm project from the 42 curriculum. The goal is to sort a list of integers stored in a stack using a strictly limited set of operations and the **fewest moves possible**.

You are given two stacks (`a` and `b`) and a set of 11 operations to manipulate them. Stack `a` starts with all the unsorted integers; stack `b` starts empty. The program must output the shortest sequence of operations that leaves stack `a` sorted in ascending order with the smallest value on top.

To handle a wide range of input sizes and disorder levels efficiently, the program implements **four distinct sorting strategies** that are selected automatically (or manually via flags) based on how disordered the input is.

---

## Stack Operations

| Operation | Effect |
|-----------|--------|
| `sa` | Swap the top two elements of stack a |
| `sb` | Swap the top two elements of stack b |
| `ss` | `sa` and `sb` simultaneously |
| `pa` | Push top of b onto a |
| `pb` | Push top of a onto b |
| `ra` | Rotate a upward (top becomes bottom) |
| `rb` | Rotate b upward (top becomes bottom) |
| `rr` | `ra` and `rb` simultaneously |
| `rra` | Reverse rotate a (bottom becomes top) |
| `rrb` | Reverse rotate b (bottom becomes top) |
| `rrr` | `rra` and `rrb` simultaneously |

---

## Algorithms

The program selects a strategy based on the **disorder** of the input — a value between `0.0` (already sorted) and `1.0` (worst possible order), computed as the ratio of inverted pairs to total pairs before any move is made.

### 1. Simple — O(n²) · `--simple`

An **insertion sort** adaptation. Repeatedly finds the minimum remaining element in stack `a` and rotates it into its correct position. Works well for very small inputs or nearly-sorted data, but scales poorly.

**Used when:** disorder < 0.2 (adaptive mode)

### 2. Medium — O(n√n) · `--medium`

A **chunk-based sorting** strategy. The value range is divided into approximately √n chunks. Elements are pushed to stack `b` chunk by chunk (largest chunks first), then pulled back to `a` in order. The number of rotations per element is minimized by always choosing the nearest target.

**Used when:** 0.2 ≤ disorder < 0.5 (adaptive mode)

### 3. Complex — O(n log n) · `--complex`

A **radix sort** adaptation using binary (LSD). Numbers are first mapped to normalized indices (0 to n−1) to allow bitwise comparison. Each bit position is processed in a pass: elements whose current bit is `0` stay in `a`, elements whose bit is `1` are pushed to `b`, then everything is merged back. Requires log₂(n) passes.

**Used when:** disorder ≥ 0.5 (adaptive mode)

### 4. Adaptive — `--adaptive` *(default)*

Measures the disorder of the initial stack, then dispatches to one of the three algorithms above based on the thresholds described. This is the default behavior when no flag is provided.

**Threshold rationale:**
- Below `0.2`: the list is nearly sorted — only a few elements are out of place — so the simple O(n²) insertion approach generates very few operations in practice.
- Between `0.2` and `0.5`: moderate disorder benefits from chunk-based grouping, which avoids the full overhead of log passes while doing much better than naïve insertion.
- Above `0.5`: high disorder means many elements are far from their targets; radix sort's predictable O(n log n) pass structure outperforms both other methods.

**Space complexity (all strategies):** O(n) — the two stacks together always hold all n elements; no additional heap allocation grows with n beyond the initial stack storage.

---

## Benchmark Targets

| Input size | Pass (minimum) | Good | Excellent |
|------------|----------------|------|-----------|
| 100 numbers | < 2 000 ops | < 1 500 ops | < 700 ops |
| 500 numbers | < 12 000 ops | < 8 000 ops | < 5 500 ops |

---

## Instructions

### Compilation

```bash
make          # builds push_swap
make bonus    # also builds checker
make clean    # removes object files
make fclean   # removes objects + binaries
make re       # fclean + all
```

### Usage

```bash
# Default (adaptive strategy)
./push_swap 4 67 3 87 23

# Force a specific strategy
./push_swap --simple   5 4 3 2 1
./push_swap --medium   5 4 3 2 1
./push_swap --complex  5 4 3 2 1
./push_swap --adaptive 5 4 3 2 1

# Count operations
ARG="4 67 3 87 23"; ./push_swap --adaptive $ARG | wc -l

# Verify correctness with checker
ARG="4 67 3 87 23"; ./push_swap --complex $ARG | ./checker $ARG

# Benchmark mode (outputs metrics to stderr)
./push_swap --bench --adaptive 4 67 3 87 23

# Large input test
shuf -i 0-9999 -n 500 > args.txt
./push_swap $(cat args.txt) | wc -l
```

### Error handling

The program prints `Error` to stderr and exits on:
- Non-integer arguments
- Integers outside the `int` range
- Duplicate values

```bash
./push_swap --adaptive 0 one 2 3   # → Error
./push_swap --simple 3 2 3         # → Error
```

### Checker (bonus)

```bash
./checker 3 2 1 0
# reads operations from stdin, prints OK or KO
```

### Test cases

####
```bash
valgrind --leak-check=full --show-leak-kinds=all ./push_swap 4 67 3 1 89
```

#### Medium inputs (5 numbers)
```bash
ARG="1 5 2 4 3"; ./push_swap $ARG | ./checker_linux $ARG
```

#### Benchmark Mode and Disorder Calculation
```bash
./push_swap --bench --simple 5 4 3 2 1 2>/dev/null
```
```bash
./push_swap --bench --simple 5 4 3 2 1 2>bench.txt >/dev/null && cat bench.txt
```

####  Large inputs (100 numbers)
```bash
NUMS=$(shuf -i 1-500 -n 100 | tr '\n' ' ')
./push_swap --bench $NUMS | grep -E "disorder|total_ops"
```

#### Strategy flags testing
```bash
NUMS=$(shuf -i 1-200 -n 50 | tr '\n' ' ')
echo "Input: $NUMS"
echo ""

for FLAG in --simple --medium --complex --adaptive; do
    OPS=$(./push_swap $FLAG $NUMS | tee /tmp/ops.txt | wc -l)
    RESULT=$(cat /tmp/ops.txt | ./checker_linux $NUMS)
    echo "$FLAG: $OPS ops → $RESULT"
done
```

#### Very large inputs (500 numbers)
```bash
for i in 1 2; do
    echo "=== Run $i ==="
    NUMS=$(shuf -i 1-1000 -n 500 | tr '\n' ' ')
    OPS=$(./push_swap $NUMS | tee /tmp/ops.txt | wc -l)
    RESULT=$(cat /tmp/ops.txt | ./checker_linux $NUMS)
    echo "ops: $OPS → $RESULT"
done
```

---

## Contributions

| Login | Name | Contributions |
|-------|------|---------------|
| **jukohler** | Justin Kohler | Project setup and Makefile · Libft integration (ft_atoi, ft_bzero, ft_memset, ft_putsr_fd, ft_strcmp, and supporting libft functions) · Stack operation primitives (`sa`, `sb`, `ss` — `operation_one.c`) · push_swap header (`push_swap.h`) · ft_printf integration . Simple and medium strategy logic checker_bonus.h . checker_bonus.c (`read_line, run_checker` functions) |
| **adarabi** | Atoussa Darabi | Sorting algorithms and complex and adaptive strategy logic · Utility functions (`utils`) · Project structure refactoring (Makefile removal/restructure) · Adaptive dispatcher and disorder metric · Algorithm testing and validation . README . checker_bonus.c (`main, apply_op` functions) |

---

## Resources

### Algorithm & sorting references
- [Sorting algorithms visualizer](https://visualgo.net/en/sorting) — visual walkthrough of classical sorts
- [Radix sort explained](https://en.wikipedia.org/wiki/Radix_sort) — LSD/MSD approaches
- [Big-O cheat sheet](https://www.bigocheatsheet.com/) — complexity quick reference
- [push_swap medium tutorial](https://medium.com/@jamierobertdawson/push-swap-the-least-amount-of-moves-with-twepascal
o-stacks-d1e76a71789a) — chunk strategy walkthrough
- Knuth, D. E. — *The Art of Computer Programming, Vol. 3: Sorting and Searching*

### 42 tooling
- [42 Norm](https://github.com/42School/norminette) — norminette linter

### AI usage
AI was used during this project for:
- **Explaining algorithm concepts** — understanding radix sort bit manipulation and chunk-based partitioning strategies.
- **Debugging assistance** — identifying off-by-one errors in rotate/reverse-rotate logic.
