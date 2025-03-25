"""
The transformation rule is based on identifying sequences and contiguous blocks of colors and applying context-dependent replacement rules. The context includes the colors of neighboring pixels, the position of the pixel within the grid (e.g., top rows, left edge), and the presence of specific color sequences.

1.  **Identify Contiguous Blocks:** Find all contiguous blocks of the same color.

2.  **Identify Sequences:** Find all horizontal and vertical sequences of 2 or more colors.

3.  **Apply Replacement Rules:**
    *   **Example 1 (Generalized):**
        * Within contiguous blocks of color '8' adjacent to color '9', '8' is replaced based on the *relative position* of '8' and '9' within their respective blocks. If the '8' is on the edge of *its* block that borders a block of '9', then it may change to '3' or '4'. Further examples needed to determine exact rule for '3' versus '4'.
        *   '9's that are adjacent to '8' blocks are transformed into a '3'.
    *   **Example 2 (Generalized):**
        *   In the top three rows, '5' is replaced by '2'.
        *   On the left edge, '5' is replaced by '1', and '2' is replaced by '1'.
        *   The sequence '5, 2, 2' is replaced by '2, 2, 2'.
        *   The sequence '5, 2, 1' is replaced by '1, 1, 1'.
    *   **Example 3 (Generalized):**
        *   If '7' is followed by '8' (horizontally), the '7' becomes '6'.
        *   If '8' is followed by '7' (horizontally), the '8' becomes... (needs further clarification) The '7' following the '8' becomes '5'.
        *   The sequence '7, 8, 7' becomes '6, 8, 5'.

4.  **Priority:** If multiple rules apply to a pixel, positional rules (top row, left edge) take precedence, followed by sequence rules, then adjacency.
"""

import numpy as np

def get_contiguous_blocks(grid):
    """
    Identifies contiguous blocks of the same color in the grid.
    Returns a list of blocks, where each block is a list of (row, col) coordinates.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    blocks = []

    def dfs(row, col, color, block):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color
        ):
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
                if len(block) > 0:
                    blocks.append(block)
    return blocks

def get_sequences(grid):
    """
    Identifies horizontal and vertical sequences of 2 or more colors.
    Returns a list of sequences, where each sequence is a list of (row, col) coordinates.
    """
    rows, cols = grid.shape
    sequences = []

    # Horizontal sequences
    for r in range(rows):
        for c in range(cols - 1):
            sequence = [(r, c)]
            for c2 in range(c + 1, cols):
                if grid[r, c2] != grid[r, c2-1]:
                    if len(sequence) >= 2:
                        sequences.append(sequence)
                    sequence = [(r,c2)]
                else:
                    sequence.append((r,c2))
            if len(sequence) >=2:
                sequences.append(sequence)


    # Vertical sequences
    for c in range(cols):
        for r in range(rows - 1):
            sequence = [(r,c)]
            for r2 in range(r+1, rows):
                if grid[r2,c] != grid[r2-1, c]:
                    if len(sequence) >= 2:
                        sequences.append(sequence)
                    sequence = [(r2,c)]
                else:
                    sequence.append((r2,c))
            if len(sequence) >= 2:
                sequences.append(sequence)

    return sequences


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Identify Contiguous Blocks
    blocks = get_contiguous_blocks(input_grid)

    # Identify Sequences
    sequences = get_sequences(input_grid)
    
    # Apply Replacement Rules
    for r in range(rows):
        for c in range(cols):
            # Example 2: Positional Rules
            if r < 3:  # Top three rows
                if output_grid[r, c] == 5:
                    output_grid[r, c] = 2
            if c == 0:  # Left edge
                if output_grid[r, c] == 5:
                    output_grid[r, c] = 1
                elif output_grid[r, c] == 2:
                    output_grid[r, c] = 1

            # Example 2: sequence rules
            if c+2 < cols:
                if input_grid[r,c] == 5 and input_grid[r,c+1] == 2 and input_grid[r,c+2] == 2:
                    output_grid[r,c] = 2
                    output_grid[r,c+1] = 2
                    output_grid[r,c+2] = 2
                if input_grid[r,c] == 5 and input_grid[r,c+1] == 2 and input_grid[r,c+2] == 1:
                    output_grid[r,c] = 1
                    output_grid[r,c+1] = 1
                    output_grid[r,c+2] = 1
            if r+2 < rows:
                if input_grid[r,c] == 5 and input_grid[r+1,c] == 2 and input_grid[r+2,c] == 1:
                    output_grid[r,c] = 1
                    output_grid[r+1,c] = 1
                    output_grid[r+2,c] = 1

            # Example 3: sequence rules
            if c+1 < cols:
                if input_grid[r,c] == 7 and input_grid[r,c+1] == 8:
                    output_grid[r,c] = 6
                if input_grid[r,c] == 8 and input_grid[r,c+1] == 7:
                    output_grid[r,c+1] = 5 # apply to 7
            if c+2 < cols:
                if input_grid[r,c] == 7 and input_grid[r,c+1] == 8 and input_grid[r,c+2] == 7:
                    output_grid[r,c] = 6
                    output_grid[r,c+2] = 5

            # Example 1: Adjacency Rules (within blocks)
            if input_grid[r,c] == 8:
                for block in blocks:
                    if (r,c) in block:
                        #check neighbors in other blocks
                        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < rows and 0 <= nc < cols:
                                adjacent_to_9 = False
                                for other_block in blocks:
                                    if input_grid[nr,nc] == 9 and (nr,nc) in other_block:
                                        adjacent_to_9 = True
                                        break #found a 9
                                if adjacent_to_9:
                                  output_grid[r,c] = 4 #simplified for now, needs refinement.

            if input_grid[r,c] == 9:
              for block in blocks:
                if (r,c) in block:
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if input_grid[nr,nc] == 8:
                                output_grid[r,c] = 3 #simplified
                                break

    return output_grid