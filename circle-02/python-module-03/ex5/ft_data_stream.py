import random
from typing import Generator, Tuple

PLAYERS = ["alice", "bob", "charlie", "dylan"]
ACTIONS = [
    "run",
    "eat",
    "sleep",
    "grab",
    "move",
    "climb",
    "swim",
    "release",
    "use",
]


def gen_event() -> Generator[Tuple[str, str], None, None]:
    while True:
        player = random.choice(PLAYERS)
        action = random.choice(ACTIONS)
        yield (player, action)


def consume_event(
    event_list: list[Tuple[str, str]],
) -> Generator[Tuple[str, str], None, None]:
    while len(event_list) > 0:
        index = random.randrange(len(event_list))
        event = event_list.pop(index)
        yield event


def main() -> None:
    print("=== Game Data Stream Processor ===")

    event_stream = gen_event()

    for i in range(1000):
        player, action = next(event_stream)
        print(f"Event {i}: Player {player} did action {action}")

    events_list = [next(event_stream) for _ in range(10)]
    print(f"Built list of 10 events: {events_list}")

    for event in consume_event(events_list):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {events_list}")


if __name__ == "__main__":
    main()
