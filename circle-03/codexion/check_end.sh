#!/bin/sh
# usage: check_end.sh <time_to_burnout> < log
# The log must end with exactly one "burned out" line (nothing after it),
# printed at most 10 ms after the coder's deadline.
awk -v bo="$1" '
{ lines[NR] = $0 }
/is compiling/ { last[$2] = $1 }
/burned out/ { cnt++ }
END {
	if (NR == 0) { print "  ERROR: empty log"; exit 1 }
	if (cnt != 1) { print "  ERROR: expected 1 burnout line, got " cnt; exit 1 }
	split(lines[NR], f, " ")
	if (lines[NR] !~ /burned out/) {
		print "  ERROR: something printed after the burnout"; exit 1 }
	start = (f[2] in last) ? last[f[2]] : 0
	d = f[1] - (start + bo)
	printf("  coder %d burned out at %d ms (%d ms after its deadline)\n",
		f[2], f[1], d)
	if (d < -5 || d > 10) { print "  ERROR: burnout message too late/early"; exit 1 }
}'
