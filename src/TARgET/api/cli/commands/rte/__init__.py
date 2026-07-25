import argparse
from .print_rte import register_command as register_print_command


def register_commands(subparsers):
    """
    Register all RTE commands with the given subparsers.
    """
    rte_parser = subparsers.add_parser(
        "rte",
        help="Operations on runtime environments.",
    )

    rte_subparsers = rte_parser.add_subparsers(
        dest="rte_command",
        required=True,
    )

    register_print_command(rte_subparsers)  # Register the print command for RTEs