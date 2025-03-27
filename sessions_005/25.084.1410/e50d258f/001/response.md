```python
import numpy as np
from collections import deque

"""
Identifies all separate contiguous blocks of non-white (0) pixels in the input grid using 4-way connectivity.
Counts the number of red (2) pixels within each block.
Selects the block containing the maximum number of red pixels.
Extracts the rectangular subgrid corresponding to the bounding box of the selected block from the input grid.
The extracted subgrid becomes the output.
"""

def find_blocks(grid):
    """
    Finds all contiguous blocks of non-background pixels.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents a block
              and contains 'coords' (list of (row, col) tuples) and
              'bbox' (min_row, min_col, max_row, max_col).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []
    background_color = 0

    for r in range(rows):
        for c in range(cols):
            # If pixel is not background and not visited, start BFS
            if grid[r, c] != background_color and not visited[r, c]:
                coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    coords.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, background color, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != background_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                blocks.append({
                    'coords': coords,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return blocks

def transform(input_grid):
    """
    Transforms the input grid based on the described rules.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    grid_np = np.array(input_grid, dtype=int)
    target_color = 2 # Red

    # 1. Identify all separate contiguous blocks of non-white pixels
    blocks = find_blocks(grid_np)

    if not blocks:
        return [] # Return empty grid if no blocks found

    max_target_count = -1
    selected_block = None

    # 2. For each block, count the target color (red) pixels
    # 3. Determine which block has the highest count
    for block in blocks:
        current_target_count = 0
        for r, c in block['coords']:
            if grid_np[r, c] == target_color:
                current_target_count += 1

        if current_target_count > max_target_count:
            max_target_count = current_target_count
            selected_block = block
        # Simple tie-breaking: first block found with max count wins

    if selected_block is None:
         # This case implies all blocks had 0 red pixels, or no blocks.
         # If there are blocks but none have red, the first block is implicitly selected by loop logic if max count remains -1
         # Let's refine: if max_target_count is still -1 or 0 after checking all blocks, but blocks exist,
         # maybe we need a different rule? The examples *always* have red.
         # Assuming based on examples: there will be at least one red pixel in one block.
         # If truly no red pixels exist, the logic would select the first block encountered. Let's stick with that for now.
         if blocks:
             selected_block = blocks[0] # Default to first block if no red found
         else:
             return [] # No blocks at all

    # 4. Extract the rectangular subgrid (bounding box) of the selected block
    min_r, min_c, max_r, max_c = selected_block['bbox']
    output_grid_np = grid_np[min_r : max_r + 1, min_c : max_c + 1]

    # Convert numpy array back to list of lists for the final output
    output_grid = output_grid_np.tolist()

    return output_grid
```