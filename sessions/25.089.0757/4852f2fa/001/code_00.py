"""
Identify the single, contiguous object composed of azure (8) pixels in the input grid.
Determine the smallest rectangular bounding box that completely encloses this azure object. Extract the subgrid defined by this bounding box; this is the "pattern".
Count the total number of yellow (4) pixels present anywhere in the input grid. Let this count be N.
Construct the output grid by horizontally tiling the extracted "pattern" N times. The height of the output grid will be the height of the pattern, and the width will be the width of the pattern multiplied by N.
"""

import numpy as np
from scipy.ndimage import label, find_objects

def find_contiguous_object_coords(grid, color):
    """
    Finds the coordinates of the pixels belonging to the first contiguous object
    of the specified color found in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color value of the object to find.

    Returns:
        list: A list of (row, col) tuples for the object's pixels, or None if not found.
    """
    binary_grid = (grid == color).astype(int)
    labeled_array, num_features = label(binary_grid)

    if num_features == 0:
        return None

    # find_objects returns a list of slices for each feature (object)
    # We assume there's only one object of the target color based on the task description
    obj_slice = find_objects(labeled_array)[0]
    coords = []
    for r in range(obj_slice[0].start, obj_slice[0].stop):
        for c in range(obj_slice[1].start, obj_slice[1].stop):
            if grid[r, c] == color:
                coords.append((r, c))
    return coords


def get_bounding_box(coords):
    """
    Calculates the minimal bounding box (min_row, min_col, max_row, max_col)
    for a list of coordinates.

    Args:
        coords (list): A list of (row, col) tuples.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) inclusive, or None if coords is empty.
    """
    if not coords:
        return None
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    min_row = min(rows)
    min_col = min(cols)
    max_row = max(rows)
    max_col = max(cols)
    return min_row, min_col, max_row, max_col

def extract_subgrid(grid, bbox):
    """
    Extracts a subgrid based on the bounding box.

    Args:
        grid (np.array): The input grid.
        bbox (tuple): (min_row, min_col, max_row, max_col).

    Returns:
        np.array: The extracted subgrid.
    """
    min_row, min_col, max_row, max_col = bbox
    return grid[min_row:max_row + 1, min_col:max_col + 1]

def count_pixels(grid, color):
    """
    Counts the number of pixels of a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to count.

    Returns:
        int: The count of pixels with the specified color.
    """
    return np.sum(grid == color)

def transform(input_grid):
    """
    Transforms the input grid by finding an azure object, determining its bounding box,
    counting yellow pixels, and tiling the azure object's pattern horizontally
    based on the yellow pixel count.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)

    # Define colors
    azure_color = 8
    yellow_color = 4
    background_color = 0 # Assuming background is white (0)

    # 1. Identify the single, contiguous object composed of azure (8) pixels
    # We use a simpler approach here: just find all azure pixels directly
    # and then determine their bounding box. This works if there's only one object.
    # A more robust method would use labeling as in the helper function.
    azure_coords = list(zip(*np.where(grid_np == azure_color)))

    if not azure_coords:
         # Handle cases where no azure object is found (return empty or original?)
         # Based on examples, this shouldn't happen, but good practice.
         # Let's assume an empty grid of appropriate size might be desired,
         # but for now, let's return an empty list.
         return [] # Or handle as per specific error requirement

    # 2. Determine the smallest rectangular bounding box and extract the pattern
    bbox = get_bounding_box(azure_coords)
    pattern = extract_subgrid(grid_np, bbox)

    # Replace non-azure colors within the pattern's bounding box with background color
    # This ensures only the azure shape and background are in the pattern
    pattern[pattern != azure_color] = background_color


    # 3. Count the total number of yellow (4) pixels
    replication_factor = count_pixels(grid_np, yellow_color)

    # Handle case where no yellow pixels are found (replication_factor is 0)
    if replication_factor == 0:
        # Decide what to return: empty grid, or maybe the single pattern?
        # The examples always have at least one yellow pixel.
        # Returning an empty list seems consistent with 0 width tiling.
        return []

    # 4. Construct the output grid by horizontally tiling the extracted "pattern" N times
    output_grid_np = np.tile(pattern, (1, replication_factor))

    # Convert the final numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid