"""
1. **Identify the Frame:** The grid is surrounded by a frame of azure (8) pixels.

2.  **Identify Inner Pixels:** Locate all pixels directly adjacent (horizontally or vertically) to the azure frame. These are the "inner pixels."

3.  **Determine Color Mapping:** For each inner pixel in the input grid, find its color and the corresponding color of the same pixel in the output grid. Create a dictionary where the keys are the input colors and the values are the corresponding output colors. If an inner pixel's color doesn't change between the input and the output, it still needs an entry in the dictionary; map the color to itself.

4.  **Apply Transformation:** Iterate through the inner pixels of the input grid. For each inner pixel, look up its color in the color mapping dictionary created in step 3. Change the pixel's color in the output grid to the corresponding value from the dictionary.

5.  **Preserve Frame:** The azure frame remains unchanged. The output grid is a copy of the input grid with only the inner pixels potentially modified.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def find_frame_color(grid):
    """ Assumes a rectangular, framed grid and returns the frame color.
        We'll just check the top-left pixel.
    """
    return grid[0,0]

def find_inner_pixels(grid, frame_color):
    """Finds pixels adjacent to the frame."""
    rows, cols = grid.shape
    inner_pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] != frame_color:
                for nr, nc in get_neighbors(grid, r, c):
                    if grid[nr, nc] == frame_color:
                        inner_pixels.append( (r,c) )
                        break # Optimization, don't add the same pixel twice
    return inner_pixels

def determine_color_mapping(input_grid, output_grid, frame_color):
    """Determine the input->output color mapping for inner pixels."""
    inner_pixels = find_inner_pixels(input_grid, frame_color)
    color_mapping = {}
    for r, c in inner_pixels:
        input_color = input_grid[r, c]
        output_color = output_grid[r, c]
        color_mapping[input_color] = output_color  # Store the mapping
    return color_mapping

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify the Frame
    frame_color = find_frame_color(input_grid)

    # 2. Identify Inner Pixels
    inner_pixels = find_inner_pixels(input_grid, frame_color)


    # 3. Determine Color Mapping (using training examples)
    color_mapping = {}
    if 'train' in dir() and 'test' in dir(): #we only know the train examples
        for example in train:
            in_grid = example['input']
            out_grid = example['output']
            if in_grid.shape == input_grid.shape:
                color_mapping.update(determine_color_mapping(in_grid, out_grid, frame_color) )

    # 4. Apply Transformation
    for r, c in inner_pixels:
        input_color = input_grid[r,c]
        if input_color in color_mapping:
          output_grid[r, c] = color_mapping[input_color]

    # 5. Preserve Frame (already handled)

    return output_grid