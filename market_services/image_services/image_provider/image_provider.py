from toolboxs.decorators import singleton
from market_services.image_services.image_processing_pipeline.image_processing_pipeline import ImageProcessingPipeline

# --
# ...
# --


@singleton
class ImageProvider:
    def __init__(self, **kwargs):
        self.image_processing_pipeline = ImageProcessingPipeline()
