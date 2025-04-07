```python
import numpy as np
import sys

# Helper function to find the unique solid rectangular block of a given color
def find_unique_solid_block(grid, color):
    """
    Finds the bounding box of the unique solid rectangular block of a given color.
    
    Args:
        grid (np.array): The input grid.
        color (int): The target color.
        
    Returns:
        tuple: (r_min, r_max, c_min, c_max) coordinates of the block, inclusive.
        Returns None if no such block is found, or if it's not unique, 
        not solid, or not rectangular.
    """
    h, w = grid.shape
    # Find all locations of the target color
    locations = np.argwhere(grid == color)
    if locations.shape[0] == 0:
        return None # Color not present

    visited = np.zeros_like(grid, dtype=bool)
    found_blocks = []

    # Iterate through potential starting points of blocks
    for r_init, c_init in locations:
        if visited[r_init, c_init]:
            continue

        # Use Breadth-First Search (BFS) to find all connected pixels of the same color
        q = [(r_init, c_init)]
        visited[r_init, c_init] = True
        block_pixels = set([(r_init, c_init)])
        
        # Efficient queue implementation using list index
        head = 0
        while head < len(q):
            r, c = q[head]
            head += 1
            
            # Explore 4 neighbors (up, down, left, right)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                # Check bounds and if neighbor is the target color and not visited
                if 0 <= nr < h and 0 <= nc < w and \
                   grid[nr, nc] == color and not visited[nr, nc]:
                    visited[nr, nc] = True
                    q.append((nr, nc))
                    block_pixels.add((nr, nc))

        # After BFS, determine the bounding box of the found connected component
        if not block_pixels: continue # Should not happen if locations is not empty
        
        min_r = min(r for r, c in block_pixels)
        max_r = max(r for r, c in block_pixels)
        min_c = min(c for r, c in block_pixels)
        max_c = max(c for r, c in block_pixels)

        # Check if this component forms a solid rectangle
        # Calculate expected number of pixels in the bounding box
        block_h = max_r - min_r + 1
        block_w = max_c - min_c + 1
        expected_pixels = block_h * block_w
        
        # If the number of pixels found by BFS equals the number of pixels in the bounding box, it's a solid rectangle
        is_solid_rectangle = (len(block_pixels) == expected_pixels)

        if is_solid_rectangle:
            found_blocks.append((min_r, max_r, min_c, max_c))

    # The task logic relies on finding exactly one such block
    if len(found_blocks) == 1:
        return found_blocks[0]
    else:
        # Handle cases where the assumption fails (0 or >1 blocks found)
        if len(found_blocks) == 0:
             # This case means the color exists but not in a solid rectangular shape
             print(f"Warning: No solid rectangular block of color {color} found.", file=sys.stderr)
        else:
             # This case means multiple solid rectangular blocks were found
             print(f"Warning: Found {len(found_blocks)} solid rectangular blocks of color {color}. Expected 1.", file=sys.stderr)
        return None # Indicate failure to find the required unique block


# Define the color constant
AZURE = 8

"""
Transformation Rule Description:
1. Locate the unique, solid, rectangular block composed entirely of azure pixels (color 8) within the input grid.
2. Determine the column range (start and end columns) spanned by this azure block.
3. Identify the row index of the top edge of the azure block (`r_top`).
4. Select three specific rows from the input grid based on their position relative to `r_top`:
   - The row 2 positions above the azure block (`r_top - 2`).
   - The row 8 positions above the azure block (`r_top - 8`).
   - The row 9 positions above the azure block (`r_top - 9`).
5. Extract segments (slices) from these three selected rows. Each segment uses the column range determined in step 2.
6. Construct the output grid by stacking these three row segments vertically. The order of stacking is:
   - Top row: Segment from `r_top - 2`.
   - Middle row: Segment from `r_top - 8`.
   - Bottom row: Segment from `r_top - 9`.
7. If the unique solid azure block cannot be found, or if the calculated row indices fall outside the grid boundaries, the transformation fails (indicated by returning a minimal grid).
"""

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule based on a unique azure block.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid. 
                         Returns [[0]] if the transformation rule cannot be applied.
    """
    # Convert input to numpy array for easier slicing and manipulation
    input_array = np.array(input_grid, dtype=int)
    h, w = input_array.shape

    # 1. Find the unique solid rectangular block of azure (8)
    block_coords = find_unique_solid_block(input_array, AZURE)

    # 7. Handle failure case: block not found or not unique/solid/rectangular
    if block_coords is None:
        print(f"Error: Could not find the required unique solid azure block.", file=sys.stderr)
        # Return a 1x1 black grid as an error indicator, common in ARC viewers.
        return [[0]] 

    # Extract block coordinates
    r_min, r_max, c_min, c_max = block_coords
    # 3. Identify top row index
    r_top = r_min 

    # 4. Define the target row indices relative to the block's top row
    row_idx_1 = r_top - 2
    row_idx_2 = r_top - 8
    row_idx_3 = r_top - 9

    target_rows = [row_idx_1, row_idx_2, row_idx_3]
    
    # 7. Handle failure case: Check if target rows are within grid bounds
    if not (0 <= row_idx_1 < h and 0 <= row_idx_2 < h and 0 <= row_idx_3 < h):
        print(f"Error: Target row indices {target_rows} calculated relative to azure block are out of bounds (grid height {h}).", file=sys.stderr)
        return [[0]] # Return error grid

    # 5. Extract the row slices using the block's column range (step 2 implied here)
    try:
        slice1 = input_array[row_idx_1, c_min : c_max + 1]
        slice2 = input_array[row_idx_2, c_min : c_max + 1]
        slice3 = input_array[row_idx_3, c_min : c_max + 1]
    except IndexError:
        # This catch is a safeguard, though bounds checks should prevent it.
        print(f"Error: Failed to extract slices using azure block columns {c_min}-{c_max} from rows {target_rows}.", file=sys.stderr)
        return [[0]] # Return error grid

    # 6. Construct the output grid by stacking the slices in the specified order
    output_array = np.vstack([slice1, slice2, slice3])

    # Convert the resulting numpy array back to a list of lists format
    output_grid = output_array.tolist()

    return output_grid
```