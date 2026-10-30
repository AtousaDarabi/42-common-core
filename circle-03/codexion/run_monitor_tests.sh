#!/bin/sh
# usage (from the coders/ folder): sh tests/run_monitor_tests.sh ./codexion
# args of the program: n burnout compile debug refactor ncompiles cooldown sched
BIN=${1:-./codexion}
LOG=$(mktemp)
fail=0

bad() { echo "  FAIL: $1"; fail=1; }

# the simulation must end by itself, without any burnout
success()
{
	echo "== should finish OK: $*"
	timeout 30 "$BIN" "$@" > "$LOG" || { bad "crash/hang/exit code"; return; }
	grep -q "burned out" "$LOG" && bad "unexpected burnout"
	sh tests/check_log.sh "$1" "$3" "$7" < "$LOG" || bad "log check"
	awk -v n="$1" -v req="$6" '/is compiling/ { c[$2]++ }
		END { for (i = 1; i <= n; i++) if (c[i] < req) exit 1 }' "$LOG" \
		|| bad "a coder compiled fewer than $6 times"
}

# a coder must burn out; exactly one message, last line, on time
burnout()
{
	echo "== should burn out: $*"
	timeout 30 "$BIN" "$@" > "$LOG" || { bad "crash/hang/exit code"; return; }
	sh tests/check_end.sh "$2" < "$LOG" || bad "burnout check"
}

refuse()
{
	echo "== should be rejected: $*"
	"$BIN" "$@" > /dev/null 2>&1 && bad "accepted invalid input"
}

echo "== 1 coder: 2 lines, burnout at ~800 ms"
timeout 5 "$BIN" 1 800 200 200 200 3 50 fifo > "$LOG"
[ "$(wc -l < "$LOG")" -eq 2 ] || bad "expected exactly 2 lines"
sh tests/check_end.sh 800 < "$LOG" || bad "burnout check"

success 4 800 200 200 200 3 50 fifo
success 5 800 100 100 100 5 10 fifo
success 5 800 100 100 100 5 10 edf
success 31 800 20 20 20 4 5 edf
success 200 800 20 20 20 3 5 fifo
burnout 4 310 200 200 200 5 50 fifo
burnout 3 250 200 100 100 5 10 edf
burnout 5 300 150 100 100 5 20 fifo
refuse 5 800 200
refuse abc 800 200 200 200 3 50 fifo
refuse 5 -800 200 200 200 3 50 fifo
refuse 5 800 200 200 200 3.5 50 fifo
refuse 5 800 200 200 200 3 50 lifo

rm -f "$LOG"
[ $fail -eq 0 ] && echo "ALL OK" || echo "SOME TESTS FAILED"
exit $fail
