```python
import numpy as np

"""
The transformation operates on a grid containing a border and four internal 5x5 
pattern regions (P1, P2, P3, P4) separated by columns of the border color. 
The first three regions (P1, P2, P3) each consist of a common 'background' 
color (Bg) and a distinct 'foreground' object color (F1, F2, F3). The fourth 
region (P4) initially contains only the background color.

The transformation rule modifies only the P4 region in the output:

1. Identify the common background color (Bg) from the input P4.
2. Identify the foreground colors F1, F2, F3 for patterns P1, P2, P3 respectively.
3. Select a 'Primary Pattern' (P_prim) from P1, P2, P3 based on its foreground 
   color, using the priority: Red (2) > Blue (1). Let the foreground color of 
   P_prim be F_prim.
4. Identify the two patterns *not* selected as primary ('Secondary Patterns').
5. Select a 'Background Source Color' (F_bg_src) from the foreground colors of 
   the Secondary Patterns, using the priority: Green (3) > Yellow (4).
6. Construct the new 5x5 pattern for the output P4 region. This new pattern uses 
   the spatial structure (shape) of P_prim. Pixels in the new P4 corresponding 
   to F_prim pixels in P_prim are set to F_prim. Pixels corresponding to Bg 
   pixels in P_prim are set to F_bg_src.

The border, separators, and the contents of P1, P2, and P3 remain unchanged 
in the output grid.
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
    # Find all unique colors in the pattern
    unique_colors = np.unique(pattern_array)
    # Iterate through unique colors
    for color in unique_colors:
        # If a color is found that is not the background, it's the foreground
        if color != background_color:
            # Ensure return type is standard int
            return int(color) 
    # Return None if no foreground color is found (e.g., pattern is all background)
    return None

def transform(input_grid):
    """
    Transforms the input grid according to the described pattern composition rule.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    
    # Convert input list of lists to a NumPy array for efficient slicing
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize the output grid as a copy of the input grid
    output_np = input_np.copy()
    
    # Define the row and column slices for the pattern regions (P1, P2, P3, P4)
    # Assumes a 7x25 grid structure with 1-pixel border/separators
    rows_slice = slice(1, 6) # Inner content is rows 1 through 5 (0-indexed)
    p_col_slices = {
        1: slice(1, 6),   # P1: cols 1-5
        2: slice(7, 12),  # P2: cols 7-11
        3: slice(13, 18), # P3: cols 13-17
        4: slice(19, 24)  # P4: cols 19-23
    }
    
    # === Step 1: Identify Background Color (Bg) ===
    # Get the slice corresponding to the P4 region
    p4_slice = (rows_slice, p_col_slices[4])
    # Assume P4 is filled uniformly with the background color initially. 
    # Take the color of the top-left pixel of P4.
    bg_color = int(input_np[p4_slice][0, 0]) 

    # === Step 2: Identify Foreground Colors (F1, F2, F3) ===
    foregrounds = {} # Dictionary: pattern index (1, 2, 3) -> foreground color
    patterns = {}    # Dictionary: pattern index (1, 2, 3) -> pattern numpy array
    for i in range(1, 4): # Iterate through P1, P2, P3
        p_slice = (rows_slice, p_col_slices[i]) # Get slice for current pattern
        patterns[i] = input_np[p_slice]         # Extract pattern array
        foregrounds[i] = find_foreground(patterns[i], bg_color) # Find its foreground color

    # === Step 3: Select Primary Pattern (P_prim) and its color (F_prim) ===
    primary_pattern_idx = None
    primary_fg_color = None
    
    # Check for Red (2) with priority
    for idx in [1, 2, 3]:
        if foregrounds.get(idx) == 2:
            primary_pattern_idx = idx
            break # Found Red, stop checking
            
    # If no Red found, check for Blue (1)
    if primary_pattern_idx is None:
        for idx in [1, 2, 3]:
            if foregrounds.get(idx) == 1:
                primary_pattern_idx = idx
                break # Found Blue, stop checking

    # Error handling if neither Red nor Blue is found (shouldn't happen per examples)
    if primary_pattern_idx is None:
        print("Error: Could not determine Primary Pattern (No Red=2 or Blue=1 found).")
        # Returning the original grid in case of unexpected input
        return input_grid 
        
    # Store the primary foreground color and the pattern array itself
    primary_fg_color = foregrounds[primary_pattern_idx]
    primary_pattern_array = patterns[primary_pattern_idx]

    # === Step 4: Identify Secondary Patterns and their foreground colors ===
    secondary_indices = [idx for idx in [1, 2, 3] if idx != primary_pattern_idx]
    secondary_fg_colors = [foregrounds[idx] for idx in secondary_indices if foregrounds.get(idx) is not None]

    # === Step 5: Select Background Source Color (F_bg_src) ===
    bg_source_fg_color = None
    
    # Check for Green (3) among secondary foregrounds with priority
    if 3 in secondary_fg_colors:
        bg_source_fg_color = 3
    # Else, check for Yellow (4) among secondary foregrounds
    elif 4 in secondary_fg_colors:
        bg_source_fg_color = 4
        
    # Handle case where neither Green nor Yellow is found in secondary patterns
    if bg_source_fg_color is None:
        # This scenario is not present in the training examples.
        # As a fallback, we might use the original background color.
        print(f"Warning: Could not determine Background Source Color (No Green=3 or Yellow=4 found in secondary colors: {secondary_fg_colors}). Using original Bg color.")
        bg_source_fg_color = bg_color # Fallback

    # === Step 6: Construct Output P4 ===
    # Create a new 5x5 array, initialized (e.g., with zeros or copy of P_prim)
    output_p4_region = np.zeros_like(primary_pattern_array) 
    
    # Iterate through each pixel of the primary pattern's shape
    rows, cols = primary_pattern_array.shape
    for r in range(rows):
        for c in range(cols):
            # If the pixel in the primary pattern has the primary foreground color
            if primary_pattern_array[r, c] == primary_fg_color:
                # Set the corresponding output pixel to the primary foreground color
                output_p4_region[r, c] = primary_fg_color
            # If the pixel in the primary pattern has the background color
            elif primary_pattern_array[r, c] == bg_color:
                # Set the corresponding output pixel to the determined background source color
                output_p4_region[r, c] = bg_source_fg_color
            else:
                # Handle unexpected pixel colors if any (e.g., copy them directly)
                # Based on examples, only F_prim and Bg are expected in P1, P2, P3
                output_p4_region[r, c] = primary_pattern_array[r, c] 

    # === Step 7: Assemble Final Output ===
    # Place the newly constructed P4 region into the output grid copy
    output_np[p4_slice] = output_p4_region

    # Convert the final NumPy array back to a list of lists for the required output format
    return output_np.tolist()
```