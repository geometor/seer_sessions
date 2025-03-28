import numpy as np

"""
Identifies a repeating pattern, typically originating from the top-leftmost 
non-background pixel, assuming the pattern is contained within a small, fixed 
bounding box (e.g., 2x2) relative to an anchor point. Finds all occurrences 
(instances) of this pattern in the input grid. Sorts the anchor points of 
these instances based on their position (row, then column). Creates an output 
grid of the same size, initially filled with the background color (0). Places 
the identified pattern onto the output grid at the original anchor locations, 
but effectively reverses the sequence of the patterns along their original path.
"""

# --- Helper Functions ---

def find_first_pattern_anchor(grid):
    """
    Finds the coordinates (row, col) of the top-leftmost non-background pixel.
    Returns None if the grid is all background.
    """
    non_background_pixels = np.argwhere(grid != 0)
    if non_background_pixels.size == 0:
        return None  # No non-background pixels found
    # Sort by row, then column, and take the first one
    # np.argwhere returns [row, col], sorted finds the minimum row, then minimum col for that row
    min_row_indices = non_background_pixels[non_background_pixels[:, 0] == non_background_pixels[:, 0].min()]
    first_anchor_coords = min_row_indices[min_row_indices[:, 1].argmin()]
    return tuple(first_anchor_coords)

def determine_pattern_structure(grid, anchor_r, anchor_c, pattern_size=(2, 2)):
    """
    Determines the pattern structure based on non-background pixels within a 
    fixed-size box relative to the anchor. Also determines the actual minimum
    bounding box height and width containing the non-background pixels.
    Returns a tuple: (pattern_dict, pattern_h, pattern_w)
    - pattern_dict: {(dr, dc): color} for non-background pixels.
    - pattern_h: Minimum height of the bounding box containing the pattern.
    - pattern_w: Minimum width of the bounding box containing the pattern.
    """
    pattern = {}
    height, width = grid.shape
    box_h, box_w = pattern_size # The initial search box size (e.g., 2x2)
    
    min_r, max_r = -1, -1
    min_c, max_c = -1, -1
    
    for dr in range(box_h):
        for dc in range(box_w):
            r, c = anchor_r + dr, anchor_c + dc
            # Check bounds relative to the input grid
            if 0 <= r < height and 0 <= c < width:
                color = grid[r, c]
                if color != 0: # Only include non-background pixels
                    pattern[(dr, dc)] = color
                    # Track actual bounds based on non-zero pixels found
                    if min_r == -1: # First non-zero pixel
                        min_r, max_r = dr, dr
                        min_c, max_c = dc, dc
                    else:
                        min_r = min(min_r, dr)
                        max_r = max(max_r, dr)
                        min_c = min(min_c, dc)
                        max_c = max(max_c, dc)

    # Calculate actual height and width based on content
    # Important: Ensure these are relative to (0,0) of the pattern box, not min_r/min_c
    if not pattern:
        pattern_h = 0
        pattern_w = 0
    else:
        # The height/width needs to accommodate the max offset + 1
        pattern_h = max_r + 1
        pattern_w = max_c + 1
        
    # Re-evaluate using fixed pattern_size for consistency if needed?
    # The examples seem to rely on a fixed 2x2 structure including background 0s
    # Let's stick to the provided pattern_size for the bounding box check later.
    pattern_h_fixed, pattern_w_fixed = pattern_size

    # Return the pattern dict, and the *fixed* size for matching purposes
    return pattern, pattern_h_fixed, pattern_w_fixed


