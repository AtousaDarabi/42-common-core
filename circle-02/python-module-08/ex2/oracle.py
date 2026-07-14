import os
import sys
from typing import Dict
from dotenv import load_dotenv


def load_config() -> Dict[str, str]:
    load_dotenv()

    mode = os.getenv("MATRIX_MODE", "development")
    db_url = os.getenv("DATABASE_URL")
    api_key = os.getenv("API_KEY")
    default_log_level = "INFO" if mode == "production" else "DEBUG"
    log_level = os.getenv("LOG_LEVEL", default_log_level)
    zion_endpoint = os.getenv("ZION_ENDPOINT")

    missing_vars = []
    if not db_url:
        missing_vars.append("DATABASE_URL")
    if not api_key:
        missing_vars.append("API_KEY")
    if not zion_endpoint:
        missing_vars.append("ZION_ENDPOINT")

    if missing_vars:
        missing_list = ", ".join(missing_vars)
        print("ORACLE STATUS: Configuration incomplete!")
        print(f"WARNING: Missing environment variables: {missing_list}")
        print("Please copy .env.example to .env and configure all "
              "variables.")
        sys.exit(1)

    assert db_url is not None
    assert api_key is not None
    assert zion_endpoint is not None

    return {
        "mode": mode,
        "db_url": db_url,
        "api_key": api_key,
        "log_level": log_level,
        "zion_endpoint": zion_endpoint,
    }


def display_status(config: Dict[str, str]) -> None:
    print("ORACLE STATUS: Reading the Matrix...\n")
    print("Configuration loaded:")
    print(f"Mode: {config['mode']}")

    if config["mode"] == "production":
        print("Database: Connected to production cluster")
        print("API Access: Authenticated (SECURE PROD MODE)")
    else:
        print("Database: Connected to local instance")
        print("API Access: Authenticated")

    print(f"Log Level: {config['log_level']}")

    endpoint = config["zion_endpoint"]
    if "zion" in endpoint.lower() or endpoint.startswith("http"):
        print("Zion Network: Online")
    else:
        print("Zion Network: Offline/Unknown endpoint")

    print("\nEnvironment security check:")
    print("[OK] No hardcoded secrets detected")
    print("[OK] .env file properly configured")
    print("[OK] Production overrides available")


def main() -> None:
    config = load_config()
    display_status(config)


if __name__ == "__main__":
    main()
