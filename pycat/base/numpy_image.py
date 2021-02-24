from enum import Enum
from typing import Sequence

from numpy import array as np_array
from numpy import dstack, float32, frombuffer, argwhere
from numpy import max as np_max
from numpy import min as np_min
from numpy import ndarray, tensordot, uint8
from numpy.linalg import norm
from pyglet.image import ImageData, Texture
from pyglet.resource import image as load_image


class ImageFormat(Enum):

    L = 'L'  # 1-channel Luminance texture
    LA = 'LA'  # 2-channel LuminanceAlpha texture
    RGB = 'RGB'  # 3-channel RGB texture
    RGBA = 'RGBA'  # 4-channel RGBA texture

    def channels(self):
        return len(self.value)


class NumpyImage(ndarray):

    # change to take array buffer
    # make classmethod called zeros with rows, cols, channels parameters
    def __new__(cls, rows: int, cols: int, channels: int = 1):
        if channels == 1:
            return super().__new__(cls, shape=(rows, cols), dtype=uint8)
        return super().__new__(cls, shape=(rows, cols, channels), dtype=uint8)

    # @classmethod
    # def from_file(cls, file: str) -> 'NumpyImage':
    #     return

    # @classmethod
    # def from_texture(cls, texture: Texture) -> 'NumpyImage':
    #     return

    @property
    def texture(self) -> Texture:
        return NumpyImage.get_texture_from_array(self)

    @property
    def rows(self) -> int:
        return self.shape[0]

    @property
    def cols(self) -> int:
        return self.shape[1]

    @property
    def channels(self) -> int:
        return 1 if len(self.shape) == 2 else self.shape[2]

    @staticmethod
    def get_array_from_file(file: str) -> ndarray:
        """Return a numpy array of pixel data from an image file."""
        return NumpyImage.get_array_from_texture(load_image(file))

    @staticmethod
    def get_array_from_texture(texture: Texture) -> ndarray:
        return NumpyImage.get_array_from_image_data(texture.get_image_data())

    @staticmethod
    def get_array_from_image_data(img: ImageData) -> ndarray:
        array: ndarray = frombuffer(img.get_data(), dtype=uint8).copy()
        return array.reshape(img.height, img.width, len(img.format))

    @staticmethod
    def get_texture_from_array(array: ndarray) -> Texture:
        img_format = NumpyImage.get_compatible_format(array)
        h, w = array.shape[:2]
        img_data = ImageData(w, h, img_format.value, array.tobytes())
        texture = img_data.get_texture()
        texture.anchor_x = texture.width / 2
        texture.anchor_y = texture.height / 2
        return texture

    @staticmethod
    def check_format_compatibility(array: ndarray, img_format: ImageFormat):
        assert 1 < len(array.shape) < 4
        if len(array.shape) == 2:
            assert img_format == ImageFormat.L
        else:
            channels = array.shape[2]
            assert 1 < channels < 5
            if channels == 2:
                assert img_format == ImageFormat.LA
            elif channels == 3:
                assert img_format == ImageFormat.RGB
            else:
                assert img_format == ImageFormat.RGBA

    @staticmethod
    def get_compatible_format(array: ndarray) -> ImageFormat:
        assert 1 < len(array.shape) < 4
        if len(array.shape) == 2:
            return ImageFormat.L
        else:
            channels = array.shape[2]
            assert 1 < channels < 5
            if channels == 2:
                return ImageFormat.LA
            elif channels == 3:
                return ImageFormat.RGB
            else:
                return ImageFormat.RGBA

    @staticmethod
    def get_luminance_array(array: ndarray) -> ndarray:
        assert len(array.shape) == 3
        assert array.shape[2] == 3
        luminance_coefficients = np_array([.299, .587, .114])
        float_array = array.astype(float32, copy=False)
        luminance = tensordot(float_array, luminance_coefficients, (2, 0))
        return luminance.astype(uint8, copy=False)

    @staticmethod
    def get_luminance_texture(array: ndarray) -> Texture:
        lum_array = NumpyImage.get_luminance_array(array)
        img_format = ImageFormat.L
        return NumpyImage.get_texture_from_array(lum_array, img_format)

    @staticmethod
    def get_magnitude_array(array: ndarray) -> ndarray:
        assert len(array.shape) == 3
        assert array.shape[2] == 3
        rgb = array.astype(float32, copy=False)
        return norm(rgb, axis=2)  # * 0.57735  # keep max val 255

    @staticmethod
    def get_magnitude_texture(array: ndarray) -> Texture:
        mag_array = NumpyImage.get_magnitude_array(array)
        NumpyImage.normalize_array(mag_array)
        mag_array *= 255
        return NumpyImage.get_texture_from_array(
            mag_array.astype(uint8, copy=False), ImageFormat.L)

    @staticmethod
    def normalize_array(array: ndarray):
        max_val = np_max(array)
        min_val = np_min(array)
        value_range = max_val - min_val
        array -= min_val
        if value_range != 0:
            array /= value_range

    @staticmethod
    def stack_arrays(array_list: Sequence[ndarray]) -> ndarray:
        """Stacks arrays with the same width and height along the channel axis.

        Example:

        If you have arrays corresponding to the r, g, and b color channels

        - `rgb = NumpyImage.stack_arrays([r, g, b])`
        - `rgba = NumpyImage.stack_arrays([rgb, a])`
        """
        return dstack(array_list)

    @staticmethod
    def crop_alpha_texture(texture: Texture) -> Texture:
        img_data: ImageData = texture.get_image_data()
        assert img_data.format == ImageFormat.RGBA.value
        img_array = NumpyImage.get_array_from_image_data(img_data)
        region = argwhere(img_array[..., 3])   # get alpha non-zero indices
        min_x, max_x = np_min(region[:, 1]), np_max(region[:, 1])
        min_y, max_y = np_min(region[:, 0]), np_max(region[:, 0])
        t: Texture = texture.get_region(min_x, min_y, max_x-min_x, max_y-min_y)
        t.anchor_x = t.width/2
        t.anchor_y = t.height/2
        return t

    @staticmethod
    def crop_alpha_array(img_array: ndarray) -> ndarray:
        region = argwhere(img_array[..., 3])   # get alpha non-zero indices
        min_j, max_j = np_min(region[:, 1]), np_max(region[:, 1])
        min_i, max_i = np_min(region[:, 0]), np_max(region[:, 0])
        return img_array[min_i:max_i, min_j:max_j, ...]
