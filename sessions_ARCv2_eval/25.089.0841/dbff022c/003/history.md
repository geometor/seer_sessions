
## train_1

**input:**
```
0 4 4 4 4 4 0 3 4 6 9 5
0 4 0 4 0 4 0 3 6 7 2 9
0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 0 0 3 0 0 0 0 0 0 0
0 3 0 0 3 0 0 7 7 7 7 0
0 3 0 0 3 0 0 7 0 7 7 0
0 0 3 0 3 0 0 7 0 0 7 0
0 0 0 3 0 0 0 7 7 0 7 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 4 4 4 4 4 0 3 4 6 9 5
0 4 6 4 6 4 0 3 6 7 2 9
0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 3 3 3 0 0 7 7 7 7 0
0 3 3 3 3 0 0 7 0 7 7 0
0 0 3 3 3 0 0 7 0 0 7 0
0 0 0 3 0 0 0 7 7 0 7 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
2 6 0 0 8 8 8 8 0 0
4 5 0 0 8 0 0 8 0 0
6 8 0 0 8 0 0 8 0 0
8 1 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 4 4 4
0 5 0 0 0 5 0 4 0 4
0 0 5 5 5 5 0 4 4 4
0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 4 4 4
```


**output:**
```
2 6 0 0 8 8 8 8 0 0
4 5 0 0 8 1 1 8 0 0
6 8 0 0 8 1 1 8 0 0
8 1 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 4 4 4
0 5 0 0 0 5 0 4 5 4
0 0 5 5 5 5 0 4 4 4
0 0 0 0 0 0 0 4 5 4
0 0 0 0 0 0 0 4 4 4
```


## train_3

**input:**
```
0 2 6 0 4 4 4 4 4 0 2 2 2 2 0
0 7 1 0 4 0 0 0 4 0 2 0 2 2 0
0 0 0 0 4 0 0 0 4 0 2 2 0 2 0
0 0 0 0 4 4 4 4 4 0 2 2 2 2 0
```


**output:**
```
0 2 6 0 4 4 4 4 4 0 2 2 2 2 0
0 7 1 0 4 0 0 0 4 0 2 7 2 2 0
0 0 0 0 4 0 0 0 4 0 2 2 7 2 0
0 0 0 0 4 4 4 4 4 0 2 2 2 2 0
```

Okay, let's analyze the provided examples.

**Perception of Task Elements:**

1.  **Input/Output Structure:** Both input and output are grids of colored pixels (represented by integers 0-9). The output grid retains the same dimensions as the input grid.
2.  **Core Transformation:** The primary transformation involves filling in areas of white pixels (color 0) within the input grid. The surrounding structures and most other pixels remain unchanged.
3.  **Object Identification:** The non-white pixels form distinct shapes or objects. These objects often appear as closed boundaries (like rectangles or other polygons), sometimes complex.
4.  **Identifying Target Areas:** The white pixels that get filled are those completely enclosed within a non-white shape. White pixels connected to the grid's border are *not* filled. This suggests a concept of "inside" vs. "outside".
5.  **Fill Color Determination:** The color used to fill an enclosed white area seems dependent on the color of the single, unique non-white color that forms the immediate boundary around that white area. There appears to be a specific mapping or set of rules:
    *   If the boundary color is Green (3), the fill color is Green (3).
    *   If the boundary color is Orange (7), the fill color is Orange (7).
    *   If the boundary color is Gray (5), the fill color is Gray (5).
    *   If the boundary color is Gray (8), the fill color is Blue (1).
    *   If the boundary color is Red (2), the fill color is Orange (7).
    *   If the boundary color is Yellow (4), the fill color depends on the context of the *entire grid*:
        *   If Magenta (6) exists anywhere in the input grid, the fill color is Magenta (6) (seen in train\_1).
        *   Otherwise, if Gray (5) exists anywhere in the input grid, the fill color is Gray (5) (seen in train\_2).
        *   Otherwise, the fill color is Yellow (4) (seen in train\_3).
6.  **Process:** The process seems to be:
    *   Identify all white pixels enclosed by a single color.
    *   Determine the specific boundary color for each enclosed region.
    *   Apply the color mapping rule (including the conditional logic for Yellow) to find the fill color.
    *   Modify the input grid by replacing the enclosed white pixels with their determined fill color.

**Facts (YAML):**


