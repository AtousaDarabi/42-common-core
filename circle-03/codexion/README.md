 *This project has been created as part of the 42 curriculum by adarabi.*

 # Codexion: Full Project Explanation

## 1. The Big Idea

This project is a modified version of the famous **Dining Philosophers** problem:

| Dining Philosophers | Codexion |
|---|---|
| Philosopher | Coder |
| Fork | Dongle (USB dongle) |
| Eating | Compiling |
| Sleeping / thinking | Debugging and refactoring |
| Starving to death | Burnout |

You must write a C program that runs several threads at the same time. Each thread is one coder, and all of them compete for limited resources (the dongles). The goal is that **no coder burns out**, and that no deadlock or race condition occurs.

---

## 2. The Scenario

- `n` coders sit around a circular table, and there are `n` dongles on the table: one between each pair of neighbouring coders.
- Each coder repeats this cycle: **Compile → Debug → Refactor → Compile again**
- To compile, a coder must hold **both dongles** (left and right) at the same time.
- After compiling, the coder puts both dongles back on the table.
- Coders do not talk to each other and do not know who is close to burnout.

```
        Coder1
   D1 /        \ D2
 Coder4        Coder2
   D4 \        / D3
        Coder3
```

Coder 1 needs dongles D1 and D2, and Coder 2 needs D2 and D3. So D2 is shared between them.

**Special case:** If there is only 1 coder, there is only 1 dongle. That coder can never compile and must burn out exactly after `time_to_burnout`.

---

## 3. Arguments

```
./codexion number_of_coders time_to_burnout time_to_compile time_to_debug time_to_refactor number_of_compiles_required dongle_cooldown scheduler
```

| Argument | Meaning |
|---|---|
| `number_of_coders` | Number of coders (= number of dongles) |
| `time_to_burnout` | If a coder does not **start** compiling again within this time (ms) since the start of their last compile (or the start of the simulation), they burn out |
| `time_to_compile` | Duration of a compile (the coder holds two dongles during this time) |
| `time_to_debug` | Duration of debugging |
| `time_to_refactor` | Duration of refactoring (right after it, the coder immediately tries to get dongles again) |
| `number_of_compiles_required` | If every coder has compiled at least this many times, the simulation ends |
| `dongle_cooldown` | After a dongle is released, it is **unavailable** for this long (ms) |
| `scheduler` | Only `fifo` or `edf` |

**Validation:** All arguments are mandatory. Negative numbers, non-integers (such as `abc` or `3.5`), and an invalid scheduler must be rejected.

---

## 4. Scheduler: Who Gets the Dongle?

When several coders want the same dongle, the scheduler decides.

### FIFO (First In, First Out)
Whoever requested first gets the dongle first.

### EDF (Earliest Deadline First)
The coder with the earlier burnout deadline goes first:

```
deadline = last_compile_start + time_to_burnout
```

**Example:** `time_to_burnout = 800`
- Coder A started their last compile at t=0, so their deadline is 800.
- Coder B started their last compile at t=100, so their deadline is 900.
- Both want dongle D2. With **EDF**, A gets it (800 < 900). With **FIFO**, whoever requested first wins.

To implement this, you must write a **priority queue (heap)**, because standard C does not provide one. For FIFO, the heap key is the request arrival time; for EDF, it is the deadline.

---

## 5. Dongle Cooldown

A dongle cannot be used immediately after it is released.

**Example:** `dongle_cooldown = 50`
- Coder 1 releases dongle D2 at t=202.
- Coder 2 wants to take it at t=210, but the dongle is not available until t=252.
- So Coder 2 must wait (for example with `pthread_cond_timedwait`) until t=252.

---

## 6. The Monitor Thread

A separate thread must continuously check whether anyone has burned out:

```
if (now - last_compile_start) >= time_to_burnout:
    set the stop flag
    print the log "X burned out"   <- at most 10 ms after the actual burnout
```

This thread also checks whether every coder has reached `number_of_compiles_required`. If so, the simulation ends without a burnout.

---

## 7. Log Format

