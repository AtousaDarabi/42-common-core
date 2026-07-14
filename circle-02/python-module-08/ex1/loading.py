import sys
import importlib
from types import ModuleType
from typing import Dict, Tuple

REQUIRED_PACKAGES: Dict[str, Tuple[str, str]] = {
    "pandas": ("pandas", "Data manipulation"),
    "numpy": ("numpy", "Numerical computation"),
    "matplotlib": ("matplotlib", "Visualization"),
}


def check_and_import_dependencies() -> Dict[str, ModuleType]:
    missing = []
    modules: Dict[str, ModuleType] = {}

    print("LOADING STATUS: Loading programs...")
    print("Checking dependencies:")

    for module_name, (pkg_name, description) in REQUIRED_PACKAGES.items():
        try:
            mod = importlib.import_module(module_name)
            version = getattr(mod, "__version__", "unknown")
            print(f"[OK] {pkg_name} ({version}) - {description} ready")
            modules[module_name] = mod
        except ImportError:
            print(f"[MISSING] {pkg_name} - {description} NOT installed")
            missing.append(pkg_name)

    if missing:
        print("\nERROR: Missing dependencies detected!")
        print("\nTo install using pip:")
        print("  pip install -r requirements.txt")
        print("\nTo install using Poetry:")
        print("  poetry install")
        print("  poetry run python loading.py")
        sys.exit(1)

    return modules


def run_analysis(
    pd: ModuleType, np: ModuleType, matplotlib_module: ModuleType
) -> None:
    print("\nAnalyzing Matrix data...")
    print("Processing 1000 data points...")

    np.random.seed(42)
    data_points = 1000
    signal = np.random.normal(loc=100, scale=15, size=data_points)
    noise = np.random.uniform(low=-10, high=10, size=data_points)
    matrix_values = signal + noise

    df = pd.DataFrame(
        {"Signal": signal, "Noise": noise, "MatrixValue": matrix_values}
    )

    # matplotlib itself only exposes __version__; the actual plotting
    # API lives in the matplotlib.pyplot submodule, so it is imported
    # separately here rather than assumed to be on the top-level module.
    plt = importlib.import_module("matplotlib.pyplot")

    print("Generating visualization...")
    plt.figure(figsize=(10, 6))
    plt.hist(df["MatrixValue"], bins=30, color="#00FF66", edgecolor="black")
    plt.title("Matrix Signal Data Analysis", fontsize=14, color="black")
    plt.xlabel("Signal Intensity", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.5)

    output_file = "matrix_analysis.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()

    print("Analysis complete!")
    print(f"Results saved to: {output_file}")


def main() -> None:
    modules = check_and_import_dependencies()
    run_analysis(modules["pandas"], modules["numpy"], modules["matplotlib"])


if __name__ == "__main__":
    main()
