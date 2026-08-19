from toolboxs.decorators import singleton
from image_services.image_processing_pipeline.image_processing_pipline import ImageProcessingPipline

# --
# ...
# --


@singleton
class ImageProvider:
    def __init__(self, **kwargs):
        self.image_processing_pipline = ImageProcessingPipline()
