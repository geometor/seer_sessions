"""
Transforms the input grid by identifying a source region (leftmost non-background object) and a target region (rightmost non-background object). It then identifies a "pattern color" within the source region, which is the numerically smallest color different from the most frequent color (frame color) in that region. This pattern (pixels of the pattern color) is then copied/translated horizontally from the source to the target region. The horizontal shift is determined by the difference in the minimum column indices of the two regions. The pattern pixels only overwrite pixels within the boundaries of the target region's identified coordinates.
"""

import numpy as np
from scipy.ndimage import label, find_objects
from collections import Counter
import copy

def find_regions(grid_np, background_color=0):
    """
    Finds connected regions of non-background pixels.

    Args:
        grid_np (np.array): The input grid as a NumPy array.
        background_color (int): The color value considered background.

    Returns:
        list: A list of dictionaries, where each dictionary represents a region
              and contains 'coords' (set of (row, col) tuples), 'min_col',
              'max_col', 'min_row', 'max_row'. Returns an empty list if no
              non-background regions are found.
    """
    mask = grid_np != background_color
    labeled_array, num_features = label(mask) # Default 8-connectivity

    regions = []
    if num_features == 0:
        return regions

    # Use find_objects to quickly get bounding boxes, but extract exact coords
    # object_slices = find_objects(labeled_array) # Less efficient for exact coords

    for i in range(1, num_features + 1): # Labels are 1-based
        coords_array = np.argwhere(labeled_array == i)
        if coords_array.size == 0:
            continue

        coords_set = set(tuple(coord) for coord in coords_array)
        rows = coords_array[:, 0]
        cols = coords_array[:, 1]

        regions.append({
            'coords': coords_set,
            'min_row': np.min(rows),
            'max_row': np.max(rows),
            'min_col': np.min(cols),
            'max_col': np.max(cols),
            'label': i # Keep track of the label if needed later
        })

    return regions

def get_region_colors_and_counts(grid_np, region_coords, background_color=0):
    """
    Counts the occurrences of non-background colors within a region.

    Args:
        grid_np (np.array): The grid.
        region_coords (set): A set of (row, col) tuples for the region.
        background_color (int): The background color to ignore.

    Returns:
        collections.Counter: A Counter object mapping non-background colors
                             to their counts within the region.
    """
    color_counts = Counter()
    for r, c in region_coords:
        color = grid_np[r, c]
        if color != background_color:
            color_counts[color] += 1
    return color_counts


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Initialize output grid as a copy of the input
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = input_np.shape
    background_color = 0

    # 1. Find all connected non-background regions
    regions = find_regions(input_np, background_color)

    # 2. Need at least two regions (source and target)
    if len(regions) < 2:
        return output_grid.tolist() # Return original if not enough regions

    # 3. Identify Source (leftmost) and Target (rightmost) regions
    # Sort regions by their minimum column index
    regions.sort(key=lambda r: r['min_col'])
    source_region = regions[0]
    target_region = regions[-1] # Assume rightmost is target

    # 4. Get colors and counts in the source region
    source_colors_counts = get_region_colors_and_counts(input_np, source_region['coords'], background_color)

    if not source_colors_counts:
         return output_grid.tolist() # Source region only has background? unlikely but safe

    # 5. Determine Source Frame Color (most frequent non-background color)
    # Handle cases with only one color or ties (take the first one from most_common)
    most_common = source_colors_counts.most_common(1)
    source_frame_color = most_common[0][0] if most_common else None # color value

    # 6. Determine Pattern Color (smallest non-background color != frame color)
    pattern_color = None
    sorted_unique_colors = sorted(source_colors_counts.keys())

    # Check if there's more than one unique non-bg color first
    if len(sorted_unique_colors) > 1:
        for color in sorted_unique_colors:
            if color != source_frame_color:
                pattern_color = color
                break
    # If only one color, or if loop didn't find a different one (e.g., tie logic resulted in smallest being frame), no pattern
    # OR if source_frame_color is None (only background found)
    if pattern_color is None:
         return output_grid.tolist() # No pattern color found to copy

    # 7. Find Pattern Pixels in the source region
    pattern_pixels = []
    for r, c in source_region['coords']:
        if input_np[r, c] == pattern_color:
            pattern_pixels.append((r, c))

    if not pattern_pixels:
        return output_grid.tolist() # No pixels of pattern color found

    # 8. Calculate the horizontal translation vector
    delta_col = target_region['min_col'] - source_region['min_col']

    # 9. Get target region coordinates as a set for efficient checking
    target_coords_set = target_region['coords']

    # 10. Copy pattern pixels to the target region if applicable
    for r_s, c_s in pattern_pixels:
        # Calculate potential target coordinates
        target_r = r_s
        target_c = c_s + delta_col

        # Check if target coordinate is within grid bounds
        if 0 <= target_r < height and 0 <= target_c < width:
            # Check if the target coordinate falls within the target region's pixels
            if (target_r, target_c) in target_coords_set:
                # Update the output grid
                output_grid[target_r, target_c] = pattern_color

    # Return the modified grid as a list of lists
    return output_grid.tolist()
