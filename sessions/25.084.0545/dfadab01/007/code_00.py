"""
1.  **Anti-Diagonal Mirroring:** Create an output grid that's the mirror image of the input grid along the anti-diagonal (top-right to bottom-left).  The element at `input[r][c]` is placed at `output[c][r]`.

2.  **Recoloring Based on Output Patterns:** The following color transformations are applied based on patterns observed in the *output* grid after the mirroring:

    *   **Horizontal Blue Lines:**
        *   If a pixel is part of a horizontal line of blue (1) pixels in the output, change the pixels immediately to the left of the blue line to white (0).
        *   If a pixel is part of a horizontal line of blue (1) pixels in the output, change the pixels immediately to the right of the blue line to blue(1).
        *   If a pixel is part of a horizontal line of blue (1) pixels in the output, change the pixels immediately above the blue line to green(3).
    *   **Yellow 2x2 squares**:
        * If a pixel is part of a 2x2 square of yellow (4) pixels, then change *all* of the yellow(4) pixels in that square to orange(7).
    *   **Orange to Black:**
        * If a pixel is orange (7) change it to black (0).

3.  **No Default Preservation:** Unlike the original program, there is *no* default preservation of color. All changes are based on the above rules.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((cols, rows), dtype=int)

    # Mirror along the anti-diagonal.
    for r in range(rows):
        for c in range(cols):
            output_grid[c, r] = input_grid[r, c]

    modified_grid = output_grid.copy()

    # Recoloring based on output patterns
    for r in range(cols):
        for c in range(rows):
            # Horizontal Blue Lines
            if output_grid[r, c] == 1:
                # Check for horizontal blue line
                if c > 0 and output_grid[r, c-1] == 1:  # Check left
                   continue # already processed
                else:

                    line_length = 0
                    for i in range(c,rows):
                        if output_grid[r,i] == 1:
                            line_length += 1
                        else:
                            break


                    if line_length > 0 :
                        if c > 0: modified_grid[r, c - 1] = 0  # Left to white
                        if c + line_length < rows : modified_grid[r,c+line_length] = 1
                        if r > 0:
                          for i in range(c,c+line_length):
                            modified_grid[r - 1, i] = 3  # Above to green

            # Yellow 2x2 Squares
            if output_grid[r, c] == 4:
                if r < cols - 1 and c < rows - 1:
                    if (output_grid[r+1, c] == 4 and
                        output_grid[r, c+1] == 4 and
                        output_grid[r+1, c+1] == 4):
                        modified_grid[r, c] = 7
                        modified_grid[r+1, c] = 7
                        modified_grid[r, c+1] = 7
                        modified_grid[r+1, c+1] = 7

    # Orange to Black
    for r in range(cols):
        for c in range(rows):
            if modified_grid[r, c] == 7:
                modified_grid[r, c] = 0

    return modified_grid.tolist()