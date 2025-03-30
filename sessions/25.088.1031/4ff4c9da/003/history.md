
Previous Code:
```python
import numpy as np
from collections import deque

"""
Finds all contiguous blocks of azure (8) pixels in the input grid to identify 
source pattern shapes. Then, searches the input grid for blocks of any single 
color (other than white (0) or azure (8)) that exactly match the shape and 
bounding box size of any identified source pattern. Finally, recolors these 
matching target blocks to azure (8) in the output grid.
"""

def find_contiguous_blocks(grid, color):
    """
    Finds all contiguous blocks of a specified color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the blocks to find.

    Returns:
        list: A list of blocks, where each block is a list of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    blocks = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                # Start BFS to find the whole block
                current_block = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    current_block.append((row, col))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if current_block:
                    blocks.append(current_block)
    return blocks

def get_shape_and_bbox(block):
    """
    Calculates the normalized shape, bounding box, and top-left corner of a block.

    Args:
        block (list): A list of (row, col) tuples representing the block.

    Returns:
        tuple: (shape_frozenset, bbox_height, bbox_width, min_r, min_c)
               shape_frozenset: A frozenset of relative (dr, dc) coordinates.
               bbox_height: Height of the bounding box.
               bbox_width: Width of the bounding box.
               min_r: Top-most row index of the block.
               min_c: Left-most column index of the block.
    """
    if not block:
        return frozenset(), 0, 0, 0, 0

    rows, cols = zip(*block)
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    
    bbox_height = max_r - min_r + 1
    bbox_width = max_c - min_c + 1
    
    # Normalize coordinates relative to the top-left corner
    relative_coords = frozenset((r - min_r, c - min_c) for r, c in block)
    
    return relative_coords, bbox_height, bbox_width, min_r, min_c

def transform(input_grid):
    """
    Transforms the input grid based on pattern matching and recoloring.
    
    1. Finds all source patterns (contiguous blocks of azure/8).
    2. Stores the unique shapes and bounding boxes of these source patterns.
    3. Finds all potential target patterns (contiguous blocks of other colors, excluding 0 and 8).
    4. Compares the shape and bounding box of each potential target pattern to the source patterns.
    5. If a match is found, recolors the target pattern pixels to azure/8 in the output grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # --- Step 1 & 2: Identify unique source patterns (Azure=8) ---
    source_patterns = set()
    azure_blocks = find_contiguous_blocks(input_grid, 8)
    for block in azure_blocks:
        shape, bbox_h, bbox_w, _, _ = get_shape_and_bbox(block)
        if shape: # Ignore empty blocks if any somehow occur
             source_patterns.add((shape, bbox_h, bbox_w))

    # --- Step 3 & 4: Find potential target patterns and check against source patterns ---
    # Iterate through colors 1-7 and 9 (potential target colors)
    for target_color in list(range(1, 8)) + [9]:
        potential_target_blocks = find_contiguous_blocks(input_grid, target_color)
        
        for block in potential_target_blocks:
            shape, bbox_h, bbox_w, min_r, min_c = get_shape_and_bbox(block)
            
            # Check if this block's shape matches any source pattern shape
            if shape and (shape, bbox_h, bbox_w) in source_patterns:
                # --- Step 5: Recolor matched target patterns in the output grid ---
                for dr, dc in shape:
                    r, c = min_r + dr, min_c + dc
                    # Check bounds just in case, though should be within grid
                    if 0 <= r < rows and 0 <= c < cols:
                         output_grid[r, c] = 8 # Recolor to Azure
            
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
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

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
2 2 2 1 8 8 8 1 8 8 8 1 2 2 2 1 2
0 0 1 1 1 8 0 1 1 8 0 1 0 0 2 1 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 8 1 1 1 8 1 1 1 1 2 1 1
8 8 8 1 8 8 8 1 8 8 8 1 2 2 2 1 8
0 0 1 1 1 8 0 1 1 8 0 1 0 0 2 1 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 1 1 2 2 0 1 1 2 0 1 0 0 2 1 0
0 0 1 1 2 2 0 1 1 2 0 1 0 0 2 1 0
8 8 8 1 2 2 2 1 2 2 2 1 2 2 2 1 8
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 1 1 2 2 0 1 1 8 0 1 0 0 8 1 0
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 5.536332179930781
Okay, let's analyze the results and refine our understanding.

**General Assessment and Strategy**

The provided Python code implements a reasonable hypothesis based on the initial examples: identify template shapes from azure (8) blocks and recolor any non-white, non-azure blocks that match these templates (in shape and bounding box) to azure.

This strategy worked perfectly for the first two training examples. However, it failed on the third example. The `Transformed Output` for Example 3 changed *more* blocks to azure than the `Expected Output`. This indicates that the initial hypothesis (and the code implementing it) is too broad; there must be an additional condition or constraint determining *which* matching blocks should be recolored.

The current code finds *all* azure shapes, stores their geometries, and then recolors *any* other colored block that matches *any* of those stored geometries. The failure in Example 3 suggests that either not all azure blocks serve as templates, or not all matching blocks should be transformed.

**Strategy:**
1.  Gather detailed metrics on all examples, focusing on the properties of the azure blocks and the blocks that change color in the *expected* output vs. the *transformed* output, especially for Example 3.
2.  Identify the specific blocks that were incorrectly changed in Example 3 by the current code.
3.  Analyze the properties (location, neighbors, relation to azure blocks) of the correctly changed blocks versus the incorrectly changed blocks in Example 3 to find the missing condition.
4.  Update the factual observations (YAML) and the natural language program to reflect the refined understanding, explicitly noting the condition discovered. If a clear condition cannot be determined from the provided examples, the natural language program should reflect the best current hypothesis while acknowledging the discrepancy in Example 3.

**Metrics Gathering**

Let's gather some specific data about the examples. We need to identify the azure template shapes and the target shapes that get changed.


