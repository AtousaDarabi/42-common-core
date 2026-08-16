import abc
import typing
from typing import Any


class DataProcessor(abc.ABC):

    def __init__(self, name: str) -> None:
        self.name: str = name
        self._data_store: list[str] = []
        self._processed_count: int = 0

    @abc.abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abc.abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._data_store:
            raise IndexError("No data available to output.")

        data_item = self._data_store.pop(0)
        rank = self._processed_count - len(self._data_store) - 1
        return rank, data_item

    @property
    def processed_count(self) -> int:
        return self._processed_count

    @property
    def remaining_count(self) -> int:
        return len(self._data_store)


class NumericProcessor(DataProcessor):

    def __init__(self) -> None:
        super().__init__("Numeric Processor")

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)) and not isinstance(data, bool):
            return True
        if isinstance(data, list):
            return all(
                isinstance(x, (int, float)) and not isinstance(x, bool)
                for x in data
            )
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")

        items = data if isinstance(data, list) else [data]
        for item in items:
            self._data_store.append(str(item))
            self._processed_count += 1


class TextProcessor(DataProcessor):

    def __init__(self) -> None:
        super().__init__("Text Processor")

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(x, str) for x in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")

        items = data if isinstance(data, list) else [data]
        for item in items:
            self._data_store.append(item)
            self._processed_count += 1


class LogProcessor(DataProcessor):

    def __init__(self) -> None:
        super().__init__("Log Processor")

    @staticmethod
    def _is_valid_dict(d: Any) -> bool:
        return isinstance(d, dict) and all(
            isinstance(k, str) and isinstance(v, str) for k, v in d.items()
        )

    def validate(self, data: Any) -> bool:
        if self._is_valid_dict(data):
            return True
        if isinstance(data, list):
            return all(self._is_valid_dict(x) for x in data)
        return False

    def ingest(
        self, data: dict[str, str] | list[dict[str, str]]
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        def _format_log(d: dict[str, str]) -> str:
            if "log_level" in d and "log_message" in d:
                return f"{d['log_level']}: {d['log_message']}"
            return " ".join(f"{k}: {v}" for k, v in d.items())

        items = data if isinstance(data, list) else [data]
        for item in items:
            self._data_store.append(_format_log(item))
            self._processed_count += 1


class DataStream:

    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)

    def process_stream(self, stream: list[typing.Any]) -> None:
        for item in stream:
            handled = False
            for proc in self.processors:
                if proc.validate(item):
                    proc.ingest(item)
                    handled = True
                    break
            if not handled:
                print(
                    "DataStream error - Can't process element in stream:"
                    f" {item}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self.processors:
            print("No processor found, no data")
            return

        for proc in self.processors:
            print(
                f"{proc.name}: total {proc.processed_count} items "
                f"processed, remaining {proc.remaining_count} on processor"
            )


def main() -> None:
    print("=== Code Nexus - Data Stream ===")
    print("Initialize Data Stream...")
    stream_engine = DataStream()

    stream_engine.print_processors_stats()

    print("\nRegistering Numeric Processor")
    numeric_proc = NumericProcessor()
    stream_engine.register_processor(numeric_proc)

    batch_data: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {"log_level": "INFO", "log_message": "User wil is connected"},
        ],
        42,
        ["Hi", "five"],
    ]

    print("\nSend first batch of data on stream:", batch_data)
    stream_engine.process_stream(batch_data)

    stream_engine.print_processors_stats()

    print("\nRegistering other data processors")
    text_proc = TextProcessor()
    log_proc = LogProcessor()
    stream_engine.register_processor(text_proc)
    stream_engine.register_processor(log_proc)

    print("\nSend the same batch again")
    stream_engine.process_stream(batch_data)

    stream_engine.print_processors_stats()

    print(
        "\nConsume some elements from the data processors: Numeric 3, Text 2,"
        " Log 1"
    )
    for _ in range(3):
        numeric_proc.output()
    for _ in range(2):
        text_proc.output()
    for _ in range(1):
        log_proc.output()

    stream_engine.print_processors_stats()


if __name__ == "__main__":
    main()
