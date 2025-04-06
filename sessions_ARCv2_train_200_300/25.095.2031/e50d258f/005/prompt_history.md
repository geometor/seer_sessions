
## train_1

**input:**
```
1 1 1 8 0 0 0 0 0 0
1 8 1 1 0 1 8 8 1 8
8 2 8 1 0 8 1 8 2 8
1 1 1 8 0 8 8 8 8 1
8 1 8 8 0 8 1 2 8 2
0 0 0 0 0 8 8 8 1 8
0 0 0 0 0 1 1 8 1 8
0 8 2 2 0 8 1 1 8 2
0 2 2 1 0 0 0 0 0 0
0 2 1 8 0 0 0 0 0 0
```


**output:**
```
8 2 2
2 2 1
2 1 8
```


## train_2

**input:**
```
0 0 0 0 0 0 8 8 8 8
0 8 8 8 8 0 8 2 2 8
0 8 1 8 8 0 8 8 8 8
0 8 8 2 8 0 8 2 1 8
0 8 8 8 8 0 8 8 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 0
0 0 0 8 8 8 2 8 8 0
0 0 0 8 2 8 1 8 8 0
0 0 0 8 1 8 8 8 8 0
```


**output:**
```
8 8 8 8
8 2 2 8
8 8 8 8
8 2 1 8
8 8 8 8
```


## train_3

**input:**
```
2 8 8 8 0 0 0 0 0 0
8 8 1 8 0 0 0 0 0 0
1 8 8 8 0 0 0 0 0 0
8 8 8 2 0 0 1 8 8 2
8 2 8 1 0 0 8 8 1 8
8 1 8 8 0 0 8 2 8 8
0 0 0 0 0 0 8 8 8 1
0 0 0 0 0 0 1 8 8 8
0 0 0 0 0 0 8 8 1 8
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 8 8 8
8 8 1 8
1 8 8 8
8 8 8 2
8 2 8 1
8 1 8 8
```

## Perception

The input is a 10x10 grid of digits. The digits used are 0, 1, 2, and 8. The digit '0' appears to function as a background or empty space. The digits '1', '2', and '8' form distinct clusters or shapes within the grid, separated by the '0' digits.

The output is a smaller rectangular grid containing only the digits '1', '2', and '8'. The '0' digits are absent in the output. The dimensions of the output grid vary between examples.

The core transformation seems to involve identifying a specific cluster of non-zero digits in the input grid and extracting the minimal rectangular region (bounding box) that encompasses this cluster. Based on the examples, the selected cluster is the one whose bounding box contains *only* non-zero digits from the input grid (no '0's fall within the selected bounding box).

## Facts


```yaml
Data:
  - type: Grid
    description: Represents the input and output structures.
    properties:
      rows: Integer (Input is 10, Output varies)
      columns: Integer (Input is 10, Output varies)
      cells: List of Lists of Integers

Digits:
  - type: BackgroundDigit
    value: 0
    description: Represents empty space, separating foreground objects.
  - type: ForegroundDigit
    value: [1, 2, 8]
    description: Represents the content of objects or patterns.

Objects:
  - type: ConnectedComponent
    description: A cluster of adjacent (horizontally or vertically) ForegroundDigits. Input grids may contain multiple components.
    properties:
      cells: List of coordinates containing ForegroundDigits belonging to the component.
      bounding_box: The minimal rectangle enclosing all cells of the component.
        properties:
          min_row: Integer
          max_row: Integer
          min_col: Integer
          max_col: Integer
      is_solid: Boolean (Derived property - True if the bounding box in the input grid contains only ForegroundDigits, False otherwise)

Transformation:
  - action: IdentifyComponents
    description: Find all distinct ConnectedComponents of ForegroundDigits in the input grid.
  - action: CalculateBoundingBoxes
    description: Determine the minimal bounding box for each identified component.
  - action: CheckSolidity
    description: For each component's bounding box, check if all cells within that box in the *input* grid contain ForegroundDigits.
  - action: SelectComponent
    description: Choose the single component whose bounding box is solid (contains no BackgroundDigits).
    assumption: Exactly one such component exists in each input.
  - action: ExtractSubgrid
    description: Create the output grid by copying the portion of the input grid defined by the selected component's bounding box.
```


