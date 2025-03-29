```python
import numpy as np
from collections import Counter, defaultdict

"""
Transformation Rule:

1.  **Analyze Grid Structure:** Identify the delimiter color (white, 0) and the grid lines formed by this color. Determine the uniform height (`cell_h`) and width (`cell_w`) of the cells (subgrids) delimited by these lines, accounting for the 1-pixel thickness of the delimiters. Identify the top-left starting coordinates (`r_start`, `c_start`) of each cell.
2.  **Extract Cell Patterns:** Iterate through each identified cell location. Extract the `cell_h` x `cell_w` subgrid (pattern) from each cell. Record each unique pattern found and the list of coordinates where it appears. Check if each pattern contains the delimiter color.
3.  **Identify Source Pattern:** Find the pattern that appears in exactly one cell location. This is the "source pattern". Store its content.
4.  **Identify Target Cells:** Examine every cell location in the input grid. A cell is identified as a "target cell" if its pattern meets two conditions:
    *   a) It is *not* the source pattern.
    *   b) Its pattern contains at least one pixel matching the delimiter color (white, 0).
5.  **Construct Output Grid:** Create the output grid as a copy of the input grid.
6.  **Apply Replacement:** Iterate through the coordinates of all identified "target cells". For each target cell location, replace the corresponding `cell_h` x `cell_w` area in the output grid with the source pattern. Cells that are not target cells (including the original source cell and any cells whose patterns do not contain the delimiter color) remain unchanged from the input grid.
7.  **Return Output:** Return the modified output grid.
"""

# --- Helper Functions ---

def find_cell_structure(grid):
    """
    Finds the delimiter color, cell dimensions (accounting for delimiter thickness),
    and cell start coordinates. Assumes a regular grid structure delimited by a
    single color (usually 0) with a thickness of 1.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (cell_h, cell_w, cell_start_rows, cell_start_cols, delimiter_color)
               Returns (None, None, None, None, -1) if no clear structure is found or grid is empty.
    """
    height, width = grid.shape
    if height == 0 or width == 0:
        return None, None, None, None, -1 # Empty grid

    delimiter_color = 0 # Standard ARC delimiter

    # Find horizontal and vertical delimiter lines
    h_lines = [r for r in range(height) if np.all(grid[r, :] == delimiter_color)]
    v_lines = [c for c in range(width) if np.all(grid[:, c] == delimiter_color)]

    # Add boundaries to the list of lines
    h_points = sorted(list(set([-1] + h_lines + [height])))
    v_points = sorted(list(set([-1] + v_lines + [width])))

    # Calculate gaps between lines (including delimiter thickness)
    h_gaps = [h_points[i+1] - h_points[i] for i in range(len(h_points)-1)]
    v_gaps = [v_points[i+1] - v_points[i] for i in range(len(v_points)-1)]

    # Filter out gaps of size 1 (the delimiter lines themselves)
    # These remaining gaps represent cell_dimension + delimiter_thickness (1)
    h_cell_gaps_with_delim = [g for g in h_gaps if g > 1]
    v_cell_gaps_with_delim = [g for g in v_gaps if g > 1]

    # Determine cell height and width by taking the most common gap size and subtracting 1 (for the delimiter)
    # If no delimiters, the cell is the whole grid
    if h_cell_gaps_with_delim:
        most_common_h_gap = Counter(h_cell_gaps_with_delim).most_common(1)[0][0]
        cell_h = most_common_h_gap - 1
    else:
        cell_h = height # No horizontal delimiters

    if v_cell_gaps_with_delim:
        most_common_v_gap = Counter(v_cell_gaps_with_delim).most_common(1)[0][0]
        cell_w = most_common_v_gap - 1
    else:
        cell_w = width # No vertical delimiters

    # Ensure calculated dimensions are positive
    if cell_h <= 0 or cell_w <= 0:
        # This might happen if the gaps are only size 1 (all delimiters) or calculation failed
         # Fallback: treat as single cell if no delimiters were found initially
        if not h_lines and not v_lines:
            return height, width, [0], [0], delimiter_color
        else: # Structure is unclear or only delimiters
             return None, None, None, None, delimiter_color


    # Determine cell start rows and columns (position after a delimiter or 0)
    # Handle case where grid starts immediately with content (no leading delimiter)
    cell_start_rows = [0] if not h_lines or h_lines[0] != 0 else []
    cell_start_rows.extend([r + 1 for r in h_lines if r + 1 < height])
    cell_start_rows = sorted(list(set(r for r in cell_start_rows if r < height))) # Ensure within bounds


    cell_start_cols = [0] if not v_lines or v_lines[0] != 0 else []
    cell_start_cols.extend([c + 1 for c in v_lines if c + 1 < width])
    cell_start_cols = sorted(list(set(c for c in cell_start_cols if c < width))) # Ensure within bounds

    # Basic sanity check
    if not cell_start_rows or not cell_start_cols:
         # If grid is only delimiter lines, or calculation failed?
         # Re-check if it should be treated as a single cell
         if cell_h == height and cell_w == width and not h_lines and not v_lines:
             return height, width, [0], [0], delimiter_color
         else: # Unexpected structure
              return None, None, None, None, delimiter_color

    # Filter start rows/cols to only include those where a cell of expected size can actually start
    valid_start_rows = [r for r in cell_start_rows if r + cell_h <= height]
    valid_start_cols = [c for c in cell_start_cols if c + cell_w <= width]

    # If filtering removed all starts, something is wrong
    if not valid_start_rows or not valid_start_cols:
         # One last check: maybe it's a single cell grid without delimiters
         if not h_lines and not v_lines and cell_h == height and cell_w == width:
             return height, width, [0], [0], delimiter_color
         return None, None, None, None, delimiter_color


    return cell_h, cell_w, valid_start_rows, valid_start_cols, delimiter_color

def get_cell_content(grid, r_start, c_start, cell_h, cell_w):
    """Extracts the content of a cell."""
    height, width = grid.shape
    # We assume r_start, c_start, cell_h, cell_w are valid based on find_cell_structure
    end_r = r_start + cell_h
    end_c = c_start + cell_w
    return grid[r_start : end_r, c_start : end_c]

def pattern_contains_delimiter(pattern_np, delimiter_color):
    """Checks if a numpy pattern array contains the delimiter color."""
    return np.any(pattern_np == delimiter_color)

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Transforms the input grid by finding a unique source pattern and copying it
    onto cells whose original pattern contained the delimiter color (white, 0).
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid_np = np.copy(input_grid_np) # Create the output grid template
    height, width = input_grid_np.shape

    # 1. Analyze Grid Structure
    cell_h, cell_w, cell_start_rows, cell_start_cols, delim_color = find_cell_structure(input_grid_np)

    # If structure is not found or grid is essentially a single cell, return original
    if cell_h is None or (len(cell_start_rows) * len(cell_start_cols) <= 1):
         return input_grid # No transformation possible/needed

    # 2. Extract Cell Patterns & Check for Delimiter
    # Stores pattern_tuple -> {'coords': list_of_(r,c), 'contains_delim': bool}
    cell_patterns_info = defaultdict(lambda: {'coords': [], 'contains_delim': False})

    for r_start in cell_start_rows:
        for c_start in cell_start_cols:
             # Extract cell content
             cell = get_cell_content(input_grid_np, r_start, c_start, cell_h, cell_w)

             # Check if extracted cell actually has the expected dimensions
             # This handles potential issues with uneven grids if find_cell_structure logic isn't perfect
             if cell.shape == (cell_h, cell_w):
                # Use tuple representation for hashing in the dictionary
                cell_tuple = tuple(map(tuple, cell))
                cell_patterns_info[cell_tuple]['coords'].append((r_start, c_start))
                # Check for delimiter only once per unique pattern
                if not cell_patterns_info[cell_tuple]['contains_delim']:
                     cell_patterns_info[cell_tuple]['contains_delim'] = pattern_contains_delimiter(cell, delim_color)


    # 3. Identify Source Pattern
    source_pattern_tuple = None
    source_pattern_np = None
    for pattern_tuple, info in cell_patterns_info.items():
        if len(info['coords']) == 1:
            source_pattern_tuple = pattern_tuple
            source_pattern_np = np.array(pattern_tuple, dtype=int)
            break # Assume only one unique pattern exists based on examples

    if source_pattern_tuple is None:
        # No unique pattern found. This might be an edge case or error.
        # Return the original grid as no clear source is defined.
        return input_grid

    # 4. Identify Target Cell Locations
    target_locations = []
    for pattern_tuple, info in cell_patterns_info.items():
        # A pattern corresponds to target locations if:
        # a) It's NOT the source pattern
        # b) It contains the delimiter color
        if pattern_tuple != source_pattern_tuple and info['contains_delim']:
            target_locations.extend(info['coords']) # Add all locations with this pattern

    # 5. & 6. Construct Output Grid & Apply Replacement
    # Output grid is already a copy. Now overwrite target locations.
    for r_start, c_start in target_locations:
        # Ensure target cell boundaries are valid before writing
        # (Should be guaranteed by how start rows/cols and locations were determined)
        if r_start + cell_h <= height and c_start + cell_w <= width:
            # Overwrite the target cell area in the output grid with the source pattern
            output_grid_np[r_start : r_start + cell_h, c_start : c_start + cell_w] = source_pattern_np

    # 7. Return the result
    return output_grid_np.tolist()
```