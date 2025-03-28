import numpy as np

"""
Identifies a repeating pattern, typically originating from the top-leftmost 
non-background pixel, assuming the pattern is contained within a small, fixed 
bounding box (e.g., 2x2) relative to an anchor point. Finds all occurrences 
(instances) of this pattern in the input grid, focusing on those arranged 
along a diagonal. Sorts the anchor points of these instances based on their 
position (row, then column). Creates an output grid of the same size, 
initially filled with the background color (0). Places the identified pattern 
onto the output grid at the original anchor locations, but in the reverse 
order of their sorted sequence.
"""

def find_first_pattern_anchor(grid):
    """Finds the coordinates of the top-leftmost non-background pixel."""
    non_background_pixels = np.argwhere(grid != 0)
    if non_background_pixels.size == 0:
        return None  # No non-background pixels found
    # Sort by row, then column, and take the first one
    sorted_indices = sorted(non_background_pixels.tolist(), key=lambda x: (x[0], x[1]))
    return tuple(sorted_indices[0])

def determine_pattern_structure(grid, anchor_r, anchor_c, pattern_size=(2, 2)):
    """
    Determines the pattern structure based on non-background pixels within a 
    fixed-size box relative to the anchor.
    Returns a dictionary {(dr, dc): color}.
    """
    pattern = {}
    height, width = grid.shape
    box_h, box_w = pattern_size
    
    for dr in range(box_h):
        for dc in range(box_w):
            r, c = anchor_r + dr, anchor_c + dc
            # Check bounds
            if 0 <= r < height and 0 <= c < width:
                color = grid[r, c]
                if color != 0: # Only include non-background pixels in the pattern definition
                    pattern[(dr, dc)] = color
    return pattern

def find_all_pattern_instances(grid, pattern):
    """
    Finds all locations (anchor points) in the grid where the pattern matches.
    """
    if not pattern: # Handle empty pattern case
        return []
        
    height, width = grid.shape
    anchors = []
    
    # Determine the max offset in the pattern to avoid checking out of bounds
    max_dr = max(dr for dr, dc in pattern.keys()) if pattern else 0
    max_dc = max(dc for dr, dc in pattern.keys()) if pattern else 0

    for r in range(height - max_dr):
        for c in range(width - max_dc):
            match = True
            # Check if the pattern matches at this anchor (r, c)
            for (dr, dc), expected_color in pattern.items():
                current_color = grid[r + dr, c + dc]
                if current_color != expected_color:
                    match = False
                    break
            
            # Check if pixels *outside* the pattern definition but *within* its bounding box are background (implicit check)
            # This helps distinguish patterns like in example 3. Let's derive the pattern's bounding box size.
            if match:
                 pattern_h = max_dr + 1
                 pattern_w = max_dc + 1
                 for dr_check in range(pattern_h):
                     for dc_check in range(pattern_w):
                         if (dr_check, dc_check) not in pattern: # If this relative pos is NOT in the pattern dict
                             # Check if the corresponding grid cell is background (0)
                              if grid[r + dr_check, c + dc_check] != 0:
                                  match = False
                                  break
                     if not match:
                         break

            if match:
                anchors.append((r, c))
                
    return anchors

def draw_pattern(output_grid, anchor, pattern):
    """Draws the pattern onto the output grid at the specified anchor."""
    height, width = output_grid.shape
    anchor_r, anchor_c = anchor
    for (dr, dc), color in pattern.items():
        target_r, target_c = anchor_r + dr, anchor_c + dc
        if 0 <= target_r < height and 0 <= target_c < width:
            output_grid[target_r, target_c] = color

def transform(input_grid):
    """
    Reverses the order of repeating patterns found along a diagonal path.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output grid with background color
    output_grid = np.zeros_like(input_np)

    # 1. Find the anchor of the first pattern instance
    first_anchor = find_first_pattern_anchor(input_np)
    if first_anchor is None:
        # If no pattern (all background), return the empty grid
        return output_grid.tolist() 

    # 2. Determine the structure of the pattern (using 2x2 assumption for now)
    #    Might need refinement if 2x2 isn't general enough.
    pattern = determine_pattern_structure(input_np, first_anchor[0], first_anchor[1], pattern_size=(2, 2))

    if not pattern:
        # If the first anchor led to an empty pattern (e.g., isolated pixel at edge), handle appropriately
        # This case is unlikely given problem structure but good to consider.
        # For now, assume a valid pattern is always found if first_anchor exists.
         # Let's try drawing just the first anchor pixel if pattern is empty? Or return empty grid?
         # Let's assume pattern is non-empty based on examples. If this fails, reconsider.
         pass


    # 3. Find all instances (anchors) of this pattern in the input grid
    input_anchors = find_all_pattern_instances(input_np, pattern)
    
    if not input_anchors:
         # If somehow no instances (or only the first one wasn't found again), return empty grid
         return output_grid.tolist()

    # 4. Sort the identified anchor points by position (row, then column)
    #    This naturally orders them along the diagonal they occupy.
    sorted_input_anchors = sorted(input_anchors, key=lambda p: (p[0], p[1]))

    # 5. Determine the target anchor positions by reversing the sorted list
    output_anchors = sorted_input_anchors[::-1] # Reversed list

    # 6. Draw the pattern at each target anchor position in the output grid
    for anchor in output_anchors:
        draw_pattern(output_grid, anchor, pattern)

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()