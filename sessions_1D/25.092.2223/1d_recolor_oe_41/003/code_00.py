"""
Transformation Rule Description:
1. Interpret the input 1D array as a 2D grid. Assume dimensions are 4x8 if the input list length is 32.
2. Identify all distinct contiguous objects composed of yellow (4) pixels using 4-way adjacency (horizontal and vertical).
3. For each identified yellow object:
   a. Count the total number of pixels (size) in the object.
   b. If the object's total size is odd, determine the target color as orange (7).
   c. If the object's total size is even, determine the target color as green (3).
4. Create an output grid, initially a copy of the input grid.
5. For each yellow object, update all pixels belonging to that object in the output grid to its determined target color (orange or green).
6. Non-yellow pixels remain unchanged.
7. Convert the final 2D output grid back into a 1D list format.

Note: This rule perfectly explains Example 1 but contradicts the provided outputs for Examples 2 and 3, where single objects appear to be colored with both green and orange. The implementation follows the rule derived from Example 1.
"""

import numpy as np
from collections import deque

def _find_objects(grid, target_color):
    """
    Finds all contiguous objects of a specific color in the grid using 4-way connectivity.

    Args:
        grid (np.array): The 2D input grid.
        target_color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is a list of
              (row, col) coordinates belonging to that object.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            # If the cell has the target color and hasn't been visited yet, start a search
            if grid[r, c] == target_color and (r, c) not in visited:
                # Start Breadth-First Search (BFS) to find the current object
                current_object_coords = []
                q = deque([(r, c)])
                visited.add((r, c))
                
                while q:
                    curr_r, curr_c = q.popleft()
                    current_object_coords.append((curr_r, curr_c))
                    
                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        # Check if the neighbor is within grid boundaries
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if the neighbor has the target color and hasn't been visited
                            if grid[nr, nc] == target_color and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                q.append((nr, nc))
                                
                # Add the completed object (list of coordinates) to the list of objects
                if current_object_coords:
                    objects.append(current_object_coords)
                    
    return objects

def transform(input_list):
    """
    Transforms the input grid by recoloring contiguous yellow objects based 
    on the parity of their total size. Odd-sized objects become orange (7), 
    even-sized objects become green (3).

    Args:
        input_list (list): A 1D list representing the input grid.

    Returns:
        list: A 1D list representing the transformed output grid.
    """
    
    # --- Step 1: Determine grid dimensions and reshape ---
    input_len = len(input_list)
    rows, cols = -1, -1
    if input_len == 32: # Specific case observed in training
        rows, cols = 4, 8
    else:
        # Simple heuristic for square or near-square grids if length is not 32
        # TODO: Add more robust dimension inference if needed for test cases
        sqrt_len = int(np.sqrt(input_len))
        if sqrt_len * sqrt_len == input_len:
            rows, cols = sqrt_len, sqrt_len
        else: # Fallback or raise error if dimensions unclear
             raise ValueError(f"Cannot determine grid dimensions for input length {input_len}. Expecting length 32 (4x8) based on training.")

    input_grid = np.array(input_list).reshape((rows, cols))
    
    # --- Step 2: Initialize output grid ---
    # Start with a copy of the input, non-yellow pixels will remain unchanged
    output_grid = np.copy(input_grid)
    
    # --- Define target and output colors ---
    yellow = 4
    green = 3
    orange = 7
    
    # --- Step 3: Find all yellow objects ---
    yellow_objects = _find_objects(input_grid, yellow)
    
    # --- Step 4 & 5: Process each yellow object and recolor output grid ---
    for obj_coords in yellow_objects:
        # Calculate the total size of the current object
        obj_size = len(obj_coords)
        
        # Determine the target color based on the parity of the object's size
        if obj_size % 2 == 0: # Even size
            target_color = green
        else: # Odd size
            target_color = orange
            
        # Recolor all pixels belonging to this object in the output grid
        for r, c in obj_coords:
            output_grid[r, c] = target_color
            
    # --- Step 6: Format output ---
    # Flatten the 2D output grid back into a 1D list
    output_list = output_grid.flatten().tolist()
    
    # --- Step 7: Return result ---
    return output_list