## Natural Language Program

1.  **Identify Non-Zero Components:** Scan the input grid and identify all distinct connected components formed by adjacent (sharing an edge) non-zero digits (1, 2, or 8). Treat the digit 0 as empty space separating components.
2.  **Determine Bounding Boxes:** For each identified component, calculate its minimal bounding box by finding the minimum and maximum row and column indices occupied by the digits within that component.
3.  **Find Solid Bounding Box:** Examine each component's bounding box. Check if the rectangular subgrid defined by this bounding box in the original input grid contains *only* non-zero digits (i.e., it contains no 0s).
4.  **Select Target Component:** Select the component whose bounding box was identified as solid in the previous step. (Based on the examples, it's assumed there will be exactly one such component).
5.  **Extract Output:** The output grid is the rectangular subgrid from the input grid corresponding exactly to the bounding box of the selected solid component.
```python
"""
Identifies all distinct connected components of non-zero digits (1, 2, or 8) in the input grid, treating 0 as a separator.
For each component, calculates its minimal bounding box.
Finds the single component whose bounding box subgrid in the original input contains *only* non-zero digits (a "solid" bounding box).
Extracts and returns the subgrid corresponding to this solid bounding box.
"""

from collections import deque

def _find_components(grid: list[list[int]]) -> list[list[tuple[int, int]]]:
    """
    Finds all connected components of non-zero elements in the grid.

    Args:
        grid: The input grid.

    Returns:
        A list of components, where each component is a list of (row, col) tuples.
    """
    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0 and (r, c) not in visited:
                # Start BFS to find a new component
                current_component = []
                q = deque([(r, c)])
                visited.add((r, c))

                while q:
                    curr_r, curr_c = q.popleft()
                    current_component.append((curr_r, curr_c))

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds and if neighbor is non-zero and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr][nc] != 0 and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                
                components.append(current_component)

    return components

def _get_bounding_box(component: list[tuple[int, int]]) -> tuple[int, int, int, int]:
    """
    Calculates the minimal bounding box for a component.

    Args:
        component: A list of (row, col) tuples representing the component.

    Returns:
        A tuple (min_row, min_col, max_row, max_col).
    """
    if not component:
        return (0, 0, -1, -1) # Indicate empty or invalid

    min_r = min(r for r, c in component)
    min_c = min(c for r, c in component)
    max_r = max(r for r, c in component)
    max_c = max(c for r, c in component)

    return min_r, min_c, max_r, max_c

def _is_solid(grid: list[list[int]], bbox: tuple[int, int, int, int]) -> bool:
    """
    Checks if the subgrid defined by the bounding box contains only non-zero elements.

    Args:
        grid: The input grid.
        bbox: The bounding box tuple (min_row, min_col, max_row, max_col).

    Returns:
        True if the bounding box area is solid (no zeros), False otherwise.
    """
    min_r, min_c, max_r, max_c = bbox
    if min_r > max_r or min_c > max_c: # Handle empty case if needed
        return False

    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if grid[r][c] == 0:
                return False
    return True

def _extract_subgrid(grid: list[list[int]], bbox: tuple[int, int, int, int]) -> list[list[int]]:
    """
    Extracts the subgrid defined by the bounding box.

    Args:
        grid: The input grid.
        bbox: The bounding box tuple (min_row, min_col, max_row, max_col).

    Returns:
        The extracted subgrid as a list of lists.
    """
    min_r, min_c, max_r, max_c = bbox
    subgrid = []
    for r in range(min_r, max_r + 1):
        subgrid.append(grid[r][min_c : max_c + 1])
    return subgrid

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by finding the solid non-zero component and extracting its bounding box.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the extracted solid subgrid.
    """
    
    # 1. Identify Non-Zero Components
    components = _find_components(input_grid)
    
    solid_bbox = None

    # Iterate through components to find the solid one
    for component in components:
        if not component:
            continue
            
        # 2. Determine Bounding Boxes for each component
        bbox = _get_bounding_box(component)
        
        # 3. Find Solid Bounding Box
        if _is_solid(input_grid, bbox):
            # 4. Select Target Component (assuming only one solid)
            solid_bbox = bbox
            break # Found the solid bounding box

    if solid_bbox is None:
        # Handle case where no solid bounding box is found, though examples suggest one always exists
        return [] 

    # 5. Extract Output
    output_grid = _extract_subgrid(input_grid, solid_bbox)

    return output_grid
```
```python
"""
Transforms the input grid by:
1. Identifying all distinct connected components of non-zero digits (1, 2, or 8), treating 0 as background.
2. Calculating the bounding box, area, and cell count for each component.
3. Filtering to find components that perfectly fill their bounding box (area equals cell count).
4. Selecting the perfectly filled component with the minimum bounding box area.
5. Extracting and returning the subgrid corresponding to the selected component's bounding box.
"""

from collections import deque
import sys # Used for float('inf') as initial minimum area

def _find_components(grid: list[list[int]]) -> list[list[tuple[int, int]]]:
    """
    Finds all connected components of non-zero elements in the grid using BFS.

    Args:
        grid: The input grid.

    Returns:
        A list of components, where each component is a list of (row, col) tuples.
    """
    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    components = []

    for r in range(rows):
        for c in range(cols):
            # Start BFS if cell is non-zero and not visited
            if grid[r][c] != 0 and (r, c) not in visited:
                current_component = []
                q = deque([(r, c)])
                visited.add((r, c))

                while q:
                    curr_r, curr_c = q.popleft()
                    current_component.append((curr_r, curr_c))

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds and if neighbor is non-zero and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr][nc] != 0 and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                
                components.append(current_component) # Add the completed component

    return components

def _get_bounding_box(component: list[tuple[int, int]]) -> tuple[int, int, int, int]:
    """
    Calculates the minimal bounding box for a component.

    Args:
        component: A list of (row, col) tuples representing the component.

    Returns:
        A tuple (min_row, min_col, max_row, max_col). Returns (0, 0, -1, -1) for empty components.
    """
    if not component:
        return (0, 0, -1, -1) # Indicate empty or invalid

    # Find min/max row and column from the component's cell coordinates
    min_r = min(r for r, c in component)
    min_c = min(c for r, c in component)
    max_r = max(r for r, c in component)
    max_c = max(c for r, c in component)

    return min_r, min_c, max_r, max_c

def _calculate_bbox_area(bbox: tuple[int, int, int, int]) -> int:
    """Calculates the area of a bounding box."""
    min_r, min_c, max_r, max_c = bbox
    if min_r > max_r or min_c > max_c: # Handle invalid/empty bbox
        return 0
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return height * width

def _extract_subgrid(grid: list[list[int]], bbox: tuple[int, int, int, int]) -> list[list[int]]:
    """
    Extracts the subgrid defined by the bounding box.

    Args:
        grid: The input grid.
        bbox: The bounding box tuple (min_row, min_col, max_row, max_col).

    Returns:
        The extracted subgrid as a list of lists.
    """
    min_r, min_c, max_r, max_c = bbox
    if min_r > max_r or min_c > max_c: # Handle invalid/empty bbox
        return []
        
    subgrid = []
    for r in range(min_r, max_r + 1):
        # Extract the row slice corresponding to the bbox columns
        subgrid.append(grid[r][min_c : max_c + 1])
    return subgrid


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation logic to find and extract the smallest, 
    perfectly filled, non-zero component from the input grid.
    """
    
    # 1. Identify Non-Zero Components
    components = _find_components(input_grid)
    
    min_area = sys.float_info.max # Initialize with positive infinity
    best_bbox = None

    # 2. Calculate Component Properties & 3. Find Perfectly Filled Components
    for component in components:
        if not component:
            continue # Skip empty components if any occur

        cell_count = len(component)
        bbox = _get_bounding_box(component)
        bbox_area = _calculate_bbox_area(bbox)

        # Check if the component perfectly fills its bounding box
        is_perfectly_filled = (bbox_area == cell_count)

        # 4. Select Smallest Perfectly Filled Component
        if is_perfectly_filled:
            # If this component is smaller than the current best, update
            if bbox_area < min_area:
                min_area = bbox_area
                best_bbox = bbox

    # Handle case where no perfectly filled component is found
    if best_bbox is None:
        return [] 

    # 5. Extract Output using the bounding box of the selected component
    output_grid = _extract_subgrid(input_grid, best_bbox)

    return output_grid
```

Previous Code:
```python
"""
Transforms the input grid by:
1. Identifying all distinct connected components of non-zero digits (1, 2, or 8), treating 0 as background.
2. Calculating the bounding box, area, and cell count for each component.
3. Filtering to find components that perfectly fill their bounding box (area equals cell count).
4. Selecting the perfectly filled component with the minimum bounding box area.
5. Extracting and returning the subgrid corresponding to the selected component's bounding box.
"""

from collections import deque
import sys # Used for float('inf') as initial minimum area

def _find_components(grid: list[list[int]]) -> list[list[tuple[int, int]]]:
    """
    Finds all connected components of non-zero elements in the grid using BFS.

    Args:
        grid: The input grid.

    Returns:
        A list of components, where each component is a list of (row, col) tuples.
    """
    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    components = []

    for r in range(rows):
        for c in range(cols):
            # Start BFS if cell is non-zero and not visited
            if grid[r][c] != 0 and (r, c) not in visited:
                current_component = []
                q = deque([(r, c)])
                visited.add((r, c))

                while q:
                    curr_r, curr_c = q.popleft()
                    current_component.append((curr_r, curr_c))

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds and if neighbor is non-zero and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr][nc] != 0 and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                
                components.append(current_component) # Add the completed component

    return components

def _get_bounding_box(component: list[tuple[int, int]]) -> tuple[int, int, int, int]:
    """
    Calculates the minimal bounding box for a component.

    Args:
        component: A list of (row, col) tuples representing the component.

    Returns:
        A tuple (min_row, min_col, max_row, max_col). Returns (0, 0, -1, -1) for empty components.
    """
    if not component:
        return (0, 0, -1, -1) # Indicate empty or invalid

    # Find min/max row and column from the component's cell coordinates
    min_r = min(r for r, c in component)
    min_c = min(c for r, c in component)
    max_r = max(r for r, c in component)
    max_c = max(c for r, c in component)

    return min_r, min_c, max_r, max_c

def _calculate_bbox_area(bbox: tuple[int, int, int, int]) -> int:
    """Calculates the area of a bounding box."""
    min_r, min_c, max_r, max_c = bbox
    if min_r > max_r or min_c > max_c: # Handle invalid/empty bbox
        return 0
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return height * width

def _extract_subgrid(grid: list[list[int]], bbox: tuple[int, int, int, int]) -> list[list[int]]:
    """
    Extracts the subgrid defined by the bounding box.

    Args:
        grid: The input grid.
        bbox: The bounding box tuple (min_row, min_col, max_row, max_col).

    Returns:
        The extracted subgrid as a list of lists.
    """
    min_r, min_c, max_r, max_c = bbox
    if min_r > max_r or min_c > max_c: # Handle invalid/empty bbox
        return []
        
    subgrid = []
    for r in range(min_r, max_r + 1):
        # Extract the row slice corresponding to the bbox columns
        subgrid.append(grid[r][min_c : max_c + 1])
    return subgrid


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation logic to find and extract the smallest, 
    perfectly filled, non-zero component from the input grid.
    """
    
    # 1. Identify Non-Zero Components
    components = _find_components(input_grid)
    
    min_area = sys.float_info.max # Initialize with positive infinity
    best_bbox = None

    # 2. Calculate Component Properties & 3. Find Perfectly Filled Components
    for component in components:
        if not component:
            continue # Skip empty components if any occur

        cell_count = len(component)
        bbox = _get_bounding_box(component)
        bbox_area = _calculate_bbox_area(bbox)

        # Check if the component perfectly fills its bounding box
        is_perfectly_filled = (bbox_area == cell_count)

        # 4. Select Smallest Perfectly Filled Component
        if is_perfectly_filled:
            # If this component is smaller than the current best, update
            if bbox_area < min_area:
                min_area = bbox_area
                best_bbox = bbox

    # Handle case where no perfectly filled component is found
    if best_bbox is None:
        return [] 

    # 5. Extract Output using the bounding box of the selected component
    output_grid = _extract_subgrid(input_grid, best_bbox)

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 1 1 8 0 0 0 0 0 0
1 8 1 1 0 1 8 8 1 8
8 2 8 1 0 8 1 8 2 8
1 1 1 8 0 8 8 8 8 1
8 1 8 8 0 8 1 2 8 2
0 0 0 0 0 8 8 8 1 8
0 0 0 0 0 1 1 8 1 8
0 8 2 2 0 8 1 1 8 2
0 2 2 1 0 0 0 0 0 0
0 2 1 8 0 0 0 0 0 0
```
Expected Output:
```
8 2 2
2 2 1
2 1 8
```
Transformed Output:
```
8 2 2
2 2 1
2 1 8
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 2:
Input:
```
0 0 0 0 0 0 8 8 8 8
0 8 8 8 8 0 8 2 2 8
0 8 1 8 8 0 8 8 8 8
0 8 8 2 8 0 8 2 1 8
0 8 8 8 8 0 8 8 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 0
0 0 0 8 8 8 2 8 8 0
0 0 0 8 2 8 1 8 8 0
0 0 0 8 1 8 8 8 8 0
```
Expected Output:
```
8 8 8 8
8 2 2 8
8 8 8 8
8 2 1 8
8 8 8 8
```
Transformed Output:
```
8 8 8 8
8 1 8 8
8 8 2 8
8 8 8 8
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
Color Count Correct: False
Score: None

## Example 3:
Input:
```
2 8 8 8 0 0 0 0 0 0
8 8 1 8 0 0 0 0 0 0
1 8 8 8 0 0 0 0 0 0
8 8 8 2 0 0 1 8 8 2
8 2 8 1 0 0 8 8 1 8
8 1 8 8 0 0 8 2 8 8
0 0 0 0 0 0 8 8 8 1
0 0 0 0 0 0 1 8 8 8
0 0 0 0 0 0 8 8 1 8
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
2 8 8 8
8 8 1 8
1 8 8 8
8 8 8 2
8 2 8 1
8 1 8 8
```
Transformed Output:
```
2 8 8 8
8 8 1 8
1 8 8 8
8 8 8 2
8 2 8 1
8 1 8 8
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0
## General Assessment

The initial code successfully identified and extracted "solid" rectangular components (where the component's non-zero cells perfectly fill its bounding box). It correctly solved Examples 1 and 3 but failed on Example 2.

The failure occurred because the selection criterion ("smallest area") was incorrect. Example 2 requires selecting a component (Area 20) that is neither the smallest (Area 16) nor the largest (Area 24) among the solid rectangular components.

The new strategy involves adding a filtering step: only consider solid rectangular components that touch at least one edge of the 10x10 input grid. After filtering, the selection criterion remains finding the component with the minimum area, using top-most, then left-most as tie-breakers. This revised strategy appears consistent with all three training examples.

## Metrics Gathering

Let's verify the properties of the solid rectangular components (which are also the maximal solid rectangles in these examples) for each training case.

**Definitions:**
*   **Component:** A set of connected non-zero cells found via BFS.
*   **BBox:** Minimal bounding box (min_r, min_c, max_r, max_c).
*   **Solid:** The component perfectly fills its bounding box (number of cells == bbox_area). All examples here have components that are solid rectangles.
*   **Touches Edge:** True if min_r=0, min_c=0, max_r=9, or max_c=9 (assuming 10x10 grid, 0-indexed).
*   **Area:** (max_r - min_r + 1) * (max_c - min_c + 1)



*code_execution:*
```python
import numpy as np
from collections import deque

def find_components(grid):
    rows, cols = grid.shape
    visited = set()
    components = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_component = []
                q = deque([(r, c)])
                visited.add((r, c))
                min_r, min_c, max_r, max_c = r, c, r, c
                while q:
                    curr_r, curr_c = q.popleft()
                    current_component.append((curr_r, curr_c))
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                
                bbox = (min_r, min_c, max_r, max_c)
                area = (max_r - min_r + 1) * (max_c - min_c + 1)
                is_solid = (len(current_component) == area)
                touches_edge = (min_r == 0 or min_c == 0 or max_r == rows - 1 or max_c == cols - 1)
                
                # Only store solid components for analysis based on observations
                if is_solid:
                    components.append({
                        'bbox': bbox,
                        'area': area,
                        'touches_edge': touches_edge,
                        'top_left': (min_r, min_c),
                        'cell_count': len(current_component) # Should equal area if solid
                    })
    return components

# Example 1 Data
grid1 = np.array([
    [1, 1, 1, 8, 0, 0, 0, 0, 0, 0],
    [1, 8, 1, 1, 0, 1, 8, 8, 1, 8],
    [8, 2, 8, 1, 0, 8, 1, 8, 2, 8],
    [1, 1, 1, 8, 0, 8, 8, 8, 8, 1],
    [8, 1, 8, 8, 0, 8, 1, 2, 8, 2],
    [0, 0, 0, 0, 0, 8, 8, 8, 1, 8],
    [0, 0, 0, 0, 0, 1, 1, 8, 1, 8],
    [0, 8, 2, 2, 0, 8, 1, 1, 8, 2],
    [0, 2, 2, 1, 0, 0, 0, 0, 0, 0],
    [0, 2, 1, 8, 0, 0, 0, 0, 0, 0]
])

# Example 2 Data
grid2 = np.array([
    [0, 0, 0, 0, 0, 0, 8, 8, 8, 8],
    [0, 8, 8, 8, 8, 0, 8, 2, 2, 8],
    [0, 8, 1, 8, 8, 0, 8, 8, 8, 8],
    [0, 8, 8, 2, 8, 0, 8, 2, 1, 8],
    [0, 8, 8, 8, 8, 0, 8, 8, 8, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 8, 8, 8, 8, 8, 8, 0],
    [0, 0, 0, 8, 8, 8, 2, 8, 8, 0],
    [0, 0, 0, 8, 2, 8, 1, 8, 8, 0],
    [0, 0, 0, 8, 1, 8, 8, 8, 8, 0]
])

# Example 3 Data
grid3 = np.array([
    [2, 8, 8, 8, 0, 0, 0, 0, 0, 0],
    [8, 8, 1, 8, 0, 0, 0, 0, 0, 0],
    [1, 8, 8, 8, 0, 0, 0, 0, 0, 0],
    [8, 8, 8, 2, 0, 0, 1, 8, 8, 2],
    [8, 2, 8, 1, 0, 0, 8, 8, 1, 8],
    [8, 1, 8, 8, 0, 0, 8, 2, 8, 8],
    [0, 0, 0, 0, 0, 0, 8, 8, 8, 1],
    [0, 0, 0, 0, 0, 0, 1, 8, 8, 8],
    [0, 0, 0, 0, 0, 0, 8, 8, 1, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

components1 = find_components(grid1)
components2 = find_components(grid2)
components3 = find_components(grid3)

print("--- Example 1 Components ---")
for comp in components1: print(comp)
print("\n--- Example 2 Components ---")
for comp in components2: print(comp)
print("\n--- Example 3 Components ---")
for comp in components3: print(comp)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Example 1 Components ---
{'bbox': (0, 0, 4, 3), 'area': 20, 'touches_edge': True, 'top_left': (0, 0), 'cell_count': 20}
{'bbox': (1, 5, 7, 9), 'area': 35, 'touches_edge': True, 'top_left': (1, 5), 'cell_count': 35}
{'bbox': (7, 1, 9, 3), 'area': 9, 'touches_edge': True, 'top_left': (7, 1), 'cell_count': 9}

--- Example 2 Components ---
{'bbox': (0, 6, 4, 9), 'area': 20, 'touches_edge': True, 'top_left': (0, 6), 'cell_count': 20}
{'bbox': (1, 1, 4, 4), 'area': 16, 'touches_edge': False, 'top_left': (1, 1), 'cell_count': 16}
{'bbox': (6, 3, 9, 8), 'area': 24, 'touches_edge': True, 'top_left': (6, 3), 'cell_count': 24}

--- Example 3 Components ---
{'bbox': (0, 0, 5, 3), 'area': 24, 'touches_edge': True, 'top_left': (0, 0), 'cell_count': 24}
{'bbox': (3, 6, 8, 9), 'area': 24, 'touches_edge': True, 'top_left': (3, 6), 'cell_count': 24}

```
**Analysis of Metrics:**

*   **Example 1:** Solid components have areas 20, 35, 9. *Correction:* My manual analysis missed a cell, the first component is 5x4=20, not 4x4=16. All touch the edge. Applying the new rule: Filter -> [Area 20, Area 35, Area 9]. Select min area -> Area 9. Target BBox: (7,1)-(9,3). **Matches expectation.**
*   **Example 2:** Solid components have areas 20, 16, 24. Filter (Touches Edge): Keep Area 20 (True), discard Area 16 (False), keep Area 24 (True). Filtered list: [Area 20, Area 24]. Select min area -> Area 20. Target BBox: (0,6)-(4,9). **Matches expectation.**
*   **Example 3:** Solid components have areas 24, 24. Filter (Touches Edge): Keep Area 24 (True), Keep Area 24 (True). Filtered list: [Area 24 (0,0), Area 24 (3,6)]. Select min area -> Tie (24). Tie-breaker (min row) -> (0,0) wins over (3,6). Target BBox: (0,0)-(5,3). **Matches expectation.**

The metrics confirm the refined hypothesis works for all training examples.

## Facts


```yaml
Data:
  - type: Grid
    description: Represents the input and output structures.
    properties:
      rows: Integer (Input is 10, Output varies)
      columns: Integer (Input is 10, Output varies)
      cells: List of Lists of Integers (0, 1, 2, 8)

Digits:
  - type: BackgroundDigit
    value: 0
    description: Represents empty space.
  - type: ForegroundDigit
    value: [1, 2, 8]
    description: Represents the content of objects.

Objects:
  - type: SolidRectangleComponent
    description: >
      A connected component of ForegroundDigits that perfectly
      fills its minimal bounding box within the input grid.
      Essentially, a rectangular block composed entirely of
      non-zero digits.
    properties:
      cells: List of coordinates (row, col) belonging to the component.
      bounding_box: The minimal rectangle enclosing the component.
        properties:
          min_row: Integer
          max_row: Integer
          min_col: Integer
          max_col: Integer
      area: Integer (Calculated from bounding_box dimensions)
      cell_count: Integer (Number of cells in the component; must equal area)
      touches_grid_edge: Boolean (True if the bounding_box touches row 0, col 0, row 9, or col 9 of the input grid)
      top_left_corner: Tuple (min_row, min_col)

Transformation:
  - action: IdentifySolidRectangles
    description: Find all distinct SolidRectangleComponents in the input grid.
  - action: FilterByEdgeContact
    description: Create a candidate list containing only those SolidRectangleComponents where touches_grid_edge is True.
  - action: SelectTargetComponent
    description: >
      From the candidate list, select the component based on the following
      prioritized criteria:
      1. Minimum area.
      2. Minimum top_left_corner row index (if tie in area).
      3. Minimum top_left_corner column index (if tie in row index).
    assumption: Exactly one component will satisfy the criteria.
  - action: ExtractSubgrid
    description: >
      Create the output grid by copying the portion of the input grid
      defined by the selected component's bounding_box.
```


## Natural Language Program

1.  **Identify Solid Rectangular Components:** Scan the 10x10 input grid to find all distinct connected components formed by adjacent non-zero digits (1, 2, 8). For each component, determine its minimal bounding box. Identify components that are "solid rectangles," meaning their non-zero cells exactly fill their bounding box (component cell count equals bounding box area).
2.  **Filter by Edge Contact:** Examine each identified solid rectangular component. Create a candidate list containing only those components whose bounding box touches any of the four outer edges (top, bottom, left, or right) of the 10x10 input grid.
3.  **Select the Target Component:** From the candidate list, select the single target component using the following rules, in order:
    *   Choose the component with the smallest bounding box area.
    *   If multiple components share the smallest area, choose the one whose top-left corner has the smallest row index (i.e., the highest one).
    *   If multiple components are still tied, choose the one whose top-left corner has the smallest column index (i.e., the leftmost one).
4.  **Extract Output:** Create the output grid by extracting the subgrid from the input grid that corresponds exactly to the bounding box of the selected target component.