```
timestamp_in_ms X has taken a dongle
timestamp_in_ms X is compiling
timestamp_in_ms X is debugging
timestamp_in_ms X is refactoring
timestamp_in_ms X burned out
```

Rules:
- Logs must not get mixed together, so printing is protected by a **mutex**.
- No other message may be printed after a burnout message.
- Every `is compiling` line must be preceded by two `has taken a dongle` lines.

---

## 8. Full Examples

### Example 1: One coder

```
./codexion 1 800 200 200 200 3 50 fifo
```
Output:
```
0 1 has taken a dongle
800 1 burned out
```
The coder picks up one dongle, but there is no second dongle. They wait forever and burn out after 800 ms.

### Example 2: Several coders

```
./codexion 4 800 200 200 200 2 50 fifo
```
One possible output (simplified):
```
0   1 has taken a dongle
0   1 has taken a dongle
0   1 is compiling
0   3 has taken a dongle
0   3 has taken a dongle
0   3 is compiling
200 1 is debugging
200 3 is debugging
250 2 has taken a dongle      <- after the cooldown
250 2 has taken a dongle
250 2 is compiling
...
```
Explanation: Coders 1 and 3 are not neighbours and share no dongle, so they can compile at the same time. Coders 2 and 4 must wait until the dongles are released and the cooldown has passed.

### Example 3: Burnout (from the PDF itself)
```
0 1 has taken a dongle
2 1 has taken a dongle
2 1 is compiling
202 1 is debugging
402 1 is refactoring
...
1505 4 burned out
```
Coder 4 never managed to get two dongles, so they burned out at t=1505 and the simulation stopped.

---

## 9. Concurrency Problems You Must Solve

1. **Deadlock:** If everyone picks up their left dongle at the same time and waits for the right one, everyone is stuck forever. You must break one of the four **Coffman conditions**. Common approaches:
   - Resource ordering: always take the lower-numbered dongle first.
   - Take both dongles atomically (under a single lock).
   - Asymmetric start: even and odd coders start with a different order.

2. **Starvation:** No particular coder should be left behind forever. EDF helps because it uses deadlines, but you must make sure that reasonable parameters do not cause starvation.

3. **Race conditions:** All shared data (dongle state, `last_compile_start`, compile counts, the stop flag) must be protected by mutexes.

4. **Timing precision:** A burnout must be reported at most 10 ms after the real time. Use `gettimeofday` for timing and avoid long `usleep` calls, since the monitor might wake up late.

---

## 10. Technical Rules

- **Forbidden:** global variables. Put everything in structs and pass them to the threads.
- **Allowed functions:** `pthread_create/join`, `pthread_mutex_*`, `pthread_cond_*` (including `timedwait` and `broadcast`), `gettimeofday`, `usleep`, `write`, `malloc/free`, `printf`, `fprintf`, `strcmp`, `strlen`, `atoi`, `memset`
- **libft:** not allowed.
- **Compilation:** `cc -Wall -Wextra -Werror -pthread`
- **Makefile:** rules `NAME`, `all`, `clean`, `fclean`, `re`, with no unnecessary relinking
- **Files:** `Makefile`, `*.c`, `*.h` in the `coders/` directory
- **Norm:** the code must follow the school's Norm.
- **Memory:** no memory leaks and no crashes (segfault, etc.).
- **Threads:** one thread per coder, plus one separate thread for the monitor.

---

## 11. The README.md File

It must be at the root of the repository, **written in English**, with this content:

