
Previous Code:
```python
import numpy as np
from collections import deque

"""
Identifies unique shapes formed by contiguous blocks of azure (8) pixels in the 
input grid. These serve as templates. Then, searches the input grid specifically 
for contiguous blocks of red (2) pixels. If a red block exactly matches the 
shape and bounding box size of any identified azure template shape, that red 
block is recolored to azure (8) in the output grid. Other colors are ignored 
for transformation.
"""

def find_contiguous_blocks(grid, color):
    """
    Finds all contiguous blocks of a specified color in the grid using BFS.
    Considers only orthogonal neighbors (up, down, left, right).

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
                    
                    # Check 4 orthogonal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
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
    
    1. Find all contiguous blocks of azure (8) pixels to identify source patterns.
    2. Store the unique shapes (relative coordinates) and bounding box dimensions 
       of these azure source patterns.
    3. Find all contiguous blocks of red (2) pixels (potential target patterns).
    4. For each red block, calculate its shape and bounding box dimensions.
    5. Compare the shape and bounding box of each red block to the stored set of 
       azure source patterns.
    6. If a red block's shape and bounding box exactly match any source pattern, 
       recolor all pixels of that red block to azure (8) in the output grid.
    """
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # --- Step 1 & 2: Identify unique source patterns (Azure=8) ---
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

    # --- Step 3, 4 & 5: Find red blocks and check against source patterns ---
    target_color = 2 # Specifically look for red blocks
    # Find all contiguous blocks of red pixels
    potential_target_blocks = find_contiguous_blocks(input_grid, target_color)
    
    # Process each potential red target block
    for block in potential_target_blocks:
        # Get its normalized shape, bounding box dimensions, and top-left corner
        shape, bbox_h, bbox_w, min_r, min_c = get_shape_and_bbox(block)
        
        # Check if this red block's shape and bounding box match any source pattern
        if shape and (shape, bbox_h, bbox_w) in source_patterns:
            # --- Step 6: Recolor matched red blocks in the output grid ---
            # Iterate through the relative coordinates of the shape
            for dr, dc in shape:
                # Calculate the absolute coordinates in the grid
                r, c = min_r + dr, min_c + dc
                # Double-check bounds (should always be within grid)
                if 0 <= r < rows and 0 <= c < cols:
                     output_grid[r, c] = 8 # Recolor the pixel to Azure
            
    # Return the modified grid
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 8 0 2 1
1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 8 8 8 2 1
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 8 0 2 1
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1
```
Expected Output:
```
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 1 2 0 8 0 2 1 0 0 2 0 0 1 2 0 8 0 2 1
1 1 1 2 8 8 8 2 1 1 1 2 1 1 1 2 8 8 8 2 1
0 0 1 2 0 8 0 2 1 0 0 2 0 0 1 2 0 8 0 2 1
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 1 2 0 8 0 2 1 0 0 2 0 0 1 2 0 8 0 2 1
1 1 1 2 8 8 8 2 1 1 1 2 1 1 1 2 8 8 8 2 1
0 0 1 2 0 8 0 2 1 0 0 2 0 0 1 2 0 8 0 2 1
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1
```
Transformed Output:
```
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 8 0 2 1
1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 8 8 8 2 1
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 8 0 2 1
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1
0 0 1 2 0 1 0 2 1 0 0 2 0 0 1 2 0 1 0 2 1
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1 1 1 2 1
```
Match: False
Pixels Off: 15
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 6.802721088435391

