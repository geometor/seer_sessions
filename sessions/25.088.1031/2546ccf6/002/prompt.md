
Previous Code:
```python
import numpy as np
from collections import Counter

"""
Handles transformations within a grid structure defined by lines of a specific color (C_grid).
The transformation rules depend on the color of the pattern found within specific cells:
1. Identify the grid structure (lines and cells).
2. Extract the content (block) and determine the primary pattern color for relevant input cells:
   - For Green (3) rule: Top-Left (TL), Middle-Left (ML), Middle-Center (MC).
   - For Blue (1) rule: Bottom-Middle (BM), Bottom-Right (BR), Extra-Bottom-Right (ExtraBR - cell below BR).
3. Initialize the output grid as a copy of the input grid.
4. Clear the content of cells involved in transformations in the output grid.
5. Apply transformations based on pattern color:
   - Green (3): Cyclically shift patterns: TL -> ML, ML -> MC, MC -> TM (Top-Middle).
   - Blue (1): Rearrange patterns: BM -> BM, BR -> BR, ExtraBR -> ExtraBM (cell below BM), BM -> ExtraBR (copy).
6. Return the modified output grid. Cells not involved in these specific color transformations remain unchanged.
"""

def find_grid_lines(grid):
    """Finds the most frequent non-background color and its line coordinates."""
    height, width = grid.shape
    non_background_colors = grid[grid != 0]

    if non_background_colors.size == 0:
        # Empty grid or all background
        return None, [], []

    # Find the most frequent non-background color, likely the grid color
    color_counts = Counter(non_background_colors)
    grid_color = color_counts.most_common(1)[0][0]

    h_lines = []
    v_lines = []

    # Find horizontal lines (rows consisting mainly of grid_color or background)
    for r in range(height):
        row = grid[r, :]
        if np.all((row == grid_color) | (row == 0)):
             # Basic check: if the row *only* contains grid or background color
             # A more robust check might count non-grid/non-bg colors
             if np.any(row == grid_color): # Ensure it's not an all-background row
                 h_lines.append(r)

    # Find vertical lines (columns consisting mainly of grid_color or background)
    for c in range(width):
        col = grid[:, c]
        if np.all((col == grid_color) | (col == 0)):
            if np.any(col == grid_color):
                v_lines.append(c)

    # Refine lines: Sometimes corners cause extra lines to be detected.
    # Assume major lines define roughly equal cells. We expect 2 horizontal and 2 vertical lines for a 3x3 grid structure.
    # A more sophisticated approach would involve looking at line thickness or spacing,
    # but for these examples, let's assume the first few detected lines are the main ones.
    # This part might need adjustment for grids with different structures.

    # Simplification: Find the indices that *separate* the grid sections.
    # Find indices where the *next* row/col is a grid line
    h_separators = [r for r in h_lines if r + 1 < height]
    v_separators = [c for c in v_lines if c + 1 < width]

    # Basic assumption: 2 main horizontal and 2 main vertical lines define the 3x3 core
    # Let's find the indices bounding the central cell as a heuristic
    if len(h_lines) >= 2 and len(v_lines) >= 2:
         # Take the lines that seem to bound the central area
         h_lines_final = sorted(list(set(h_lines))) # Unique sorted
         v_lines_final = sorted(list(set(v_lines))) # Unique sorted

         # Heuristic: Assume the lines defining the 3x3 grid are the most prominent
         # Find pairs of lines with significant gaps between them
         h_gaps = np.diff(h_lines_final)
         v_gaps = np.diff(v_lines_final)

         if len(h_gaps) > 0 and len(v_gaps) > 0:
             # Find the indices of the largest gaps, suggesting cell boundaries
             # This is still fragile. A better way is needed for general cases.
             # For now, let's assume the first two lines found are the main ones for simplicity
             # based on the examples structure (e.g., row 4 and 9, col 4 and 9/14).

             # Let's try finding the lines that bound the largest non-grid areas
             h_boundaries = [0] + h_lines_final + [height]
             v_boundaries = [0] + v_lines_final + [width]

             h_cell_dims = np.diff(h_boundaries)
             v_cell_dims = np.diff(v_boundaries)

             # Assume the first two grid lines define the main structure
             final_h = h_lines_final[:2] if len(h_lines_final) >=2 else h_lines_final
             final_v = v_lines_final[:2] if len(v_lines_final) >=2 else v_lines_final

             # Check if there's a third horizontal line for the extra rows
             if len(h_lines_final) > 2:
                 final_h.append(h_lines_final[2])

             # Check if there's a third vertical line for the extra columns (less common)
             if len(v_lines_final) > 2:
                  final_v.append(v_lines_final[2])

             return grid_color, final_h, final_v


    # Fallback if structure isn't clear
    return grid_color, sorted(list(set(h_lines))), sorted(list(set(v_lines)))


def get_cell_coords(grid_shape, h_lines, v_lines):
    """Calculates the coordinates (r_start, r_end, c_start, c_end) for each cell."""
    coords = {}
    height, width = grid_shape

    # Define row boundaries (start_inclusive, end_exclusive)
    row_starts = [0] + [h + 1 for h in h_lines]
    row_ends = [h for h in h_lines] + [height]

    # Define column boundaries
    col_starts = [0] + [v + 1 for v in v_lines]
    col_ends = [v for v in v_lines] + [width]

    # Check if dimensions make sense (enough boundaries for cells)
    if len(row_starts) < 1 or len(row_ends) < 1 or len(col_starts) < 1 or len(col_ends) < 1:
         return {} # Cannot define cells

    # Define the 3x3 main grid cells
    cell_names_3x3 = [
        ["TL", "TM", "TR"],
        ["ML", "MC", "MR"],
        ["BL", "BM", "BR"]
    ]

    for r_idx in range(min(3, len(row_starts))):
        for c_idx in range(min(3, len(col_starts))):
            # Ensure indices are valid
             if r_idx < len(row_ends) and c_idx < len(col_ends):
                r_start, r_end = row_starts[r_idx], row_ends[r_idx]
                c_start, c_end = col_starts[c_idx], col_ends[c_idx]
                if r_start < r_end and c_start < c_end: # Valid cell dimensions
                    coords[cell_names_3x3[r_idx][c_idx]] = (r_start, r_end, c_start, c_end)

    # Define potential extra cells below the main 3x3 grid
    if len(row_starts) > 3 and len(row_ends) > 3:
        r_start, r_end = row_starts[3], row_ends[3]
        # Check columns corresponding to BM and BR
        if "BM" in coords:
            _, _, c_start, c_end = coords["BM"]
            if r_start < r_end and c_start < c_end:
                 coords["ExtraBM"] = (r_start, r_end, c_start, c_end)
        if "BR" in coords:
            _, _, c_start, c_end = coords["BR"]
            if r_start < r_end and c_start < c_end:
                 coords["ExtraBR"] = (r_start, r_end, c_start, c_end)

    return coords

def extract_cell_block(grid, coords):
    """Extracts the subgrid corresponding to the cell coordinates."""
    if coords is None:
        return None
    r_start, r_end, c_start, c_end = coords
    return grid[r_start:r_end, c_start:c_end]

def get_pattern_color(cell_block, C_grid, background_color=0):
    """Finds the primary color in the cell block, excluding grid and background."""
    if cell_block is None or cell_block.size == 0:
        return None

    unique_colors = np.unique(cell_block)
    pattern_colors = [c for c in unique_colors if c != C_grid and c != background_color]

    if not pattern_colors:
        return None
    # If multiple pattern colors exist, this simple logic might fail.
    # Assume only one significant pattern color per cell for this task.
    return pattern_colors[0]

def clear_cell(grid, coords, background_color=0):
    """Sets the pixels within the cell boundaries to the background color."""
    if coords is None:
        return
    r_start, r_end, c_start, c_end = coords
    grid[r_start:r_end, c_start:c_end] = background_color

def place_cell_block(grid, cell_block, coords):
    """Copies the cell_block into the grid at the specified coordinates."""
    if coords is None or cell_block is None:
        return
    r_start, r_end, c_start, c_end = coords
    # Ensure the block fits (it should if coords are correct)
    block_h, block_w = cell_block.shape
    target_h = r_end - r_start
    target_w = c_end - c_start
    if block_h == target_h and block_w == target_w:
         grid[r_start:r_end, c_start:c_end] = cell_block
    else:
        # Handle potential size mismatch (e.g., clip the block if too large)
        h = min(block_h, target_h)
        w = min(block_w, target_w)
        grid[r_start:r_start+h, c_start:c_start+w] = cell_block[:h, :w]
        # print(f"Warning: Size mismatch placing block at {coords}. Block: {block_h}x{block_w}, Target: {target_h}x{target_w}")


def transform(input_grid):
    """
    Applies color-dependent cell transformations based on Green(3) and Blue(1) rules.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 1. Identify Grid Structure
    C_grid, h_lines, v_lines = find_grid_lines(input_grid)
    if C_grid is None or not h_lines or not v_lines:
        # Cannot determine grid structure, return copy
        print("Warning: Could not determine grid structure.")
        return output_grid

    # 2. Get Cell Coordinates
    cell_coords = get_cell_coords((height, width), h_lines, v_lines)
    if not cell_coords:
        print("Warning: Could not determine cell coordinates.")
        return output_grid

    # 3. Store Input Cell Contents and Colors for relevant cells
    input_blocks = {}
    input_colors = {}
    green_cells = ["TL", "ML", "MC"]
    blue_cells = ["BM", "BR", "ExtraBR"] # Note: ExtraBM is a target, not a source

    for cell_name in green_cells + blue_cells:
        coords = cell_coords.get(cell_name)
        if coords:
            block = extract_cell_block(input_grid, coords)
            input_blocks[cell_name] = block
            input_colors[cell_name] = get_pattern_color(block, C_grid)

    # --- Apply Transformations ---

    # 4. Process Green (3) Transformation: TL -> ML, ML -> MC, MC -> TM
    tm_coords = cell_coords.get("TM")
    tl_coords = cell_coords.get("TL")
    ml_coords = cell_coords.get("ML")
    mc_coords = cell_coords.get("MC")

    # Check which input cells have Green patterns
    tl_is_green = input_colors.get("TL") == 3
    ml_is_green = input_colors.get("ML") == 3
    mc_is_green = input_colors.get("MC") == 3

    # Clear target cells if any source cell is green
    if tl_is_green or ml_is_green or mc_is_green:
        clear_cell(output_grid, tl_coords)
        clear_cell(output_grid, tm_coords)
        clear_cell(output_grid, ml_coords)
        clear_cell(output_grid, mc_coords)

    # Place patterns in new locations
    if tl_is_green:
        place_cell_block(output_grid, input_blocks.get("TL"), ml_coords) # TL -> ML
    if ml_is_green:
        place_cell_block(output_grid, input_blocks.get("ML"), mc_coords) # ML -> MC
    if mc_is_green:
        place_cell_block(output_grid, input_blocks.get("MC"), tm_coords) # MC -> TM

    # 5. Process Blue (1) Transformation: BM -> BM, BR -> BR, ExtraBR -> ExtraBM, BM -> ExtraBR
    bm_coords = cell_coords.get("BM")
    br_coords = cell_coords.get("BR")
    extra_bm_coords = cell_coords.get("ExtraBM")
    extra_br_coords = cell_coords.get("ExtraBR")

    # Check which input cells have Blue patterns
    bm_is_blue = input_colors.get("BM") == 1
    br_is_blue = input_colors.get("BR") == 1
    extra_br_is_blue = input_colors.get("ExtraBR") == 1

    # Clear target cells if any source cell is blue
    if bm_is_blue or br_is_blue or extra_br_is_blue:
        clear_cell(output_grid, bm_coords)
        clear_cell(output_grid, br_coords)
        clear_cell(output_grid, extra_bm_coords)
        clear_cell(output_grid, extra_br_coords)

    # Place patterns in new locations
    if bm_is_blue:
        place_cell_block(output_grid, input_blocks.get("BM"), bm_coords)      # BM -> BM
        place_cell_block(output_grid, input_blocks.get("BM"), extra_br_coords) # BM -> ExtraBR (copy)
    if br_is_blue:
        place_cell_block(output_grid, input_blocks.get("BR"), br_coords)      # BR -> BR
    if extra_br_is_blue:
        place_cell_block(output_grid, input_blocks.get("ExtraBR"), extra_bm_coords) # ExtraBR -> ExtraBM

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 6 0 0 0 4 6 4 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 4 0 6 0 4 0 0 6 0 0 0 0
0 0 0 0 6 0 4 4 0 6 0 4 4 0 6 0 0 0 0
0 0 0 0 6 0 0 4 0 6 0 4 0 0 6 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 6 0 0 4 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 4 4 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 4 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 4 6 0 0 0 0 6 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
```
Expected Output:
```
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 6 0 0 0 4 6 4 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 4 0 6 0 4 0 0 6 0 0 0 0
0 0 0 0 6 0 4 4 0 6 0 4 4 0 6 0 0 0 0
0 0 0 0 6 0 0 4 0 6 0 4 0 0 6 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 6 0 0 4 0 6 0 4 0 0 6 0 0 0 0
0 0 0 0 6 0 4 4 0 6 0 4 4 0 6 0 0 0 0
0 0 0 0 6 0 0 4 0 6 0 4 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 4 6 4 0 0 0 6 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
```
Transformed Output:
```
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 6 0 0 0 4 6 4 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 4 0 6 0 4 0 0 6 0 0 0 0
0 0 0 0 6 0 4 4 0 6 0 4 4 0 6 0 0 0 0
0 0 0 0 6 0 0 4 0 6 0 4 0 0 6 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 6 0 0 4 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 4 4 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 4 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 4 6 0 0 0 0 6 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
0 0 0 0 6 0 0 0 0 6 0 0 0 0 6 0 0 0 0
```
Match: False
Pixels Off: 5
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 3.0959752321981284

