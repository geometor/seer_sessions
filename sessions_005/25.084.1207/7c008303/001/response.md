```python
import numpy as np

"""
Identifies a horizontal and a vertical line of azure (8) pixels which divide the input grid.
Locates a 6x6 'pattern' region (containing green (3) and white (0) pixels) and a 2x2 'color key' region (containing four distinct non-azure, non-white pixels) in diagonally opposite quadrants relative to the intersection of the azure lines.
Generates a 6x6 output grid. The output grid is conceptually divided into four 3x3 quadrants (top-left, top-right, bottom-left, bottom-right).
Each cell of the 2x2 color key corresponds to one of these output quadrants (color_key[0,0] -> top-left, color_key[0,1] -> top-right, color_key[1,0] -> bottom-left, color_key[1,1] -> bottom-right).
For each pixel in the 6x6 pattern region: if the pixel is green (3), the corresponding pixel in the output grid is colored with the key color associated with its quadrant; if the pixel is white (0), the corresponding output pixel remains white (0).
"""

def transform(input_grid):
    """
    Transforms the input grid based on pattern recoloring guided by a color key.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed 6x6 output grid, or an empty
        list if the expected structures (lines, pattern, key) are not found.
    """
    grid = np.array(input_grid, dtype=int)
    H, W = grid.shape

    # 1. Find Separators (Azure lines)
    hr = -1 # Row index of horizontal line
    vc = -1 # Column index of vertical line

    # Find horizontal line (row filled with 8s)
    for r in range(H):
        if np.all(grid[r, :] == 8):
            hr = r
            break

    # Find vertical line (column filled with 8s)
    for c in range(W):
        if np.all(grid[:, c] == 8):
            vc = c
            break

    # Check if separators were found
    if hr == -1 or vc == -1:
        # This case should ideally not happen for valid task inputs
        # but returning an empty list for robustness.
        # print("Error: Azure separator lines not found.")
        return [] 

    # 2. Locate Pattern (6x6, green/white) and Color Key (2x2, distinct colors) Grids
    pattern_grid = None
    color_key_grid = None

    # Define potential top-left corners for pattern (6x6) and key (2x2)
    # based on their position relative to the intersection (hr, vc).
    # The pattern grid must be exactly 6x6 and the key grid 2x2.
    # We check the four quadrants relative to the intersection (hr, vc):
    # Top-Left (TL): row < hr, col < vc
    # Top-Right (TR): row < hr, col > vc
    # Bottom-Left (BL): row > hr, col < vc
    # Bottom-Right (BR): row > hr, col > vc
    pattern_corners = {
        "TL": (hr - 6, vc - 6), "TR": (hr - 6, vc + 1),
        "BL": (hr + 1, vc - 6), "BR": (hr + 1, vc + 1),
    }
    key_corners = {
        "TL": (hr - 2, vc - 2), "TR