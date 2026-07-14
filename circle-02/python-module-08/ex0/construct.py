import os
import sys
import site


def check_venv() -> None:
    in_venv = (
        getattr(sys, "base_prefix", sys.prefix) != sys.prefix
        or hasattr(sys, "real_prefix")
    )

    if in_venv:
        env_path = sys.prefix
        env_name = os.path.basename(env_path)
        site_packages = site.getsitepackages()
        pkg_path = site_packages[0] if site_packages else "Not found"

        print()
        print("MATRIX STATUS: Welcome to the construct")
        print()
        print(f"Current Python: {sys.executable}")
        print(f"Virtual Environment: {env_name}")
        print(f"Environment Path: {env_path}")
        print()
        print("SUCCESS: You're in an isolated environment!")
        print("Safe to install packages without affecting")
        print("the global system.")
        print()
        print("Package installation path:")
        print(pkg_path)
    else:
        print()
        print("MATRIX STATUS: You're still plugged in")
        print()
        print(f"Current Python: {sys.executable}")
        print("Virtual Environment: None detected")
        print()
        print("WARNING: You're in the global environment!")
        print("The machines can see everything you install.")
        print()
        print("To enter the construct, run:")
        print("python -m venv matrix_env")
        print("source matrix_env/bin/activate    # On Unix")
        print(r"matrix_env\Scripts\activate      # On Windows")
        print()
        print("Then run this program again.")
        print()


if __name__ == "__main__":
    check_venv()
