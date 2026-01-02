import argparse
from engine.fta.drawing.rankedFtaDraw import draw_ranked_fta
#from engine.fta.acceptors.rankedAcceptor import RankedAcceptor
#from engine.fta.random.ranked_fta_generator import RandomRankedFtaGenerator
from engine.utils.rankedFta_xml_import import load_fta_from_xml

def main():
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