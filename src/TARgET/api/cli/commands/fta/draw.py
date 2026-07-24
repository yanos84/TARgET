from TARgET.tools.utils.rankedFta_xml_import import load_fta_from_xml
from TARgET.tools.drawing.rankedFtaDraw import draw_ranked_fta


def run(args):
    fta = load_fta_from_xml(args.fta_file)

    dot = draw_ranked_fta(fta)

    dot.render(
        args.output,
        format=args.format,
        cleanup=True,
    )


def register_command(subparsers):
    draw_parser = subparsers.add_parser(
        "draw",
        help="Draw a ranked finite tree automaton.",
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