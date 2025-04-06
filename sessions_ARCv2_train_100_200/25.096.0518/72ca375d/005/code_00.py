import collections
import numpy as np # Although not strictly necessary for the list-based approach, keep it for potential future array use

"""
Identifies all connected objects of the same non-zero digit in the input grid. 
Filters out objects consisting of only a single cell. 
From the remaining objects, selects the one with the highest density (number of cells / bounding box area). 
Ties in density are broken by selecting the object with the largest size (number of cells). 
Further ties are broken by selecting the object positioned highest (minimum top row), and then leftmost (minimum left column). 
The output is a new grid representing the bounding box of the selected object, 
containing the object's digit only at the locations corresponding to the object's cells within the box, and 0 otherwise.
"""

# --- Helper Function: Find Objects ---
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
            # Calculate density, handle potential division by zero for single-cell objects 
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

# --- Helper Function: Extract Representation ---
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
        
    return output_grid

# --- Main Transformation Function ---
def transform(input_grid: list[list[int]]) -> list[list[int]]:
    
    # 1. Identify all distinct objects and calculate their properties
    all_objects = find_objects(input_grid)

    # 2. Filter out objects with size 1
    filtered_objects = [obj for obj in all_objects if obj['size'] > 1]

    # 3. Handle the case where no objects remain after filtering
    if not filtered_objects:
        # Return empty list as per ARC conventions for no suitable object found
        return [] 

    # 4. Select the target object based on prioritized criteria:
    #    - Primary: Maximum density
    #    - Tie-breaker 1: Maximum size
    #    - Tie-breaker 2: Minimum row index of top-left corner (use negative for max)
    #    - Tie-breaker 3: Minimum col index of top-left corner (use negative for max)
    selected_object = max(filtered_objects, key=lambda obj: (
        obj['density'], 
        obj['size'], 
        -obj['min_r'], 
        -obj['min_c']
    ))

    # 5. Create the output grid representation based on the selected object
    output_grid = extract_object_representation(selected_object)

    # 6. Return the final output grid
    return output_grid