from PIL import Image
import numpy as np
from image_services.models.image_data_model import ImageDataModel
from image_services.core.base import Base
from image_services.background_operation.config.background_operation_config import BackgroundOperationConfig

# --
# ...
# --


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

    # ...
    # --

    def find_product_box(self, image_data_model: ImageDataModel) -> ImageDataModel:
        """
        image: PIL Image

        return:
            x1, y1, x2, y2
        """

        mask = self.remove(image_data_model.image_data, session=self.session, only_mask=True)

        mask = np.array(mask)

        if mask.ndim == 3:
            mask = mask[:, :, 0]

        image_data_model.mask = mask

        ys, xs = np.where(mask > 20)

        if len(xs) == 0:
            return None

        x1 = xs.min()
        y1 = ys.min()
        x2 = xs.max()
        y2 = ys.max()

        image_data_model.product_box = x1, y1, x2, y2

        return image_data_model
