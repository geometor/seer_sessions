import numpy as np
from collections import Counter

"""
This program transforms an input grid based on reflection rules across a central axis.
The specific reflection behavior depends on the orientation and color of the axis,
the background color, and the color of the object being reflected.

Based on the training examples:

Case 1 (Vertical Blue Axis, Red Background - like train_1):
1. Find the vertical axis (Blue, color 1) and background color (Red, color 2).
2. Identify Azure objects (color 8) located to the left of the axis.
3. Reflect these Azure objects across the axis, copying the Azure color to the destination.
4. For each row containing part of an original left-side Azure object, fill the space between the original object's rightmost pixel and the axis with Blue (1).
5. Similarly, fill the space between the axis and the reflected object's leftmost pixel with Blue (1) on those same rows.
6. Other colors (like Yellow, color 4) remain unchanged.

Case 2 (Horizontal Red Axis, Azure Background - like train_2):
1. Find the horizontal axis (Red, color 2) and background color (Azure, color 8).
2. Identify Green objects (color 3) located below the axis.
3. Reflect these Green objects across the axis, copying the Green color to the destination.
4. Identify Blue pixels (color 1) located above the axis.
5. Reflect these Blue pixels across the axis.
6. For each reflected Blue pixel, check the color of the corresponding destination cell in the *original input grid*.
7. If the original destination cell was the background color (Azure, 8), change the cell in the *output grid* to Red (2). Otherwise, the destination cell keeps its value (which might have been changed by the Green reflection if they overlap, or its original value).
"""

def find_axis(grid):
    """Finds the central axis (row or column)."""
    height, width = grid.shape
    
    # Check for horizontal axis (row)
    for r in range(height):
        row = grid[r, :]
        unique_colors = np.unique(row)
        if len(unique_colors) == 1:
             # Check if it spans the full width and is not the most frequent color overall (potential background)
             counts = Counter(grid.flatten())
             axis_color = unique_colors[0]
             # Simple check: assume axis is not the absolute most frequent color if others exist
             if len(counts) > 1 and counts[axis_color] == width: 
                 # Check if it's roughly central
                 if abs(r - (height - 1) / 2) < height * 0.2: # Allow some leeway from perfect center
                     return 'H', r, axis_color

    # Check for vertical axis (column)
    for c in range(width):
        col = grid[:, c]
        unique_colors = np.unique(col)
        if len(unique_colors) == 1:
             counts = Counter(grid.flatten())
             axis_color = unique_colors[0]
             if len(counts) > 1 and counts[axis_color] == height:
                 # Check if it's roughly central
                 if abs(c - (width - 1) / 2) < width * 0.2:
                    return 'V', c, axis_color
                    
    # Fallback/Error case: No clear single-color axis found
    # This part might need refinement based on more complex cases
    # For now, assume an axis as described is always present based on examples
    # Try finding the most frequent color that forms a line
    counts = Counter(grid.flatten())
    most_common_color, _ = counts.most_common(1)[0]
    
    for r in range(height):
         row = grid[r, :]
         if np.all(row == most_common_color):
              # Is this the *only* row with this property? Could be ambiguous
              # Check centrality again
              if abs(r - (height - 1) / 2) < height * 0.2:
                  return 'H', r, most_common_color

    for c in range(width):
         col = grid[:, c]
         if np.all(col == most_common_color):
              if abs(c - (width - 1) / 2) < width * 0.2:
                 return 'V', c, most_common_color
                 
    # If still nothing, raise an error or return None
    # Based on provided examples, we expect to find one.
    # print("Warning: Axis not definitively found using simple checks.")
    # Let's try the most frequent color logic again, less strictly
    if height > 1:
        for r in range(height):
            row = grid[r, :]
            unique_colors = np.unique(row)
            if len(unique_colors) == 1:
                 # Simplification: First full line found is axis
                 return 'H', r, unique_colors[0]
    if width > 1:
        for c in range(width):
            col = grid[:, c]
            unique_colors = np.unique(col)
            if len(unique_colors) == 1:
                 return 'V', c, unique_colors[0]
                 
    # Should not happen based on examples
    raise ValueError("Could not find axis")


