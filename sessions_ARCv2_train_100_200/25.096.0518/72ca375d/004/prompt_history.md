
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0
0 0 4 4 0 0 8 8 8 0
0 0 0 0 0 0 8 0 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 4
4 4
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 2 2 2 0 0 7 7 0
0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 6 6 6
0 6 6 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 0 3 0 0 5 0 0 5 0
0 0 3 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0
8 8 8 8 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
5 0 0 5
5 5 5 5
```

Okay, I will analyze the provided examples to understand the transformation task.

**Perception of Elements:**

1.  **Input:** A 10x10 grid of single digits (0-9). The non-zero digits form distinct, potentially overlapping or adjacent, connected shapes or "objects". 0 represents the background.
2.  **Output:** A smaller rectangular grid containing digits.
3.  **Objects:** Within the input grid, contiguous blocks of the same non-zero digit can be considered as distinct objects.
4.  **Transformation:** The core task seems to involve identifying one specific object from the input grid based on some criteria and then extracting a representation of that object as the output.
5.  **Extraction Logic:** The output grid appears to correspond to the bounding box of the selected object. Within this bounding box, cells matching the selected object's digit retain their value, while all other cells (including background 0s and potentially parts of other objects falling within the bounding box) are set to 0 in the output.
6.  **Selection Criteria:** The critical step is determining *which* object is selected. Analyzing the examples:
    *   In `train_1`, the object made of '4' is selected. Its bounding box is 2x2, area 4, and it contains 4 cells (density 4/4 = 1.0). Other objects ('8', '2') have lower densities (5/6, 6/10 respectively).
    *   In `train_2`, the object made of '6' is selected. Its bounding box is 2x4, area 8, and it contains 6 cells (density 6/8 = 0.75). Other objects ('2', '7') have lower densities (5/8, 4/6 respectively).
    *   In `train_3`, the object made of '5' is selected. Its bounding box is 2x4, area 8, and it contains 6 cells (density 6/8 = 0.75). Other objects ('3', '8') have lower densities (4/6, 9/14 respectively).
    *   The pattern suggests selecting the object with the highest "density", calculated as the number of cells in the object divided by the area of its bounding box.

**Facts (YAML):**


```yaml
InputType: Grid
InputProperties:
  - Size: 10x10
  - Cells: Contain single digits (0-9)
  - Background: Represented by digit 0
  - Objects: Formed by connected non-zero cells of the same digit

OutputType: Grid
OutputProperties:
  - Size: Variable, smaller than input
  - Cells: Contain single digits (0 or the digit of the selected object)

Transformation: Object Selection and Extraction

SelectionCriteria:
  - Identify all distinct connected non-zero objects.
  - For each object:
      - Calculate its size (number of cells).
      - Determine its bounding box.
      - Calculate the area of its bounding box.
      - Calculate its density (size / area).
  - Select the object with the maximum density.
  - (Assumption: No ties in maximum density in provided examples; if ties occur, a secondary rule like smallest bounding box area or top-left position might be needed).

ExtractionSteps:
  - Get the bounding box (min_row, max_row, min_col, max_col) and digit (D) of the selected object.
  - Create an output grid with dimensions (max_row - min_row + 1) x (max_col - min_col + 1).
  - Iterate through the cells (r, c) within the bounding box range in the input grid.
  - If input[r][c] == D, set output[r - min_row][c - min_col] = D.
  - Otherwise, set output[r - min_row][c - min_col] = 0.

Relationships:
  - The output grid is derived from a sub-region (bounding box) of the input grid.
  - The content of the output grid depends on the single object selected based on the maximum density criterion.
```


**Natural Language Program:**

1.  Parse the input grid to identify all distinct connected groups of identical non-zero digits (these are the "objects").
2.  For each identified object:
    a.  Count the number of cells belonging to the object (its `size`).
    b.  Find the minimum and maximum row and column indices occupied by the object's cells to determine its `bounding_box`.
    c.  Calculate the `area` of the bounding box (height * width).
    d.  Calculate the `density` of the object (`size` / `area`).
3.  Find the object that has the highest `density` among all objects. Let this be the `selected_object` and its digit be `selected_digit`.
4.  Determine the `bounding_box` of the `selected_object` (min_row, max_row, min_col, max_col).
5.  Create a new output grid with dimensions `(max_row - min_row + 1)` rows and `(max_col - min_col + 1)` columns.
6.  Iterate through each row `r` from `min_row` to `max_row` and each column `c` from `min_col` to `max_col` of the input grid.
7.  For each input cell `input[r][c]`:
    a.  If `input[r][c]` is equal to the `selected_digit`, set the corresponding cell in the output grid `output[r - min_row][c - min_col]` to `selected_digit`.
    b.  Otherwise, set the output grid cell `output[r - min_row][c - min_col]` to 0.
8.  Return the generated output grid.
```python
import collections

