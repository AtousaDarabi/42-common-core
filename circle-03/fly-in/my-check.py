import sys
import subprocess


def main() -> int:
    result = subprocess.run([sys.executable, "my.py"])
    print(result.returncode)   # 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