def find_background_color(grid, axis_info):
    """Finds the most frequent color excluding the axis color."""
    axis_orientation, axis_index, axis_color = axis_info
    counts = Counter(grid.flatten())
    
    # Remove axis color count
    if axis_color in counts:
        del counts[axis_color]
        
    if not counts:
        # Handle grids that might only contain the axis color?
        # Or grids where background is same as axis (unlikely in ARC?)
        # Fallback: Assume 0 (black/white usually) if no other color exists
         return 0 
        
    # Most frequent remaining color is background
    background_color, _ = counts.most_common(1)[0]
    return background_color

def reflect_point(r, c, axis_info, grid_shape):
    """Calculates reflected coordinates across the axis."""
    axis_orientation, axis_index, _ = axis_info
    height, width = grid_shape
    
    r_refl, c_refl = r, c
    
    if axis_orientation == 'V':
        c_refl = axis_index + (axis_index - c)
    elif axis_orientation == 'H':
        r_refl = axis_index + (axis_index - r)
        
    # Ensure reflected points are within bounds (although logic should handle this)
    r_refl = max(0, min(height - 1, r_refl))
    c_refl = max(0, min(width - 1, c_refl))
            
    return r_refl, c_refl

def transform(input_grid):
    """
    Transforms the input grid based on reflection rules derived from examples.
    """
    input_grid = np.array(input_grid)
    output_grid = input_grid.copy()
    height, width = input_grid.shape

    # 1. Identify Axis and Background
    try:
        axis_info = find_axis(input_grid)
    except ValueError as e:
        print(f"Error finding axis: {e}")
        # Return copy if axis isn't found (or handle as needed)
        return output_grid.tolist() 
        
    axis_orientation, axis_index, axis_color = axis_info
    background_color = find_background_color(input_grid, axis_info)

    # 2. Apply transformation rules based on axis type
    
    # Case 1: Vertical Axis (like train_1)
    if axis_orientation == 'V' and axis_color == 1 and background_color == 2:
        azure_pixels_left = []
        affected_rows = set()
        
        # Find Azure (8) pixels left of the axis
        for r in range(height):
            for c in range(axis_index):
                if input_grid[r, c] == 8:
                    azure_pixels_left.append((r, c))
                    affected_rows.add(r)

        # Reflect Azure pixels
        for r, c in azure_pixels_left:
            r_refl, c_refl = reflect_point(r, c, axis_info, (height, width))
            # Check bounds just in case, though reflection logic should be okay
            if 0 <= r_refl < height and 0 <= c_refl < width:
                 output_grid[r_refl, c_refl] = 8

        # Fill between original and reflected Azure pixels with Blue (1)
        for r in affected_rows:
            # Find original max col and reflected min col for this row
            cols_orig = [c for row, c in azure_pixels_left if row == r]
            if not cols_orig: continue # Should not happen if row is in affected_rows
            
            max_c_orig = max(cols_orig)
            
            # Reflect the original *minimum* column point to find the *minimum* reflected column
            min_c_orig = min(cols_orig)
            _, min_c_refl = reflect_point(r, min_c_orig, axis_info, (height,width))

            # Fill left side of axis
            if max_c_orig + 1 < axis_index:
                output_grid[r, max_c_orig + 1 : axis_index] = 1
            
            # Fill right side of axis
            if axis_index + 1 < min_c_refl:
                 output_grid[r, axis_index + 1 : min_c_refl] = 1
                 
    # Case 2: Horizontal Axis (like train_2)
    elif axis_orientation == 'H' and axis_color == 2 and background_color == 8:
        # Reflect Green (3) from bottom to top first
        for r in range(axis_index + 1, height):
            for c in range(width):
                if input_grid[r, c] == 3:
                    r_refl, c_refl = reflect_point(r, c, axis_info, (height, width))
                    if 0 <= r_refl < height and 0 <= c_refl < width:
                        output_grid[r_refl, c_refl] = 3
                        
        # Reflect Blue (1) from top to bottom conditionally
        for r in range(axis_index):
             for c in range(width):
                 if input_grid[r, c] == 1:
                     r_refl, c_refl = reflect_point(r, c, axis_info, (height, width))
                     if 0 <= r_refl < height and 0 <= c_refl < width:
                         # Check the ORIGINAL input grid's destination color
                         if input_grid[r_refl, c_refl] == background_color: # Background is 8
                             output_grid[r_refl, c_refl] = 2 # Change to Red

    # If axis/color combination doesn't match known cases, return copy
    # else:
        # print(f"Warning: Unhandled axis/color combination: {axis_info}, bg: {background_color}")
        # pass # Returns the initial copy

    return output_grid.tolist()