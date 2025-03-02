"""
The transformation identifies the locations of non-white pixels (seed pixels) in the input grid.
These seed pixels define a rectangular region.
The output grid is formed by filling this rectangular region.
The corners of the rectangle are determined by the positions of the seed pixels.
If a seed pixel is blue (1), it marks the top-left corner.
If a seed pixel is red (2), it marks the top-right corner.
If a seed pixel is azure (8), it marks the bottom-left corner.
The color of the top-left seed pixel determines the fill color of the rectangle.
If no top-left seed pixel is found, the rectangle is filled with azure (8) by default.
If the rectangle would extend outside the input, truncate at edge.
"""

import numpy as np

def get_seed_pixels(grid):
    # Find the coordinates of all non-white pixels, categorized by color.
    seed_pixels = {1: None, 2: None, 8: None}
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                if grid[r,c] in seed_pixels:
                  seed_pixels[grid[r, c]] = (r, c)
    return seed_pixels

def transform(input_grid):
    # Initialize the output grid with the same dimensions and filled with white (0).
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Get the categorized seed pixels.
    seed_pixels = get_seed_pixels(input_grid)

    # Determine the corners of the rectangle.
    top_left = seed_pixels.get(1)
    top_right = seed_pixels.get(2)
    bottom_left = seed_pixels.get(8)
    
    # set fill defaults
    fill_color = 8
    start_row = 0
    start_col = 0
    end_row = rows
    end_col = cols

    # adjust if we have seed pixels
    if top_left:
        start_row = top_left[0]
        start_col = top_left[1]
        fill_color = 1
    if top_right:
        end_col = top_right[1] + 1 # inclusive
    if bottom_left:
        end_row = bottom_left[0] + 1 # inclusive

    # Fill the rectangular region in the output grid.
    for r in range(start_row, min(end_row,rows)):
        for c in range(start_col, min(end_col, cols)):
            output_grid[r, c] = fill_color

    return output_grid