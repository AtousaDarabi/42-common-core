*This project has been created as part of the 42 curriculum by adarabi.*

# Codexion

## Description

Codexion is a C concurrency simulation inspired by the dining philosophers
problem. Each coder is represented by a POSIX thread and needs the two adjacent
USB dongles to compile. After compiling, a coder debugs and refactors before
requesting the dongles again. The simulation ends when a coder burns out or all
coders reach the requested number of compiles.

The dongle scheduler supports FIFO (request arrival order) and EDF (earliest
burnout deadline). A cooldown period makes each dongle unavailable immediately
after it is released.

## Instructions

Build with the required compiler flags:

```sh
make
```

Run:

```sh
./codexion number_of_coders time_to_burnout time_to_compile \
  time_to_debug time_to_refactor number_of_compiles_required \
  dongle_cooldown fifo|edf
```

All durations are positive integer milliseconds. The coder count must be
positive, the compile count must be a non-negative integer, and the scheduler
must be exactly `fifo` or `edf`.

For example:

```sh
./codexion 4 800 120 100 100 3 10 fifo
```

The program prints timestamped coder states to standard output. Invalid
arguments and runtime initialization failures are reported to standard error.
Use `make clean` to remove object files and `make fclean` to remove all build
artifacts.

## Blocking cases handled

- **Deadlock and Coffman's conditions:** A coder requests both adjacent
  dongles as one atomic grant. It never holds one dongle while waiting for the
  other, removing hold-and-wait and circular-wait from the resource protocol.
- **Duplicate ownership:** The central resource mutex serializes grants, and
  each dongle's own mutex protects its held and cooldown state.
- **Starvation and arbitration:** Waiting requests are stored in a binary heap.
  The dispatcher considers eligible requests in FIFO order or by EDF deadline;
  an unavailable pair does not prevent an unrelated eligible pair from being
  granted.
- **Cooldown:** Release records a per-dongle availability time. Waiting threads
  sleep on a condition variable until a release or the relevant cooldown
  deadline.
- **Burnout:** A dedicated monitor checks each coder's deadline at 1 ms
  intervals and stops the simulation as soon as a deadline is reached.
- **Log interleaving:** A logging mutex protects each complete output line.

## Thread synchronization mechanisms

Each coder is a POSIX thread. A separate monitor thread detects burnout and
checks whether all coders have completed the required number of compiles.
`pthread_mutex_t` protects shared simulation state, each dongle's ownership and
cooldown fields, and output. `pthread_cond_t` wakes coders when resources are
released, cooldowns expire, or the simulation stops. There is no separate
custom event object: condition-variable broadcasts serve as the notification
mechanism.

For example, the dispatcher locks the simulation state before examining the
heap, then locks both dongle mutexes in index order before changing ownership.
This prevents two coders from being granted the same dongle. Coder phase
changes, compile counters, and monitor decisions are read or changed while the
simulation mutex is held, so the monitor and worker threads communicate
without unsynchronized shared-state access. The logging mutex is always
acquired only for output, keeping complete lines intact.

## Resources

- `man 7 pthreads` and the POSIX thread API documentation.
- `man 3 pthread_mutex_lock`, `man 3 pthread_cond_wait`, and
  `man 3 pthread_cond_timedwait`.
- The dining philosophers problem and deadlock avoidance through atomic
  resource allocation.
- AI was used to draft the initial implementation and this documentation,
  including argument validation, heap-based scheduling, synchronization, and
  monitoring. The code and its behavior must be reviewed and understood by the
  student, then validated with tests and peer review before evaluation.