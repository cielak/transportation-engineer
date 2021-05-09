from itertools import product

import numpy as np
from matplotlib import pyplot as plt
from skimage import io
from skimage.draw import circle_perimeter, random_shapes
from skimage.transform import PiecewiseAffineTransform, warp


def read_image():
    def add_crosses(image):
        for r, c in get_image_mesh_points():
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
    img, _ = random_shapes(image_shape, max_shapes=10, multichannel=False, random_seed=100)
    add_crosses(img)
    return img


def get_image_mesh_points():
    coord = [0, 23, 40, 60, 81, 99]
    return np.array([(r, c) for (r, c) in product(coord, coord)])


def get_perfect_mesh_points():
    coord = [0, 20, 40, 60, 80, 99]
    return np.array([(r, c) for (r, c) in product(coord, coord)])


def calculate_transform(reality, expectation):
    transform = PiecewiseAffineTransform()
    transform.estimate(reality, expectation)
    return transform


def apply_transform(transform, image):
    return warp(transform, image)


def display_image(image):
    io.imshow(image)
    plt.show()


def confirm_mesh(image_data, perfect_mesh_points):
    def add_markers(image, points):
        for r, c in points:
            rr, cc = circle_perimeter(r, c, 3, shape=image.shape)
            image[rr, cc] = 0.5

    display = image_data.copy()
    add_markers(display, perfect_mesh_points)
    display_image(display)


def verify_result(original_image, transformed_image):
    fig, axes = plt.subplots(nrows=1, ncols=2)
    ax = axes.ravel()
    ax[0].imshow(original_image, cmap='gray')
    ax[0].set_title('Original image')
    ax[1].imshow(transformed_image, cmap='gray')
    ax[1].set_title('Transformed image')
    plt.show()


def main():
    image_data = read_image()
    image_mesh_points = get_image_mesh_points()
    perfect_mesh_points = get_perfect_mesh_points()
    confirm_mesh(image_data, perfect_mesh_points)
    transform = calculate_transform(perfect_mesh_points, image_mesh_points)
    verify_result(image_data, apply_transform(image_data, transform))


if __name__ == "__main__":
    main()
