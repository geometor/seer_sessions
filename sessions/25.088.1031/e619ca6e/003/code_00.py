import numpy as np
from scipy.ndimage import label, generate_binary_structure
import collections

"""
Transforms the input grid based on the number of distinct green (color 3) objects found using 8-way connectivity.

- If 0 green objects: Returns the input grid unchanged.
- If 1 green object: Keeps the original object. Calculates its bounding box height (H) and width (W). Adds copies of the object translated relative to its original position by vectors (H, -W), (H, W), and (2H, 2W).
- If 2 or more green objects: Finds the combined bounding box enclosing each unique pair of green objects. Fills the rectangular area defined by each of these combined bounding boxes with green. The original green objects are preserved as they fall within these filled areas.
"""

# Define a structure to hold object information
Object = collections.namedtuple('Object', ['pixels', 'bbox']) # bbox = (min_r, min_c, max_r, max_c) inclusive

def find_objects(grid, target_color):
    """
    Identifies connected components (objects) of a specified color in a grid.
    Uses 8-way connectivity.

    Args:
        grid: The input numpy array grid.
        target_color: The integer color value to find objects of.

    Returns:
        A list of Object namedtuples. Each tuple contains:
          - pixels: A set of (row, col) tuples for the object.
          - bbox: A tuple (min_r, min_c, max_r, max_c) representing the
                  inclusive bounding box.
        Returns an empty list if no objects are found.
    """
    # Create a binary mask where target_color pixels are True
    binary_grid = (grid == target_color)
    # Define 8-way connectivity structure
    structure = generate_binary_structure(rank=2, connectivity=2)
    # Label connected components
    labeled_grid, num_labels = label(binary_grid, structure=structure)

    objects = []
    if num_labels > 0:
        # For each label, find coordinates and calculate bounding box
        for i in range(1, num_labels + 1):
            coords = np.argwhere(labeled_grid == i)
            # Ensure the component still exists (can happen with edge cases)
            if coords.size > 0:
                pixels = set(map(tuple, coords))
                # Extract row and column coordinates
                rows, cols = zip(*coords)
                # Calculate inclusive bounding box
                min_r, max_r = min(rows), max(rows)
                min_c, max_c = min(cols), max(cols)
                bbox = (min_r, min_c, max_r, max_c)
                # Store object info
                objects.append(Object(pixels, bbox))

    return objects

def transform(input_grid):
    """
    Applies the transformation rule based on the number of green objects.
    """

    # Define the target color
    green_color = 3
    # Find all distinct connected green objects
    objects = find_objects(input_grid, green_color)
    num_objects = len(objects)
    # Initialize the output grid as a copy of the input
    output_grid = np.copy(input_grid)
    grid_h, grid_w = input_grid.shape

    # --- Case 1: Single Object ---
    if num_objects == 1:
        the_object = objects[0]
        pixels = the_object.pixels
        min_r, min_c, max_r, max_c = the_object.bbox

        # Calculate Height (H) and Width (W) of the bounding box
        H = max_r - min_r + 1
        W = max_c - min_c + 1

        # Define translation vectors based on object dimensions
        # These were derived empirically from training example 2
        translations = [(H, -W), (H, W), (2 * H, 2 * W)]

        # Apply each translation to create copies of the object
        for dr, dc in translations:
            for r, c in pixels:
                # Calculate the new coordinates for the pixel
                new_r, new_c = r + dr, c + dc
                # Check if the new coordinates are within the grid bounds
                if 0 <= new_r < grid_h and 0 <= new_c < grid_w:
                    # Paint the translated pixel green
                    output_grid[new_r, new_c] = green_color
        # The original object remains because output_grid started as a copy

    # --- Case 2: Two or More Objects ---
    elif num_objects >= 2:
        # Iterate through all unique pairs of distinct objects
        for i in range(num_objects):
            for j in range(i + 1, num_objects):
                obj_i = objects[i]
                obj_j = objects[j]

                # Get bounding boxes for the pair of objects
                min_r_i, min_c_i, max_r_i, max_c_i = obj_i.bbox
                min_r_j, min_c_j, max_r_j, max_c_j = obj_j.bbox

                # Calculate the combined bounding box that encloses both objects
                comb_min_r = min(min_r_i, min_r_j)
                comb_min_c = min(min_c_i, min_c_j)
                comb_max_r = max(max_r_i, max_r_j)
                comb_max_c = max(max_c_i, max_c_j)

                # Fill the combined bounding box rectangle with green
                # Clip coordinates to grid boundaries for safe slicing
                fill_r_start = max(0, comb_min_r)
                # +1 because numpy slicing end index is exclusive
                fill_r_end = min(grid_h, comb_max_r + 1) 
                fill_c_start = max(0, comb_min_c)
                 # +1 because numpy slicing end index is exclusive
                fill_c_end = min(grid_w, comb_max_c + 1)

                # Ensure the slice dimensions are valid before filling
                if fill_r_start < fill_r_end and fill_c_start < fill_c_end:
                     output_grid[fill_r_start:fill_r_end, fill_c_start:fill_c_end] = green_color

    # --- Case 3: Zero Objects ---
    # If num_objects is 0, no changes are made, and the original grid copy is returned.

    return output_grid