## Example 2:
Input:
```
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
2 2 2 1 2 1 2 1 2 2 2 1 2 2 2 1 2 1 2 1 2 2 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 2 2 1 2 1 2 1 2 2 2 1 2 2 2 1 2 1 2 1 2 2 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 2 1 2 1 0 1 8 8 0 1 0 0 2 1 0 1 0 1 2 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 2 2 1 2 1 2 1 2 2 2 1 2 2 2 1 8 1 2 1 2 2 2
2 2 2 1 2 1 2 1 2 2 2 1 2 2 2 1 8 1 2 1 2 2 2
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
2 2 2 1 2 1 2 1 2 2 2 1 2 2 2 1 2 1 2 1 2 2 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 2 2 1 2 1 2 1 2 2 2 1 2 2 2 1 2 1 2 1 2 2 2
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
```
Expected Output:
```
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
2 2 2 1 2 1 2 1 2 2 2 1 2 2 2 1 2 1 2 1 2 2 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 2 2 1 2 1 2 1 2 2 2 1 2 2 2 1 2 1 2 1 2 2 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 2 1 2 1 0 1 8 8 0 1 0 0 2 1 0 1 0 1 2 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 2 2 1 2 1 8 1 2 2 2 1 2 2 2 1 8 1 8 1 2 2 2
2 2 2 1 2 1 8 1 2 2 2 1 2 2 2 1 8 1 8 1 2 2 2
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
2 2 2 1 2 1 2 1 2 2 2 1 2 2 2 1 2 1 2 1 2 2 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 2 1 2 1 0 1 8 8 0 1 0 0 2 1 0 1 0 1 2 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 2 1 2 1 0 1 8 8 0 1 0 0 2 1 0 1 0 1 2 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 2 2 1 2 1 2 1 2 2 2 1 2 2 2 1 2 1 2 1 2 2 2
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
```
Transformed Output:
```
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
2 2 2 1 2 1 2 1 2 2 2 1 2 2 2 1 2 1 2 1 2 2 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 2 2 1 2 1 2 1 2 2 2 1 2 2 2 1 2 1 2 1 2 2 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 2 1 2 1 0 1 8 8 0 1 0 0 2 1 0 1 0 1 2 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 2 2 1 2 1 8 1 2 2 2 1 2 2 2 1 8 1 8 1 2 2 2
2 2 2 1 2 1 8 1 2 2 2 1 2 2 2 1 8 1 8 1 2 2 2
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
2 2 2 1 2 1 2 1 2 2 2 1 2 2 2 1 2 1 2 1 2 2 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 2 1 2 1 0 1 8 8 0 1 0 0 2 1 0 1 0 1 2 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 2 1 2 1 0 1 8 8 0 1 0 0 2 1 0 1 0 1 2 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 2 2 1 2 1 2 1 2 2 2 1 2 2 2 1 2 1 2 1 2 2 2
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
0 0 2 1 2 1 0 1 2 2 0 1 0 0 2 1 0 1 0 1 2 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 3:
Input:
```
0 0 1 1 2 2 0 1 1 2 0 1 0 0 2 1 0
0 0 1 1 2 2 0 1 1 2 0 1 0 0 2 1 0
1 1 1 1 2 2 1 1 1 2 1 1 1 1 2 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 2 2 1 1 8 1 1 1 2 1 1 2 2 2 1 2
2 2 2 1 8 1 8 1 2 1 2 1 2 2 2 1 2
0 0 1 1 1 8 0 1 1 2 0 1 0 0 2 1 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 2 1 1 1 2 1 1 1 1 2 1 1
8 8 8 1 2 1 2 1 2 1 2 1 2 2 2 1 2
0 0 1 1 1 2 0 1 1 2 0 1 0 0 2 1 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 1 1 2 2 0 1 1 2 0 1 0 0 2 1 0
0 0 1 1 2 2 0 1 1 2 0 1 0 0 2 1 0
2 2 2 1 2 2 2 1 2 2 2 1 2 2 2 1 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 1 1 2 2 0 1 1 2 0 1 0 0 2 1 0
```
Expected Output:
```
0 0 1 1 2 2 0 1 1 2 0 1 0 0 2 1 0
0 0 1 1 2 2 0 1 1 2 0 1 0 0 2 1 0
1 1 1 1 2 2 1 1 1 2 1 1 1 1 2 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 2 2 1 1 8 1 1 1 8 1 1 2 2 2 1 2
2 2 2 1 8 1 8 1 8 1 8 1 2 2 2 1 2
0 0 1 1 1 8 0 1 1 8 0 1 0 0 2 1 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 8 1 1 1 8 1 1 1 1 2 1 1
8 8 8 1 8 1 8 1 8 1 8 1 2 2 2 1 2
0 0 1 1 1 8 0 1 1 8 0 1 0 0 2 1 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 1 1 2 2 0 1 1 2 0 1 0 0 2 1 0
0 0 1 1 2 2 0 1 1 2 0 1 0 0 2 1 0
8 8 8 1 2 2 2 1 2 2 2 1 2 2 2 1 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 1 1 2 2 0 1 1 2 0 1 0 0 2 1 0
```
Transformed Output:
```
0 0 1 1 2 2 0 1 1 2 0 1 0 0 2 1 0
0 0 1 1 2 2 0 1 1 2 0 1 0 0 2 1 0
1 1 1 1 2 2 1 1 1 2 1 1 1 1 2 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 2 2 1 1 8 1 1 1 8 1 1 2 2 2 1 2
2 2 2 1 8 1 8 1 8 1 8 1 2 2 2 1 2
0 0 1 1 1 8 0 1 1 8 0 1 0 0 2 1 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 8 1 1 1 8 1 1 1 1 2 1 1
8 8 8 1 8 1 8 1 8 1 8 1 2 2 2 1 8
0 0 1 1 1 8 0 1 1 8 0 1 0 0 2 1 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 1 1 2 2 0 1 1 2 0 1 0 0 2 1 0
0 0 1 1 2 2 0 1 1 2 0 1 0 0 2 1 0
8 8 8 1 2 2 2 1 2 2 2 1 2 2 2 1 8
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 1 1 2 2 0 1 1 8 0 1 0 0 8 1 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 2.768166089965405
