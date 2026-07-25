from TARgET.tools.serialization.rte_xml_import import RteXMLImporter
from TARgET.core.rte.rte import Rte

def run(args):
    rte = RteXMLImporter.import_rte(args.rte_file)
    print(rte)

def register_command(subparsers):
    print_parser = subparsers.add_parser(
        "print",
        help="Prints the contents of an RTE XML file.",
    )

    print_parser.add_argument("rte_file")
    print_parser.set_defaults(handler=run)

    