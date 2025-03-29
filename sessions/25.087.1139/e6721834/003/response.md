```python
import numpy as np
from collections import Counter

"""
Identifies two distinct regions in the input grid based on background color by splitting the grid in half either vertically or horizontally.
One region (Source) has a background color of magenta (6) or azure (8).
The other region (Target) has a different background color.
The output grid has the dimensions of one half and the background color of the Target Region.
The non-background shapes from the Source Region are overlaid onto the output grid
at the exact same coordinates they occupied within the Source Region.
"""

def get_most_common_color(grid_part: np.ndarray) -> int:
    """Finds the most common color in a grid or subgrid, ignoring empty grids."""
    if grid_part.size == 0:
        # Return a value indicating no dominant color or handle as error
        # In this context, splits usually won't create empty grids unless input is very small.
        return -1 # Using -1 to indicate issue or empty grid
    colors, counts = np.unique(grid_part, return_counts=True)
    # Handle cases where all pixels are the same (only one color)
    if colors.size == 1:
        return colors[0]
    # Find the color with the highest count
    most_common_color = colors[np.argmax(counts)]
    return int(most_common_color) # Ensure return type is standard int


def transform(input_grid_list: list) -> list:
    """
    Transforms the input grid according to the rules:
    1. Split the grid into two halves (vertically or horizontally).
    2. Identify Source (BG 6 or 8) and Target halves.
    3. Create output grid with Target BG and dimensions of one half.
    4. Copy non-BG pixels from Source to the output grid at the same coordinates.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    height, width = input_grid.shape

    region1 = None
    region2 = None
    bg1 = -1
    bg2 = -1
    output_shape = None
    split_found = False

    # Step 1 & 2: Determine split and identify regions/backgrounds
    # Check for vertical split first
    if width > 1 and width % 2 == 0:
        mid_w = width // 2
        part1 = input_grid[:, :mid_w]
        part2 = input_grid[:, mid_w:]
        bg1_candidate = get_most_common_color(part1)
        bg2_candidate = get_most_common_color(part2)

        # Check if backgrounds are different, confirming the split
        if bg1_candidate != bg2_candidate and bg1_candidate != -1 and bg2_candidate != -1:
             region1 = part1
             region2 = part2
             bg1 = bg1_candidate
             bg2 = bg2_candidate
             output_shape = region1.shape # output shape is shape of one half
             split_found = True

    # If no vertical split found, check for horizontal split
    if not split_found and height > 1 and height % 2 == 0:
        mid_h = height // 2
        part1 = input_grid[:mid_h, :]
        part2 = input_grid[mid_h:, :]
        bg1_candidate = get_most_common_color(part1)
        bg2_candidate = get_most_common_color(part2)

        # Check if backgrounds are different, confirming the split
        if bg1_candidate != bg2_candidate and bg1_candidate != -1 and bg2_candidate != -1:
            region1 = part1
            region2 = part2
            bg1 = bg1_candidate
            bg2 = bg2_candidate
            output_shape = region1.shape # output shape is shape of one half
            split_found = True # Set flag even though it's horizontal

    # Handle case where no split is identified (should not happen with valid inputs based on examples)
    if not split_found:
        # Default behavior or error handling needed if this case is possible
        # Based on the task description and examples, a split should always be identifiable.
        # Returning input grid might be a fallback, but it's likely an error state.
        # For now, let's assume valid inputs always allow a split.
        # If this needs robust handling, raise an error or return input:
        # raise ValueError("Could not determine grid split based on background colors.")
         print(f"Warning: Could not determine split for input grid shape {input_grid.shape}")
         # Attempting a default? Maybe just return the input? Unclear.
         # Let's stick to the observed pattern: a split exists.
         # If bg1 or bg2 are still -1, this indicates an issue.
         if bg1 == -1 or bg2 == -1:
              raise ValueError("Failed to identify backgrounds for split regions.")


    # Step 2 (cont.): Identify Source (BG 6 or 8) and Target regions
    source_region = None
    target_region = None
    source_bg = -1
    target_bg = -1

    if bg1 in [6, 8]: # 6=magenta, 8=azure
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
        # This case implies neither region has BG 6 or 8, contradicting task rules.
        raise ValueError("Could not identify source region (background 6 or 8).")

    # Step 3: Create the base output grid
    # output_shape is already determined during split detection
    output_grid = np.full(output_shape, target_bg, dtype=int)

    # Step 4: Transfer shapes from Source Region to Output Grid
    # Iterate through the source region dimensions
    r_max, c_max = source_region.shape
    for r in range(r_max):
        for c in range(c_max):
            pixel_color = source_region[r, c]
            # If the pixel color is not the source background color, it's part of a shape
            if pixel_color != source_bg:
                # Copy the shape pixel to the *exact same coordinates* in the output grid
                output_grid[r, c] = pixel_color

    # Step 5: Return the completed output grid as a list of lists
    return output_grid.tolist()
```