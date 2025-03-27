"""
Identifies connected components of non-orange (7) pixels using 8-way adjacency.
For each component, determines its bounding box.
If a component's bounding box is exactly 3x3 pixels in size:
1. Extracts the 3x3 subgrid from the input grid corresponding to this bounding box.
2. Applies a specific pixel rearrangement within this 3x3 subgrid:
    - Input(0,0) -> Output(2,0)
    - Input(0,1) -> Output(1,2)
    - Input(0,2) -> Output(0,0)
    - Input(1,0) -> Output(0,1)
    - Input(1,1) -> Output(1,1) (Center pixel remains)
    - Input(1,2) -> Output(2,1)
    - Input(2,0) -> Output(0,2)
    - Input(2,1) -> Output(1,0)
    - Input(2,2) -> Output(2,2)
   (Coordinates are relative to the top-left of the 3x3 subgrid).
3. Places the rearranged 3x3 subgrid into the output grid at the same location as the bounding box.
Pixels outside of these identified 3x3 bounding boxes remain unchanged from the input grid.
The output grid is initialized as a copy of the input grid.
"""

import numpy as np
from collections import deque

def _find_non_bg_components(grid, bg_color):
    """
    Finds connected components of pixels that are not the background color
    using 8-way adjacency.

    Args:
        grid (np.array): The input grid.
        bg_color (int): The background color to ignore.

    Returns:
        list[set]: A list of components, where each component is a set of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = set()
    components = []

    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is non-background and not visited
            if grid[r, c] != bg_color and (r, c) not in visited:
                # Start BFS to find a new component
                current_component = set()
                q = deque([(r, c)])
                visited.add((r, c))
                
                while q:
                    curr_r, curr_c = q.popleft()
                    current_component.add((curr_r, curr_c))
                    
                    # Explore 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue  # Skip self
                                
                            nr, nc = curr_r + dr, curr_c + dc
                            
                            # Check grid boundaries
                            if 0 <= nr < rows and 0 <= nc < cols:
                                # Check if neighbor is non-background and not visited
                                if grid[nr, nc] != bg_color and (nr, nc) not in visited:
                                    visited.add((nr, nc))
                                    q.append((nr, nc))
                                    
                if current_component: # Add component only if it's not empty
                    components.append(current_component)
                
    return components

def _get_bounding_box(component):
    """
    Calculates the bounding box of a component.

    Args:
        component (set): A set of (row, col) tuples representing the component.

    Returns:
        tuple: ((min_r, min_c), (max_r, max_c)) or None if component is empty.
    """
    if not component:
        return None
        
    min_r = min(r for r, c in component)
    min_c = min(c for r, c in component)
    max_r = max(r for r, c in component)
    max_c = max(c for r, c in component)
    
    return (min_r, min_c), (max_r, max_c)

def _apply_permutation(subgrid_3x3):
    """
    Applies the specific pixel rearrangement to a 3x3 subgrid.

    Args:
        subgrid_3x3 (np.array): A 3x3 numpy array.

    Returns:
        np.array: The rearranged 3x3 numpy array.
    """
    # Ensure the input is indeed 3x3
    if subgrid_3x3.shape != (3, 3):
        raise ValueError("Input subgrid must be 3x3")

    # Create a new 3x3 array to store the result
    permuted_subgrid = np.zeros_like(subgrid_3x3)

    # Apply the specific mapping
    permuted_subgrid[0, 0] = subgrid_3x3[0, 2]
    permuted_subgrid[0, 1] = subgrid_3x3[1, 0]
    permuted_subgrid[0, 2] = subgrid_3x3[2, 0]
    permuted_subgrid[1, 0] = subgrid_3x3[2, 1]
    permuted_subgrid[1, 1] = subgrid_3x3[1, 1]
    permuted_subgrid[1, 2] = subgrid_3x3[0, 1]
    permuted_subgrid[2, 0] = subgrid_3x3[0, 0]
    permuted_subgrid[2, 1] = subgrid_3x3[1, 2]
    permuted_subgrid[2, 2] = subgrid_3x3[2, 2]
    
    return permuted_subgrid

def transform(input_grid):
    """
    Transforms the input grid by applying a specific permutation to 3x3 blocks
    defined by the bounding boxes of non-orange connected components.
    """
    # Convert input list of lists to a numpy array for efficient manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_np = np.copy(input_np)
    
    # Define the background color (orange)
    bg_color = 7
    
    # Find all connected components of non-background pixels
    components = _find_non_bg_components(input_np, bg_color)
    
    # Process each component
    for component in components:
        # Calculate the bounding box of the component
        bbox = _get_bounding_box(component)
        if not bbox: # Should not happen if component is not empty, but check anyway
            continue
            
        (min_r, min_c), (max_r, max_c) = bbox
        
        # Calculate the dimensions of the bounding box
        height = max_r - min_r + 1
        width = max_c - min_c + 1
        
        # Check if the bounding box is exactly 3x3
        if height == 3 and width == 3:
            # Extract the 3x3 subgrid from the *original input* grid
            subgrid = input_np[min_r : min_r + 3, min_c : min_c + 3]
            
            # Apply the permutation to the extracted subgrid
            permuted_subgrid = _apply_permutation(subgrid)
            
            # Place the permuted subgrid into the *output* grid at the same location
            output_np[min_r : min_r + 3, min_c : min_c + 3] = permuted_subgrid
            
    # Convert the final numpy array back to a list of lists for the required output format
    return output_np.tolist()
