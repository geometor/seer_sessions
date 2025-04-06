"""
Identify all separate connected regions (blobs) of non-zero numbers in the input grid using 4-way connectivity (up, down, left, right).
Calculate the size of each blob by counting its non-zero cells.
Find the blob with the largest size. If there's a tie, the first one encountered during a top-to-bottom, left-to-right scan is chosen implicitly.
Determine the minimum bounding box (min_row, max_row, min_col, max_col) enclosing this largest blob.
Extract the rectangular sub-grid from the input corresponding to this bounding box. The output is this extracted section, including any original zero values within the box.
"""

import numpy as np
from collections import deque

def _find_largest_blob_and_bbox(grid: np.ndarray) -> tuple[int, int, int, int]:
    """
    Finds the largest blob of non-zero cells and its bounding box.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A tuple (min_row, max_row, min_col, max_col) for the largest blob.
        Returns (0, 0, 0, 0) if the grid is empty or contains only zeros.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    max_blob_size = -1
    best_bbox = (0, 0, 0, 0) # min_row, max_row, min_col, max_col

    for r in range(rows):
        for c in range(cols):
            # If this cell is non-zero and not visited, start a BFS
            if grid[r, c] != 0 and not visited[r, c]:
                q = deque([(r, c)])
                visited[r, c] = True
                current_blob_size = 0
                blob_cells = [] # Store coordinates to calculate bbox later
                
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    
                    # This cell is part of the current blob
                    blob_cells.append((row, col))
                    current_blob_size += 1 # Count only non-zero cells for size comparison
                    
                    # Update bounding box for this cell
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check bounds and if neighbor is non-zero and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Finished exploring this blob, compare its size
                if current_blob_size > max_blob_size:
                    max_blob_size = current_blob_size
                    best_bbox = (min_r, max_r, min_c, max_c)
                    
    # Handle edge case where no non-zero cells were found
    if max_blob_size == -1 and rows > 0 and cols > 0:
         return (0, 0, 0, 0) # Or perhaps signal an error / empty output? Examples suggest non-empty. Let's assume valid input. If grid IS all zero, what should happen? Let's assume input guarantees at least one non-zero blob if output is expected. If the largest blob is just one cell, bbox is (r,r,c,c).
    elif max_blob_size == -1: # Empty grid case
        return (0, -1, 0, -1) # Indices that lead to empty slice


    return best_bbox


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by extracting the bounding box of the largest
    connected non-zero blob.
    """
    # Handle empty input case
    if not input_grid or not input_grid[0]:
        return []

    # Convert to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)

    # Find the bounding box of the largest blob
    min_row, max_row, min_col, max_col = _find_largest_blob_and_bbox(grid_np)

    # Handle case where no blob was found (e.g., all zeros or empty grid result from helper)
    if max_row < min_row or max_col < min_col:
         # This case needs clarification based on requirements for all-zero inputs.
         # Based on examples, we expect a non-empty output, suggesting inputs have blobs.
         # If an all-zero input IS possible, returning empty list might be appropriate.
         return [] 

    # Extract the subgrid defined by the bounding box
    # Note: slicing includes start index but excludes end index, so add 1 to max indices
    output_grid_np = grid_np[min_row : max_row + 1, min_col : max_col + 1]

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid