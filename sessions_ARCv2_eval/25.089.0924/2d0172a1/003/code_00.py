import numpy as np
from collections import Counter

def transform(input_grid):
    """
    Extracts the minimal bounding box containing all pixels whose color is not the most frequent color (background color).

    1. Analyze the input grid to find unique colors and their frequencies.
    2. Identify the background color as the most frequent color.
    3. Locate all pixels that do *not* match the background color.
    4. If no such pixels exist, return an empty grid.
    5. Otherwise, determine the minimum and maximum row and column indices (bounding box) encompassing these non-background pixels.
    6. Extract the subgrid defined by this bounding box from the input grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    
    # Handle empty input grid case
    if grid.size == 0:
        return []

    # 1. Find unique colors and their counts
    unique_colors, counts = np.unique(grid, return_counts=True)

    # Handle the case where the grid has only one color
    if len(unique_colors) <= 1:
        # If only one color exists, it's the background, so no 'object' pixels exist.
        return [] 

    # 2. Determine the background color (most frequent)
    background_color = unique_colors[np.argmax(counts)]

    # 3. Locate all pixels that are *not* the background color
    object_pixels_coords = np.where(grid != background_color)

    # 4. If no non-background pixels are found, return an empty grid
    if object_pixels_coords[0].size == 0:
        return []

    # 5. Calculate the bounding box coordinates
    min_row = np.min(object_pixels_coords[0])
    max_row = np.max(object_pixels_coords[0])
    min_col = np.min(object_pixels_coords[1])
    max_col = np.max(object_pixels_coords[1])

    # 6. Extract the subgrid using the bounding box coordinates
    # Slicing is inclusive of start index, exclusive of end index, so add 1 to max values.
    output_grid_np = grid[min_row:max_row + 1, min_col:max_col + 1]

    # Convert the resulting NumPy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid