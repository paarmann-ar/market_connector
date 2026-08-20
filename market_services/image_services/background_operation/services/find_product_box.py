import cv2
import numpy as np

from market_services.image_services.background_operation.config.background_operation_config import BackgroundOperationConfig
from market_services.image_services.core.base import Base
from market_services.image_services.models.image_data_model import ImageDataModel


class FindProductBox(Base):
    def __init__(self, **kwargs):
        super(**kwargs).__init__(**kwargs)

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return BackgroundOperationConfig().get_dictionary()

    # --
    # ...
    # --

    def __call__(self) -> str:
        pass

    # --
    # ...
    # --

    def find_product_box(self, image_data_model: ImageDataModel) -> ImageDataModel:

        try:
            # Get segmentation mask from the background-removal model.
            mask = self.remove(image_data_model.image_data, session=self.session, only_mask=True)

            mask = np.array(mask)

            # Convert RGB/RGBA mask to grayscale.
            if mask.ndim == 3:
                mask = mask[:, :, 0]

            # Make sure the mask is binary.
            binary_mask = np.where(mask > 20, 255, 0).astype(np.uint8)

            # Find connected components.
            num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_mask, connectivity=8)

            if num_labels <= 1:
                return None

            # Ignore background (label 0).
            components = []

            for label in range(1, num_labels):
                x = stats[label, cv2.CC_STAT_LEFT]
                y = stats[label, cv2.CC_STAT_TOP]
                width = stats[label, cv2.CC_STAT_WIDTH]
                height = stats[label, cv2.CC_STAT_HEIGHT]
                area = stats[label, cv2.CC_STAT_AREA]

                components.append(
                    {
                        "label": label,
                        "x": x,
                        "y": y,
                        "width": width,
                        "height": height,
                        "area": area,
                    }
                )

            # Sort components by area.
            components.sort(key=lambda component: component["area"], reverse=True)

            # Largest connected component = main product.
            main_component = components[0]

            label = main_component["label"]

            # Keep only the main product in the mask.
            product_mask = np.where(labels == label, 255, 0).astype(np.uint8)

            # Find product coordinates.
            ys, xs = np.where(product_mask > 0)

            if len(xs) == 0:
                return None

            x1 = int(xs.min())
            y1 = int(ys.min())
            x2 = int(xs.max()) + 1
            y2 = int(ys.max()) + 1

            # Save clean product mask.
            image_data_model.mask = product_mask

            # Save product bounding box.
            image_data_model.product_box = (x1, y1, x2, y2)

            return image_data_model

        except Exception as exp:
            print(f"find_product_box: {exp}")

            return None
