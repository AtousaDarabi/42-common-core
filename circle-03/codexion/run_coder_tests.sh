#!/bin/sh
# usage (from the coders/ folder): sh tests/run_coder_tests.sh ./test_coder.out
# args of run: n burnout compile debug refactor ncompiles cooldown sched run_ms
BIN=${1:-./test_coder.out}
LOG=$(mktemp)
fail=0

run()
{
	echo "== $*"
	timeout 20 "$BIN" "$@" > "$LOG" || { echo "  FAIL: crash/hang"; fail=1; return; }
	sh ./check_log.sh "$1" "$3" "$7" < "$LOG" || { echo "  FAIL"; fail=1; }
}

run 1 100000 50 50 50 1 10 fifo 500
run 2 100000 50 50 50 1 10 fifo 1000
run 3 100000 50 50 50 1 10 fifo 1000
run 5 100000 50 50 50 1 10 fifo 1000
run 5 100000 50 50 50 1 10 edf 1000
run 4 100000 30 30 30 1 0 fifo 1000
run 50 100000 20 20 20 1 5 edf 1500
run 200 100000 20 20 20 1 5 fifo 2000
rm -f "$LOG"
[ $fail -eq 0 ] && echo "ALL OK" || echo "SOME TESTS FAILED"
exit $fail