"""
This function transforms an input grid based on identifying connected objects of non-zero digits. 
It calculates the 'density' (number of cells / bounding box area) for each object. 
The object with the highest density is selected. 
The output is a grid representing the bounding box of the selected object, 
containing the object's digit where the object exists within the box, and 0 otherwise.
"""

def find_objects(grid: list[list[int]]) -> list[dict]:
    """
    Identifies all distinct connected objects of the same non-zero digit in the grid.
    Calculates properties for each object: digit, cells, bounding box, size, area, density.

    Args:
        grid: The input grid (list of lists of ints).

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains its properties. Returns an empty list if no objects are found.
    """
    rows = len(grid)
    if rows == 0:
        return []
    cols = len(grid[0])
    if cols == 0:
        return []

    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            # Skip visited cells or background (0)
            if (r, c) in visited or grid[r][c] == 0:
                continue

            # Start finding a new object using Breadth-First Search (BFS)
            digit = grid[r][c]
            current_object_cells = set()
            queue = collections.deque([(r, c)])
            visited.add((r, c))

            min_r, max_r = r, r
            min_c, max_c = c, c

            while queue:
                curr_r, curr_c = queue.popleft()
                current_object_cells.add((curr_r, curr_c))

                # Update bounding box
                min_r = min(min_r, curr_r)
                max_r = max(max_r, curr_r)
                min_c = min(min_c, curr_c)
                max_c = max(max_c, curr_c)

                # Explore neighbors (up, down, left, right)
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = curr_r + dr, curr_c + dc

                    # Check boundaries
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Check if neighbor is part of the same object and not visited
                        if (nr, nc) not in visited and grid[nr][nc] == digit:
                            visited.add((nr, nc))
                            queue.append((nr, nc))

            # Calculate object properties
            size = len(current_object_cells)
            height = max_r - min_r + 1
            width = max_c - min_c + 1
            area = height * width
            # Avoid division by zero if area is somehow 0 (shouldn't happen with non-empty objects)
            density = size / area if area > 0 else 0 

            objects.append({
                'digit': digit,
                'cells': current_object_cells,
                'min_r': min_r,
                'max_r': max_r,
                'min_c': min_c,
                'max_c': max_c,
                'size': size,
                'area': area,
                'density': density
            })

    return objects

