```python
import numpy as np

"""
Identify four 5x5 pattern regions (P1, P2, P3, P4) separated by border-colored 
columns within a larger bordered grid. Determine the common background color (Bg) 
from the initial P4 region. Find the unique foreground color (F1, F2, F3) for 
each of the first three regions (P1, P2, P3).

Select a 'Primary Pattern' (P_prim) from P1, P2, P3 based on its foreground 
color, using the priority: Red (2) > Blue (1). Let the foreground color of 
P_prim be F_prim.

Identify the two remaining patterns as 'Secondary Patterns'. Select a 
'Background Source Color' (F_bg_src) from the foreground colors of the 
Secondary Patterns, using the priority: Green (3) > Yellow (4).

Construct a new 5x5 pattern for the output P4 region. This new pattern uses the 
shape of P_prim. Where P_prim has its foreground color (F_prim), the new pattern 
also has F_prim. Where P_prim has the background color (Bg), the new pattern 
has the Background Source Color (F_bg_src).

The final output grid is a copy of the input grid, with the P4 region 
replaced by the newly constructed pattern.
"""

def find_foreground(pattern_array, background_color):
    """
    Finds the unique color in a pattern array that is not the background color.
    
    Args:
        pattern_array (np.array): A 2D numpy array representing the pattern region.
        background_color (int): The background color value.

    Returns:
        int or None: The foreground color value, or None if only the background 
                     color is found or the pattern is empty/invalid.
    """
    unique_colors = np.unique(pattern_array)
    for color in unique_colors:
        if color != background_color:
            # Ensure return type is standard int, handle potential numpy types
            return int(color) 
    return None

def transform(input_grid):
    """
    Transforms the input grid according to the described pattern composition rule.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    
    # Convert input to numpy array for easier slicing and manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize the output grid as a copy of the input
    output_np = input_np.copy()
    
    # Define the row and column slices for the pattern regions (P1, P2, P3, P4)
    # Assumes a 7x25 grid structure with 1-pixel border/separators
    rows_slice = slice(1, 6) # Inner content is rows 1-5 (inclusive)
    p_col_slices = {
        1: slice(1, 6),   # P1: cols 1-5
        2: slice(7, 12),  # P2: cols 7-11
        3: slice(13, 18), # P3: cols 13-17
        4: slice(19, 24)  # P4: cols 19-23
    }
    
    # 1. Identify Background Color (Bg) from input P4
    p4_slice = (rows_slice, p_col_slices[4])
    # Assume P4 is filled uniformly with the background color initially
    bg_color = int(input_np[p4_slice][0, 0]) 

    # 2. Identify Foreground Colors (F1, F2, F3)
    foregrounds = {} # Map pattern index (1, 2, 3) to its foreground color
    patterns = {}    # Map pattern index (1, 2, 3) to its numpy array
    for i in range(1, 4):
        p_slice = (rows_slice, p_col_slices[i])
        patterns[i] = input_np[p_slice]
        foregrounds[i] = find_foreground(patterns[i], bg_color)

    # 3. Select Primary Pattern (P_prim) and its color (F_prim)
    primary_pattern_idx = None
    primary_fg_color = None
    
    # Check for Red (2)
    if foregrounds.get(1) == 2:
        primary_pattern_idx = 1
    elif foregrounds.get(2) == 2:
        primary_pattern_idx = 2
    elif foregrounds.get(3) == 2:
        primary_pattern_idx = 3
        
    # If no Red, check for Blue (1)
    if primary_pattern_idx is None:
        if foregrounds.get(1) == 1:
            primary_pattern_idx = 1
        elif foregrounds.get(2) == 1:
            primary_pattern_idx = 2
        elif foregrounds.get(3) == 1:
            primary_pattern_idx = 3

    if primary_pattern_idx is None:
        # This case should not happen based on examples, but handle defensively
        print("Error: Could not determine Primary Pattern (No Red or Blue found).")
        return input_grid # Return original grid if logic fails
        
    primary_fg_color = foregrounds[primary_pattern_idx]
    primary_pattern_array = patterns[primary_pattern_idx]

    # 4. Identify Secondary Patterns and their foreground colors
    secondary_indices = [idx for idx in [1, 2, 3] if idx != primary_pattern_idx]
    secondary_fg_colors = [foregrounds[idx] for idx in secondary_indices if foregrounds[idx] is not None]

    # 5. Select Background Source Color (F_bg_src)
    bg_source_fg_color = None
    
    # Check for Green (3) among secondary foregrounds
    if 3 in secondary_fg_colors:
        bg_source_fg_color = 3
    # Else, check for Yellow (4) among secondary foregrounds
    elif 4 in secondary_fg_colors:
        bg_source_fg_color = 4
        
    if bg_source_fg_color is None:
        # This case should not happen based on examples, but handle defensively
        # What if other colors are present? The rule might need extension.
        # Based only on given examples, one of these should be present.
        print(f"Warning: Could not determine Background Source Color (No Green or Yellow found in secondary colors: {secondary_fg_colors}). Using original Bg.")
        # Decide on fallback - maybe use original Bg? Or raise error? Let's use Bg for now.
        bg_source_fg_color = bg_color # Fallback to original background

    # 6. Construct Output P4
    output_p4_region = np.zeros_like(primary_pattern_array)
    for r in range(primary_pattern_array.shape[0]):
        for c in range(primary_pattern_array.shape[1]):
            if primary_pattern_array[r, c] == primary_fg_color:
                output_p4_region[r, c] = primary_fg_color
            elif primary_pattern_array[r, c] == bg_color:
                output_p4_region[r, c] = bg_source_fg_color
            else:
                # Should not happen if patterns only have Fg and Bg
                # Keep original pixel from primary pattern as fallback? Or error?
                output_p4_region[r, c] = primary_pattern_array[r, c] 

    # 7. Assemble Final Output
    output_np[p4_slice] = output_p4_region

    # Convert the output numpy array back to a list of lists
    return output_np.tolist()
```