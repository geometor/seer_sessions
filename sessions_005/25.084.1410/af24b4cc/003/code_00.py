import numpy as np
from collections import Counter

"""
Transforms a 9x10 input grid containing six 2x2 colored blocks into a 4x5 output grid.

1. Initialize a 4x5 output grid filled with white (0).
2. Identify six specific 2x2 blocks in the input grid based on their top-left coordinates:
   (1,1), (1,4), (1,7), (5,1), (5,4), (5,7).
3. For each input block, determine its representative color using the following rules:
   a. Count the frequency of each non-white (non-zero) color within the 2x2 block.
   b. Find the highest frequency.
   c. If only one color has this highest frequency, choose that color.
   d. If two distinct non-white colors share the highest frequency (which must be 2):
      i. Let the block pixels be [[TL, TR], [BL, BR]].
      ii. Check if the block matches the pattern: TL == TR == A and BL == BR == B, where A != B.
      iii. If this pattern exists AND A > B, choose color A.
      iv. Otherwise (if the pattern doesn't match, or if A <= B), choose the color of the bottom-right pixel (BR).
   e. If there are no non-white colors, choose white (0).
4. Map the representative color of each input block to a specific pixel in the output grid:
   - Input block at (1,1) -> Output pixel at (1,1)
   - Input block at (1,4) -> Output pixel at (1,2)
   - Input block at (1,7) -> Output pixel at (1,3)
   - Input block at (5,1) -> Output pixel at (2,1)
   - Input block at (5,4) -> Output pixel at (2,2)
   - Input block at (5,7) -> Output pixel at (2,3)
5. Return the completed 4x5 output grid.
"""

def determine_block_color(block):
    """
    Determines the representative color for a 2x2 block based on frequency
    and specific tie-breaking rules.

    Args:
        block (np.array): A 2x2 numpy array representing the block.

    Returns:
        int: The selected representative color.
    """
    # Flatten the block and get pixel values
    pixels = block.flatten().tolist()
    tl, tr, bl, br = pixels[0], pixels[1], pixels[2], pixels[3]

    # Count frequencies of non-white colors
    counts = Counter(p for p in pixels if p != 0)

    # Handle case with no non-white colors
    if not counts:
        return 0

    # Find the maximum frequency
    max_freq = 0
    for color in counts:
        if counts[color] > max_freq:
            max_freq = counts[color]

    # Get colors with the maximum frequency
    most_frequent_colors = [color for color, freq in counts.items() if freq == max_freq]

    # If only one color has the max frequency, return it
    if len(most_frequent_colors) == 1:
        return most_frequent_colors[0]
    # Handle tie-breaking (exactly two colors, frequency 2)
    elif len(most_frequent_colors) == 2 and max_freq == 2:
        # Check for the [[A, A], [B, B]] pattern
        is_AABB_pattern = (tl == tr and bl == br and tl != bl)
        if is_AABB_pattern:
            color_A = tl
            color_B = bl
            # Apply the special tie-breaker: if pattern is AABB and A > B, return A
            if color_A > color_B:
                return color_A
            # Otherwise (A <= B), fall through to the default tie-breaker

        # Default tie-breaker: return the bottom-right pixel's color
        return br
    else:
         # This case should ideally not be reached given the problem constraints
         # but as a fallback, return the bottom-right color.
         return br


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to numpy array for easier slicing
    input_np = np.array(input_grid, dtype=int)

    # Initialize the 4x5 output grid with white (0)
    output_grid = np.zeros((4, 5), dtype=int)

    # Define the mapping from input block top-left corners to output pixel coordinates
    mapping = {
        (1, 1): (1, 1),
        (1, 4): (1, 2),
        (1, 7): (1, 3),
        (5, 1): (2, 1),
        (5, 4): (2, 2),
        (5, 7): (2, 3),
    }

    # Process each block according to the mapping
    for (r_in, c_in), (r_out, c_out) in mapping.items():
        # Extract the 2x2 block from the input grid
        block = input_np[r_in:r_in+2, c_in:c_in+2]

        # Determine the representative color for the block
        selected_color = determine_block_color(block)

        # Place the selected color into the output grid at the mapped coordinates
        output_grid[r_out, c_out] = selected_color

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()