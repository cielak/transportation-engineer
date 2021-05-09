from itertools import product

import numpy as np
import pytest
from skimage.draw import random_shapes

from calibrator.calibrator import calibrate, verify_result


def generate_image():
    def add_crosses(image):
        for r, c in real_mesh():
            x_value = 1
            x_size = 1
            image[r, c] = x_value
            if r < image.shape[0] - x_size:
                image[r + x_size, c] = x_value
            if c < image.shape[1] - x_size:
                image[r, c + x_size] = x_value
            if r >= x_size:
                image[r - x_size, c] = x_value
            if c >= x_size:
                image[r, c - x_size] = x_value

    image_shape = (100, 100)
    img, _ = random_shapes(
        image_shape, max_shapes=10, multichannel=False, random_seed=100
    )
    add_crosses(img)
    return img


def real_mesh():
    coord = [0, 23, 40, 60, 81, 99]
    return np.array([(r, c) for (r, c) in product(coord, coord)])


def perfect_mesh():
    coord = [0, 20, 40, 60, 80, 99]
    return np.array([(r, c) for (r, c) in product(coord, coord)])


@pytest.fixture
def prototype():
    return generate_image(), real_mesh(), perfect_mesh()


def test_calibrate_prototype(prototype):
    original_image, image_mesh_points, perfect_mesh_points = prototype
    verify_result(
        original_image,
        calibrate(original_image, image_mesh_points, perfect_mesh_points),
    )
    assert input("Does the image look properly calibrated? [y/n] ") == "y"
