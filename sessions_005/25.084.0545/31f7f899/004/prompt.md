
Previous Code:
```python
"""
1.  **Find Azure Line:** Locate the longest vertical line of azure (color 8) pixels. This line acts as a separator.

2.  **Identify Colored Objects:** Identify contiguous regions (objects) of the same color that are horizontally or vertically adjacent to each other (excluding the azure line). Each object must be adjacent to the azure line at some point.

3. **Find true lowest color:** For each colored object:
    * get the lowest row and lowest color of this object.

4.  **Modify Top and Bottom:** For each colored object:
    *   Find the top and bottom row extents for the entire object.
    *   Within the *horizontal bounds of the entire object*, change all pixels in the top and bottom rows to the lowest color found in the last step.

5.  **Output:** Return the modified grid.
"""

import numpy as np

def find_azure_line(grid):
    """Finds the 'azure' (8) vertical line, handling potential variations."""
    azure_lines = []
    rows, cols = grid.shape
    for c in range(cols):
      current_line = []
      for r in range(rows):
        if grid[r,c] == 8:
          current_line.append((r,c))
        else:
          if len(current_line) > 0:
            azure_lines.append(current_line)
          current_line = []
      if len(current_line) > 0:
            azure_lines.append(current_line)
    
    #find longest line
    longest_line = []
    for line in azure_lines:
      if len(line) > len(longest_line):
        longest_line = line

    return longest_line

def find_objects(grid, azure_line):
    """Identifies contiguous colored objects adjacent to the azure line."""
    rows, cols = grid.shape
    objects = []
    visited = set()
    azure_line_set = set(azure_line)

    def is_adjacent_to_azure_line(r, c, azure_line_set):
        """Checks if a cell is adjacent to the azure line."""
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) in azure_line_set:
                return True
        return False
    
    def dfs(r, c, current_object):
      """Performs Depth-First Search to find connected components."""
      if (r,c) in visited or not (0 <= r < rows and 0 <= c < cols) or grid[r,c] == 8:
        return
      
      #check if the current object is connected to azure, if not, stop
      if not is_adjacent_to_azure_line(r,c, azure_line_set):
        if not any(is_adjacent_to_azure_line(orow,ocol, azure_line_set) for orow,ocol in current_object):
          return
      
      visited.add((r,c))
      current_object.append((r,c))

      #Explore Neighbors
      for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        dfs(r + dr, c+dc, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 8 and (r, c) not in visited:  # Not azure and not visited
                current_object = []
                dfs(r, c, current_object)
                if len(current_object) > 0:
                  if any(is_adjacent_to_azure_line(orow,ocol, azure_line_set) for orow,ocol in current_object):
                    objects.append(current_object)

    return objects

def get_lowest_color(obj, grid):
    """find lowest row, and get the color"""
    lowest_row = -1
    lowest_color = -1

    for r,c in obj:
      if lowest_row == -1 or r > lowest_row:
        lowest_row = r
        lowest_color = grid[r,c]
    
    return lowest_color

def transform(input_grid):
    # initialize output_grid
    grid = np.array(input_grid)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # change output pixels 
    azure_line = find_azure_line(grid)
    objects = find_objects(grid, azure_line)

    for obj in objects:
      #get object details
      top_row = min([pixel[0] for pixel in obj])
      buttom_row = max([pixel[0] for pixel in obj])
      min_col = min([pixel[1] for pixel in obj])
      max_col = max([pixel[1] for pixel in obj])
      replacement_color = get_lowest_color(obj, grid)

      #replace colors
      for r,c in obj:
        if r == top_row or r == buttom_row:
            output_grid[r,c] = replacement_color
    

    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 5 8 8 8 8 8 8 8 8 8 8 8
8 5 8 8 8 8 2 8 8 8 8 8 8
8 5 8 8 8 8 2 7 8 8 8 8 8
8 5 8 8 8 8 2 7 1 8 8 8 8
6 5 6 6 6 6 2 7 1 6 6 6 6
8 5 8 8 8 8 2 7 1 8 8 8 8
8 5 8 8 8 8 2 7 8 8 8 8 8
8 5 8 8 8 8 2 8 8 8 8 8 8
8 5 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 1 8 8 8 8
8 8 8 8 8 8 8 7 1 8 8 8 8
8 8 8 8 8 8 2 7 1 8 8 8 8
8 5 8 8 8 8 2 7 1 8 8 8 8
6 5 6 6 6 6 2 7 1 6 6 6 6
8 5 8 8 8 8 2 7 1 8 8 8 8
8 8 8 8 8 8 2 7 1 8 8 8 8
8 8 8 8 8 8 8 7 1 8 8 8 8
8 8 8 8 8 8 8 8 1 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 5 8 8 8 8 8 8 8 8 8 8 8
8 5 8 8 8 8 2 8 8 8 8 8 8
8 5 8 8 8 8 2 7 8 8 8 8 8
8 5 8 8 8 8 2 7 1 8 8 8 8
6 5 6 6 6 6 2 7 1 6 6 6 6
8 5 8 8 8 8 2 7 1 8 8 8 8
8 5 8 8 8 8 2 7 8 8 8 8 8
8 5 8 8 8 8 2 8 8 8 8 8 8
8 5 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 16
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 18.93491124260356

## Example 2:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 4 8 7 8 5 8 8 8 8 8 9 8 8
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
6 6 4 6 7 6 5 6 1 6 6 6 9 6 6
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
8 8 4 8 7 8 5 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 7 8 5 8 1 8 8 8 9 8 8
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
6 6 4 6 7 6 5 6 1 6 6 6 9 6 6
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
8 8 8 8 7 8 5 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 4 8 7 8 5 8 8 8 8 8 9 8 8
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
6 6 4 6 7 6 5 6 1 6 6 6 9 6 6
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
8 8 4 8 7 8 5 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 12
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 10.666666666666657

## Example 3:
Input:
```
8 8 8 8 8 8 8
8 8 1 8 8 8 8
4 8 1 8 1 8 7
4 6 1 6 1 6 7
4 8 1 8 1 8 7
8 8 1 8 8 8 8
8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8
8 8 8 8 8 8 7
4 8 1 8 1 8 7
4 6 1 6 1 6 7
4 8 1 8 1 8 7
8 8 8 8 8 8 7
8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8
8 8 1 8 8 8 8
4 8 1 8 1 8 7
4 6 1 6 1 6 7
4 8 1 8 1 8 7
8 8 1 8 8 8 8
8 8 8 8 8 8 8
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 16.32653061224488
