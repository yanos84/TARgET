from TARgET.tools.serialization.rankedFta_xml_import import load_fta_from_xml
from TARgET.tools.drawing.rankedFtaDraw import draw_ranked_fta

"""
A cli command that draws a ranked finite tree automaton.
Syntax:
    python -m TARgET.api.cli.commands.fta.draw <fta_file> [-o <output>] [--format <format>] (from the root of the TARgET project)
    or target fta draw <fta_file> [-o <output>] [--format <format>] (from anywhere if the project is installed)

"""


def run(args):
    """
    Draws a ranked finite tree automaton from an XML file and saves it in the specified format.
    Args:
        args: The command line arguments.
    """
    fta = load_fta_from_xml(args.fta_file)

    dot = draw_ranked_fta(fta)

    dot.render(
        args.output,
        format=args.format,
        cleanup=True,
    )


def register_command(subparsers):
    """
    Registers the 'draw' command with the provided subparsers.
    Args:
        subparsers: The subparsers object to which the 'draw' command will be added.
    """
    draw_parser = subparsers.add_parser(
        "draw",
        help="Draw a ranked finite tree automaton. If no output file is specified, the drawn RFTA will be saved as 'fta' in the current directory.  The default format is PNG.  You can specify the format using the --format option (choices: png, pdf, svg).  ",
    )

    draw_parser.add_argument("fta_file")

    draw_parser.add_argument(
        "-o",
        "--output",
        default="fta",
    )

    draw_parser.add_argument(
        "--format",
        choices=["png", "pdf", "svg"],
        default="png",
    )

    draw_parser.set_defaults(handler=run)