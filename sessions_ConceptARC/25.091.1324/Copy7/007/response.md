```python
import numpy as np
from scipy.ndimage import label, find_objects
from collections import Counter
import copy

"""
Transforms the input grid by copying a pattern from a source object to a target location.

The transformation follows these steps:
1. Identify all connected groups of non-background (0) pixels (objects) using 8-way connectivity.
2. If there are fewer than two objects, return the original grid unchanged.
3. Identify the leftmost object (minimum starting column) as the 'source' and the rightmost object (maximum starting column) as the 'target'.
4. Analyze the source object:
    a. Count the occurrences of each non-background color within the source object.
    b. Determine the most frequent non-background color ('frame_color').
    c. Determine the numerically smallest non-background color that is *not* the frame_color ('pattern_color'). If no such color exists (e.g., the source only has one non-background color), return the original grid.
5. Find all pixel coordinates within the source object that contain the 'pattern_color'. These are the 'pattern_pixels'.
6. Calculate the horizontal translation required to move the pattern from the source's starting column to the target's starting column: `delta_col = target.min_col - source.min_col`.
7. Create a copy of the input grid to serve as the output grid.
8. For each pattern pixel coordinate (r_s, c_s):
    a. Calculate the corresponding target coordinate: (target_r, target_c) = (r_s, c_s + delta_col).
    b. Check if the target coordinate (target_r, target_c) is within the bounds of the grid.
    c. If it is within bounds, update the *output grid* at (target_r, target_c) with the 'pattern_color', overwriting any existing value at that location.
9. Return the modified output grid.
"""

def find_regions(grid_np, background_color=0):
    """
    Finds connected regions (objects) of non-background pixels using 8-way connectivity.

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
    # Use 8-way connectivity (default for label)
    labeled_array, num_features = label(mask)

    regions = []
    if num_features == 0:
        return regions

    # Use find_objects to get bounding slices, then extract exact coordinates
    object_slices = find_objects(labeled_array)

    for i in range(num_features): # Labels are 1-based, index is 0-based
        obj_label = i + 1
        # Handle case where find_objects returns None for a label (shouldn't happen here)
        if object_slices[i] is None: continue 
        obj_slice = object_slices[i]

        # Extract coordinates ONLY for this object's label within its slice
        coords_relative = np.argwhere(labeled_array[obj_slice] == obj_label)

        # Convert relative coordinates back to absolute grid coordinates
        coords_absolute = [(r + obj_slice[0].start, c + obj_slice[1].start) for r, c in coords_relative]

        if not coords_absolute:
            continue # Should not happen if find_objects worked correctly but good practice

        coords_set = set(coords_absolute)
        rows = [r for r, c in coords_absolute]
        cols = [c for r, c in coords_absolute]

        regions.append({
            'coords': coords_set,
            'min_row': np.min(rows),
            'max_row': np.max(rows),
            'min_col': np.min(cols),
            'max_col': np.max(cols),
            'label': obj_label # Keep track of the label if needed later
        })

    return regions

def get_region_colors_and_counts(grid_np, region_coords, background_color=0):
    """
    Counts the occurrences of non-background colors within a region's coordinates.

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
        # Ensure coordinates are within bounds (should be, but defensive check)
        if 0 <= r < grid_np.shape[0] and 0 <= c < grid_np.shape[1]:
            color = grid_np[r, c]
            if color != background_color:
                color_counts[color] += 1
    return color_counts


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original input
    output_grid = np.copy(input_np)
    height, width = input_np.shape
    background_color = 0

    # 1. Identify all connected non-background regions (objects)
    regions = find_regions(input_np, background_color)

    # 2. Check if there are at least two objects (source and target)
    if len(regions) < 2:
        # Not enough objects to define source and target
        return output_grid.tolist() 

    # 3. Identify Source (leftmost) and Target (rightmost) regions
    # Sort regions based on their minimum column index (left-to-right)
    regions.sort(key=lambda r: r['min_col'])
    source_region = regions[0]
    # Use the region with the largest min_col as target, robust to >2 regions
    target_region = max(regions, key=lambda r: r['min_col']) 
    # Alternative: target_region = regions[-1] if sorting is guaranteed stable

    # 4. Get colors and counts in the source region
    source_colors_counts = get_region_colors_and_counts(input_np, source_region['coords'], background_color)

    # Check if the source region actually contains non-background colors
    if not source_colors_counts:
        # Source region is empty or only background? Should not happen with find_regions logic
         return output_grid.tolist() 

    # 5. Determine Source Frame Color (most frequent non-background color)
    # Handle cases with only one color or ties (take the first one from most_common)
    most_common = source_colors_counts.most_common(1)
    if not most_common: # Should be covered by check above, but defensive
         return output_grid.tolist()
    source_frame_color = most_common[0][0] # color value

    # 6. Determine Pattern Color (smallest non-background color != frame color)
    pattern_color = None
    # Get unique non-background colors present and sort them numerically
    sorted_unique_colors = sorted(source_colors_counts.keys())

    # Iterate through sorted colors to find the smallest one that isn't the frame color
    for color in sorted_unique_colors:
        if color != source_frame_color:
            pattern_color = color
            break # Found the smallest different color

    # If no pattern color found (e.g., only one non-bg color exists in source)
    if pattern_color is None:
        # No distinct pattern color to copy
         return output_grid.tolist() 

    # 7. Find Pattern Pixels in the source region
    pattern_pixels = []
    for r, c in source_region['coords']:
        # Check the color at the coordinate in the original input grid
        if input_np[r, c] == pattern_color:
            pattern_pixels.append((r, c))

    # If no pixels of the pattern color were found (shouldn't happen if pattern_color was set)
    if not pattern_pixels:
        return output_grid.tolist() 

    # 8. Calculate the horizontal translation vector (difference in starting columns)
    delta_col = target_region['min_col'] - source_region['min_col']

    # 9. Copy pattern pixels to the target location, overwriting existing pixels
    for r_s, c_s in pattern_pixels:
        # Calculate potential target coordinates
        target_r = r_s
        target_c = c_s + delta_col

        # 10. Check if target coordinate is within the overall grid bounds
        if 0 <= target_r < height and 0 <= target_c < width:
            # Update the output grid with the pattern color, overwriting whatever was there
            output_grid[target_r, target_c] = pattern_color

    # Return the modified grid as a standard Python list of lists
    return output_grid.tolist()
```