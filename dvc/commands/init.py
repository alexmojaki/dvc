import argparse
import logging

import colorama

from .. import analytics
from ..cli.command import CmdBaseNoRepo
from ..cli.utils import append_doc_link
from ..utils import boxify
from ..utils import format_link as fmt_link

logger = logging.getLogger(__name__)


def _welcome_message():
    from ..ui import ui

    if analytics.is_enabled():
        ui.write(
            boxify(
                "DVC has enabled anonymous aggregate usage analytics.\n"
                "Read the analytics documentation (and how to opt-out) here:\n"
                + fmt_link("https://dvc.org/doc/user-guide/analytics"),
                border_color="red",
            )
        )

    msg = (
        "{yellow}What's next?{nc}\n"
        "{yellow}------------{nc}\n"
        f"- Check out the documentation: {fmt_link('https://dvc.org/doc')}\n"
        f"- Get help and share ideas: {fmt_link('https://dvc.org/chat')}\n"
        f"- Star us on GitHub: {fmt_link('https://github.com/iterative/dvc')}"
    ).format(yellow=colorama.Fore.YELLOW, nc=colorama.Fore.RESET)

    ui.write(msg)


class CmdInit(CmdBaseNoRepo):
    def run(self):
        from ..exceptions import InitError
        from ..repo import Repo

        try:
            with Repo.init(
                ".",
                no_scm=self.args.no_scm,
                force=self.args.force,
                subdir=self.args.subdir,
            ) as repo:
                self.config = repo.config
                _welcome_message()
        except InitError:
            logger.exception("failed to initiate DVC")
            return 1
        return 0


def add_parser(subparsers, parent_parser):
    """Setup parser for `dvc init`."""
    INIT_HELP = "Initialize DVC in the current directory."
    INIT_DESCRIPTION = (
        "Initialize DVC in the current directory. Expects directory\n"
        "to be a Git repository unless --no-scm option is specified."
    )

    init_parser = subparsers.add_parser(
        "init",
        parents=[parent_parser],
        description=append_doc_link(INIT_DESCRIPTION, "init"),
        help=INIT_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    init_parser.add_argument(
        "--no-scm",
        action="store_true",
        default=False,
        help="Initiate DVC in directory that is "
        "not tracked by any SCM tool (e.g. Git).",
    )
    init_parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        default=False,
        help=(
            "Overwrite existing '.dvc/' directory. "
            "This operation removes local cache."
        ),
    )
    init_parser.add_argument(
        "--subdir",
        action="store_true",
        default=False,
        help=(
            "Necessary for running this command inside a subdirectory of a "
            "parent SCM repository."
        ),
    )
    init_parser.set_defaults(func=CmdInit)
