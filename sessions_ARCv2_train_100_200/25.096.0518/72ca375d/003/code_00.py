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