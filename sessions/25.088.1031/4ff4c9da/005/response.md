```python
import numpy as np
from collections import deque

"""
Identifies unique template shapes formed by contiguous blocks of azure (8) pixels in the 
input grid, considering 8-way adjacency (orthogonal and diagonal). These templates 
are characterized by their normalized shape (relative coordinates) and bounding box 
dimensions. 

Then, searches the input grid for contiguous blocks of red (2) pixels, also using 
8-way adjacency. 

If a red block exactly matches the shape and bounding box dimensions of any identified 
azure template shape, that red block is recolored entirely to azure (8) in the output 
grid. All other pixels retain their original color.
"""

def find_contiguous_blocks(grid, color):
    """
    Finds all contiguous blocks of a specified color in the grid using BFS.
    Considers 8-way adjacency (orthogonal and diagonal neighbors).

    Args:
        grid (np.array): The input grid (2D NumPy array).
        color (int): The color of the blocks to find.

    Returns:
        list: A list of blocks, where each block is a list of (row, col) tuples
              representing the coordinates of the pixels in that block.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    blocks = []

    # Define 8 directions for neighbors (orthogonal + diagonal)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), 
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for r in range(rows):
        for c in range(cols):
            # If we find a pixel of the target color that hasn't been visited
            if grid[r, c] == color and not visited[r, c]:
                # Start a Breadth-First Search (BFS) to find the entire contiguous block
                current_block = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    current_block.append((row, col))
                    
                    # Check 8 neighbors (orthogonal and diagonal)
                    for dr, dc in directions:
                        nr, nc = row + dr, col + dc
                        
                        # Check if the neighbor is within grid bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if the neighbor has the same color and hasn't been visited
                            if not visited[nr, nc] and grid[nr, nc] == color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                
                # Add the found block to the list if it's not empty
                if current_block:
                    blocks.append(current_block)
    return blocks

def get_shape_and_bbox(block):
    """
    Calculates the normalized shape, bounding box dimensions, and top-left 
    corner of a block. The shape is represented as a frozenset of relative 
    coordinates (dr, dc) from the top-left corner.

    Args:
        block (list): A list of (row, col) tuples representing the block.

    Returns:
        tuple: (shape_frozenset, bbox_height, bbox_width, min_r, min_c)
               shape_frozenset: A frozenset of relative (dr, dc) coordinates.
               bbox_height: Height of the bounding box.
               bbox_width: Width of the bounding box.
               min_r: Top-most row index of the block in the original grid.
               min_c: Left-most column index of the block in the original grid.
               Returns (frozenset(), 0, 0, 0, 0) for an empty block.
    """
    if not block:
        return frozenset(), 0, 0, 0, 0

    # Extract all row and column coordinates
    rows, cols = zip(*block)
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    
    # Calculate bounding box dimensions
    bbox_height = max_r - min_r + 1
    bbox_width = max_c - min_c + 1
    
    # Normalize coordinates relative to the top-left corner (min_r, min_c)
    # This creates a representation of the shape independent of its position
    relative_coords = frozenset((r - min_r, c - min_c) for r, c in block)
    
    return relative_coords, bbox_height, bbox_width, min_r, min_c

def transform(input_grid):
    """
    Transforms the input grid by recoloring specific red blocks to azure.
    
    1. Find all contiguous blocks (using 8-way adjacency) of azure (8) pixels 
       to identify source patterns (templates).
    2. Store the unique shapes (relative coordinates) and bounding box dimensions 
       of these azure source patterns.
    3. Find all contiguous blocks (using 8-way adjacency) of red (2) pixels 
       (potential target patterns).
    4. For each red block, calculate its shape and bounding box dimensions.
    5. Compare the shape and bounding box of each red block to the stored set of 
       azure source patterns.
    6. If a red block's shape and bounding box exactly match any source pattern, 
       recolor all pixels of that red block to azure (8) in the output grid.
    """
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # --- Step 1 & 2: Identify unique source patterns (Azure=8) using 8-way adjacency ---
    source_patterns = set() # Use a set to store unique (shape, bbox_h, bbox_w) tuples
    # Find all contiguous blocks of azure pixels
    azure_blocks = find_contiguous_blocks(input_grid, 8) 
    # Process each azure block
    for block in azure_blocks:
        # Get its normalized shape and bounding box dimensions
        shape, bbox_h, bbox_w, _, _ = get_shape_and_bbox(block)
        # Add the shape and dimensions to the set if the shape is not empty
        if shape: 
             source_patterns.add((shape, bbox_h, bbox_w))

    # --- Step 3, 4 & 5: Find red blocks (Red=2) using 8-way adjacency and check against source patterns ---
    target_color = 2 # Specifically look for red blocks
    # Find all contiguous blocks of red pixels
    potential_target_blocks = find_contiguous_blocks(input_grid, target_color)
    
    # Process each potential red target block
    for block in potential_target_blocks:
        # Get its normalized shape, bounding box dimensions, and original coordinates
        shape, bbox_h, bbox_w, _, _ = get_shape_and_bbox(block) # min_r, min_c not needed here
        
        # Check if this red block's shape and bounding box match any source pattern
        if shape and (shape, bbox_h, bbox_w) in source_patterns:
            # --- Step 6: Recolor matched red blocks in the output grid ---
            # Iterate through the actual coordinates of the matched block
            for r, c in block:
                # Double-check bounds (though coordinates from block should always be valid)
                if 0 <= r < rows and 0 <= c < cols:
                     output_grid[r, c] = 8 # Recolor the pixel to Azure
            
    # Return the modified grid
    return output_grid
```