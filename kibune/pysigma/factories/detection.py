from typing import Any, Optional

from kibune.pysigma import schemas
from kibune.pysigma.parser import prepare_condition
from kibune.pysigma.utils import normalize_detection


class DetectionFactory:
    @staticmethod
    def from_data(*, data: dict[Any, Any]):
        detection: dict[Any, Any] = data["detection"]
        condition: Optional[schemas.Condition] = None

        if "condition" in detection:
            condition = prepare_condition(detection.pop("condition"))

        detection = normalize_detection(detection)

        return schemas.Detection(
            detection=detection,
            condition=condition,
        )
