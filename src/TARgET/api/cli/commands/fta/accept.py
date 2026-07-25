from TARgET.tools.utils.rankedFta_xml_import import load_fta_from_xml
from TARgET.tools.utils.rankedTree_xml_import import TreeXMLImporter
from TARgET.engine.fta.acceptors.rankedAcceptor import RankedBottomUpAcceptor as RankedAcceptor

"""
A cli command that decides whether a ranked tree is accepted by a given ranked finite tree automaton (RFTA).
Syntax:
    python -m TARgET.api.cli.commands.fta.accept <fta_file> <tree_file> [-o <output>] (from the root of the TARgET project)
    or target fta accept <fta_file> <tree_file> [-o <output>] (from anywhere if the project is installed)"""


def run(args):
    fta = load_fta_from_xml(args.fta_file)
    tree = TreeXMLImporter.import_tree(args.tree_file)

    acceptor = RankedAcceptor()
    if acceptor.accepts(fta, tree):
        print("Tree accepted")
    else:
        print("Tree rejected")

    


def register_command(subparsers):
    accept_parser = subparsers.add_parser(
        "accept",
        help="Decides whether a ranked tree is accepted by a given ranked finite tree automaton (RFTA).",
    )

    accept_parser.add_argument("fta_file")
    accept_parser.add_argument("tree_file")

    accept_parser.add_argument(
        "-o",
        "--output",
        default="fta",
    )


    accept_parser.set_defaults(handler=run)