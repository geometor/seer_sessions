"""
Transforms an input grid based on the following multi-step process:
1.  Determine the background color (most frequent color).
2.  Identify the target color (most frequent non-background color). If none exists, return a grid filled with the background color.
3.  Find all connected components (8-way adjacency) of the target color in the input grid.
4.  Filter out components consisting of only a single pixel ("singleton components"). Collect all pixels belonging to the remaining ("valid") components.
5.  If no valid components remain, return a grid filled with the background color.
6.  Calculate the bounding box enclosing all pixels from the valid components.
7.  Create an intermediate grid: fill the bounding box with the target color, and the outside with the background color.
8.  Modify the intermediate grid: for each pixel within the bounding box, if the corresponding pixel in the *original input grid* was the background color, set the intermediate grid pixel back to the background color ("background punch-out").
9.  Find connected components (8-way) of the target color in this modified intermediate grid.
10. Create the final output grid by copying the modified intermediate grid. Then, for any target color component found in the *modified intermediate grid* (from step 9) that has a size of exactly 1, change its pixel(s) in the final output grid to the background color.
"""

import numpy as np
from collections import Counter
from scipy.ndimage import label

# --- Helper Functions ---

def find_most_frequent_color(grid_flat):
    """Finds the most frequent color in a flattened grid list."""
    if not grid_flat:
        return 0 # Default to white/0 if grid is empty
    counts = Counter(grid_flat)
    # Check if counts is empty (can happen for single-element grids processed strangely)
    if not counts:
         # If grid_flat has elements, return the first, else default to 0
         return grid_flat[0] if grid_flat else 0
    most_common = counts.most_common(1)
    return most_common[0][0]

def find_target_color(grid_flat, background_color):
    """Finds the most frequent non-background color in a flattened grid list."""
    non_background_colors = [c for c in grid_flat if c != background_color]
    if not non_background_colors:
        return None # No target color found
    counts = Counter(non_background_colors)
    most_common = counts.most_common(1)
    return most_common[0][0] if most_common else None

def get_component_pixels(labeled_array, num_features):
    """Extracts pixel coordinates for each component from a labeled array."""
    # component_pixels maps component label (int > 0) to list of [row, col] coords
    component_pixels = {}
    for i in range(1, num_features + 1):
        coords = np.argwhere(labeled_array == i)
        component_pixels[i] = coords
    return component_pixels

# --- Main Transformation Function ---

def transform(input_grid):
    """Applies the complex transformation logic to the input grid."""
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    grid_flat = input_array.flatten().tolist()

    # 1. Determine the background color
    background_color = find_most_frequent_color(grid_flat)

    # 2. Identify the 'target' color
    target_color = find_target_color(grid_flat, background_color)

    # Initialize output grid with background color (handles early exit cases)
    output_array = np.full((rows, cols), background_color, dtype=int)

    # 3. If no target color exists, return the background grid
    if target_color is None:
        return output_array.tolist()

    # 4. Locate all pixels matching the target color in input
    target_mask_input = (input_array == target_color)

    # 5. Group input target pixels into connected components (8-way adjacency)
    structure = np.ones((3, 3), dtype=bool) # 8-way connectivity
    labeled_input, num_features_input = label(target_mask_input, structure=structure)

    # 6. Identify all pixels belonging to input components > 1 pixel ('valid target pixels')
    valid_target_pixels_coords = []
    component_pixel_map_input = get_component_pixels(labeled_input, num_features_input)
    for i in range(1, num_features_input + 1):
        # If component size is greater than 1
        if len(component_pixel_map_input[i]) > 1:
            valid_target_pixels_coords.extend(component_pixel_map_input[i]) # Add coords to list

    # 7. If no valid components remain, return the background grid
    if not valid_target_pixels_coords:
        return output_array.tolist()

    # 8. Calculate the overall bounding box for the valid pixels
    valid_target_pixels_coords_array = np.array(valid_target_pixels_coords)
    min_row = np.min(valid_target_pixels_coords_array[:, 0])
    max_row = np.max(valid_target_pixels_coords_array[:, 0])
    min_col = np.min(valid_target_pixels_coords_array[:, 1])
    max_col = np.max(valid_target_pixels_coords_array[:, 1])

    # 9. Create an intermediate grid: target color in bbox, background outside
    intermediate_grid = np.full((rows, cols), background_color, dtype=int)
    intermediate_grid[min_row:max_row+1, min_col:max_col+1] = target_color

    # 10. Apply background punch-out within the bounding box
    # Iterate only within the bounding box for efficiency
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            # If the corresponding pixel in the ORIGINAL input was background...
            if input_array[r, c] == background_color:
                # ...set the intermediate grid pixel to background.
                intermediate_grid[r, c] = background_color

    # 11. Create the final output grid (copy of intermediate for now)
    output_array = np.copy(intermediate_grid)

    # 12. Find connected components (8-way) of the target color *in the modified intermediate grid*
    target_mask_intermediate = (intermediate_grid == target_color)
    labeled_intermediate, num_features_intermediate = label(target_mask_intermediate, structure=structure)

    # 13. Remove singleton components from the final output grid
    component_pixel_map_intermediate = get_component_pixels(labeled_intermediate, num_features_intermediate)
    for i in range(1, num_features_intermediate + 1):
        component_coords = component_pixel_map_intermediate[i]
        # If this component in the *intermediate* grid is a singleton...
        if len(component_coords) == 1:
            # ...change the single pixel of this component to background color in the final output.
            r, c = component_coords[0]
            output_array[r, c] = background_color

    # 14. Return the final output grid as a list of lists
    return output_array.tolist()