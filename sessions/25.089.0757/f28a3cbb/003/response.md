```python
import numpy as np
from collections import Counter

"""
Determine the dimensions (Height H, Width W) of the input grid.
Identify the color of the top-left pixel (input[0,0]) as the Top-Left Color (TL_Color).
Identify the color of the bottom-right pixel (input[H-1, W-1]) as the Bottom-Right Color (BR_Color).
Count the frequency of each color in the input grid. Determine the Background Color (BG_Color) as the color with the highest frequency, excluding TL_Color and BR_Color.
Create a new output grid of the same dimensions (H x W) and fill it entirely with the BG_Color.
Fill the 4x4 square region from row 0 to row 3 and from column 0 to column 3 in the output grid with TL_Color.
Fill the 4x4 square region from row H-4 to row H-1 and from column W-4 to W-1 in the output grid with BR_Color.
Return the modified output grid.
"""

def find_background_color(grid, tl_color, br_color):
    """
    Finds the most frequent color in the grid, excluding the specified
    top-left and bottom-right corner colors.
    """
    # Flatten the grid to a 1D list of colors
    flat_grid = grid.flatten()

    # Count the frequency of each color
    color_counts = Counter(flat_grid)

    # Remove corner colors from counts if they exist
    if tl_color in color_counts:
        del color_counts[tl_color]
    if br_color in color_counts:
        del color_counts[br_color]

    # If after removing corner colors, there are still colors left...
    if color_counts:
        # Find the most frequent among the remaining colors
        # .most_common(1) returns a list like [(color, count)]
        bg_color = color_counts.most_common(1)[0][0]
        return bg_color
    else:
        # Fallback case: If all pixels were corner colors (unlikely in ARC context but safe)
        # Re-count all colors and pick the most frequent overall.
        # Or, handle specific logic if needed. Here, we'll just pick one arbitrarily if this edge case happens.
        # Let's recalculate and pick the most frequent overall if no other colors exist.
        full_counts = Counter(flat_grid)
        if full_counts:
            return full_counts.most_common(1)[0][0]
        else:
            return 0 # Default to black/white if grid is empty


def transform(input_grid):
    """
    Transforms the input grid by expanding the 3x3 corner blocks to 4x4
    blocks in the output, using the most frequent non-corner color as background.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Determine the dimensions (Height H, Width W) of the input grid.
    H, W = input_np.shape

    # Identify the color of the top-left pixel as the Top-Left Color (TL_Color).
    tl_color = input_np[0, 0]

    # Identify the color of the bottom-right pixel as the Bottom-Right Color (BR_Color).
    br_color = input_np[H-1, W-1]

    # Determine the Background Color (BG_Color).
    bg_color = find_background_color(input_np, tl_color, br_color)

    # Create a new output grid of the same dimensions (H x W) and fill it entirely with the BG_Color.
    output_grid = np.full((H, W), bg_color, dtype=int)

    # Fill the 4x4 square region in the top-left corner with TL_Color.
    # Rows 0 to 3 (exclusive of 4), Columns 0 to 3 (exclusive of 4)
    output_grid[0:4, 0:4] = tl_color

    # Fill the 4x4 square region in the bottom-right corner with BR_Color.
    # Rows H-4 to H-1 (exclusive of H), Columns W-4 to W-1 (exclusive of W)
    # Ensure indices do not go below 0 for small grids (though ARC min size is 1x1, corner logic implies >= 4x4 usually)
    start_row = max(0, H - 4)
    start_col = max(0, W - 4)
    output_grid[start_row:H, start_col:W] = br_color

    # Return the modified output grid as a list of lists
    return output_grid.tolist()
```