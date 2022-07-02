import json
from collections import defaultdict
from typing import Dict, List, Union

from . import REVISION_FIELD, REVISIONS_KEY, SRC_FIELD, TYPE_KEY
from .converter.image import ImageConverter
from .converter.vega import VegaConverter


def _get_converter(
    renderer_class, props
) -> Union[VegaConverter, ImageConverter]:
    from dvc_render import ImageRenderer, VegaRenderer

    if renderer_class.TYPE == VegaRenderer.TYPE:
        return VegaConverter(props)
    if renderer_class.TYPE == ImageRenderer.TYPE:
        return ImageConverter(props)

    raise ValueError(f"Invalid renderer class {renderer_class}")


def _group_by_rev(datapoints):
    grouped = defaultdict(list)
    for datapoint in datapoints:
        rev = datapoint.pop(REVISION_FIELD)
        grouped[rev].append(datapoint)
    return dict(grouped)


def to_json(renderer, split: bool = False) -> List[Dict]:
    from copy import deepcopy

    if renderer.TYPE == "vega":
        grouped = _group_by_rev(deepcopy(renderer.datapoints))
        if split:
            content = renderer.get_filled_template(skip_anchors=["data"])
        else:
            content = renderer.get_filled_template()
        if grouped:
            return [
                {
                    TYPE_KEY: renderer.TYPE,
                    REVISIONS_KEY: sorted(grouped.keys()),
                    "content": json.loads(content),
                    "datapoints": grouped,
                }
            ]
        return []
    if renderer.TYPE == "image":
        return [
            {
                TYPE_KEY: renderer.TYPE,
                REVISIONS_KEY: [datapoint.get(REVISION_FIELD)],
                "url": datapoint.get(SRC_FIELD),
            }
            for datapoint in renderer.datapoints
        ]
    raise ValueError(f"Invalid renderer: {renderer.TYPE}")