## Example 2:
Input:
```
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
3 0 3 3 2 0 0 0 0 2 0 0 0 0 2 0 0 0
0 3 3 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
0 0 3 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 3 0 2 0 3 0 0 2 0 0 0 0 2 0 0 0
0 3 3 0 2 0 3 3 0 2 0 0 0 0 2 0 0 0
3 0 3 3 2 3 3 0 3 2 0 0 0 0 2 0 0 0
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
0 0 0 0 2 0 1 0 0 2 0 0 1 0 2 0 0 0
0 0 0 0 2 0 0 1 1 2 1 1 0 0 2 0 0 0
0 0 0 0 2 0 0 1 0 2 0 1 0 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 2 0 0 0 0 2 0 1 0 0 2 0 0 0
0 0 0 0 2 0 0 0 0 2 1 1 0 0 2 0 0 0
0 0 0 0 2 0 0 0 0 2 0 0 1 0 2 0 0 0
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
```
Expected Output:
```
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
3 0 3 3 2 3 3 0 3 2 0 0 0 0 2 0 0 0
0 3 3 0 2 0 3 3 0 2 0 0 0 0 2 0 0 0
0 0 3 0 2 0 3 0 0 2 0 0 0 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 3 0 2 0 3 0 0 2 0 0 0 0 2 0 0 0
0 3 3 0 2 0 3 3 0 2 0 0 0 0 2 0 0 0
3 0 3 3 2 3 3 0 3 2 0 0 0 0 2 0 0 0
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
0 0 0 0 2 0 1 0 0 2 0 0 1 0 2 0 0 0
0 0 0 0 2 0 0 1 1 2 1 1 0 0 2 0 0 0
0 0 0 0 2 0 0 1 0 2 0 1 0 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 2 0 0 1 0 2 0 1 0 0 2 0 0 0
0 0 0 0 2 0 0 1 1 2 1 1 0 0 2 0 0 0
0 0 0 0 2 0 1 0 0 2 0 0 1 0 2 0 0 0
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
```
Transformed Output:
```
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
0 0 0 0 2 3 0 3 3 2 0 0 0 0 2 0 0 0
0 0 0 0 2 0 3 3 0 2 0 0 0 0 2 0 0 0
0 0 0 0 2 0 0 3 0 2 0 0 0 0 2 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 3 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
0 3 3 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
3 0 3 3 2 0 0 0 0 2 0 0 0 0 2 0 0 0
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
2 2 2 2 2 2 2 2 0 2 0 0 0 2 2 2 2 2
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
0 0 0 0 2 0 0 1 0 2 0 0 0 0 2 0 0 0
0 0 0 0 2 1 1 0 0 2 0 0 0 0 2 0 0 0
0 0 0 0 2 0 1 0 0 2 0 0 0 0 2 0 0 0
2 2 2 2 2 2 2 2 0 2 0 0 0 2 2 2 2 2
0 0 0 0 2 0 1 0 0 2 0 0 0 0 2 0 0 0
0 0 0 0 2 1 1 0 0 2 0 0 0 0 2 0 0 0
0 0 0 0 2 0 0 1 0 2 0 0 0 0 2 0 0 0
0 0 0 0 2 0 0 0 0 2 0 0 0 0 2 0 0 0
```
Match: False
Pixels Off: 48
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 28.070175438596493
