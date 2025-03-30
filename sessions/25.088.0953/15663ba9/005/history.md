
Previous Code:
```python
import numpy as np
from typing import List, Tuple

"""
Identifies the primary non-black color (C) in the input grid.
Iterates through each pixel of the input grid.
If a pixel has color C:
  Count its orthogonal neighbors (up, down, left, right) that also have color C.
  Let N be the list of coordinates of these same-colored neighbors.
  If the count is exactly 2:
    Let the neighbors be N[0] = (r1, c1) and N[1] = (r2, c2).
    Check if the neighbors form a corner configuration around the current pixel (r, c).
    This occurs if the neighbors are not opposite each other (i.e., r1 != r2 AND c1 != c2).
    If it's a corner configuration, change the pixel's color to yellow (4) in the output grid.
    If it's a line configuration (r1 == r2 OR c1 == c2), keep the color C.
  If the count is exactly 3:
    Change the pixel's color to red (2) in the output grid.
  Otherwise (count 0, 1, 4, or 2 in a line):
    Keep the original color C.
Pixels that are not of the primary color C (including black background) remain unchanged.
"""

def find_primary_color(grid: np.ndarray) -> int:
    """Finds the most frequent non-black color in the grid."""
    colors, counts = np.unique(grid, return_counts=True)
    # Filter out black (color 0)
    non_black_mask = colors != 0
    non_black_colors = colors[non_black_mask]
    non_black_counts = counts[non_black_mask]

    if non_black_colors.size == 0:
        # Handle case where grid might be all black or empty
        return 0 
    
    # Find the index of the most frequent non-black color
    most_frequent_idx = np.argmax(non_black_counts)
    return non_black_colors[most_frequent_idx]

def get_orthogonal_neighbors_coords(grid: np.ndarray, r: int, c: int) -> List[Tuple[int, int]]:
    """Gets the coordinates of orthogonal neighbors within grid bounds."""
    neighbors_coords = []
    rows, cols = grid.shape
    # Define potential moves (up, down, left, right)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        # Check if the neighbor coordinates are within the grid boundaries
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors_coords.append((nr, nc))
    return neighbors_coords

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on neighbor count and configuration.
    - Primary color pixels with 3 primary color neighbors become Red (2).
    - Primary color pixels with 2 primary color neighbors in a corner configuration become Yellow (4).
    - All other pixels retain their original color.
    """
    input_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_np = np.copy(input_np)
    rows, cols = input_np.shape

    # Step 1: Identify the primary non-black color
    primary_color = find_primary_color(input_np)
    
    # If no primary color found (e.g., all black grid), return the original grid
    if primary_color == 0: 
        return output_np.tolist() 

    # Step 2: Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            # Step 3: Check if the current pixel is of the primary color
            if input_np[r, c] == primary_color:
                
                # Step 4: Find orthogonal neighbors and count those with the primary color
                neighbor_coords = get_orthogonal_neighbors_coords(input_np, r, c)
                primary_neighbors = []
                for nr, nc in neighbor_coords:
                    if input_np[nr, nc] == primary_color:
                        primary_neighbors.append((nr, nc))
                
                neighbor_count = len(primary_neighbors)

                # Step 5: Apply transformation rules based on neighbor count and configuration
                
                # Rule for Red (3 neighbors)
                if neighbor_count == 3:
                    output_np[r, c] = 2 # Red
                    
                # Rule for Yellow (2 neighbors in a corner)
                elif neighbor_count == 2:
                    # Get coordinates of the two primary neighbors
                    (r1, c1) = primary_neighbors[0]
                    (r2, c2) = primary_neighbors[1]
                    
                    # Check if neighbors are in a corner configuration (not opposite each other)
                    # Opposite means rows are same OR columns are same.
                    # Corner means rows are different AND columns are different.
                    if r1 != r2 and c1 != c2:
                        output_np[r, c] = 4 # Yellow
                    # Else (if neighbor_count is 2 but neighbors are in a line): 
                    # no change needed, pixel remains primary_color (already set in output_np copy)
                        
                # Else (neighbor_count is 0, 1, 4, or 2-in-a-line):
                # no change needed, pixel remains primary_color (already set in output_np copy)

    # Step 6: Return the transformed grid as a list of lists
    return output_np.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 0 0 0 0 0
0 0 3 3 3 0 0 3 0 0 0 0 0
0 0 3 0 0 0 0 3 0 0 0 0 0
0 0 3 0 0 3 3 3 0 0 0 0 0
0 0 3 3 3 3 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 3 3 0 3 0
0 0 0 0 0 0 0 0 3 0 0 3 0
0 0 0 0 3 3 3 3 3 0 0 3 0
0 0 0 0 3 0 0 0 0 0 0 3 0
0 0 0 0 3 0 0 0 3 3 3 3 0
0 0 0 0 3 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 3 3 4 0 0 0 0 0
0 0 4 3 2 0 0 3 0 0 0 0 0
0 0 3 0 0 0 0 3 0 0 0 0 0
0 0 3 0 0 2 3 4 0 0 0 0 0
0 0 4 3 3 4 0 0 0 4 3 4 0
0 0 0 0 0 0 0 0 4 2 0 3 0
0 0 0 0 0 0 0 0 3 0 0 3 0
0 0 0 0 4 3 3 3 2 0 0 3 0
0 0 0 0 3 0 0 0 0 0 0 3 0
0 0 0 0 3 0 0 0 2 3 3 4 0
0 0 0 0 4 3 3 3 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 3 3 4 0 0 0 0 0
0 0 4 3 4 0 0 3 0 0 0 0 0
0 0 3 0 0 0 0 3 0 0 0 0 0
0 0 3 0 0 4 3 4 0 0 0 0 0
0 0 4 3 3 4 0 0 0 4 3 4 0
0 0 0 0 0 0 0 0 4 4 0 3 0
0 0 0 0 0 0 0 0 3 0 0 3 0
0 0 0 0 4 3 3 3 4 0 0 3 0
0 0 0 0 3 0 0 0 0 0 0 3 0
0 0 0 0 3 0 0 0 4 3 3 4 0
0 0 0 0 4 3 3 3 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 5
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 5.917159763313606

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0
0 8 8 0 0 0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 0 0 8 0 0 8 8 8 8 8
0 0 8 0 8 8 8 8 0 0 8 0 0 0 8
0 0 8 8 8 0 0 0 0 0 8 8 0 0 8
0 0 0 0 0 0 0 0 0 0 0 8 0 0 8
0 0 0 0 0 0 0 0 0 8 8 8 0 8 8
0 0 8 8 8 0 0 0 0 8 0 0 0 8 0
0 0 8 0 8 0 0 0 0 8 8 8 8 8 0
0 0 8 8 8 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 8 8 8 8 8 4 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0
0 4 2 0 0 0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 0 0 8 0 0 4 8 8 8 4
0 0 8 0 2 8 8 4 0 0 8 0 0 0 8
0 0 4 8 4 0 0 0 0 0 4 2 0 0 8
0 0 0 0 0 0 0 0 0 0 0 8 0 0 8
0 0 0 0 0 0 0 0 0 4 8 2 0 2 4
0 0 4 8 4 0 0 0 0 8 0 0 0 8 0
0 0 8 0 8 0 0 0 0 4 8 8 8 4 0
0 0 4 8 4 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 8 8 8 8 8 4 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0
0 4 4 0 0 0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 0 0 8 0 0 4 8 8 8 4
0 0 8 0 4 8 8 4 0 0 8 0 0 0 8
0 0 4 8 4 0 0 0 0 0 4 4 0 0 8
0 0 0 0 0 0 0 0 0 0 0 8 0 0 8
0 0 0 0 0 0 0 0 0 4 8 4 0 4 4
0 0 4 8 4 0 0 0 0 8 0 0 0 8 0
0 0 8 0 8 0 0 0 0 4 8 8 8 4 0
0 0 4 8 4 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 5
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 5.555555555555571

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 1 1 1 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 1 0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0
0 0 0 0 0 0 0 0 1 1 1 0 0 1 1 0
0 0 0 1 1 1 1 1 1 0 0 0 0 0 1 0
0 0 0 1 0 0 0 0 0 0 1 1 1 0 1 0
0 0 0 1 1 1 1 1 1 1 1 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 1 1 1 1 4 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 2 1 4 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 4 1 2 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 1 0 0 2 1 4 0 0 0 0 0 0 0
0 0 0 4 1 1 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 1 1 4 0 0
0 0 0 0 0 0 0 0 4 1 2 0 0 2 4 0
0 0 0 4 1 1 1 1 2 0 0 0 0 0 1 0
0 0 0 1 0 0 0 0 0 0 2 1 2 0 1 0
0 0 0 4 1 1 1 1 1 1 4 0 4 1 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 1 1 1 1 4 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 4 1 4 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 4 1 4 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 1 0 0 4 1 4 0 0 0 0 0 0 0
0 0 0 4 1 1 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 1 1 4 0 0
0 0 0 0 0 0 0 0 4 1 4 0 0 4 4 0
0 0 0 4 1 1 1 1 4 0 0 0 0 0 1 0
0 0 0 1 0 0 0 0 0 0 4 1 4 0 1 0
0 0 0 4 1 1 1 1 1 1 4 0 4 1 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 7.142857142857139