def extract_object(grid: list[list[int]], selected_object: dict) -> list[list[int]]:
    """
    Extracts the selected object into a new grid representing its bounding box.

    Args:
        grid: The original input grid.
        selected_object: The dictionary containing the properties of the object to extract.

    Returns:
        A new grid containing the extracted object representation.
    """
    min_r = selected_object['min_r']
    max_r = selected_object['max_r']
    min_c = selected_object['min_c']
    max_c = selected_object['max_c']
    digit = selected_object['digit']

    height = max_r - min_r + 1
    width = max_c - min_c + 1

    output_grid = [[0 for _ in range(width)] for _ in range(height)]

    # Iterate through the bounding box in the original grid
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            # If the cell in the original grid matches the object's digit,
            # place the digit in the corresponding output grid cell.
            if grid[r][c] == digit:
                output_grid[r - min_r][c - min_c] = digit
            # Otherwise, it remains 0 (as initialized).

    return output_grid


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by finding the object with the highest density
    and extracting its representation within its bounding box.
    """
    
    # 1. Find all distinct objects and their properties
    objects = find_objects(input_grid)

    # Handle cases with no objects
    if not objects:
        return [] # Or potentially return an empty grid of specific size based on requirements

    # 2. Find the object with the maximum density
    # If there's a tie in density, the first one encountered in the list is chosen.
    # A secondary sort key (e.g., area, top-left position) could be added if needed.
    selected_object = max(objects, key=lambda obj: obj['density'])

    # 3. Extract the selected object into its bounding box grid
    output_grid = extract_object(input_grid, selected_object)

    return output_grid

```
```python
import collections
import numpy as np # Used for potential array operations, though list-based is primary

"""
Transforms an input grid by identifying connected objects of non-zero digits. 
Calculates the 'density' (number of cells / bounding box area) for each object. 
Selects the object with the highest density. If densities are tied, selects the one with the smallest bounding box area. Further ties are broken by selecting the top-most, then left-most object.
The output is a new grid representing the bounding box of the selected object. 
Within this output grid, cells corresponding to the actual positions of the selected object's cells (within its bounding box in the input) are filled with the object's digit, while all other cells are set to 0.
"""

def find_objects(grid: list[list[int]]) -> list[dict]:
    """
    Identifies all distinct connected objects of the same non-zero digit in the grid using BFS.
    Calculates properties for each object: digit, cells, bounding box, size, area, density.

    Args:
        grid: The input grid (list of lists of ints).

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains its properties. Returns an empty list if no objects are found.
    """
    rows = len(grid)
    if rows == 0: return []
    cols = len(grid[0])
    if cols == 0: return []
    
    visited = set()
    objects = []

    # Iterate through each cell to find starting points of objects
    for r in range(rows):
        for c in range(cols):
            # Skip visited cells or background (0)
            if (r, c) in visited or grid[r][c] == 0:
                continue

            # Found a potential start of a new object, begin BFS
            digit = grid[r][c]
            current_object_cells = set()
            queue = collections.deque([(r, c)])
            visited.add((r, c)) # Mark starting cell as visited

            # Initialize bounding box coordinates
            min_r, max_r = r, r
            min_c, max_c = c, c

            # Perform BFS to find all connected cells of the same digit
            while queue:
                curr_r, curr_c = queue.popleft()
                current_object_cells.add((curr_r, curr_c))

                # Update bounding box as we find more cells
                min_r = min(min_r, curr_r)
                max_r = max(max_r, curr_r)
                min_c = min(min_c, curr_c)
                max_c = max(max_c, curr_c)

                # Explore neighbors (up, down, left, right)
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = curr_r + dr, curr_c + dc

                    # Check grid boundaries
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Check if neighbor is part of the same object (same digit) and not yet visited
                        if (nr, nc) not in visited and grid[nr][nc] == digit:
                            visited.add((nr, nc))
                            queue.append((nr, nc))

            # Calculate object properties after BFS completes
            size = len(current_object_cells)
            height = max_r - min_r + 1
            width = max_c - min_c + 1
            area = height * width
            # Calculate density, handle potential division by zero for single-cell objects in invalid grids
            density = size / area if area > 0 else 0 

            # Store the found object and its properties
            objects.append({
                'digit': digit,
                'cells': current_object_cells, # Set of (row, col) tuples
                'min_r': min_r,
                'max_r': max_r,
                'min_c': min_c,
                'max_c': max_c,
                'size': size,
                'area': area,
                'density': density
            })

    return objects

def extract_object_representation(selected_object: dict) -> list[list[int]]:
    """
    Creates a new grid representing the bounding box of the selected object,
    placing the object's digit only at the locations corresponding to its cells.

    Args:
        selected_object: The dictionary containing the properties of the object to extract.

    Returns:
        A new grid (list of lists of ints) containing the extracted object representation.
    """
    # Retrieve properties of the selected object
    min_r = selected_object['min_r']
    max_r = selected_object['max_r']
    min_c = selected_object['min_c']
    max_c = selected_object['max_c']
    digit = selected_object['digit']
    cells = selected_object['cells'] # The set of (r, c) coordinates making up the object

    # Calculate dimensions of the output grid (based on bounding box)
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # Initialize the output grid with zeros
    output_grid = [[0 for _ in range(width)] for _ in range(height)]

    # Populate the output grid based on the object's actual cells
    # Iterate through the object's cells coordinates
    for r, c in cells:
        # Calculate the corresponding position in the output grid (relative to the bounding box origin)
        output_r = r - min_r
        output_c = c - min_c
        # Place the object's digit in the output grid
        output_grid[output_r][output_c] = digit
        
    # Alternative (slightly less efficient but maybe clearer): Iterate through bounding box
    # for r in range(min_r, max_r + 1):
    #     for c in range(min_c, max_c + 1):
    #         # Check if the coordinate (r, c) is actually part of the object's cells
    #         if (r, c) in cells: 
    #              output_grid[r - min_r][c - min_c] = digit

    return output_grid


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Main transformation function. Finds all objects, selects the one with the
    highest density (with tie-breaking), and extracts its representation.
    """
    
    # 1. Find all distinct objects and calculate their properties
    objects = find_objects(input_grid)

    # 2. Handle the case where no non-zero objects are found
    if not objects:
        # Return an empty grid or handle as per specific requirements (e.g., return original grid?)
        # For ARC tasks, usually means empty output or a minimal grid. Let's return empty list.
        return [] 

    # 3. Select the target object based on criteria:
    #    - Primary: Maximum density
    #    - Tie-breaker 1: Minimum bounding box area (negative area for max sort)
    #    - Tie-breaker 2: Minimum row index of top-left corner (negative min_r for max sort)
    #    - Tie-breaker 3: Minimum col index of top-left corner (negative min_c for max sort)
    selected_object = max(objects, key=lambda obj: (obj['density'], -obj['area'], -obj['min_r'], -obj['min_c']))

    # 4. Create the output grid representation based on the selected object
    output_grid = extract_object_representation(selected_object)

    # 5. Return the final output grid
    return output_grid
```
