import argparse
import logging

from ..cli.command import CmdBaseNoRepo
from ..cli.utils import append_doc_link
from ..ui import ui

logger = logging.getLogger(__name__)


class CmdVersion(CmdBaseNoRepo):
    def run(self):
        from ..info import get_dvc_info
        from ..updater import notify_updates

        dvc_info = get_dvc_info()
        ui.write(dvc_info, force=True)

        notify_updates()
        return 0


def add_parser(subparsers, parent_parser):
    VERSION_HELP = (
        "Display the DVC version and system/environment information."
    )
    version_parser = subparsers.add_parser(
        "version",
        parents=[parent_parser],
        description=append_doc_link(VERSION_HELP, "version"),
        help=VERSION_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        aliases=["doctor"],
    )
    version_parser.set_defaults(func=CmdVersion)
