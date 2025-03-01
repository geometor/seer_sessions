"""
1.  **Identify Targets:** Scan the input grid and find all single pixels that have a non-zero color (i.e., not white/0). These are our target pixels.
2.  **Create Squares, part 1**: around green pixels, build a 3x3 magenta square.
3.  **Create Squares, part 2**: around every other non-zero pixel, construct a 3 x 3 blue square.
4. **Center Pixel:** The original target pixel's color remains unchanged at the center of its new square.
5.  **Background:** All other pixels in the output grid remain white (0).
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    rows, cols = input_grid.shape

    # Identify target pixels (non-zero single pixels)
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                target_color = input_grid[r, c]

                # Determine fill color based on target color
                if target_color == 3:
                    fill_color = 6  # Magenta for green targets
                elif target_color == 8:
                    fill_color = 4
                elif target_color == 2:
                    fill_color = 1
                else:
                    fill_color = 1

                # Create 3x3 square around the target
                for i in range(max(0, r - 1), min(rows, r + 2)):
                    for j in range(max(0, c - 1), min(cols, c + 2)):
                        output_grid[i, j] = fill_color

                # Keep the original color at the center
                output_grid[r, c] = target_color
    return output_grid