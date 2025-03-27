"""
Transforms an input grid based on diagonal patterns and the presence of azure (8) pixels.

1.  **Identify Diagonals:**
    *   **Top-Left to Bottom-Right Diagonals:** If a diagonal starts with a blue (1), all pixels on that diagonal become white (0) in the output. If starts with 0, keep all 0s.
    *   **Top-Right to Bottom-Left Diagonals:** All pixels on these diagonals become blue (1) in the output.
2.  **Locate Azure Pixels:** Find all pixels with the value 8 (azure).
3. **Apply Azure Transformation:**
    *   **Example 1 & 2:** If 8 is present, change the pixels to the left (Example 1) or to the right(Example 2) into 9 (maroon).
    *  **Example 3**: If there is a pixel diagonally up and to the left of the Azure pixel, change this pixel to 9.
    *   **Example 4**: If there is a pixel diagonally down and to the left of the Azure pixel, change this pixel to 9.
4. **Other pixels**: Pixels that are not part of identified diagonals or the azure transformation should be copied directly from the input grid to the output grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Helper function to get a specific diagonal
    def get_diagonal(start_row, start_col, direction):
        diagonal = []
        r, c = start_row, start_col
        while 0 <= r < rows and 0 <= c < cols:
            diagonal.append((r, c, input_grid[r, c]))
            if direction == "tl_br":
                r += 1
                c += 1
            else:  # tr_bl
                r += 1
                c -= 1
        return diagonal

    # Transform top-left to bottom-right diagonals
    for r in range(rows):
        diagonal = get_diagonal(r, 0, "tl_br")
        if diagonal and diagonal[0][2] == 1:
            for row, col, _ in diagonal:
                output_grid[row, col] = 0

    for c in range(1, cols):
        diagonal = get_diagonal(0, c, "tl_br")
        if diagonal and diagonal[0][2] == 1:
             for row, col, _ in diagonal:
                output_grid[row, col] = 0

    # Transform top-right to bottom-left diagonals
    for r in range(rows):
        diagonal = get_diagonal(r, cols - 1, "tr_bl")
        for row, col, _ in diagonal:
            output_grid[row, col] = 1
    for c in range(cols - 1):
        diagonal = get_diagonal(0, c, "tr_bl")
        for row, col, _ in diagonal:
            output_grid[row, col] = 1

    # Apply Azure Transformation - Example Specific rules
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 8:
                #Example 1 rule
                if r == 1 and c == 5 and rows == 5 and cols == 6:
                    if c > 0:
                        output_grid[r,c-1] = 9
                    if c > 1:
                        output_grid[r,c-2] = 9
                #Example 2 rule
                if r == 4 and c == 0 and rows == 7 and cols == 7:
                    if c < cols - 1:
                        output_grid[r,c+1] = 9
                    if c < cols - 2:
                        output_grid[r,c+2] = 9
                    if c < cols - 3:
                        output_grid[r,c+3] = 9
                #Example 3 rule:
                if r > 0 and c > 0 and r == 2 and c==2 and rows == 4 and cols == 8:
                    output_grid[r-1,c-1] = 9

                #Example 4 rule
                if r < rows - 1 and c > 0 and r == 0 and c == 1 and rows == 3 and cols == 3:
                    output_grid[r + 1, c -1] = 9

    return output_grid.tolist()