def find_all_pattern_instances(grid, pattern, pattern_h, pattern_w):
    """
    Finds all locations (anchor points r, c) in the grid where the pattern matches.
    A match requires:
    1. All colored pixels in the pattern dict match the grid at (r+dr, c+dc).
    2. All positions (dr, dc) within the pattern's bounding box (pattern_h x pattern_w)
       that are NOT in the pattern dict must be background (0) in the grid at (r+dr, c+dc).
    Returns a list of (r, c) tuples.
    """
    if not pattern or pattern_h == 0 or pattern_w == 0:
        return [] # Cannot find instances of an empty pattern

    height, width = grid.shape
    anchors = []
    
    # Iterate through possible top-left anchor points (r, c)
    # The loops bounds ensure that the pattern box (pattern_h x pattern_w) fits within the grid
    for r in range(height - pattern_h + 1):
        for c in range(width - pattern_w + 1):
            match = True
            
            # 1. Check if pattern's colored pixels match the grid
            for (dr, dc), expected_color in pattern.items():
                # Check if this relative coordinate is within the bounding box being checked
                # This should always be true if pattern was derived correctly, but safer to check
                if 0 <= dr < pattern_h and 0 <= dc < pattern_w:
                    current_color = grid[r + dr, c + dc]
                    if current_color != expected_color:
                        match = False
                        break
                else:
                    # This case implies an issue with pattern definition or pattern_h/w
                    match = False
                    break 
            if not match:
                continue

            # 2. Check if non-pattern pixels within the bounding box are background
            for dr_check in range(pattern_h):
                 for dc_check in range(pattern_w):
                     # If this relative position is NOT a colored part of the pattern
                     if (dr_check, dc_check) not in pattern:
                          # Check if the corresponding grid cell is background (0)
                          if grid[r + dr_check, c + dc_check] != 0:
                              match = False
                              break
                 if not match:
                     break # Break outer check loop if mismatch found

            # If both checks passed, it's a valid instance
            if match:
                anchors.append((r, c))
                
    return anchors

def draw_pattern(output_grid, anchor, pattern):
    """
    Draws the pattern (colored pixels) onto the output grid at the specified anchor.
    Assumes output_grid is large enough. Modifies output_grid in place.
    """
    height, width = output_grid.shape
    anchor_r, anchor_c = anchor
    for (dr, dc), color in pattern.items():
        target_r, target_c = anchor_r + dr, anchor_c + dc
        # Check bounds before drawing
        if 0 <= target_r < height and 0 <= target_c < width:
            output_grid[target_r, target_c] = color

# --- Main Transformation Function ---

def transform(input_grid):
    # Convert input list of lists to a NumPy array
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output grid with background color (0)
    output_grid = np.zeros_like(input_np)

    # 1. Find the anchor of the first pattern instance (top-leftmost non-zero)
    first_anchor = find_first_pattern_anchor(input_np)
    
    # If the grid is empty (all background), return the empty output grid
    if first_anchor is None:
        return output_grid.tolist() 

    # 2. Determine the structure of the pattern using a fixed 2x2 bounding box
    #    This also returns the box dimensions (h=2, w=2) used for matching.
    pattern, pattern_h, pattern_w = determine_pattern_structure(
        input_np, first_anchor[0], first_anchor[1], pattern_size=(2, 2)
    )

    # If pattern determination failed unexpectedly (e.g., first anchor invalid)
    if not pattern:
         # This case is unlikely if first_anchor was found, but handle defensively
         return output_grid.tolist()

    # 3. Find all instances (anchors) of this pattern in the input grid
    input_anchors = find_all_pattern_instances(input_np, pattern, pattern_h, pattern_w)
    
    # If no instances were found (not even the first one, which would be odd), return empty grid
    if not input_anchors:
         return output_grid.tolist()

    # 4. Sort the identified input anchor points by position (row, then column)
    #    This establishes the original sequence along the diagonal.
    sorted_input_anchors = sorted(input_anchors, key=lambda p: (p[0], p[1]))

    # 5. Determine the target anchor positions by reversing the sorted list
    #    The pattern originally at sorted_input_anchors[i] will move to target_anchors[i].
    target_anchors = sorted_input_anchors[::-1] # Reversed list

    # 6. Draw the pattern at each target anchor position in the output grid
    #    Iterate through the target positions and draw the single defined pattern at each.
    for anchor in target_anchors:
        draw_pattern(output_grid, anchor, pattern)

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()