import logging
import typing

from . import locked
from dvc.dvcfile import DVC_FILE_SUFFIX
from dvc.stage.exceptions import (
    StageNotFound,
    StageFileDoesNotExistError,
    StageFileIsNotDvcFileError,
)

if typing.TYPE_CHECKING:
    from dvc.repo import Repo

logger = logging.getLogger(__name__)


@locked
def remove(self: "Repo", target: str, outs: bool = False):
    try:
        stages = self.stage.from_target(target)
    except (StageNotFound, StageFileDoesNotExistError) as e:
        # If the user specified a tracked file as a target instead of a stage,
        # e.g. `data.csv` instead of `data.csv.dvc`,
        # give a more helpful error message.
        if self.fs.exists(target + DVC_FILE_SUFFIX):
            raise StageFileIsNotDvcFileError(target) from e
        else:
            raise

    for stage in stages:
        stage.remove(remove_outs=outs, force=outs)

    return stages
