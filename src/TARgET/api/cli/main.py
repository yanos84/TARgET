import argparse
from .commands.fta import register_commands as register_fta_commands
from .commands.rte import register_commands as register_rte_commands
#from TARgET.tools.drawing.rankedFtaDraw import draw_ranked_fta
#from engine.fta.acceptors.rankedAcceptor import RankedAcceptor
#from engine.fta.random.ranked_fta_generator import RandomRankedFtaGenerator
#from TARgET.tools.utils.rankedFta_xml_import import load_fta_from_xml


"""
This module serves as the main entry point for the CLI tool. It uses argparse to parse command-line arguments
and subcommands. The tool currently supports a "draw" command that generates and draws a random ranked finite
 tree automaton (RFTA) based on an input XML file. The user can specify the output image file name using the
   -o or --output option. The main function handles the command parsing and execution, while the drawing 
   functionality is implemented in the draw_ranked_fta function imported from the rankedFtaDraw module. 
   This structured approach allows for easy extension of additional commands and functionalities in the future.
"""

def main():
    parser = argparse.ArgumentParser(
        prog="target",
        description=(
            "TARgET: Tree Automata, Rational Tree Expressions, "
            "and Weighted Models."
        ),
    )

    subparsers = parser.add_subparsers(
        dest="domain",
        required=True,
    )

    register_fta_commands(subparsers)
    register_rte_commands(subparsers)

    args = parser.parse_args()
    args.handler(args)


if __name__ == "__main__":
    main()