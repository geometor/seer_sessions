```python
import numpy as np
import copy

"""
This transformation rearranges rectangular blocks of non-zero digits within a 2D grid.
The process involves:
1. Identifying all distinct, contiguous, rectangular blocks of non-zero digits in the input grid.
2. Determining the height, width, digit value, and original leftmost column for each block.
3. Finding the maximum row index occupied by any non-zero cell in the original grid (anchor bottom row).
4. Sorting the identified blocks primarily by ascending height, and secondarily by ascending width.
5. Reconstructing the output grid by stacking the sorted blocks vertically. The stack starts from the bottom, with the lowest block's bottom edge aligned with the anchor bottom row found in step 3. Each subsequent block is placed directly above the previous one, maintaining its original leftmost column and width. The rest of the grid is filled with the background digit (0).
"""

def _find_blocks(grid):
    """
    Identifies contiguous rectangular blocks of non-zero numbers in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: A tuple containing:
            - list: A list of dictionaries, where each dictionary represents a block
                    and contains 'value', 'height', 'width', 'left_col', 
                    'top_row_orig', 'bottom_row_orig'.
            - int: The maximum row index occupied by any non-zero cell (anchor_bottom_row).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []
    max_bottom_row = -1

    for r in range(rows):
        for c in range(cols):
            # Check if the cell is non-zero and not yet visited
            if grid[r, c] != 0 and not visited[r, c]:
                value = grid[r, c]
                # Find the boundaries of this block using BFS/Flood Fill logic implicitly
                q = [(r, c)]
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c
                block_cells = set([(r,c)])

                while q:
                    row, col = q.pop(0)

                    # Update boundaries
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Explore neighbors (only checking direct right and down is sufficient for rectangles)
                    # More robust: check all 4 neighbors if shapes aren't guaranteed rectangular
                    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]: 
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == value:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            block_cells.add((nr,nc))

                # For strictly rectangular blocks, max/min r/c are enough.
                # If complex shapes were allowed, we'd need to track all cells.
                # Let's assume rectangles based on examples.
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                
                # Correctness check: Ensure all cells within bounds actually belong to the block
                is_rectangular = True
                count = 0
                for br in range(min_r, max_r + 1):
                    for bc in range(min_c, max_c + 1):
                        if grid[br, bc] == value:
                            count += 1
                            visited[br, bc] = True # Ensure all inner cells are marked visited
                        else:
                            # This handles L-shapes etc. - might need adjustment based on definition
                            # For the given examples, this check might not be strictly necessary
                            # if we assume perfect rectangular input blocks.
                            pass 
                #if count != height * width: # Check if it's a solid rectangle
                #    is_rectangular = False
                    # This part is tricky, the definition of block might need refinement.
                    # Sticking to the simple boundary box based on BFS extent for now.


                blocks.append({
                    'value': value,
                    'height': height,
                    'width': width,
                    'left_col': min_c,
                    'top_row_orig': min_r,
                    'bottom_row_orig': max_r
                })
                # Update the overall maximum bottom row
                max_bottom_row = max(max_bottom_row, max_r)

    return blocks, max_bottom_row


def transform(input_grid):
    """
    Rearranges blocks in the grid based on height and then width.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed grid.
    """
    # Convert input to numpy array for easier slicing and manipulation
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # Initialize output grid with background color (0)
    output_array = np.zeros_like(input_array)

    # 1. Identify all non-zero blocks and their properties
    # 3. Find the overall bottom-most row occupied by any block
    blocks, anchor_bottom_row = _find_blocks(input_array)

    # If no blocks found or anchor invalid, return the empty grid
    if not blocks or anchor_bottom_row == -1:
        return output_array.tolist()

    # 4. Sort blocks: primary key = height (ascending), secondary key = width (ascending)
    sorted_blocks = sorted(blocks, key=lambda b: (b['height'], b['width']))

    # 5. Reconstruct the grid by placing sorted blocks
    # Iterate from bottom-up placement, so process sorted list in reverse
    current_bottom_row = anchor_bottom_row
    for block in reversed(sorted_blocks):
        # Calculate the top row for placing this block in the output grid
        height = block['height']
        width = block['width']
        value = block['value']
        left_col = block['left_col']
        
        # Ensure placement doesn't go out of bounds (especially top row < 0)
        if current_bottom_row < 0:
              # This case shouldn't happen with valid inputs and logic, but good practice
              print(f"Warning: Trying to place block {value} above grid boundary.")
              continue # Skip block if it can't fit logically

        top_row_place = current_bottom_row - height + 1
        
        # Ensure top_row is not negative
        if top_row_place < 0:
             print(f"Warning: Block {value} starting at original row {block['top_row_orig']} adjusted to start at row 0.")
             # Adjust height if it would go off the top. This might not be the desired behavior.
             # Alternative: stop placing? Or does anchor guarantee space? 
             # Based on examples, anchor seems to guarantee space downwards.
             # Let's assume it fits within the grid height based on the anchor logic.
             # If top_row_place is negative, it implies the stack is taller than the grid allows starting from anchor_bottom_row.
             # The prompt logic implies stacking *upwards*, so we might clip or error.
             # Clipping might be safer:
             clipped_height = height + top_row_place # height - abs(top_row_place)
             actual_top_row = 0
             if clipped_height <= 0: continue # Skip if fully clipped
             print(f"Block {value} height {height} clipped to {clipped_height} due to grid boundary.")
             height = clipped_height # Use clipped height
             top_row_place = actual_top_row

        # Calculate right column for placement
        right_col_place = left_col + width -1
        
        # Ensure placement is within grid bounds horizontally
        if left_col < 0 or right_col_place >= cols:
            print(f"Warning: Block {value} placement horizontal bounds invalid [{left_col}:{right_col_place+1}]. Skipping.")
            continue # Skip block if horizontal placement is invalid

        # Place the block onto the output grid
        output_array[top_row_place : current_bottom_row + 1, left_col : right_col_place + 1] = value

        # Update the bottom row for the *next* block to be placed *above* this one
        current_bottom_row = top_row_place - 1

    # Convert the result back to list of lists
    return output_array.tolist()

```