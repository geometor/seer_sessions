import numpy as np

"""
Transforms an 11x11 input grid based on the location of specific red patterns 
within its 9 subgrids, potentially changing the output grid size.

The input grid is expected to be 11x11, divided by magenta (6) lines into 9 areas 
(3x3 subgrids), numbered 1-9 like a keypad. The transformation rules depend on 
the presence and location of specific 3x3 patterns within these areas.

The specific pattern shape is:
  7 C 7
  C 7 C
  7 C 7
where 'C' is the pattern color (red=2, gray=5, or azure=8) and 7 is orange.

Condition 1: If Area 5 has a red(2) pattern AND Area 8 has a red(2) pattern 
             AND all other 7 areas are entirely orange(7), then the output is 
             the input grid with an added gray(5) pattern in Area 1 and an 
             added azure(8) pattern in Area 3. Output size remains 11x11.

Condition 2: If Area 3 has a red(2) pattern AND Area 5 has a red(2) pattern 
             AND all other 7 areas are entirely orange(7), then the output is 
             the input grid with an added azure(8) pattern in Area 4 and an 
             added gray(5) pattern in Area 7. Output size remains 11x11.

Default Condition: If the input grid is not 11x11, or if neither Condition 1 
                   nor Condition 2 applies, the output is a 16x16 grid 
                   filled entirely with orange(7).
"""

# === Helper Functions ===

def get_area_coords(area_num):
    """Returns the top-left (row, col) coords for a given area number (1-9)."""
    if area_num == 1: return (0, 0)
    if area_num == 2: return (0, 4)
    if area_num == 3: return (0, 8)
    if area_num == 4: return (4, 0)
    if area_num == 5: return (4, 4)
    if area_num == 6: return (4, 8)
    if area_num == 7: return (8, 0)
    if area_num == 8: return (8, 4)
    if area_num == 9: return (8, 8)
    # This should ideally not be reached if area_num is always 1-9
    raise ValueError(f"Invalid area number: {area_num}")

def get_area(grid, area_num):
    """Extracts the 3x3 subgrid for the given area number from an 11x11 grid."""
    r, c = get_area_coords(area_num)
    # Slicing handles bounds correctly for NumPy arrays
    return grid[r:r+3, c:c+3]

def create_pattern(pattern_color):
    """Creates the specific 3x3 pattern with the given color."""
    pattern = np.full((3, 3), 7, dtype=int) # Start with all orange (7)
    pattern[0, 1] = pattern_color
    pattern[1, 0] = pattern_color
    pattern[1, 2] = pattern_color
    pattern[2, 1] = pattern_color
    return pattern

def check_pattern(area, pattern_color):
    """Checks if a 3x3 area matches the specific pattern."""
    # Ensure area is actually 3x3 before comparison
    if area is None or area.shape != (3, 3):
        return False
    expected_pattern = create_pattern(pattern_color)
    return np.array_equal(area, expected_pattern)

def check_all_orange(area):
    """Checks if a 3x3 area is entirely orange (7)."""
    # Ensure area is 3x3 before comparison
    if area is None or area.shape != (3, 3):
        return False
    return np.all(area == 7)

def set_area(grid, area_num, subgrid):
    """Places the 3x3 subgrid into the main grid at the specified area."""
    r, c = get_area_coords(area_num)
    # Check bounds before assignment to avoid errors if grid isn't 11x11
    if r + 3 <= grid.shape[0] and c + 3 <= grid.shape[1]:
        grid[r:r+3, c:c+3] = subgrid
    else:
        # This case indicates an issue if called when grid should be 11x11
        # Log or handle appropriately if needed, though the main check should prevent this.
        pass

# === Main Transform Function ===

def transform(input_grid):
    # Convert input to a NumPy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape

    # Define parameters for the default output grid
    default_output_rows, default_output_cols = 16, 16
    default_color = 7

    # Pre-create the default output grid
    default_output = np.full((default_output_rows, default_output_cols), default_color, dtype=int)

    # --- Step 1: Check if input grid dimensions are exactly 11x11 ---
    if rows != 11 or cols != 11:
        # If dimensions are not 11x11, return the default 16x16 grid
        return default_output.tolist()

    # --- Step 2 & 3: Analyze the 9 areas of the 11x11 grid ---
    area_states = {} # Stores 'orange', 'red', 'gray', 'azure', or 'other'
    is_all_orange = {} # Flags if area is purely orange (True)

    for i in range(1, 10): # Iterate through areas 1 to 9
        area = get_area(input_grid_np, i)
        if check_all_orange(area):
            area_states[i] = 'orange'
            is_all_orange[i] = True
        elif check_pattern(area, 2): # Red pattern
            area_states[i] = 'red'
            is_all_orange[i] = False
        elif check_pattern(area, 5): # Gray pattern
            area_states[i] = 'gray'
            is_all_orange[i] = False
        elif check_pattern(area, 8): # Azure pattern
            area_states[i] = 'azure'
            is_all_orange[i] = False
        else:
            area_states[i] = 'other' # Not a recognized pattern or all orange
            is_all_orange[i] = False

    # Initialize the potential output grid as a copy of the input
    # This copy will be modified if Condition 1 or 2 is met
    output_grid = np.copy(input_grid_np)

    # --- Step 4: Check Condition 1 ---
    # Trigger: Area 5 is red, Area 8 is red, and all other areas (1,2,3,4,6,7,9) are orange
    condition1_met = (
        area_states.get(5) == 'red' and
        area_states.get(8) == 'red' and
        all(is_all_orange.get(i, False) for i in range(1, 10) if i not in [5, 8])
    )

    if condition1_met:
        # Apply transformation for Condition 1: Add gray(5) to Area 1, azure(8) to Area 3
        gray_pattern = create_pattern(5)
        azure_pattern = create_pattern(8)
        set_area(output_grid, 1, gray_pattern)
        set_area(output_grid, 3, azure_pattern)
        # Return the modified 11x11 grid
        return output_grid.tolist()

    # --- Step 5: Check Condition 2 (if Condition 1 was false) ---
    # Trigger: Area 3 is red, Area 5 is red, and all other areas (1,2,4,6,7,8,9) are orange
    condition2_met = (
        area_states.get(3) == 'red' and
        area_states.get(5) == 'red' and
        all(is_all_orange.get(i, False) for i in range(1, 10) if i not in [3, 5])
    )

    if condition2_met:
        # Apply transformation for Condition 2: Add azure(8) to Area 4, gray(5) to Area 7
        azure_pattern = create_pattern(8)
        gray_pattern = create_pattern(5)
        set_area(output_grid, 4, azure_pattern)
        set_area(output_grid, 7, gray_pattern)
        # Return the modified 11x11 grid
        return output_grid.tolist()

    # --- Step 6: Default Condition ---
    # If neither Condition 1 nor Condition 2 was met, return the pre-computed default 16x16 grid
    return default_output.tolist()