```yaml
Grid:
  - Type: 2D Array
  - Cell Values: Integers 0-9 (representing colors)
  - Background Color: White (0)

Objects:
  - Type: Contiguous areas of non-white pixels.
  - Property: Often form closed boundaries.
  - Property: Can be composed of a single color (monochromatic) or multiple colors.

Target Areas:
  - Type: Regions of white (0) pixels.
  - Property: Must be completely enclosed by non-white pixels (not connected to the grid border by other white pixels).
  - Relationship: Each enclosed white region is bordered by exactly one unique non-white color in the examples provided.

Transformation:
  - Action: Fill enclosed white regions with a specific color.
  - Rule: The fill color (F) is determined by the unique border color (B) of the enclosed region.
  - Mapping:
      - If B=3 (Green), F=3 (Green).
      - If B=7 (Orange), F=7 (Orange).
      - If B=5 (Gray), F=5 (Gray).
      - If B=8 (Gray), F=1 (Blue).
      - If B=2 (Red), F=7 (Orange).
      - If B=4 (Yellow):
          - If color 6 (Magenta) exists anywhere in the input grid, F=6 (Magenta).
          - Else if color 5 (Gray) exists anywhere in the input grid, F=5 (Gray).
          - Else, F=4 (Yellow).
  - Invariance: Pixels not part of an enclosed white region remain unchanged. Grid dimensions remain unchanged.

Assumptions:
  - Each enclosed white region is bordered by only one unique non-white color.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all white pixels (color 0) in the input grid that are connected to any border of the grid (top, bottom, left, right) through a path of adjacent (sharing a side) white pixels. Mark these as "external white".
3.  Identify all remaining white pixels. These are the "internal white" pixels, forming one or more enclosed regions.
4.  For each distinct contiguous region of internal white pixels:
    a.  Find the set of all non-white pixels that are adjacent (sharing a side or corner) to any pixel within this internal white region.
    b.  Determine the unique color B present in this set of adjacent non-white pixels. (Assume there is only one unique color B).
    c.  Determine the fill color F based on the border color B:
        i.  If B is Gray (8), set F to Blue (1).
        ii. Else if B is Red (2), set F to Orange (7).
        iii. Else if B is Yellow (4):
            1. Scan the entire input grid. Check if Magenta (6) is present anywhere.
            2. If Magenta (6) is present, set F to Magenta (6).
            3. Else, scan the entire input grid. Check if Gray (5) is present anywhere.
            4. If Gray (5) is present, set F to Gray (5).
            5. Else, set F to Yellow (4).
        iv. Else (if B is Green (3), Orange (7), Gray (5), or any other color not covered above), set F to B.
    d.  For every pixel within the current internal white region, change its color in the output grid to the determined fill color F.
5.  Return the modified output grid.
```python
import numpy as np
from collections import deque

"""
Transformation Rule:

1. Identify regions of white pixels (color 0) in the input grid.
2. Determine if a white region is "internal" (completely enclosed by non-white pixels) or "external" (connected to the grid border by other white pixels).
3. For each internal white region:
    a. Find the single, unique color (B) of the non-white pixels directly adjacent (sharing a side) to the region.
    b. Determine the fill color (F) based on the border color (B) using the following rules:
        i. If B is Gray (8), F is Blue (1).
        ii. If B is Red (2), F is Orange (7).
        iii. If B is Yellow (4):
            - Check if Magenta (6) exists anywhere in the *entire* input grid. If yes, F is Magenta (6).
            - Else, check if Gray (5) exists anywhere in the *entire* input grid. If yes, F is Gray (5).
            - Otherwise, F is Yellow (4).
        iv. For all other border colors B (e.g., Green(3), Orange(7), Gray(5)), F is the same as B.
    c. Fill all pixels within that internal white region with the determined fill color F in the output grid.
4. External white regions and all non-white pixels remain unchanged in the output grid.
5. The output grid has the same dimensions as the input grid.
"""

def determine_fill_color(border_color, has_magenta, has_gray5):
    """Determines the fill color based on the border color and global grid colors."""
    if border_color == 8:
        return 1  # Blue
    elif border_color == 2:
        return 7  # Orange
    elif border_color == 4:
        if has_magenta:
            return 6  # Magenta
        elif has_gray5:
            return 5  # Gray
        else:
            return 4  # Yellow
    else:
        # For Green(3), Orange(7), Gray(5), etc. fill with the border color itself
        return border_color

