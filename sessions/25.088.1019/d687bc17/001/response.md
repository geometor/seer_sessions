```python
import numpy as np

"""
Transformation Rule:

1.  Identify the colors of the four border sides (top, bottom, left, right, excluding corners) of the input grid.
2.  Initialize an output grid of the same size as the input, copying the border pixels exactly. Set all interior pixels to white (0).
3.  Iterate through each interior pixel of the *input* grid.
4.  If an interior pixel's color matches the color of the top border, place a pixel of that color in the output grid at the topmost interior row (row 1) in the same column.
5.  If an interior pixel's color matches the color of the bottom border, place a pixel of that color in the output grid at the bottommost interior row (row height-2) in the same column.
6.  If an interior pixel's color matches the color of the left border, place a pixel of that color in the output grid at the leftmost interior column (column 1) in the same row.
7.  If an interior pixel's color matches the color of the right border, place a pixel of that color in the output grid at the rightmost interior column (column width-2) in the same row.
8.  Interior pixels whose color does not match any of the four border side colors are effectively removed (they remain white in the output grid).
9.  If a destination cell in the output grid receives pixels from multiple source cells (e.g., two different pixels moving to the same border spot), the last one processed according to the iteration order will overwrite previous ones. (Based on the examples, it appears only one pixel moves to a specific border-adjacent cell).
"""

def transform(input_grid):
    """
    Moves interior pixels orthogonally to the border side that matches their color.
    Non-matching pixels are removed.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # Initialize output_grid with white (0)
    output_grid = np.zeros_like(input_grid_np)

    # Copy the border from input to output
    output_grid[0, :] = input_grid_np[0, :]  # Top row
    output_grid[-1, :] = input_grid_np[-1, :] # Bottom row
    output_grid[:, 0] = input_grid_np[:, 0]  # Left column
    output_grid[:, -1] = input_grid_np[:, -1] # Right column

    # Get border colors (use a pixel from the middle of each side to avoid corners)
    # Handle edge case of 3x3 grid where middle might be corner
    top_border_col_idx = width // 2 if width > 1 else 0
    bottom_border_col_idx = width // 2 if width > 1 else 0
    left_border_row_idx = height // 2 if height > 1 else 0
    right_border_row_idx = height // 2 if height > 1 else 0

    top_color = input_grid_np[0, top_border_col_idx]
    bottom_color = input_grid_np[height - 1, bottom_border_col_idx]
    left_color = input_grid_np[left_border_row_idx, 0]
    right_color = input_grid_np[right_border_row_idx, width - 1]

    # Iterate through interior pixels of the input grid
    # Interior is from row 1 to height-2 and col 1 to width-2
    if height > 2 and width > 2: # Check if there is an interior
        for r in range(1, height - 1):
            for c in range(1, width - 1):
                pixel_color = input_grid_np[r, c]

                # Skip white pixels
                if pixel_color == 0:
                    continue

                # Check if pixel color matches any border color and move it
                if pixel_color == top_color:
                    output_grid[1, c] = pixel_color
                elif pixel_color == bottom_color:
                    output_grid[height - 2, c] = pixel_color
                elif pixel_color == left_color:
                    output_grid[r, 1] = pixel_color
                elif pixel_color == right_color:
                    output_grid[r, width - 2] = pixel_color
                # If pixel_color does not match any border, it's implicitly removed
                # because the output grid was initialized to white (0).

    return output_grid.tolist()
```