1. **First line** (italic): *This project has been created as part of the 42 curriculum by \<login1\>[, \<login2\>...]*
2. A **Description** section
3. An **Instructions** section (how to compile and run)
4. A **Resources** section (references, and a description of what you used AI for)
5. A **Blocking cases handled** section (deadlock and Coffman's conditions, starvation, cooldown, precise burnout detection, log serialization)
6. A **Thread synchronization mechanisms** section (use of mutexes and condition variables, with examples of how race conditions are prevented and how coders and the monitor communicate safely)

---

## 12. Suggested Implementation Path

1. Parse and validate the arguments
2. Define the structs (`t_data`, `t_coder`, `t_dongle`)
3. Time function (`get_time_ms`) and mutex-protected logging
4. Implement the heap (min-heap)
5. Dongle logic: mutex + condition variable + cooldown + priority queue
6. Coder routine (compile → debug → refactor)
7. Monitor thread
8. Cleanup: join all threads, destroy mutexes and condition variables, free memory
9. Test with Valgrind/Helgrind (`--tool=helgrind`) and `-fsanitize=thread`
10. Write the README

---

## 13. Evaluation Phase

During peer evaluation you may be asked to make a **small change** to your code (for example, changing a behaviour or a log). So you must fully understand your own code. The "AI Instructions" chapter also stresses that you must be able to explain any code you wrote with the help of AI.



 # The Dining Philosophers Problem

The **Dining Philosophers Problem** is one of the most famous classic problems in computer science and operating systems. Formulated by **Edsger Dijkstra** in 1965, it is widely used to illustrate the challenges of **concurrency**, **synchronization**, and the risks of **deadlock** and **starvation** in shared resource management.

---

## 1. Problem Statement

Imagine **5 philosophers** sitting around a circular table:

* In the center of the table is a large bowl of spaghetti.
* There is **one fork** placed between each pair of adjacent philosophers (totaling **5 forks**).
* Each philosopher alternates between two states: **Thinking** or **Eating**.
* To eat, a philosopher **must acquire both forks** (the ones immediately to their left and right).
* Once finished eating, the philosopher puts down both forks and resumes thinking.

> 💡 **Core Challenge:** Forks are **shared resources**. Two adjacent philosophers cannot eat at the same time.

---

## 2. Key Issues in Concurrent Processing

If philosophers pick up forks simultaneously without proper coordination, three major problems arise:

### 🔴 1. Deadlock
Suppose all 5 philosophers decide to eat at the **exact same time** and each picks up their **left fork**:
* No philosopher holds 2 forks.
* Everyone waits indefinitely for the philosopher on their right to put down their fork.
* No one drops their fork $\rightarrow$ **The system freezes completely (Deadlock).**

### 🟡 2. Starvation
A philosopher might continuously fail to acquire both forks simultaneously because their left and right neighbors alternate eating continuously. As a result, this philosopher never gets to eat and **starves**.

### 🟠 3. Livelock
To prevent deadlock, imagine enforcing a rule: *"If the second fork isn't available, put down the first fork, wait a few seconds, and try again."*
If all philosophers drop their forks at the same time and retry simultaneously, the system enters an infinite loop of repetitive actions without making any real progress.

---

## 3. Solutions

To prevent deadlock and starvation, several strategies are employed in computer systems and operating systems:

| Solution | How It Works | Pros & Cons |
| :--- | :--- | :--- |
| **Resource Hierarchy** | Number the forks $1$ to $5$. Philosophers must always request the lower-numbered fork first before acquiring the higher-numbered one. | Completely eliminates Deadlock. |
| **Limiting Diners (Semaphore)** | Allow a maximum of $4$ philosophers at the table at any given time using a semaphore. | Guarantees at least one philosopher can get $2$ forks. |
| **Atomic Pickup (Mutex / Monitor)** | A philosopher is allowed to pick up forks **only if both** left and right forks are available simultaneously. | Prevents deadlock effectively; must carefully manage starvation. |
| **Arbitrator / Waiter** | Introduce a central waiter/arbiter. Philosophers must ask permission from the waiter before grabbing any fork. | Simple to implement, but the waiter becomes a system **bottleneck**. |

---

## 4. Why Is This Problem Important?

In modern software development:
* **Philosophers** represent **Threads or Processes**.
* **Forks** represent **Shared System Resources** (such as database locks, files, memory segments, or network sockets).

Understanding this problem empowers software engineers to design robust concurrent systems that run smoothly without race conditions, resource contention, or system locks.

The animation can be found in [The Dining Philosophers Problem](https://codepen.io/Atousa/full/01a1465d-0620-748a-bb7e-2267126262a1).