def transform(input_grid):
    """
    Applies the transformation rule to fill internal white regions based on border colors.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    height, width = input_grid_np.shape
    visited = np.zeros_like(input_grid_np, dtype=bool)

    # Pre-calculate if colors 6 or 5 exist anywhere in the grid
    has_magenta = np.any(input_grid_np == 6)
    has_gray5 = np.any(input_grid_np == 5)

    # Iterate through each pixel to find starting points of white regions
    for r in range(height):
        for c in range(width):
            # If it's a white pixel and hasn't been visited yet, start exploring the region
            if input_grid_np[r, c] == 0 and not visited[r, c]:
                
                region_coords = []
                neighbor_colors = set()
                is_external = False
                queue = deque([(r, c)])
                visited[r, c] = True
                region_visited_mask = np.zeros_like(input_grid_np, dtype=bool) # Track visited within this specific region BFS
                region_visited_mask[r,c] = True

                # Breadth-First Search (BFS) to find the connected white region
                while queue:
                    curr_r, curr_c = queue.popleft()
                    region_coords.append((curr_r, curr_c))

                    # Check if this pixel touches the border
                    if curr_r == 0 or curr_r == height - 1 or curr_c == 0 or curr_c == width - 1:
                        is_external = True
                        # Note: We continue the BFS to mark all connected white cells as visited,
                        # even if external, to avoid processing them again.

                    # Explore 4-directional neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check if neighbor is within grid bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            neighbor_val = input_grid_np[nr, nc]
                            # If neighbor is white and not visited in this BFS
                            if neighbor_val == 0 and not region_visited_mask[nr, nc]:
                                visited[nr, nc] = True # Mark globally visited
                                region_visited_mask[nr, nc] = True # Mark visited for this region's BFS
                                queue.append((nr, nc))
                            # If neighbor is non-white, record its color
                            elif neighbor_val != 0:
                                neighbor_colors.add(neighbor_val)
                        # If neighbor is out of bounds, it implicitly connects to the 'outside'
                        # else: # If neighbor would be out of bounds
                           # is_external = True # This isn't strictly needed due to the border check above

                # After exploring the entire region, check if it's internal and has a single border color
                if not is_external and len(neighbor_colors) == 1:
                    border_color = list(neighbor_colors)[0]
                    fill_color = determine_fill_color(border_color, has_magenta, has_gray5)
                    
                    # Fill the identified internal region in the output grid
                    for reg_r, reg_c in region_coords:
                        output_grid[reg_r, reg_c] = fill_color
                # If it's external, or has multiple/no border colors, do nothing (leave as white 0)

    return output_grid.tolist()
```

Previous Code:
```python
import numpy as np
from collections import deque

"""
Transformation Rule:

1. Identify regions of white pixels (color 0) in the input grid.
2. Determine if a white region is "internal" (completely enclosed by non-white pixels) or "external" (connected to the grid border by other white pixels).
3. For each internal white region:
    a. Find the single, unique color (B) of the non-white pixels directly adjacent (sharing a side) to the region.
    b. Determine the fill color (F) based on the border color (B) using the following rules:
        i. If B is Gray (8), F is Blue (1).
        ii. If B is Red (2), F is Orange (7).
        iii. If B is Yellow (4):
            - Check if Magenta (6) exists anywhere in the *entire* input grid. If yes, F is Magenta (6).
            - Else, check if Gray (5) exists anywhere in the *entire* input grid. If yes, F is Gray (5).
            - Otherwise, F is Yellow (4).
        iv. For all other border colors B (e.g., Green(3), Orange(7), Gray(5)), F is the same as B.
    c. Fill all pixels within that internal white region with the determined fill color F in the output grid.
4. External white regions and all non-white pixels remain unchanged in the output grid.
5. The output grid has the same dimensions as the input grid.
"""

def determine_fill_color(border_color, has_magenta, has_gray5):
    """Determines the fill color based on the border color and global grid colors."""
    if border_color == 8:
        return 1  # Blue
    elif border_color == 2:
        return 7  # Orange
    elif border_color == 4:
        if has_magenta:
            return 6  # Magenta
        elif has_gray5:
            return 5  # Gray
        else:
            return 4  # Yellow
    else:
        # For Green(3), Orange(7), Gray(5), etc. fill with the border color itself
        return border_color

def transform(input_grid):
    """
    Applies the transformation rule to fill internal white regions based on border colors.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    height, width = input_grid_np.shape
    visited = np.zeros_like(input_grid_np, dtype=bool)

    # Pre-calculate if colors 6 or 5 exist anywhere in the grid
    has_magenta = np.any(input_grid_np == 6)
    has_gray5 = np.any(input_grid_np == 5)

    # Iterate through each pixel to find starting points of white regions
    for r in range(height):
        for c in range(width):
            # If it's a white pixel and hasn't been visited yet, start exploring the region
            if input_grid_np[r, c] == 0 and not visited[r, c]:
                
                region_coords = []
                neighbor_colors = set()
                is_external = False
                queue = deque([(r, c)])
                visited[r, c] = True
                region_visited_mask = np.zeros_like(input_grid_np, dtype=bool) # Track visited within this specific region BFS
                region_visited_mask[r,c] = True

                # Breadth-First Search (BFS) to find the connected white region
                while queue:
                    curr_r, curr_c = queue.popleft()
                    region_coords.append((curr_r, curr_c))

                    # Check if this pixel touches the border
                    if curr_r == 0 or curr_r == height - 1 or curr_c == 0 or curr_c == width - 1:
                        is_external = True
                        # Note: We continue the BFS to mark all connected white cells as visited,
                        # even if external, to avoid processing them again.

                    # Explore 4-directional neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check if neighbor is within grid bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            neighbor_val = input_grid_np[nr, nc]
                            # If neighbor is white and not visited in this BFS
                            if neighbor_val == 0 and not region_visited_mask[nr, nc]:
                                visited[nr, nc] = True # Mark globally visited
                                region_visited_mask[nr, nc] = True # Mark visited for this region's BFS
                                queue.append((nr, nc))
                            # If neighbor is non-white, record its color
                            elif neighbor_val != 0:
                                neighbor_colors.add(neighbor_val)
                        # If neighbor is out of bounds, it implicitly connects to the 'outside'
                        # else: # If neighbor would be out of bounds
                           # is_external = True # This isn't strictly needed due to the border check above

                # After exploring the entire region, check if it's internal and has a single border color
                if not is_external and len(neighbor_colors) == 1:
                    border_color = list(neighbor_colors)[0]
                    fill_color = determine_fill_color(border_color, has_magenta, has_gray5)
                    
                    # Fill the identified internal region in the output grid
                    for reg_r, reg_c in region_coords:
                        output_grid[reg_r, reg_c] = fill_color
                # If it's external, or has multiple/no border colors, do nothing (leave as white 0)

    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 4 4 4 4 4 0 3 4 6 9 5
