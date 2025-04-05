"""
Identifies the shape formed by the least frequent non-zero digit(s) in the input 
grid. Finds the largest contiguous group of other non-zero digits. Moves the 
marker shape to be centered within the bounding box of this largest group, 
overwriting existing digits. Sets the original locations of the marker shape to zero.
"""

import numpy as np
from collections import Counter
import math
from scipy.ndimage import label, find_objects, center_of_mass

def find_marker_info(grid):
    """
    Finds the least frequent non-zero digit, its locations, and its bounding box shape.
    
    Args:
        grid (np.array): The input grid.
        
    Returns:
        tuple: (marker_value, marker_locations, marker_shape, marker_origin) or (None, None, None, None)
               - marker_value: The integer value of the marker.
               - marker_locations: List of (row, col) tuples for the marker.
               - marker_shape: np.array representing the marker shape within its bounding box.
               - marker_origin: (row, col) of the top-left corner of the marker's bounding box in the original grid.
    """
    non_zeros = grid[grid != 0]
    if non_zeros.size == 0:
        return None, None, None, None

    counts = Counter(non_zeros)
    min_freq = min(counts.values())
    candidates = [digit for digit, freq in counts.items() if freq == min_freq]
    
    # Assuming the first candidate is the marker if there's a tie
    marker_value = candidates[0] 
    
    locations = np.argwhere(grid == marker_value)
    if locations.size == 0:
        return None, None, None, None
        
    marker_locations = [tuple(loc) for loc in locations]
    
    # Determine bounding box and shape
    if not marker_locations:
         return marker_value, [], None, None

    min_r = min(r for r, c in marker_locations)
    max_r = max(r for r, c in marker_locations)
    min_c = min(c for r, c in marker_locations)
    max_c = max(c for r, c in marker_locations)
    
    marker_origin = (min_r, min_c)
    shape_height = max_r - min_r + 1
    shape_width = max_c - min_c + 1
    
    marker_shape = np.zeros((shape_height, shape_width), dtype=int)
    for r, c in marker_locations:
        marker_shape[r - min_r, c - min_c] = marker_value
        
    return marker_value, marker_locations, marker_shape, marker_origin


def find_largest_component_center(grid, marker_value):
    """
    Finds the center of the bounding box of the largest connected component 
    of non-zero, non-marker digits. Uses 8-way connectivity.
    
    Args:
        grid (np.array): The input grid.
        marker_value (int): The value of the marker digit to exclude.
        
    Returns:
        tuple: (center_row, center_col) or (None, None) if no components found.
    """
    # Create a mask: 1 for target components, 0 for background and marker
    mask = (grid != 0) & (grid != marker_value)
    if not np.any(mask):
        return None, None

    # Label connected components (8-way connectivity default with structure=np.ones((3,3)))
    labeled_array, num_features = label(mask, structure=np.ones((3,3), dtype=bool))
    
    if num_features == 0:
        return None, None
        
    # Find the largest component
    component_sizes = np.bincount(labeled_array.ravel())
    # component_sizes[0] is the background size, ignore it
    if len(component_sizes) <= 1: # Only background label exists
         return None, None

    largest_component_label = np.argmax(component_sizes[1:]) + 1 # +1 because we ignored index 0
    
    # Find the bounding box (slice) of the largest component
    component_slice = find_objects(labeled_array == largest_component_label)[0]

    # Calculate the center of the bounding box
    # slice objects store (start, stop) for each dimension
    row_slice, col_slice = component_slice
    center_row = (row_slice.start + row_slice.stop - 1) // 2
    center_col = (col_slice.start + col_slice.stop - 1) // 2

    # Alternative: Center of mass (might be float)
    # center_row_f, center_col_f = center_of_mass(mask, labels=labeled_array, index=largest_component_label)
    # center_row = int(round(center_row_f))
    # center_col = int(round(center_col_f))
    
    return center_row, center_col

def transform(input_grid):
    """
    Identifies the shape formed by the least frequent non-zero digit(s), finds the 
    largest contiguous group of other non-zero digits, moves the marker shape to be 
    centered within the bounding box of this largest group, overwriting existing digits,
    and sets the original locations of the marker shape to zero.
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    
    # --- Step 1, 2, 3: Find marker info ---
    marker_value, marker_locations, marker_shape, _ = find_marker_info(input_np)
    
    if marker_value is None or marker_shape is None:
        # No marker found or marker is empty, return original grid
        return input_grid 
        
    # --- Step 4, 5: Find target center ---
    target_center_row, target_center_col = find_largest_component_center(input_np, marker_value)
    
    if target_center_row is None:
        # If no other components, maybe place at grid center? 
        # Based on example 3, it seems we need the target component.
        # Let's stick to the logic derived from examples. If no target, maybe no change?
        # Re-evaluating test case 3: the marker (4s) moves to the center of the 1s.
        # Re-evaluating train case 1: marker (4) moves to center of the X of 2s.
        # Re-evaluating train case 2: marker (7) moves to center of the border of 3s.
        # The logic holds. If no target component, the behavior is undefined by examples.
        # Returning original grid might be safest if no target is found.
         # Check if the only non-zeros ARE the marker
        non_zeros = input_np[input_np != 0]
        if len(np.unique(non_zeros)) == 1 and np.unique(non_zeros)[0] == marker_value:
             # Grid only contains the marker, no target component. Return original.
             # Or perhaps center it on the grid? Examples don't cover this. Let's return original.
             return input_grid
        # Fallback: if target component logic failed but there ARE other numbers, place at grid center?
        # Let's stick to requiring a target component for now based on strict interpretation of examples.
        # If this fails tests, we might need a fallback. For now, if no target component, return unchanged.
        print(f"Warning: No target component found for marker {marker_value}. Returning original grid.") # Added for debugging
        return input_grid # Or handle error appropriately


    # --- Step 7a: Clear original marker locations ---
    for r, c in marker_locations:
        output_np[r, c] = 0
        
    # --- Step 7b: Place marker shape centered at target ---
    shape_h, shape_w = marker_shape.shape
    
    # Calculate top-left corner for pasting the marker shape
    paste_r_start = target_center_row - (shape_h - 1) // 2
    paste_c_start = target_center_col - (shape_w - 1) // 2
    
    # Paste the shape, element by element, respecting shape's zeros (if any)
    for r_offset in range(shape_h):
        for c_offset in range(shape_w):
            paste_r = paste_r_start + r_offset
            paste_c = paste_c_start + c_offset
            
            # Check grid bounds
            if 0 <= paste_r < output_np.shape[0] and 0 <= paste_c < output_np.shape[1]:
                # Only overwrite if the marker shape has a non-zero value at this offset
                if marker_shape[r_offset, c_offset] != 0:
                     output_np[paste_r, paste_c] = marker_shape[r_offset, c_offset]

    # Convert back to list of lists
    output_grid = output_np.tolist()
    return output_grid