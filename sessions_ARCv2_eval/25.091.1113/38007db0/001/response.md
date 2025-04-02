```python
import numpy as np
from collections import Counter

"""
Transformation Rule:

1.  **Identify Grid Structure:** The input grid is composed of smaller, equally-sized square subgrids arranged in a larger grid format. These subgrids are separated by single-pixel-thick lines of a uniform 'frame_color'.
2.  **Extract Subgrids:** Determine the size of the subgrids and extract each subgrid from the input. Maintain their original row arrangement.
3.  **Identify Unique Pattern per Row:** For each row of subgrids in the input:
    a.  Compare all subgrids within that row.
    b.  Count the occurrences of each distinct subgrid pattern.
    c.  If one pattern appears exactly once in the row, select the subgrid containing that unique pattern.
    d.  If all patterns in the row are identical (i.e., only one distinct pattern exists, repeated multiple times), select the first (leftmost) subgrid from that row.
4.  **Construct Output:** Create an output grid with the same height as the input grid but with a width equal to the width of a single subgrid. Vertically stack the selected subgrids (one from each original row) into this output grid, preserving the vertical arrangement and spacing defined by the subgrid size.
"""

def find_subgrid_size(grid):
    """
    Determines the size of the subgrids by finding the second occurrence
    of the frame color along the top row and first column.
    Assumes the top-left pixel (0,0) is part of the frame.
    """
    frame_color = grid[0, 0]
    height, width = grid.shape

    # Find horizontal size
    h_size = -1
    for c in range(1, width):
        if grid[0, c] == frame_color:
            h_size = c
            break
    
    # Find vertical size (should be the same for square subgrids)
    v_size = -1
    for r in range(1, height):
        if grid[r, 0] == frame_color:
            v_size = r
            break

    # Basic check if sizes were found and match
    if h_size == -1 or v_size == -1:
        # Fallback or error: maybe only one subgrid row/column
        if h_size != -1: return h_size
        if v_size != -1: return v_size
        # If neither works, assume full grid is the 'subgrid' (or handle error)
        # Based on examples, we expect grid lines. If not found, maybe size is the full dimension?
        # Let's assume grid lines are always present for multiple subgrids.
        # If only one subgrid vertically, v_size will be height. If only one horizontally, h_size is width.
        if h_size == -1 and v_size == -1: # Only one subgrid total
             return max(height, width) # Or specific logic if needed
        elif h_size == -1: # Only one column
             h_size = width 
        elif v_size == -1: # Only one row
             v_size = height

    if h_size != v_size:
         # This case shouldn't happen based on examples, but good to note
         print(f"Warning: Non-square subgrid structure detected? h_size={h_size}, v_size={v_size}")
         # Decide how to handle: maybe use the smaller, larger, or average? Or stick to h_size? Let's use h_size for now.

    # We add 1 because the index `c` or `r` is the position *of* the second frame line.
    # The size includes the pixels up to *before* that line. E.g., if line is at index 7, size is 7.
    # Let's re-evaluate: if grid[0,0] is frame and grid[0,7] is the next frame pixel, 
    # the subgrid content spans columns 0 through 6, which is a size of 7. So h_size itself is correct.
    # Similarly for v_size.
    
    # Correction: The logic seems to find the *start* of the next subgrid border.
    # If grid[0,0] is border and grid[0,7] is the next border pixel, the first subgrid
    # spans indices 0 to 6 horizontally. Size = 7. So the found index IS the size.
    subgrid_dim = h_size # Assuming square based on examples
    if subgrid_dim <= 0: # Handle cases where no second line was found
        subgrid_dim = max(width, height) if width == height else -1 # Fallback for single block or error
        if subgrid_dim == -1:
             raise ValueError("Could not determine subgrid size reliably.")
             
    return subgrid_dim


def extract_subgrids(grid, subgrid_size):
    """Extracts all subgrids into a list of lists."""
    height, width = grid.shape
    num_rows = height // subgrid_size
    num_cols = width // subgrid_size
    
    subgrids = []
    for r in range(num_rows):
        row_subgrids = []
        for c in range(num_cols):
            top = r * subgrid_size
            left = c * subgrid_size
            subgrid = grid[top : top + subgrid_size, left : left + subgrid_size]
            row_subgrids.append(subgrid)
        subgrids.append(row_subgrids)
    return subgrids

def select_subgrid_for_row(subgrid_row):
    """Selects the unique or first subgrid from a list of subgrids."""
    # Convert numpy arrays to tuples for hashing
    subgrid_tuples = [tuple(map(tuple, sg)) for sg in subgrid_row]
    
    # Count occurrences
    counts = Counter(subgrid_tuples)
    
    # Find unique subgrid
    unique_sg_tuple = None
    for sg_tuple, count in counts.items():
        if count == 1:
            unique_sg_tuple = sg_tuple
            break
            
    # If a unique one was found, find its original index to return the numpy array
    if unique_sg_tuple is not None:
        for i, sg_tuple in enumerate(subgrid_tuples):
            if sg_tuple == unique_sg_tuple:
                return subgrid_row[i]
    else:
        # If no unique one, return the first subgrid
        return subgrid_row[0]


def transform(input_grid):
    """
    Transforms the input grid by selecting unique or first subgrids from each row
    and stacking them vertically.
    """
    input_np = np.array(input_grid)
    height, width = input_np.shape

    # 1. Identify Grid Structure - Determine subgrid size
    try:
        subgrid_size = find_subgrid_size(input_np)
        if subgrid_size <= 0 or height % subgrid_size != 0 or width % subgrid_size != 0:
             # Fallback or default if structure unclear - treat as single block
             print(f"Warning: Grid dimensions {height}x{width} not divisible by deduced subgrid size {subgrid_size}. Treating as single block.")
             # For this specific task, an invalid structure likely means it cannot be solved by this logic.
             # However, let's try a simple fallback: If only one 'row' of subgrids exists, maybe return the unique/first?
             # Or maybe the task implies valid structure always. Let's assume valid structure.
             # Re-evaluate find_subgrid_size if issues persist.
             if subgrid_size <= 0 :
                  raise ValueError("Cannot determine subgrid size.") # More appropriate than fallback for this task
    except ValueError as e:
         print(f"Error in grid structure analysis: {e}")
         # Handle error case, maybe return input or empty grid? Let's return input.
         # return input_np 
         # Let's reconsider: returning input is likely wrong. Maybe an empty grid of required size?
         # The problem expects a transformation. Let's try to proceed assuming full grid if size fails.
         # This seems risky. Let's stick to raising the error if size determination fails.
         raise e


    # 2. Extract Subgrids
    # Check if dimensions are valid before extracting
    if height % subgrid_size != 0 or width % subgrid_size != 0:
        raise ValueError(f"Input dimensions ({height}x{width}) not divisible by subgrid size ({subgrid_size})")
        
    all_subgrids = extract_subgrids(input_np, subgrid_size)
    num_subgrid_rows = len(all_subgrids)

    if num_subgrid_rows == 0:
         # Handle empty input case or error
         return np.array([[]], dtype=int) # Return empty grid
         
    # 3. Process Rows & Select Subgrids
    selected_subgrids = []
    for subgrid_row in all_subgrids:
        if not subgrid_row: # Skip empty rows if they somehow occur
            continue
        selected = select_subgrid_for_row(subgrid_row)
        selected_subgrids.append(selected)

    # 4. Construct Output Grid
    output_height = height # Same height as input
    output_width = subgrid_size # Width of one subgrid
    output_grid = np.zeros((output_height, output_width), dtype=input_np.dtype)

    # 5. Populate Output Grid
    for i, sg in enumerate(selected_subgrids):
        # Calculate top-left corner for placing the subgrid
        row_start = i * subgrid_size
        # Check bounds before placing
        if row_start + subgrid_size <= output_height:
             output_grid[row_start : row_start + subgrid_size, 0 : subgrid_size] = sg
        else:
             # This shouldn't happen if num_subgrid_rows * subgrid_size == height
             print(f"Warning: Subgrid placement exceeds output bounds. Row {i}, Start {row_start}")


    return output_grid.tolist() # Return as list of lists per ARC standard

```