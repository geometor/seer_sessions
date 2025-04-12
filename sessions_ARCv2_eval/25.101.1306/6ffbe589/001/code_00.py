import collections

"""
The transformation identifies all distinct contiguous objects (groups of non-white pixels using 8-way adjacency) in the input grid. 
It then selects the object containing the largest number of pixels. 
A minimal bounding box is calculated for this largest object. 
The output grid has the dimensions of this bounding box. 
Only the pixels belonging to the largest object are copied from the input grid into the output grid, maintaining their relative positions within the bounding box. 
All other cells within the output grid (corresponding to background or other objects within the input bounding box area) are set to the background color (white, 0).
"""

def find_objects(grid: list[list[int]], background_color: int = 0) -> list[set[tuple[int, int]]]:
    """
    Finds all distinct connected objects of non-background pixels in the grid.

    Args:
        grid: The input grid (list of lists of integers).
        background_color: The integer value representing the background.

    Returns:
        A list of sets, where each set contains the (row, col) coordinates
        of the pixels belonging to one object.
    """
    height = len(grid)
    if height == 0:
        return []
    width = len(grid[0])
    if width == 0:
        return []

    visited = set()
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r][c] != background_color and (r, c) not in visited:
                # Found the start of a new object
                current_object_coords = set()
                q = collections.deque([(r, c)])
                visited.add((r, c))

                while q:
                    row, col = q.popleft()
                    current_object_coords.add((row, col))

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self

                            nr, nc = row + dr, col + dc

                            # Check bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                # Check if neighbor is part of the object and not visited
                                if grid[nr][nc] != background_color and (nr, nc) not in visited:
                                    visited.add((nr, nc))
                                    q.append((nr, nc))
                
                if current_object_coords:
                     objects.append(current_object_coords)

    return objects

def get_bounding_box(coords: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    """
    Calculates the minimum bounding box for a set of coordinates.

    Args:
        coords: A set of (row, col) tuples.

    Returns:
        A tuple (min_row, max_row, min_col, max_col).
        Returns (0, -1, 0, -1) if coords is empty, indicating an invalid box.
    """
    if not coords:
        return (0, -1, 0, -1) # Indicate invalid box

    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    return min_r, max_r, min_c, max_c


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Isolates the largest object in the input grid and crops the grid to its bounding box.

    Args:
        input_grid: The input grid represented as a list of lists of integers.

    Returns:
        The output grid containing only the largest object, cropped to its bounding box.
        Returns an empty grid if no non-background objects are found.
    """
    background_color = 0

    # 1. Identify all distinct objects
    objects = find_objects(input_grid, background_color)

    # Handle cases with no objects
    if not objects:
        # Return empty or minimal grid based on expected behavior (let's assume empty for now)
        # Example outputs suggest there's always *something*, but defensively:
        return [] 
        # Alternatively: return [[background_color]]

    # 2. Find the largest object (by pixel count)
    largest_object_coords = max(objects, key=len)

    # 3. Determine the bounding box of the largest object
    min_r, max_r, min_c, max_c = get_bounding_box(largest_object_coords)

    # Handle case where bounding box calculation failed (e.g., empty object passed somehow)
    if max_r < min_r or max_c < min_c:
         return [] # Or [[background_color]]

    # 4. Calculate output grid dimensions
    output_height = max_r - min_r + 1
    output_width = max_c - min_c + 1

    # 5. Create the output grid, initialized with background color
    output_grid = [[background_color for _ in range(output_width)] for _ in range(output_height)]

    # 6. Populate the output grid only with pixels from the largest object
    # Iterate through the coordinates of the largest object ONLY
    for r, c in largest_object_coords:
         # Calculate the position in the output grid relative to the bounding box origin
        out_r = r - min_r
        out_c = c - min_c
        # Copy the color from the input grid
        output_grid[out_r][out_c] = input_grid[r][c]
        
    # --- Alternative Population method (Iterate through bounding box) ---
    # This method is slightly less efficient if the object is sparse within its bbox
    # for r_in in range(min_r, max_r + 1):
    #     for c_in in range(min_c, max_c + 1):
    #         # Check if the current input coordinate belongs to the largest object
    #         if (r_in, c_in) in largest_object_coords:
    #             # Calculate the corresponding output coordinates
    #             out_r = r_in - min_r
    #             out_c = c_in - min_c
    #             # Copy the pixel color
    #             output_grid[out_r][out_c] = input_grid[r_in][c_in]
    #         # Else: it remains background color (already initialized)
    # --- End Alternative ---


    return output_grid