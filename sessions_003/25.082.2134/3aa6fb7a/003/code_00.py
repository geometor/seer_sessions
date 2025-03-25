"""
1.  **Find Azure Sequences:** Examine the input grid to identify contiguous sequences of azure (8) pixels. A sequence is defined as one or more azure pixels that are adjacent either horizontally or vertically.

2.  **Insert Blue Pixel Based on First Azure:** For each identified azure sequence, insert a single blue (1) pixel in the output grid.
    *   If the sequence is horizontal, place the blue pixel in the same row, immediately to the right of the *first* azure pixel in the sequence.
    *   If the sequence is vertical, place the blue pixel in the same column, immediately below the *first* azure pixel in the sequence.

3. **Copy background pixels**: Pixels that are not azure (8), which make up the background, are copied to the output grid. The azure pixels remain in the input grid.
"""

import numpy as np

def find_azure_sequences(grid):
    """Finds contiguous sequences of azure pixels (horizontally or vertically)."""
    rows, cols = grid.shape
    sequences = []
    visited = set()

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_sequence):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != 8:
            return

        visited.add((r, c))
        current_sequence.append((r, c))

        # Explore adjacent cells
        dfs(r + 1, c, current_sequence)  # Down
        dfs(r - 1, c, current_sequence)  # Up
        dfs(r, c + 1, current_sequence)  # Right
        dfs(r, c - 1, current_sequence)  # Left
    
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == 8 and (r,c) not in visited:
                current_sequence = []
                dfs(r,c,current_sequence)
                if len(current_sequence) > 0:
                    sequences.append(current_sequence)
    return sequences
    

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find azure sequences
    sequences = find_azure_sequences(input_grid)

    # Insert blue pixels based on the first azure pixel in each sequence
    for seq in sequences:
        first_azure = seq[0]
        r, c = first_azure

        if len(seq) > 0:
           
            # Check if it is horizontal or vertical
            is_horizontal = all(x[0] == r for x in seq)
            is_vertical = all(x[1] == c for x in seq)
            
            if is_horizontal:
                if c + 1 < cols: # Ensure we're within bounds.
                  output_grid[r, c + 1] = 1
            elif is_vertical:
                if r + 1 < rows:
                  output_grid[r + 1, c] = 1
            # Could be single, default horizontal
            elif c + 1 < cols:
                output_grid[r, c + 1] = 1

    return output_grid