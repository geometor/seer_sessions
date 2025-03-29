```python
import numpy as np

"""
Identify distinct, contiguous rectangular blocks of uniform color in the input grid. 
Determine the top-left corner coordinate and color for each block.
Construct an output grid where each cell corresponds to a block in the input.
The dimensions of the output grid are determined by the number of unique row and column indices of the block top-left corners.
The color of a cell in the output grid is the color of the corresponding block in the input grid, maintaining the relative spatial arrangement.
"""

def find_block_representatives(grid):
    """
    Identifies the top-left corner and color of each contiguous block.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of tuples, where each tuple is (row, col, color)
              representing the top-left corner and color of a block.
    """
    rows, cols = grid.shape
    representatives = []
    visited_coords = set() # Keep track of coordinates already part of a found block top-left

    for r in range(rows):
        for c in range(cols):
            # Check if this coordinate is already identified as a top-left
            if (r, c) in visited_coords:
                continue

            color = grid[r, c]
            is_top_left = True

            # Check if the cell above has the same color
            if r > 0 and grid[r - 1, c] == color:
                is_top_left = False
            # Check if the cell to the left has the same color
            elif c > 0 and grid[r, c - 1] == color:
                 is_top_left = False

            if is_top_left:
                representatives.append((r, c, color))
                visited_coords.add((r,c)) # Add this top-left coord to avoid re-adding if logic was different

    # Alternative, more robust block finding (though simpler works here):
    # Could implement a flood fill or connected components algorithm if blocks weren't guaranteed rectangular.
    # For this specific task, checking top and left neighbors is sufficient because blocks are solid rectangles.

    return representatives


def transform(input_grid):
    """
    Transforms the input grid by identifying color blocks and creating a smaller
    grid representing those blocks.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier handling
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape

    # 1. Identify all distinct, contiguous blocks and their top-left corners/colors
    block_reps = find_block_representatives(grid_np)

    # Handle empty input or no blocks found (though unlikely in ARC)
    if not block_reps:
        return [] # Or return appropriate empty representation

    # 2. Collect all unique top-leftmost row and column indices
    unique_rows = sorted(list(set(r for r, c, color in block_reps)))
    unique_cols = sorted(list(set(c for r, c, color in block_reps)))

    # 3. Determine the output grid dimensions
    output_rows = len(unique_rows)
    output_cols = len(unique_cols)

    # 4. Create the output grid (initialize with a placeholder, e.g., -1 or 0)
    # Using numpy for easy assignment, will convert back later
    output_grid_np = np.full((output_rows, output_cols), -1, dtype=int) # Use -1 to ensure all cells are filled

    # 5. Map row and column indices to output grid indices for quick lookup
    row_map = {r: i for i, r in enumerate(unique_rows)}
    col_map = {c: i for i, c in enumerate(unique_cols)}

    # 6. Populate the output grid
    for r, c, color in block_reps:
        out_r = row_map[r]
        out_c = col_map[c]
        output_grid_np[out_r, out_c] = color

    # 7. Convert the numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid
```