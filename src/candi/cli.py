import argparse as ap
import sys
from pathlib import Path

from . import __version__, classifier
from . import download_db

# Historically this tool/repo was named "gandi" (Global Anaerobic Digestion). It was
# renamed to "candi" (Compendium Of Anaerobic Digestion Microbiomes Database), but
# "gandi" is kept installed as an alias for backwards compatibility -- both names
# dispatch to this same main(), which detects which one was actually invoked so
# help text/errors refer to the right command.
DEFAULT_PROG = "candi"


def _description(prog_name):
    return (
        f"{prog_name} {__version__}: contig/genome classifier and reference-database downloader for the\n"
        "Compendium Of Anaerobic Digestion Microbiomes Database (CAnDi).\n"
        "\n"
        "Classify a genome against the database:\n"
        f"  {prog_name} classifier -i genome.fasta -o output_dir -c plasmids -d /path/to/database\n"
        "\n"
        "Download and build the reference database:\n"
        f"  {prog_name} download-db -o /path/to/database"
    )


def _build_parser(prog_name):
    parser = ap.ArgumentParser(
        prog=prog_name,
        description=_description(prog_name),
        formatter_class=ap.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-v", "--version", action="version", version=f"{prog_name} {__version__}")
    subparsers = parser.add_subparsers(dest="command", metavar="<subcommand>")
    subparsers.add_parser(
        "classifier",
        help="Classify contigs/genomes against a CAnDi reference database (ANI/AAI workflows)."
    )
    subparsers.add_parser(
        "download-db",
        help="Download and build the CAnDi reference database."
    )
    return parser


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)
    prog_name = Path(sys.argv[0]).stem or DEFAULT_PROG
    parser = _build_parser(prog_name)

    if not argv:
        parser.print_help()
        sys.exit(2)

    if argv[0] in ("-h", "--help"):
        parser.print_help()
        sys.exit(0)

    if argv[0] in ("-v", "--version"):
        print(f"{prog_name} {__version__}")
        sys.exit(0)

    command, rest = argv[0], argv[1:]
    if command == "classifier":
        classifier.main(rest, prog=f"{prog_name} classifier")
    elif command == "download-db":
        download_db.main(rest, prog=f"{prog_name} download-db")
    else:
        parser.print_help()
        print(f"\nUnknown subcommand: {command!r}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
