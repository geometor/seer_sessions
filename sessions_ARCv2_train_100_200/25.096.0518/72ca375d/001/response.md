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