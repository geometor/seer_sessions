import numpy as np
from collections import deque

"""
Transforms an input grid by:
1. Identifying all distinct contiguous objects of non-background (white, 0) colors.
2. Calculating properties for each object: color, size (pixel count), and geometric center.
3. Filtering out objects smaller than a specified minimum size threshold (e.g., 5 pixels).
4. Grouping the remaining significant objects into rows based on the proximity of their vertical center coordinates. A tolerance, potentially related to object height, is used. Objects within a group (row) are considered vertically aligned.
5. Sorting the objects within each identified row based on their horizontal center coordinates (left-to-right).
6. Constructing an output grid where the colors of the significant objects are placed according to their determined row and column layout. The output grid dimensions are determined by the number of rows found and the maximum number of objects in any row. Empty spaces in rows with fewer objects than the maximum are filled with the background color (white, 0).
"""

def find_objects(grid: np.ndarray, background_color: int = 0) -> list:
    """
    Finds all connected components (objects) of non-background colors using BFS.

    Args:
        grid (np.ndarray): The input grid.
        background_color (int): The color considered as background (default: 0).

    Returns:
        list: A list of dictionaries, each representing an object:
              {'color': int, 'pixels': list of (r, c) tuples,
               'bounds': (min_r, min_c, max_r, max_c),
               'center': (center_y, center_x), 'size': int}
              Returns empty list if grid is empty or no objects are found.
    """
    objects = []
    if grid.size == 0:
        return objects
        
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Check if it's a non-background color and hasn't been visited yet
            if color != background_color and not visited[r, c]:
                # Start BFS to find the connected component (object)
                component_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c
                pixel_sum_r, pixel_sum_c = 0, 0

                while q:
                    curr_r, curr_c = q.popleft()

                    component_pixels.append((curr_r, curr_c))
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)
                    pixel_sum_r += curr_r
                    pixel_sum_c += curr_c

                    # Explore neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        # Check bounds, same color, and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                size = len(component_pixels)
                if size > 0:
                    # Calculate center based on average pixel coordinates
                    center_y = pixel_sum_r / size
                    center_x = pixel_sum_c / size
                    
                    objects.append({
                        'color': color,
                        'pixels': component_pixels,
                        'bounds': (min_r, min_c, max_r, max_c),
                        'center': (center_y, center_x),
                        'size': size
                    })
    return objects

def filter_objects(objects: list, min_size: int) -> list:
    """Filters objects based on a minimum size threshold."""
    return [obj for obj in objects if obj['size'] >= min_size]

def group_and_sort_objects(objects: list, y_tolerance_factor: float = 0.75) -> list:
    """
    Groups objects into rows based on center y-coordinate proximity relative
    to the first object in the potential row, and sorts them horizontally.

    Args:
        objects (list): List of object dictionaries (must contain 'center', 'bounds').
        y_tolerance_factor (float): A factor multiplied by the height of the 
                                     first object in a row to determine the 
                                     vertical grouping tolerance.

    Returns:
        list: A list of lists, where each inner list represents a row
              of object colors, sorted top-to-bottom (implicitly by grouping)
              and left-to-right (explicitly by center x).
              Returns empty list if no objects.
    """
    if not objects:
        return []

    # Sort primarily by center y, then by center x as a secondary sort key
    # This helps process objects generally from top-to-bottom, left-to-right.
    objects.sort(key=lambda o: (o['center'][0], o['center'][1]))

    rows_of_objects = []
    current_row = []

    for obj in objects:
        if not current_row:
            # Start the first row with the first object encountered
            current_row.append(obj)
        else:
            # Compare the current object's y-center with the y-center 
            # of the *first* object added to the current potential row.
            first_obj_in_row = current_row[0]
            first_obj_height = first_obj_in_row['bounds'][2] - first_obj_in_row['bounds'][0] + 1
            # Calculate tolerance based on the height of the first object in the row
            y_tolerance = first_obj_height * y_tolerance_factor
            
            # Check if the current object's y-center is close enough to the first object's y-center
            if abs(obj['center'][0] - first_obj_in_row['center'][0]) <= y_tolerance:
                # Object is vertically aligned enough, add it to the current row
                current_row.append(obj)
            else:
                # Y-center is too different, finalize the previous row
                # Sort the completed row by x-coordinate before adding
                current_row.sort(key=lambda o: o['center'][1])
                rows_of_objects.append(current_row)
                # Start a new row with the current object
                current_row = [obj]

    # Add the last row being built after the loop finishes
    if current_row:
        # Sort the last row by x-coordinate
        current_row.sort(key=lambda o: o['center'][1])
        rows_of_objects.append(current_row)

    # Extract just the colors for the final output structure
    output_rows_colors = []
    for row in rows_of_objects:
        output_rows_colors.append([obj['color'] for obj in row])

    return output_rows_colors

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by finding significant objects, arranging them
    spatially based on centers, and outputting a grid of their colors.
    """
    # Define parameters (these might need tuning based on task examples)
    background_color = 0
    min_size_threshold = 5  # Filter out objects smaller than this size
    y_tolerance_factor = 0.75 # Factor for grouping objects into rows vertically

    # 1. Find all connected components (objects)
    all_objects = find_objects(input_grid, background_color)
    if not all_objects:
        # Handle cases with no non-background pixels
        return np.array([[]], dtype=int) 

    # 2. Filter out small objects (likely noise)
    key_objects = filter_objects(all_objects, min_size_threshold)

    if not key_objects:
        # If filtering removed all objects, return empty grid
        # Consider if fallback logic (e.g., using all_objects) is needed for specific tasks
        # print("Warning: Filtering removed all objects.") 
        return np.array([[]], dtype=int)

    # 3. Group objects into rows based on vertical center proximity 
    #    and sort objects within each row by horizontal center position.
    grouped_sorted_colors = group_and_sort_objects(key_objects, y_tolerance_factor)

    # 4. Construct the output grid
    if not grouped_sorted_colors:
        # Should not happen if key_objects was not empty, but check for safety
        return np.array([[]], dtype=int)

    # Determine the dimensions of the output grid
    num_rows = len(grouped_sorted_colors)
    # Find the maximum number of columns needed across all rows
    num_cols = 0
    if num_rows > 0:
       # Guard against empty inner lists, though group_and_sort should prevent this
       num_cols = max(len(row) for row in grouped_sorted_colors if row) if grouped_sorted_colors else 0
       
    if num_cols == 0: 
        # Handle cases where rows might be empty after filtering/grouping (unlikely here)
         return np.array([[]], dtype=int)

    # Create the output grid, initialized with the background color
    output_grid = np.full((num_rows, num_cols), background_color, dtype=int)

    # Populate the output grid with the sorted colors
    for r_idx, row_colors in enumerate(grouped_sorted_colors):
        if row_colors: # Ensure row is not empty
             output_grid[r_idx, :len(row_colors)] = row_colors
        # Cells beyond len(row_colors) remain background_color due to np.full initialization

    return output_grid