import numpy as np
from collections import Counter

"""
Transforms the input grid based on pixel comparisons between specific columns, using a logic primarily derived from Example 2.

1.  Determines the background color by finding the most frequent color in the input grid.
2.  Initializes the output grid as a copy of the input grid.
3.  Defines fixed column indices: key column (index 1), source column (index 8), primary target column (index 3), and secondary target column (index 15).
4.  Iterates through each row of the grid:
    a.  Retrieves the color from the key column (`key_color`) and the source column (`source_color`) for the current row in the input grid.
    b.  Compares `key_color` with `source_color` and the determined `background_color`.
    c.  If `key_color` equals `source_color` OR `key_color` equals the `background_color`:
        i.  The pixel in the primary target column (index 3) of the output grid for the current row is set to `source_color`.
    d.  Otherwise (if `key_color` is different from `source_color` AND `key_color` is different from the `background_color`):
        i.  The pixel in the secondary target column (index 15) of the output grid for the current row is set to `source_color`.
    e.  After processing the condition, the pixel in the source column (index 8) of the output grid for the current row is replaced with the `background_color`.
5.  Returns the modified output grid.

Note: This logic was observed to work correctly for Example 2 of the task but failed significantly on Example 1. This suggests the rule might be incomplete or context-dependent, possibly related to grid structure or the nature of background colors, which differs between the examples.
"""

def find_most_frequent_color(grid_np):
    """
    Finds the most frequent color in a numpy grid, ignoring color 0 (white)
    unless it's the only color present.

    Args:
        grid_np (np.ndarray): The input grid as a numpy array.

    Returns:
        int: The most frequent non-white color value. Returns 0 if the grid
             contains only white or is empty. Returns the most frequent color
             if multiple colors are equally frequent (numpy default behavior).
    """
    if grid_np.size == 0:
        return 0 # Default for empty grid

    # Flatten the grid and count occurrences of each color
    colors, counts = np.unique(grid_np.flatten(), return_counts=True)

    # If only one color exists, return it
    if len(colors) == 1:
      return colors[0]

    # Find the index of the most frequent color *ignoring white (0)*
    most_frequent_color = 0
    max_count = 0
    # Zip colors and counts and sort by count descending
    sorted_colors_by_count = sorted(zip(colors, counts), key=lambda x: x[1], reverse=True)

    for color, count in sorted_colors_by_count:
        if color != 0:
            most_frequent_color = color
            break # Found the most frequent non-white color
    else:
        # If loop finishes without break, means only white was present (or grid empty handled above)
        # but we handled the single color case earlier. This path is for multiple colors where non-zero exist
        # but if somehow all were zero, default to 0. If only white existed, return 0.
        # Check if only white exists
         if np.all(grid_np == 0):
             most_frequent_color = 0
         elif len(colors)>1 and colors[0] == 0 and counts[0]>max_count : # if white is most frequent
             # find the next most frequent color
             if len(colors) > 1:
                 most_frequent_color = colors[1] # let's try second most frequent in this case. Needs more robust logic maybe.
             else: # Only white exists
                 most_frequent_color = 0
         elif len(colors) == 1 and colors[0] == 0: # only white exists
            most_frequent_color = 0
         elif colors[0] != 0 : # Most frequent is not white
             most_frequent_color = colors[0]


    # Fallback if something unexpected happens or only white exists
    if most_frequent_color == 0 and np.any(grid_np != 0):
       # If we defaulted to 0 but there are other colors, just pick the most frequent overall
       colors_overall, counts_overall = np.unique(grid_np.flatten(), return_counts=True)
       max_count_idx_overall = np.argmax(counts_overall)
       most_frequent_color = colors_overall[max_count_idx_overall]


    # Let's refine the background logic: Most frequent non-zero. If all zero, then zero.
    unique_colors, counts = np.unique(grid_np, return_counts=True)
    non_zero_mask = unique_colors != 0
    non_zero_colors = unique_colors[non_zero_mask]
    non_zero_counts = counts[non_zero_mask]

    if non_zero_colors.size > 0:
        # Find the index of the maximum count among non-zero colors
        max_count_idx = np.argmax(non_zero_counts)
        # Return the color corresponding to the maximum count
        return non_zero_colors[max_count_idx]
    elif unique_colors.size > 0 : # Only zero is present
         return 0
    else: # Grid is empty
        return 0


def transform(input_grid):
    """
    Applies the transformation rule derived primarily from Example 2.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)

    # Determine the background color by finding the most frequent non-zero color
    background_color = find_most_frequent_color(input_np)

    # Initialize output_grid as a copy of the input grid
    output_np = np.copy(input_np)

    # Define column indices based on the task's observed pattern (from Ex 2)
    key_col_idx = 1
    source_col_idx = 8
    target_col_1_idx = 3  # Destination if key matches source OR key is background
    target_col_2_idx = 15 # Destination if key differs from source AND key is not background

    # Get the number of rows in the grid
    num_rows = input_np.shape[0]

    # Process each row independently
    for r in range(num_rows):
        # Check if column indices are valid for the current grid shape
        if key_col_idx >= input_np.shape[1] or \
           source_col_idx >= input_np.shape[1] or \
           target_col_1_idx >= input_np.shape[1] or \
           target_col_2_idx >= input_np.shape[1]:
            continue # Skip row if columns are out of bounds

        # Get the colors from the key and source columns for the current row
        key_color = input_np[r, key_col_idx]
        source_color = input_np[r, source_col_idx]

        # Apply the conditional logic to determine the destination column
        if key_color == source_color or key_color == background_color:
            # Condition met: Move to the first target column
            destination_column = target_col_1_idx
        else:
            # Condition not met: Move to the second target column
            # (Implicitly: key_color != source_color AND key_color != background_color)
            destination_column = target_col_2_idx

        # Place the source pixel's color into the determined destination column in the output grid
        output_np[r, destination_column] = source_color

        # Replace the pixel in the original source column location with the background color
        output_np[r, source_col_idx] = background_color

    # Convert the resulting numpy array back to a list of lists for the final output format
    return output_np.tolist()