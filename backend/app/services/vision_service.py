import time
from pathlib import Path

import cv2
from ultralytics import YOLO

from app.core.config import settings
from app.schemas.damage import (
    BoundingBox,
    DamageAnalysisResult,
    DamageSummary,
    DetectedDamage,
)


class VisionService:
    """
    YOLO Vision Service
    """

    def __init__(self):

        self.model = YOLO(settings.YOLO_MODEL)

    # -----------------------------------------------------
    # Analyze Image
    # -----------------------------------------------------

    def analyze_image(
        self,
        image_path: str,
    ) -> DamageAnalysisResult:

        start = time.perf_counter()

        image = cv2.imread(image_path)

        if image is None:
            raise ValueError(
                f"Unable to read image: {image_path}"
            )

        results = self.model.predict(
            source=image,
            conf=settings.VISION_CONFIDENCE,
            iou=settings.VISION_IOU,
            verbose=False,
        )

        damages = []

        total_area = 0

        repair_cost = 0

        image_h, image_w = image.shape[:2]

        for result in results:

            for box in result.boxes:

                cls = int(box.cls.item())

                confidence = float(box.conf.item())

                name = result.names[cls]

                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()

                width = x2 - x1

                height = y2 - y1

                area = (width * height) / (image_w * image_h) * 100

                total_area += area

                severity = self._severity(name, area)

                cost = self._repair_cost(name)

                repair_cost += cost

                damages.append(
                    DetectedDamage(
                        class_name=name,
                        confidence=confidence,
                        severity=severity,
                        estimated_area=round(
                            area,
                            2,
                        ),
                        estimated_cost=cost,
                        bounding_box=BoundingBox(
                            x1=float(x1),
                            y1=float(y1),
                            x2=float(x2),
                            y2=float(y2),
                        ),
                    )
                )

        annotated = self._save_prediction(
            image_path,
            results,
        )

        processing = time.perf_counter() - start

        return DamageAnalysisResult(
            success=True,
            image_path=image_path,
            model_name=Path(self.model.ckpt_path).name,
            damages=damages,
            summary=DamageSummary(
                total_damages=len(damages),
                overall_severity=self._overall(
                    total_area,
                ),
                total_damage_area=round(
                    total_area,
                    2,
                ),
                estimated_repair_cost=repair_cost,
            ),
            annotated_image_path=annotated,
            processing_time=processing,
        )

    # -----------------------------------------------------

    def _severity(
        self,
        damage_type: str,
        area: float,
    ) -> str:

        if "windscreen" in damage_type.lower():
            return "High"

        if "headlight" in damage_type.lower():
            return "Medium"

        if "taillight" in damage_type.lower():
            return "Medium"

        if area < 2:
            return "Low"

        if area < 6:
            return "Medium"

        return "High"

    # -----------------------------------------------------

    def _repair_cost(
        self,
        damage_type: str,
    ) -> float:

        repair_costs = {
            "Front-windscreen-damage": 18000,
            "Rear-windscreen-Damage": 16000,
            "Headlight-damage": 8000,
            "Taillight-Damage": 5000,
            "Sidemirror-Damage": 4000,
            "Runningboard-Damage": 6000,
            "bonnet-dent": 15000,
            "boot-dent": 12000,
            "doorouter-dent": 10000,
            "fender-dent": 8000,
            "front-bumper-dent": 14000,
            "rear-bumper-dent": 14000,
            "quaterpanel-dent": 11000,
            "roof-dent": 22000,
        }

        return repair_costs.get(
            damage_type,
            5000,
        )

    # -----------------------------------------------------

    def _overall(
        self,
        area: float,
    ) -> str:

        if area < 5:
            return "Low"

        if area < 15:
            return "Medium"

        return "High"

    # -----------------------------------------------------

    def _save_prediction(
        self,
        image_path: str,
        results,
    ) -> str:

        Path(settings.ANNOTATED_IMAGE_DIR).mkdir(
            parents=True,
            exist_ok=True,
        )

        annotated = results[0].plot()

        output = Path(settings.ANNOTATED_IMAGE_DIR) / Path(image_path).name

        cv2.imwrite(
            str(output),
            annotated,
        )

        return str(output)


vision_service: VisionService | None = None


def get_vision_service() -> VisionService:
    global vision_service
    if vision_service is None:
        vision_service = VisionService()
    return vision_service


