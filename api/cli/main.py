import argparse
from TARgET.tools.drawing.rankedFtaDraw import draw_ranked_fta
#from engine.fta.acceptors.rankedAcceptor import RankedAcceptor
#from engine.fta.random.ranked_fta_generator import RandomRankedFtaGenerator
from TARgET.tools.utils.rankedFta_xml_import import load_fta_from_xml


"""
This module serves as the main entry point for the CLI tool. It uses argparse to parse command-line arguments
and subcommands. The tool currently supports a "draw" command that generates and draws a random ranked finite
 tree automaton (RFTA) based on an input XML file. The user can specify the output image file name using the
   -o or --output option. The main function handles the command parsing and execution, while the drawing 
   functionality is implemented in the draw_ranked_fta function imported from the rankedFtaDraw module. 
   This structured approach allows for easy extension of additional commands and functionalities in the future.
"""

def main():
    """
    Main function for the CLI tool. It sets up argument parsing, handles subcommands, and executes the appropriate functionality based on user input. Currently, it supports the "draw" command to generate and draw a random ranked finite tree automaton (RFTA) from an input XML file. The user can specify the output image file name using the -o or --output option. The function utilizes the draw_ranked_fta function to perform the drawing operation and saves the resulting image to the specified output file.
    """
    parser = argparse.ArgumentParser(
        prog="rfta_tool",
        description="Generate a random ranked finite tree automaton (RFTA), "
                    "draw it, and test acceptance of a sample ranked tree."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --------Drawing----------
    draw_parser = subparsers.add_parser(
        "draw",
        help="Generate and draw a random ranked finite tree automaton."
    )
    draw_parser.add_argument("fta_file")
    draw_parser.add_argument("-o", "--output", default="fta.png", help="Output image file name.")
    args = parser.parse_args()

    if args.command == "draw":
        fta =load_fta_from_xml(args.fta_file)
        dot = draw_ranked_fta(fta)
        dot.render("fta1", format="png", cleanup=True) 

if __name__ == "__main__":
    main()