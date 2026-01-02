import argparse
from engine.fta.drawing.rankedFtaDraw import draw_ranked_fta as RankedFtaDrawer
from engine.fta.acceptors.rankedAcceptor import RankedAcceptor
from engine.fta.random.ranked_fta_generator import RandomRankedFtaGenerator

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
    #draw_parser.add_argument(