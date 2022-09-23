# Copyright (c) 2022 Kyle Schouviller (https://github.com/kyle0654)

from marshmallow import fields
from marshmallow.validate import OneOf, Range
from PIL.Image import Image
from ldm.dream.app.services.schemas import ImageField, InvocationSchemaBase
from ldm.dream.app.invocations.invocationabc import InvocationABC
from ldm.generate import Generate


class InvokeUpscale(InvocationABC):
    """Generates an image using text2img."""
    def __init__(
        self,
        generate: Generate,
        **kwargs # consume unused arguments
    ):
        self._generate: Generate = generate

    def invoke(self, image: Image, level: int, strength: float, **kwargs) -> dict:  # See args in schema below
        results = self._generate.upscale_and_reconstruct(
            image_list=[[image, 0]],
            upscale=(level, strength),
            strength=0.0, # GFPGAN strength
            save_original=False,
            image_callback=None,
        )

        # Results are image and seed, unwrap for now
        # TODO: can this return multiple results?
        return dict(image=results[0][0])


class UpscaleSchema(InvocationSchemaBase):
    """Upscale"""
    class Meta:
        type = 'upscale'
        outputs = {
            'image': ImageField()
        }
        invokes = InvokeUpscale

    image = ImageField()
    level = fields.Integer(load_default=2, validate=OneOf([2, 4]))
    strength = fields.Float(load_default=0.75, validate=Range(0.0, 1.0, min_inclusive=False, max_inclusive=True))