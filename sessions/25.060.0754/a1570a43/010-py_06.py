"""
The transformation rotates the red (2) block 90 degrees clockwise, 
while keeping the green (3) pixels in the same position.
"""

import numpy as np

def get_red_block(grid):
    # Find coordinates of all red pixels
    red_pixels = np.argwhere(grid == 2)
    return red_pixels

def rotate_coordinates(coords, center, angle_degrees):
    # Rotate coordinates around a center point
    angle_radians = np.radians(angle_degrees)
    rotation_matrix = np.array([
        [np.cos(angle_radians), -np.sin(angle_radians)],
        [np.sin(angle_radians), np.cos(angle_radians)]
    ])
    centered_coords = coords - center
    rotated_coords = np.dot(centered_coords, rotation_matrix)
    return rotated_coords + center

def transform(input_grid):
    # Initialize output grid with zeros
    output_grid = np.zeros_like(input_grid)

    # Get the red block coordinates
    red_block = get_red_block(input_grid)

    # Calculate the center of the grid (assuming it is the center of rotation)
    center = np.array([input_grid.shape[0] // 2, input_grid.shape[1] // 2])

    # Rotate the red block coordinates 90 degrees clockwise
    rotated_red_block = rotate_coordinates(red_block, center, 90)

    # Round the rotated coordinates and convert to integers to use as indices
    rotated_red_block = np.round(rotated_red_block).astype(int)

    # Place the rotated red block into the output grid
    for x, y in rotated_red_block:
        if 0 <= x < output_grid.shape[0] and 0 <= y < output_grid.shape[1]:  # Boundary check
          output_grid[x, y] = 2

    # Copy the green pixels to the output grid
    green_pixels = np.argwhere(input_grid == 3)
    for x, y in green_pixels:
        output_grid[x, y] = 3

    return output_grid