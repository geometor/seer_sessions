```python
import numpy as np
from collections import Counter

def get_most_common_color(grid_part):
    """Finds the most common color in a grid or subgrid."""
    if grid_part.size == 0:
        return -1 # Or handle appropriately, maybe raise error
    colors, counts = np.unique(grid_part, return_counts=True)
    return colors[np.argmax(counts)]

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Identifies two distinct regions in the input grid based on background color.
    One region (Source) has a background of gray (6) or azure (8).
    The other region (Target) has a different background color.
    The output grid has the dimensions and background color of the Target Region,
    with the non-background shapes from the Source Region overlaid onto it
    at their original relative positions.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape

    region1 = None
    region2 = None
    bg1 = -1
    bg2 = -1
    output_shape = None
    is_vertical_split = False

    # Check for vertical split
    # Ensure width > 1 before attempting split
    if width > 1:
        mid_w = width // 2
        # Check if width is even and if the regions actually span half the width
        # This handles cases like 1x2 grids correctly.
        if width % 2 == 0:
            part1 = input_grid[:, :mid_w]
            part2 = input_grid[:, mid_w:]
            bg1_candidate = get_most_common_color(part1)
            bg2_candidate = get_most_common_color(part2)
            # Check if backgrounds are different and define the split if so
            if bg1_candidate != bg2_candidate:
                 region1 = part1
                 region2 = part2
                 bg1 = bg1_candidate
                 bg2 = bg2_candidate
                 output_shape = region1.shape # or region2.shape, they are same
                 is_vertical_split = True


    # If not a vertical split, check for horizontal split
    # Ensure height > 1 before attempting split
    if region1 is None and height > 1:
        mid_h = height // 2
        # Ensure height is even and check regions
        if height % 2 == 0:
            part1 = input_grid[:mid_h, :]
            part2 = input_grid[mid_h:, :]
            bg1_candidate = get_most_common_color(part1)
            bg2_candidate = get_most_common_color(part2)
            # Check if backgrounds are different and define the split if so
            if bg1_candidate != bg2_candidate:
                region1 = part1
                region2 = part2
                bg1 = bg1_candidate
                bg2 = bg2_candidate
                output_shape = region1.shape # or region2.shape, they are same
                is_vertical_split = False # It's horizontal

    # If no split identified (e.g., 1x1 grid or uniform grid), return input?
    # Based on examples, a split should always be identifiable.
    if region1 is None:
        # This case shouldn't happen based on the training examples provided.
        # If it could, we'd need a rule for it. Let's assume a split is always found.
        # Maybe raise an error or return the input unchanged if necessary.
        print("Warning: Could not determine split.")
        return input_grid # Placeholder for undefined behavior

    # Identify Source (6 or 8 background) and Target regions
    source_region = None
    target_region = None
    source_bg = -1
    target_bg = -1

    if bg1 in [6, 8]:
        source_region = region1
        source_bg = bg1
        target_region = region2
        target_bg = bg2
    elif bg2 in [6, 8]:
        source_region = region2
        source_bg = bg2
        target_region = region1
        target_bg = bg1
    else:
        # This case also shouldn't happen based on examples.
        print("Warning: Could not identify source region (background 6 or 8).")
        return input_grid # Placeholder

    # Create the output grid filled with the target background color
    output_grid = np.full(output_shape, target_bg, dtype=int)

    # Iterate through the source region and copy non-background pixels (shapes)
    r_max, c_max = source_region.shape
    for r in range(r_max):
        for c in range(c_max):
            pixel_color = source_region[r, c]
            # If the pixel color is not the source background color, it's part of a shape
            if pixel_color != source_bg:
                # Copy the shape pixel to the same relative position in the output grid
                output_grid[r, c] = pixel_color

    return output_grid.tolist() # Return as list of lists per spec

```