0 4 0 4 0 4 0 3 6 7 2 9
0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 0 0 3 0 0 0 0 0 0 0
0 3 0 0 3 0 0 7 7 7 7 0
0 3 0 0 3 0 0 7 0 7 7 0
0 0 3 0 3 0 0 7 0 0 7 0
0 0 0 3 0 0 0 7 7 0 7 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 4 4 4 4 4 0 3 4 6 9 5
0 4 6 4 6 4 0 3 6 7 2 9
0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 3 3 3 0 0 7 7 7 7 0
0 3 3 3 3 0 0 7 0 7 7 0
0 0 3 3 3 0 0 7 0 0 7 0
0 0 0 3 0 0 0 7 7 0 7 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 4 4 4 4 4 0 3 4 6 9 5
0 4 6 4 6 4 0 3 6 7 2 9
0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 3 3 3 0 0 7 7 7 7 0
0 3 3 3 3 0 0 7 7 7 7 0
0 0 3 3 3 0 0 7 7 7 7 0
0 0 0 3 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 5.555555555555571

## Example 2:
Input:
```
2 6 0 0 8 8 8 8 0 0
4 5 0 0 8 0 0 8 0 0
6 8 0 0 8 0 0 8 0 0
8 1 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 4 4 4
0 5 0 0 0 5 0 4 0 4
0 0 5 5 5 5 0 4 4 4
0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 4 4 4
```
Expected Output:
```
2 6 0 0 8 8 8 8 0 0
4 5 0 0 8 1 1 8 0 0
6 8 0 0 8 1 1 8 0 0
8 1 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 4 4 4
0 5 0 0 0 5 0 4 5 4
0 0 5 5 5 5 0 4 4 4
0 0 0 0 0 0 0 4 5 4
0 0 0 0 0 0 0 4 4 4
```
Transformed Output:
```
2 6 0 0 8 8 8 8 0 0
4 5 0 0 8 1 1 8 0 0
6 8 0 0 8 1 1 8 0 0
8 1 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 4 4 4
0 5 5 5 5 5 0 4 6 4
0 0 5 5 5 5 0 4 4 4
0 0 0 0 0 0 0 4 6 4
0 0 0 0 0 0 0 4 4 4
```
Match: False
Pixels Off: 5
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 10.0

## Example 3:
Input:
```
0 2 6 0 4 4 4 4 4 0 2 2 2 2 0
0 7 1 0 4 0 0 0 4 0 2 0 2 2 0
0 0 0 0 4 0 0 0 4 0 2 2 0 2 0
0 0 0 0 4 4 4 4 4 0 2 2 2 2 0
```
Expected Output:
```
0 2 6 0 4 4 4 4 4 0 2 2 2 2 0
0 7 1 0 4 0 0 0 4 0 2 7 2 2 0
0 0 0 0 4 0 0 0 4 0 2 2 7 2 0
0 0 0 0 4 4 4 4 4 0 2 2 2 2 0
```
Transformed Output:
```
0 2 6 0 4 4 4 4 4 0 2 2 2 2 0
0 7 1 0 4 6 6 6 4 0 2 7 2 2 0
0 0 0 0 4 6 6 6 4 0 2 2 7 2 0
0 0 0 0 4 4 4 4 4 0 2 2 2 2 0
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 20.0
