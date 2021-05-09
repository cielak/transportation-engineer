from matplotlib import pyplot as plt
from skimage import io
from skimage.draw import circle_perimeter
from skimage.transform import PiecewiseAffineTransform, warp


def read_image():
    raise NotImplementedError


def get_image_mesh_points():
    raise NotImplementedError


def get_perfect_mesh_points():
    raise NotImplementedError


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
    ax[0].imshow(original_image, cmap="gray")
    ax[0].set_title("Original image")
    ax[1].imshow(transformed_image, cmap="gray")
    ax[1].set_title("Transformed image")
    plt.show()


def calibrate(image, mesh_source, mesh_destination):
    transform = calculate_transform(mesh_destination, mesh_source)
    return apply_transform(image, transform)


def main():
    image_data = read_image()
    image_mesh_points = get_image_mesh_points()
    perfect_mesh_points = get_perfect_mesh_points()
    confirm_mesh(image_data, perfect_mesh_points)
    calibrated_image_data = calibrate(
        image_data, image_mesh_points, perfect_mesh_points
    )
    verify_result(image_data, calibrated_image_data)


if __name__ == "__main__":
    main()
