import argparse

"""
Commands for operating on finite tree automata.
1. Draw a ranked finite tree automaton (RFTA) from an XML file.
"""

from .draw import register_command as register_draw_command
#from .accept import register_command as register_accept_command
#from .determinize import register_command as register_determinize_command


def register_commands(subparsers):
    """
    Register all FTA commands with the given subparsers.
    """
    fta_parser = subparsers.add_parser(
        "fta",
        help="Operations on finite tree automata.",
    )

    fta_subparsers = fta_parser.add_subparsers(
        dest="fta_command",
        required=True,
    )

    register_draw_command(fta_subparsers)  # Register the draw command for FTAs
    #register_accept_command(fta_subparsers)
    #register_determinize_command(fta_subparsers)