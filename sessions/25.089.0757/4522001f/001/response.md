```python
import numpy as np

"""
The transformation rule operates on a 3x3 input grid containing white (0), red (2), and green (3) pixels. It produces a 9x9 output grid.

1.  **Initialization**: The output grid is initialized as a 9x9 grid filled with white (0).
2.  **Identify Key Pixels**: Locate the position (row, column) of the red pixel (2) in the input grid. Check if any green pixels (3) exist in the input grid.
3.  **Determine Output Pattern**: The position of the red pixel determines which pair of potential 4x4 green blocks will be drawn in the output grid, *if* green pixels are present in the input. There are four potential 4x4 block locations, defined by their top-left corners:
    *   Top-Left (TL): (1, 1)
    *   Top-Right (TR): (1, 5)
    *   Bottom-Left (BL): (5, 1)
    *   Bottom-Right (BR): (5, 5)
    *   The selection rule is based on the parity of the sum of the red pixel's coordinates (r_red + c_red):
        *   If (r_red + c_red) is even, the diagonal pair TL (1,1) and BR (5,5) is selected.
        *   If (r_red + c_red) is odd, the anti-diagonal pair TR (1,5) and BL (5,1) is selected.
4.  **Draw Blocks**: If at least one green pixel exists in the input grid, draw 4x4 blocks of green (3) in the output grid at the selected locations. Each block fills the area from `(r_start, c_start)` to `(r_start+3, c_start+3)`.
5.  **Output**: Return the modified 9x9 output grid.
"""

def find_pixel_locations(grid, color_value):
    """Finds all locations (row, col) of a specific color_value in the grid."""
    locations = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color_value:
                locations.append((r, c))
    return locations

def draw_block(grid, r_start, c_start, height, width, color_value):
    """Draws a block of a given color in the grid."""
    grid[r_start:r_start+height, c_start:c_start+width] = color_value

def transform(input_grid):
    """
    Transforms the input grid based on the location of the red pixel
    and the presence of green pixels.
    """
    input_np = np.array(input_grid, dtype=int)
    output_height, output_width = 9, 9
    
    # Initialize output_grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Find the red pixel location (assuming exactly one)
    red_locations = find_pixel_locations(input_np, 2)
    if not red_locations:
        # Handle case where no red pixel is found (optional, based on problem constraints)
        # For now, return the empty grid or raise an error
        # Based on examples, a red pixel is always present.
        return output_grid.tolist() 
    r_red, c_red = red_locations[0]

    # Check for the presence of any green pixels
    green_locations = find_pixel_locations(input_np, 3)
    has_green = len(green_locations) > 0

    # Proceed only if green pixels are present
    if has_green:
        # Define potential block top-left corners
        block_locations = {
            "TL": (1, 1),
            "TR": (1, 5),
            "BL": (5, 1),
            "BR": (5, 5),
        }
        
        # Determine which blocks to select based on red pixel position parity
        selected_keys = []
        if (r_red + c_red) % 2 == 0:
            selected_keys = ["TL", "BR"]
        else:
            selected_keys = ["TR", "BL"]

        # Draw the selected blocks
        block_size = 4
        green_color = 3
        for key in selected_keys:
            r_start, c_start = block_locations[key]
            draw_block(output_grid, r_start, c_start, block_size, block_size, green_color)

    return output_grid.tolist()
```