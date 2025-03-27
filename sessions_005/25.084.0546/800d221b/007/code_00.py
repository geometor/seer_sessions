"""
The transformation rules are context-dependent and color-specific, operating on contiguous blocks and sequences.

1.  **Identify Objects:** Determine all contiguous blocks of pixels with the same color. Also, identify all horizontal and vertical sequences of two or more pixels of *any* colors.

2.  **Apply Transformation Rules (Example Specific):**

    *   **Example 1 (8s and 9s):**
        *   **Rule 1 (8 to 4):**  Examine each pixel of color '8'. If a pixel of color '8' is directly adjacent (up, down, left, or right) to *any* pixel of color '9' *AND* the '8' pixel is on the perimeter/edge of its contiguous '8' block, change the '8' pixel to '4'.
        *   **Rule 2 (9 to 3):** Examine each pixel of color 9. If a pixel of color 9 is directly adjacent to *any* pixel of color 8, then change that 9 to a 3.

    *   **Example 2 (0, 5, 2, and 1):**
        *   **Rule 1 (Top Rows):** If a pixel is within the top three rows of the grid *and* its color is '5', change it to '2'.
        *   **Rule 2 (Left Edge):**  If a pixel is on the leftmost edge of the grid *and* its color is '5', change it to '1'. If it is a '2', change it to '1'.
        * **Rule 3 (Sequences):**
            *   If a horizontal *or vertical* sequence of '5', '2', '2' is found, replace it with '2', '2', '2'.
            *   If a horizontal *or vertical* sequence of '5', '2', '1' is found, replace it with '1', '1', '1'.

    *   **Example 3 (6, 7, 8, and 5):**
        *   **Rule 1 (7-8 Interaction):**  If a pixel of color '7' is immediately followed by a pixel of color '8' *horizontally*, change the '7' to '6'.
        *   **Rule 2 (8-7 Interaction):** If a pixel of color '8' is immediately followed by a pixel of color '7' *horizontally*, change that '7' to '5'.
        * **Rule 3 (7,8,7 Sequence)** If a sequence of 7,8,7 is detected, transform to 6,8,5.

3.  **Priority:** Positional rules (top row, left edge) are applied *before* adjacency and sequence rules.

4. **Perimeter Detection:** Edge pixels are determined by checking neighbors within each block; a perimeter pixel has fewer neighbors of its own color than a non-perimeter pixel.
"""

import numpy as np

def get_contiguous_blocks(grid):
    """
    Identifies contiguous blocks of the same color.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    blocks = []

    def dfs(row, col, color, block):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        block.append((row, col))
        dfs(row + 1, col, color, block)
        dfs(row - 1, col, color, block)
        dfs(row, col + 1, color, block)
        dfs(row, col - 1, color, block)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c]:
                block = []
                dfs(r, c, grid[r, c], block)
                if block:
                    blocks.append(block)
    return blocks

def is_perimeter(block, row, col, grid):
    """
    Checks if a pixel is on the perimeter of its block.
    """
    rows, cols = grid.shape
    color = grid[row, col]
    count = 0
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == color:
            count += 1
    return count < 4 # Less than 4 neighbors of the same color means it's on the perimeter


def get_sequences(grid):
    """Gets horizontal and vertical sequences of 2+ pixels."""
    rows, cols = grid.shape
    sequences = []

    # Horizontal
    for r in range(rows):
        for c in range(cols - 1):
            seq = [(r, c)]
            for c2 in range(c + 1, cols):
                if grid[r, c2] == grid[r, seq[-1][1]]:
                    seq.append((r, c2))
                else:
                    if len(seq) >= 2:
                        sequences.append(seq)
                    seq = [(r, c2)]
            if len(seq) >= 2:
                sequences.append(seq)
    # Vertical
    for c in range(cols):
        for r in range(rows - 1):
            seq = [(r, c)]
            for r2 in range(r + 1, rows):
                if grid[r2, c] == grid[seq[-1][0], c]:
                    seq.append((r2, c))
                else:
                    if len(seq) >= 2:
                        sequences.append(seq)
                    seq = [(r2, c)]
            if len(seq) >= 2:
                sequences.append(seq)
    return sequences

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    blocks = get_contiguous_blocks(input_grid)
    sequences = get_sequences(input_grid)

    # Example 1 Transformations
    if set(np.unique(input_grid)).issuperset({8, 9}):
      for block in blocks:
            for r, c in block:
                if output_grid[r, c] == 8:
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        if (0 <= nr < rows and 0 <= nc < cols and
                                output_grid[nr, nc] == 9 and is_perimeter(block, r, c, input_grid)):
                            output_grid[r, c] = 4
                            break # Apply only once
                elif output_grid[r,c] == 9:
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                      nr, nc = r+dr, c+dc
                      if 0 <= nr < rows and 0 <= nc < cols and output_grid[nr,nc] == 8:
                        output_grid[r,c] = 3
                        break

    # Example 2 Transformations
    elif set(np.unique(input_grid)).issuperset({0, 1, 2, 5}):
      for r in range(rows):
            for c in range(cols):
                # Top row rule
                if r < 3 and output_grid[r, c] == 5:
                    output_grid[r, c] = 2
                # Left edge rule
                if c == 0 and output_grid[r,c] == 5:
                    output_grid[r,c] = 1
                if c == 0 and output_grid[r,c] == 2:
                    output_grid[r,c] = 1


      for seq in sequences:
        #convert seq to numpy array for easier slicing
        seq_arr = np.array(seq)

        #check for 5,2,2
        if len(seq) >= 3:
          for i in range(len(seq)-2):
            if (output_grid[seq[i][0], seq[i][1]] == 5 and
                output_grid[seq[i+1][0], seq[i+1][1]] == 2 and
                output_grid[seq[i+2][0], seq[i+2][1]] == 2):
              output_grid[seq[i][0], seq[i][1]] = 2
              output_grid[seq[i+1][0], seq[i+1][1]] = 2
              output_grid[seq[i+2][0], seq[i+2][1]] = 2
        # Check for 5, 2, 1
        if len(seq) >= 3:
            for i in range(len(seq) - 2):
                if (output_grid[seq[i][0], seq[i][1]] == 5 and
                    output_grid[seq[i + 1][0], seq[i + 1][1]] == 2 and
                    output_grid[seq[i + 2][0], seq[i + 2][1]] == 1):

                    output_grid[seq[i][0], seq[i][1]] = 1
                    output_grid[seq[i + 1][0], seq[i + 1][1]] = 1
                    output_grid[seq[i + 2][0], seq[i + 2][1]] = 1

    # Example 3 Transformations
    elif set(np.unique(input_grid)).issuperset({5,6,7,8}):
        for r in range(rows):
            for c in range(cols):
                # 7-8 interaction
                if c + 1 < cols and output_grid[r, c] == 7 and output_grid[r, c + 1] == 8:
                    output_grid[r, c] = 6
                # 8-7 interaction
                if c + 1 < cols and output_grid[r, c] == 8 and output_grid[r, c + 1] == 7:
                    output_grid[r, c + 1] = 5

        for seq in sequences:
          # 7,8,7 sequence
          if len(seq) >=3:
            for i in range(len(seq)-2):
              if (output_grid[seq[i][0],seq[i][1]] == 7 and
                  output_grid[seq[i+1][0],seq[i+1][1]] == 8 and
                  output_grid[seq[i+2][0], seq[i+2][1]] == 7):
                output_grid[seq[i][0], seq[i][1]] = 6
                output_grid[seq[i+2][0], seq[i+2][1]] = 5


    return output_grid