from TARgET.tools.serialization.rankedFta_xml_import import load_fta_from_xml
from TARgET.tools.serialization.rankedFta_xml_export import export_ranked_fta_to_xml
from TARgET.engine.fta.minimization.dfta_standard_minimization import dfta_minimizer 

"""
A cli command that minimizes a given ranked finite tree automaton (RFTA).
Syntax:
    python -m TARgET.api.cli.commands.fta.minimize <input_fta_file> <output_fta_file> [-o <output>] (from the root of the TARgET project)
    or target fta minimize <input_fta_file> [-o <output>]  (from anywhere if the project is installed)
"""


def run(args):
    fta = load_fta_from_xml(args.input_fta_file)
    minimizer = dfta_minimizer()
    minimized_fta = minimizer.minimize(fta)

    export_ranked_fta_to_xml(minimized_fta, args.output)


    


def register_command(subparsers):
    minimize_parser = subparsers.add_parser(
        "minimize",
        help="Minimizes a given deterministic ranked finite tree automaton (DFTA). If no output file is specified, the minimized DFTA will be saved as 'minimized_fta.xml' in the current directory. ",
    )

    minimize_parser.add_argument("input_fta_file")
    minimize_parser.add_argument(
        "-o",
        "--output",
        default="minimized_fta.xml",
    )


    minimize_parser.set_defaults(handler=run)