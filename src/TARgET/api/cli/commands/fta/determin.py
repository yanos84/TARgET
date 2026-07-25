from TARgET.tools.serialization.rankedFta_xml_import import load_fta_from_xml
from TARgET.tools.serialization.rankedFta_xml_export import export_ranked_fta_to_xml
from TARgET.engine.fta.determinization.ranked_determinization import determinize

"""
A cli command that determinizes a given ranked finite tree automaton (RFTA).
Syntax:
    python -m TARgET.api.cli.commands.fta.determin <input_fta_file> <output_fta_file> [-o <output>] (from the root of the TARgET project)
    or target fta determin <input_fta_file> [-o <output>]  (from anywhere if the project is installed)
"""


def run(args):
    fta = load_fta_from_xml(args.input_fta_file)

    determinized_fta = determinize(fta)
    export_ranked_fta_to_xml(determinized_fta, args.output)


    


def register_command(subparsers):
    determinize_parser = subparsers.add_parser(
        "determinize",
        help="Determinizes a given ranked finite tree automaton (RFTA). If no output file is specified, the determinized RFTA will be saved as 'determinized_fta.xml' in the current directory. ",
    )

    determinize_parser.add_argument("input_fta_file")
    #determinize_parser.add_argument("output_fta_file")

    determinize_parser.add_argument(
        "-o",
        "--output",
        default="determinized_fta.xml",
    )


    determinize_parser.set_defaults(handler=run)