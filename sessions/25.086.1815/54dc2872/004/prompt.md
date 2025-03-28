
Previous Code:
```python
import numpy as np

"""
Identifies all 'trigger' pixels (Red=2 or Orange=7).
For each trigger, identifies its associated 'mover' pattern (Red -> Green L + Azure, Orange -> Magenta L + Orange) and placement offset (Red -> (0, 2), Orange -> (0, 0)).
Searches the grid for the mover pattern corresponding to the trigger.
The *first* trigger found (scanning top-to-bottom, left-to-right) for which its corresponding mover pattern *also exists* in the grid determines the transformation.
If such a trigger/pattern pair is found:
    1. Erases the original 'mover' pattern from the grid (setting its pixels to white=0).
    2. Redraws the 'mover' pattern at a new location, calculated by adding the placement offset to the location of the *trigger* pixel that initiated the transformation. The new location defines the top-left corner for drawing the pattern.
If no trigger pixel has its corresponding mover pattern present in the grid, the original grid is returned unchanged.
"""

# Define the patterns as lists of (relative_row, relative_col, color) tuples
# relative to their top-left corner.
GREEN_L_AZURE_PATTERN = [
    (0, 0, 3), (0, 1, 3), (0, 2, 3), (0, 3, 3), # Top row: GGGG
    (1, 2, 8), (1, 3, 3),                      # Middle row: ..AG
    (2, 3, 3)                                  # Bottom row: ...G
]

MAGENTA_L_ORANGE_PATTERN = [
    (0, 0, 6), (0, 1, 6), (0, 2, 6),           # Top row: MMM
    (1, 0, 6), (1, 1, 7),                      # Middle row: MO.
    (2, 0, 6)                                  # Bottom row: M..
]

# Map trigger colors to their corresponding pattern and placement offset (dR, dC)
TRIGGER_MAP = {
    2: {'pattern': GREEN_L_AZURE_PATTERN, 'offset': (0, 2)},  # Red trigger
    7: {'pattern': MAGENTA_L_ORANGE_PATTERN, 'offset': (0, 0)}   # Orange trigger
}

# --- Helper Functions ---

def find_all_trigger_pixels(grid):
    """
    Finds all pixels whose color is a key in TRIGGER_MAP.
    Returns a list of (color, row, col) tuples, ordered by scan order
    (top-to-bottom, left-to-right).
    """
    triggers = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color in TRIGGER_MAP:
                triggers.append((color, r, c))
    return triggers

def check_pattern_at(grid, r_start, c_start, pattern):
    """
    Checks if the specified pattern exists at the given top-left coordinates (r_start, c_start)
    in the grid.
    Returns True if the pattern matches, False otherwise.
    """
    height, width = grid.shape
    for dr, dc, color in pattern:
        r, c = r_start + dr, c_start + dc
        # Check bounds and color match
        if not (0 <= r < height and 0 <= c < width and grid[r, c] == color):
            return False
    return True

def find_pattern_location(grid, pattern):
    """
    Finds the top-left corner (row, col) of the first occurrence of the pattern
    in the grid, searching top-to-bottom, left-to-right.
    Returns (row, col) or (-1, -1) if not found.
    """
    height, width = grid.shape
    # Determine pattern dimensions (max row/col offset)
    if not pattern: # Empty pattern
        return -1, -1
    # Calculate the required height and width span of the pattern
    max_dr = max(dr for dr, dc, color in pattern)
    max_dc = max(dc for dr, dc, color in pattern)
    
    # Iterate through possible top-left starting positions
    for r in range(height - max_dr):
        for c in range(width - max_dc):
            # Check if the pattern exists starting at (r, c)
            if check_pattern_at(grid, r, c, pattern):
                return r, c # Return the first location found
    return -1, -1 # Pattern not found

def modify_grid_with_pattern(grid, r_start, c_start, pattern, new_color=0):
    """
    Modifies the grid:
    - If new_color is None (draw mode): Draws the pattern at (r_start, c_start),
      overwriting existing pixels within grid bounds.
    - If new_color is not None (erase mode): Sets pixels corresponding to the
      pattern shape at (r_start, c_start) to new_color, ONLY IF the current pixel
      in the grid matches the expected pattern color at that relative position.
      This prevents accidentally erasing non-pattern pixels.
    """
    height, width = grid.shape
    for dr, dc, pattern_color in pattern:
        r, c = r_start + dr, c_start + dc
        # Ensure the coordinates are within the grid boundaries
        if 0 <= r < height and 0 <= c < width:
            if new_color is None: # Draw mode
                 grid[r, c] = pattern_color
            else: # Erase mode
                 # Only erase if the current grid pixel matches the expected pattern color
                 if grid[r, c] == pattern_color:
                     grid[r, c] = new_color # Set to background/erase color

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the transformation rule: finds the first trigger pixel (Red or Orange)
    whose associated mover pattern also exists in the grid. If found, it erases
    the original pattern and redraws it at a location offset from the trigger pixel.
    """
    # Initialize output_grid as a copy of the input to avoid modifying the original
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # --- Find the active transformation details ---
    active_trigger_loc = None
    active_pattern_loc = None
    active_pattern = None
    active_offset = None
    found_active_pair = False

    # 1. Find all potential trigger pixels in the input grid
    all_triggers = find_all_trigger_pixels(input_grid)

    # 2. Iterate through triggers in the order they were found
    for trigger_color, r_trigger, c_trigger in all_triggers:
        # 3. Get the associated pattern and offset for this trigger color
        if trigger_color not in TRIGGER_MAP:
            # This check is technically redundant due to find_all_trigger_pixels,
            # but kept for robustness.
            continue 

        details = TRIGGER_MAP[trigger_color]
        mover_pattern = details['pattern']
        offset = details['offset']

        # 4. Search for the associated mover pattern in the *original* input grid
        r_original, c_original = find_pattern_location(input_grid, mover_pattern)

        # 5. If the pattern is found, this trigger/pattern pair is the active one
        if r_original != -1:
            active_trigger_loc = (r_trigger, c_trigger)
            active_pattern_loc = (r_original, c_original)
            active_pattern = mover_pattern
            active_offset = offset
            found_active_pair = True
            break # Crucial: Stop searching once the first valid pair is found

    # --- Apply the transformation if an active pair was found ---
    if not found_active_pair:
        # If no trigger had its corresponding pattern present in the grid,
        # return the unmodified copy of the input grid.
        return output_grid 

    # 6. Unpack the details of the active transformation for clarity
    r_trigger, c_trigger = active_trigger_loc
    r_original, c_original = active_pattern_loc
    dr_offset, dc_offset = active_offset

    # 7. Erase the mover pattern from its original location in the output grid.
    # Pass the pattern's original location and the pattern definition.
    # Use new_color=0 (white/background) for erasing.
    modify_grid_with_pattern(output_grid, r_original, c_original, active_pattern, new_color=0)

    # 8. Calculate the new top-left corner for drawing the pattern.
    # Add the offset associated with the trigger color to the trigger pixel's location.
    r_new = r_trigger + dr_offset
    c_new = c_trigger + dc_offset

    # 9. Draw the mover pattern at the new location in the output grid.
    # Pass the new location and the pattern definition.
    # Use new_color=None to indicate drawing mode (use pattern's colors).
    modify_grid_with_pattern(output_grid, r_new, c_new, active_pattern, new_color=None)

    # Return the modified grid
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 7 7 7 0 0 0 0 0 0 0 0 0
0 0 1 7 0 0 2 0 0 0 0 8 0
0 0 0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0 0 0
0 0 5 4 0 0 0 0 6 0 0 0 0
0 0 0 4 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 0 9 6 0 0
0 0 0 0 0 0 0 0 0 9 0 0 0
3 3 3 3 0 0 0 0 0 0 0 0 0
0 0 8 3 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 7 7 7 0 0 0 0 0 0 0 0 0
0 0 1 7 0 0 2 0 3 3 3 3 0
0 0 0 7 0 0 0 0 0 0 8 3 0
0 0 0 0 0 0 0 0 0 0 0 3 0
0 4 4 4 0 0 0 0 0 0 0 0 0
0 0 5 4 0 0 0 0 9 9 0 0 0
0 0 0 4 0 0 0 0 9 6 0 0 0
0 0 0 0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 7 7 7 0 0 0 0 0 0 0 0 0
0 0 1 7 0 0 2 0 3 3 3 3 0
0 0 0 7 0 0 0 0 0 0 8 3 0
0 0 0 0 0 0 0 0 0 0 0 3 0
0 4 4 4 0 0 0 0 0 0 0 0 0
0 0 5 4 0 0 0 0 6 0 0 0 0
0 0 0 4 0 0 0 0 0 9 9 0 0
0 0 0 0 0 0 0 0 0 9 6 0 0
0 0 0 0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 11.538461538461547

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 6 7 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0
0 0 9 8 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0
0 0 6 7 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0
0 0 9 8 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0
0 0 6 7 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0
0 0 9 8 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
