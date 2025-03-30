import numpy as np
from scipy.ndimage import label, generate_binary_structure
import collections

"""
Transforms the input grid based on the green (color 3) objects found using 8-way connectivity.

1. Find all distinct connected green objects in the input grid. Let N be the count of these objects.
2. If N = 0: The output grid is identical to the input grid.
3. If N > 0:
    a. Initialize the output grid as a copy of the input grid (preserving the original objects and background).
    b. For *each* distinct green object found:
        i. Determine its bounding box (min_row, min_col, max_row, max_col).
        ii. Calculate the height H = max_row - min_row + 1.
        iii. Calculate the width W = max_col - min_col + 1.
        iv. Define three translation vectors based on H and W:
            - V1 = (H, -W)  (Shift down by H, left by W)
            - V2 = (H, W)   (Shift down by H, right by W)
            - V3 = (2*H, 2*W) (Shift down by 2*H, right by 2*W)
        v. For each of the three translation vectors (dr, dc):
            - Iterate through every pixel (r, c) that belongs to the *current original green object*.
            - Calculate the new coordinates: new_r = r + dr, new_c = c + dc.
            - Check if the new coordinates (new_r, new_c) are within the bounds of the grid.
            - If they are within bounds, paint the pixel at (new_r, new_c) on the output grid green (color 3).
4. Return the final modified output grid.
"""

# Define a structure to hold object information
# bbox = (min_r, min_c, max_r, max_c) inclusive
Object = collections.namedtuple('Object', ['pixels', 'bbox'])

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
    Applies the transformation rule based on the green objects found.
    """
    # Define the target color
    green_color = 3
    # Find all distinct connected green objects
    objects = find_objects(input_grid, green_color)
    num_objects = len(objects)
    # Initialize the output grid as a copy of the input
    output_grid = np.copy(input_grid)
    grid_h, grid_w = input_grid.shape

    # --- Case N = 0: No Objects ---
    if num_objects == 0:
        # Return the unchanged grid if no green objects are found
        return output_grid

    # --- Case N > 0: One or More Objects ---
    else:
        # Process each found green object independently
        for obj in objects:
            pixels = obj.pixels
            min_r, min_c, max_r, max_c = obj.bbox

            # Calculate Height (H) and Width (W) of the object's bounding box
            H = max_r - min_r + 1
            W = max_c - min_c + 1

            # Define the three translation vectors based on H and W
            translations = [(H, -W), (H, W), (2 * H, 2 * W)]

            # Apply each translation to create copies of the current object
            for dr, dc in translations:
                # Iterate through each pixel of the original object
                for r, c in pixels:
                    # Calculate the new coordinates for the pixel after translation
                    new_r, new_c = r + dr, c + dc
                    # Check if the new coordinates are within the grid boundaries
                    if 0 <= new_r < grid_h and 0 <= new_c < grid_w:
                        # Paint the translated pixel green on the output grid
                        output_grid[new_r, new_c] = green_color

        # Return the modified grid
        return output_grid
