import os
from argparse import ArgumentParser, Namespace

from dotenv import load_dotenv
from dotenv import set_key as dotenv_set_key
from dotenv import unset_key as dotenv_unset_key

load_dotenv()


def get_arguments() -> Namespace:
    parser = ArgumentParser(description="Manage environment variables.")
    subparsers = parser.add_subparsers(dest="action", required=True)

    set_parser = subparsers.add_parser("set", help="Set a key-value pair.")
    set_parser.add_argument("key", type=str, help="The key to set.")
    set_parser.add_argument("value", type=str, help="The value to set.")

    unset_parser = subparsers.add_parser("unset", help="Unset a key.")
    unset_parser.add_argument("key", type=str, help="The key to unset.")

    parser.add_argument(
        "-f",
        "--env-file",
        default=".env",
        help="Path to the .env file (default: ./.env)",
    )

    return parser.parse_args()


def set_key(env_file: str, key: str, value: str) -> None:
    dotenv_set_key(env_file, key, value)
    print(f"Set {key} to {value} in {env_file}")


def unset_key(env_file: str, key: str) -> None:
    dotenv_unset_key(env_file, key)
    print(f"Unset {key} in {env_file}")


def main():
    args = get_arguments()
    env_file = os.path.abspath(args.env_file)

    if args.action == "set":
        set_key(env_file, args.key, args.value)
    elif args.action == "unset":
        unset_key(env_file, args.key)


if __name__ == "__main__":
    main()
