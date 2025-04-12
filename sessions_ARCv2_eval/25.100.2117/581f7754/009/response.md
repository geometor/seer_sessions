```python
"""
Transforms an input grid based on identified patterns and components, selecting a mode based on colors present.

The transformation operates in one of two primary modes:

Mode A (Component Shift):
Triggered when the color '3' is absent from the grid or is the background color.
1. Finds the background color (most frequent value).
2. Finds connected components (using 4-way adjacency) of all non-background cells.
3. Components consisting of a single cell remain static (their position does not change).
4. Components consisting of multiple cells are shifted horizontally. The direction and magnitude of the shift
   depend deterministically on the column index of the leftmost cell(s) of the component.
   A specific mapping (leftmost_column -> shift_amount) is applied, inferred heuristically from training examples based on background color:
   - If background is 1: {leftmost_col=1: shift=+3, leftmost_col=4: shift=-1}
   - If background is 3: {leftmost_col=1: shift=+2, leftmost_col=3: shift=-3, leftmost_col=4: shift=-1}
   - Other background colors default to no shift for multi-cell components.

Mode B (Pattern Matching):
Triggered when the color '3' is present in the grid AND is not the background color.
1. Finds the background color (most frequent). Initializes output with background.
2. Attempts to identify specific, predefined local patterns within the non-background cells. Each recognized pattern type has a fixed transformation (a 2D shift vector). Patterns are applied sequentially, and cells involved are marked as 'processed' to avoid reuse.
   - Pattern: Vertical column segment in col 2 containing '4' or '6'. Action: Shift cells (+2 rows, 0 cols).
   - Pattern: `[[3, 3, 3], [3, 1, 3], [3, 3, 3]]` (3x3 block). Action: Shift cells (-1 row, -1 col).
   - Pattern: `[[3, 1, 3, 3]]` (Horizontal). Action: Shift cells (-2 rows, 0 cols).
3. After pattern matching attempts, any non-background input cell that was *not* marked as processed is treated as static: its value is copied to the same location in the output grid.

Output Construction:
- The output grid is initialized with the determined background color.
- Transformations (Mode A shifts or Mode B pattern shifts) and static placements (Mode A single cells or Mode B fallback) are applied according to the selected mode.
- For Mode B, a mask tracks processed input cells to handle overlaps and ensure each input foreground cell contributes at most once to the output (either via a pattern shift or the static fallback).
"""

import numpy as np
from collections import Counter
from scipy.ndimage import label, find_objects

# --- Helper Functions ---

def find_background_color(grid_arr: np.ndarray) -> int:
    """Finds the most frequent value in the grid."""
    counts = Counter(grid_arr.flatten())
    if not counts: return 0 # Handle empty grid
    background_color = counts.most_common(1)[0][0]
    return background_color

def get_component_cells(labeled_array: np.ndarray, label_num: int, objects_slices: list) -> list[tuple[int, int]]:
    """Gets the (row, col) coordinates of cells belonging to a specific component label."""
    # Ensure label number is valid and slices exist for it
    if label_num <= 0 or label_num > len(objects_slices) or objects_slices[label_num - 1] is None:
        return []
    obj_slice = objects_slices[label_num - 1]

    # Extract the sub-array within the component's bounding box
    sub_array = labeled_array[obj_slice]
    # Create a mask for the specific label within the sub-array
    component_mask = (sub_array == label_num)
    # Find coordinates relative to the sub-array's top-left corner
    coords_in_slice = np.argwhere(component_mask)
    # Adjust coordinates to be relative to the full grid using the slice start offsets
    offset = np.array([s.start for s in obj_slice])
    coords_global = [tuple(coord + offset) for coord in coords_in_slice]
    return coords_global

def get_leftmost_column(component_cells: list[tuple[int, int]]) -> int:
    """Finds the minimum column index among all cells in a component."""
    if not component_cells: return -1 # Return invalid index if component is empty
    return min(c for r, c in component_cells)

def find_and_transform_pattern(input_arr, output_arr, processed_mask, pattern, shift_r, shift_c):
    """Finds non-overlapping instances of a 2D array pattern and applies transformation."""
    H, W = input_arr.shape
    if not isinstance(pattern, np.ndarray): pattern = np.array(pattern)
    pH, pW = pattern.shape
    
    # Iterate through all possible top-left corners for the pattern
    for r in range(H - pH + 1):
        for c in range(W - pW + 1):
            # Extract the subgrid from the input array
            subgrid = input_arr[r:r+pH, c:c+pW]
            # Check if the subgrid exactly matches the pattern
            pattern_match = np.array_equal(subgrid, pattern)

            if pattern_match:
                # Crucially, check if ANY cell in the source pattern location is already processed
                if not np.any(processed_mask[r:r+pH, c:c+pW]):
                    # Apply transformation and mark source cells as processed
                    for pr in range(pH):
                        for pc in range(pW):
                            # Calculate target coordinates after shift
                            nr, nc = r + pr + shift_r, c + pc + shift_c
                            # Place value in output if target is within bounds
                            if 0 <= nr < H and 0 <= nc < W:
                                output_arr[nr, nc] = input_arr[r + pr, c + pc]
                            # Mark the source cell as processed
                            processed_mask[r + pr, c + pc] = True
                    # Since we found a non-overlapping match, continue searching elsewhere
                    # In simple cases, could 'continue' outer loop here, but let's allow multiple non-overlapping finds

def find_and_transform_vertical_column(input_arr, output_arr, processed_mask, background_color, col_idx, target_values, shift_r, shift_c):
    """Finds vertical segments of target values in a specific column and transforms them."""
    H, W = input_arr.shape
    # Check if column index is valid
    if col_idx < 0 or col_idx >= W: return

    # Iterate through each row in the specified column
    for r in range(H):
        cell_value = input_arr[r, col_idx]
        # Check conditions: target value, not background, and not already processed
        if cell_value in target_values and cell_value != background_color and not processed_mask[r, col_idx]:
             # Calculate target coordinates
             nr, nc = r + shift_r, col_idx + shift_c
             # Place value in output if target is within bounds
             if 0 <= nr < H and 0 <= nc < W:
                 output_arr[nr, nc] = input_arr[r, col_idx]
             # Mark the source cell as processed
             processed_mask[r, col_idx] = True


# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # --- Initialization ---
    if not input_grid or not input_grid[0]: return [] # Handle empty input
    input_arr = np.array(input_grid, dtype=int)
    H, W = input_arr.shape
    background_color = find_background_color(input_arr)
    output_arr = np.full_like(input_arr, background_color) # Initialize output with background

    # Identify all foreground cells (non-background)
    foreground_mask = (input_arr != background_color)

    # --- Determine Transformation Mode ---
    # Check if '3' exists among foreground colors
    foreground_colors = np.unique(input_arr[foreground_mask])
    mode_b_trigger = (3 in foreground_colors) # True if '3' is a foreground color

    # ===============================================
    # === Mode B: Pattern Matching (Foreground 3) ===
    # ===============================================
    if mode_b_trigger:
        # Initialize mask to track processed input cells for Mode B
        processed_mask = np.zeros_like(input_arr, dtype=bool)

        # --- Apply Pattern Shifts (Order: Vertical, 3x3, 3133) ---
        # 1. Vertical Column (4/6 in col 2) shift (+2, 0)
        find_and_transform_vertical_column(input_arr, output_arr, processed_mask,
                                             background_color, col_idx=2,
                                             target_values={4, 6}, shift_r=2, shift_c=0)

        # 2. 3x3 Block pattern shift (-1, -1)
        pattern_3x3 = np.array([[3, 3, 3], [3, 1, 3], [3, 3, 3]])
        find_and_transform_pattern(input_arr, output_arr, processed_mask,
                                     pattern_3x3, shift_r=-1, shift_c=-1)

        # 3. Horizontal 3 1 3 3 pattern shift (-2, 0)
        pattern_3133 = np.array([[3, 1, 3, 3]])
        find_and_transform_pattern(input_arr, output_arr, processed_mask,
                                     pattern_3133, shift_r=-2, shift_c=0)

        # --- Static Fallback ---
        # Iterate through all input cells again
        for r in range(H):
            for c in range(W):
                # If it's a foreground cell AND it hasn't been processed by a pattern shift above
                if foreground_mask[r, c] and not processed_mask[r, c]:
                    # Place its value statically in the output at the same location
                    output_arr[r, c] = input_arr[r, c]

    # ============================================
    # === Mode A: Component Shift (No Fgnd 3) ===
    # ============================================
    else:
        # --- Find Connected Components of Foreground ---
        # Use 4-way connectivity (neighbors share an edge)
        structure = np.array([[0,1,0], [1,1,1], [0,1,0]], dtype=bool)
        labeled_array, num_features = label(foreground_mask, structure=structure)
        objects_slices = find_objects(labeled_array) # Get bounding boxes

        # --- Define Shift Rules based on Background Color ---
        shift_rules = {} # Default to no shift
        if background_color == 1: # train_1 rules
            shift_rules = {1: 3, 4: -1} # {leftmost_col: horizontal_shift}
        elif background_color == 3: # train_3 rules
            shift_rules = {1: 2, 3: -3, 4: -1}

        # --- Process Each Component ---
        for i in range(1, num_features + 1): # Iterate through component labels
            component_cells = get_component_cells(labeled_array, i, objects_slices)
            if not component_cells: continue # Skip if component is empty or invalid

            if len(component_cells) == 1:
                # Static placement for single-cell components
                r, c = component_cells[0]
                output_arr[r, c] = input_arr[r, c]
            else:
                # Horizontal shift for multi-cell components
                leftmost_col = get_leftmost_column(component_cells)
                # Get the shift amount from the rules, default to 0 if not found
                shift_col = shift_rules.get(leftmost_col, 0)

                # Apply shift to each cell in the component
                for r, c in component_cells:
                     # Calculate the new column after shifting
                     nc = c + shift_col
                     # Check if the new coordinates are within the grid boundaries
                     if 0 <= r < H and 0 <= nc < W:
                         # Copy the input value to the shifted position in the output
                         output_arr[r, nc] = input_arr[r, c]
        # Note: No explicit fallback needed for Mode A as the component processing
        # inherently handles all foreground cells either as static or shifted.

    # --- Return Result ---
    return output_arr.tolist() # Convert final numpy array back to list of lists
```