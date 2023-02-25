import argparse
import inspect
import json
import importlib
import pkgutil
import os.path

from rslsync import RslClient


def add_commands(parser, clazz):
    subparsers = parser.add_subparsers(dest="subcommand", required=True)
    for name, method in inspect.getmembers(clazz, predicate=inspect.isfunction):
        if name.startswith("__"):
            continue
        name = name.replace("_", "-")
        command_group = subparsers.add_parser(name)
        parameters = inspect.signature(method).parameters
        for param_name, param_value in parameters.items():
            if param_name == "self":
                continue

            param_name = "--" + param_name.replace("_", "-")

            if param_value.default in [True, False]:
                action = "store_true"
                default = param_value.default
                command_group.add_argument(param_name, action=action, default=default)
            elif isinstance(param_value.default, int):
                default = param_value.default
                command_group.add_argument(param_name, default=default, type=int)
            elif isinstance(param_value.default, str):
                default = param_value.default
                command_group.add_argument(param_name, default=default)
            elif param_value.annotation == 'list':
                command_group.add_argument(param_name, action="extend")
            else:
                command_group.add_argument(param_name, required=True)


GENERAL_ARGS = ["url", "host", "port", "username", "password", "config", "command", "subcommand"]


def pass_args():
    parser = argparse.ArgumentParser(prog="rsl")
    parser.add_argument("--url")
    parser.add_argument("--host")
    parser.add_argument("--port")
    parser.add_argument("-u", "--username")
    parser.add_argument("-p", "--password")
    parser.add_argument("-c", "--config")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command, clazz in RslClient.list_commands():
        add_commands(subparsers.add_parser(command), clazz)

    return parser.parse_args()


def build_url(host, port):
    return "http://" + (host or "localhost") + ":" + (port or "8888")


def main():
    args = pass_args()
    if args.config:
        config = json.load(open(args.config))
        url = config.get("url") or build_url(config.get("host"), config.get("port"))
        username = config["username"]
        password = config["password"]
    else:
        url = args.url or build_url(args.host, args.port)
        username = args.username
        password = args.password

    client = RslClient(url, username, password)
    command = getattr(client, args.command.replace("-", "_"))
    subcommand = getattr(command, args.subcommand.replace("-", "_"))
    params = vars(args)
    return subcommand(**{k: v for k, v in params.items() if k not in GENERAL_ARGS})


if __name__ == "__main__":
    main()
