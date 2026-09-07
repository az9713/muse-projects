"""CLI: add / list / done over the service layer."""
import argparse
import json
import sys

from tasks import service


def main(argv=None):
    parser = argparse.ArgumentParser(prog="tasks")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="add a task")
    p_add.add_argument("title")
    p_add.add_argument("--tags", default="", help="comma-separated tags")

    p_list = sub.add_parser("list", help="list tasks")
    p_list.add_argument("--tag", default=None, help="filter by tag")
    p_list.add_argument("--open", action="store_true", help="only open tasks")

    p_done = sub.add_parser("done", help="mark a task done")
    p_done.add_argument("task_id", type=int)

    args = parser.parse_args(argv)
    if args.cmd == "add":
        tags = [t for t in args.tags.split(",") if t.strip()]
        task = service.create_task(args.title, tags)
    elif args.cmd == "list":
        if args.open:
            task = service.open_tasks(tag=args.tag)
        else:
            task = service.list_tasks(tag=args.tag)
    else:
        task = service.complete_task(args.task_id)
    print(json.dumps(task, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
