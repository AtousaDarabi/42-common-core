#!/bin/sh
# usage: check_log.sh <n_coders> <time_to_compile> <dongle_cooldown> < log
# Checks: per-coder order, time never goes backwards, neighbours never
# compile at the same time, and the cooldown between neighbours.
awk -v n="$1" -v comp="$2" -v cd="$3" '
function err(m) { errors++; if (errors < 6) print "  ERROR: " m }
function abs(x) { return x < 0 ? -x : x }
{
	t = $1; id = $2; msg = $0
	sub(/^[0-9]+ [0-9]+ /, "", msg)
	lines++
	if (t < last_t) err("time goes backwards: " $0)
	last_t = t
	st = state[id] + 0
	if (msg == "has taken a dongle" && st == 0) state[id] = 1
	else if (msg == "has taken a dongle" && st == 1) state[id] = 2
	else if (msg == "is compiling" && st == 2) {
		state[id] = 3; k = ++nc[id]; start[id, k] = t }
	else if (msg == "is debugging" && st == 3) state[id] = 4
	else if (msg == "is refactoring" && st == 4) state[id] = 0
	else err("bad sequence for coder " id ": " $0)
}
END {
	if (n == 1) {
		if (lines != 1) err("single coder: expected 1 line, got " lines)
	} else {
		for (a = 1; a <= n; a++) {
			b = a % n + 1
			for (i = 1; i <= nc[a]; i++)
				for (j = 1; j <= nc[b]; j++)
					if (abs(start[a, i] - start[b, j]) < comp + cd - 5)
						err("neighbours " a " and " b " too close")
		}
	}
	for (a = 1; a <= n; a++) total += nc[a]
	if (errors > 0) exit 1
	printf("  log OK: %d lines, %d compiles\n", lines, total)
}'
