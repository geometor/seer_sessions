import numpy as np
from typing import List, Tuple, Set
from skimage.measure import label

# Define color constants
MAGENTA = 6
MAROON = 9
ORANGE = 7
WHITE = 0
RED = 2

def find_colored_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates (row, col) of pixels with a specific color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def get_bounding_box(coords: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """Calculates the min_row, max_row, min_col, max_col for a set of coordinates."""
    if not coords:
        # Return invalid box if no coordinates
        return -1, -1, -1, -1 
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    return min(rows), max(rows), min(cols), max(cols)

def find_objects(grid: np.ndarray, color: int) -> List[List[Tuple[int, int]]]:
    """Finds connected components of a specified color.
       Uses 4-way connectivity. Returns a list of objects, where each object
       is a list of its (row, col) coordinates.
    """
    binary_grid = (grid == color)
    # connectivity=1 means 4-way adjacency (von Neumann neighborhood)
    labeled_grid, num_labels = label(binary_grid, connectivity=1, background=0, return_num=True) 
    objects = []
    for label_id in range(1, num_labels + 1):
        coords = list(zip(*np.where(labeled_grid == label_id)))
        if coords:
            objects.append(coords)
    return objects

def find_white_segments_on_row(row_slice: np.ndarray) -> List[Tuple[int, int]]:
    """Finds contiguous segments of White (0) on a single row slice.
       Returns a list of (start_col, end_col) tuples for each segment.
    """
    segments = []
    in_segment = False
    start_col = -1
    width = len(row_slice)
    for c, color in enumerate(row_slice):
        if color == WHITE and not in_segment:
            in_segment = True
            start_col = c
        elif color != WHITE and in_segment:
            in_segment = False
            segments.append((start_col, c - 1))
    # Handle segment ending at the edge
    if in_segment:
        segments.append((start_col, width - 1))
    return segments

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid according to the following rules:
    1. Identifies the unique Maroon (9) and Orange (7) objects and their coordinates.
    2. Creates an output grid initialized with the background color (Magenta 6), 
       copying non-Maroon/Orange elements from the input.
    3. Places the Orange (7) color in the output grid at the original location of the Maroon object.
    4. Determines if the Maroon and Orange objects were primarily horizontally or vertically aligned
       based on overlap of their bounding boxes in the input grid.
    5. If Horizontally aligned:
       a. Finds the row(s) shared by the bounding boxes.
       b. Defines a column range strictly between the Maroon and Orange objects.
       c. Identifies all White (0) objects from the input grid that lie entirely within this 'between' column range.
       d. Collects the column indices occupied by these White objects.
       e. Places Red (2) pixels in the output grid on the shared row(s) at the collected column indices.
    6. If Vertically aligned:
       a. Finds the column(s) shared by the bounding boxes and identifies the leftmost shared column.
       b. Identifies rows in the input grid containing at least two distinct horizontal segments of White (0).
       c. For each such row, finds the leftmost column of the rightmost White segment.
       d. Places Red (2) pixels in the output grid at two locations on that row:
          - One in the leftmost column shared by the original Maroon/Orange objects.
          - One in the column immediately to the left of the rightmost White segment's start.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # --- Find Objects and Coordinates ---
    maroon_coords = find_colored_pixels(input_grid, MAROON)
    orange_coords = find_colored_pixels(input_grid, ORANGE)

    # Handle cases where one or both objects might be missing (though not expected per examples)
    if not maroon_coords or not orange_coords:
        return output_grid 

    # --- Perform Base Transformation ---
    # Clear original Maroon location in output grid (set to background)
    for r, c in maroon_coords:
        output_grid[r, c] = MAGENTA 

    # Clear original Orange location in output grid (set to background)
    for r, c in orange_coords:
         if output_grid[r, c] == ORANGE: # Avoid clearing if it overlaps with where maroon was
             output_grid[r, c] = MAGENTA

    # Place Orange color at Maroon's original location
    for r, c in maroon_coords:
        output_grid[r, c] = ORANGE

    # --- Get Bounding Boxes for Alignment Check ---
    maroon_min_r, maroon_max_r, maroon_min_c, maroon_max_c = get_bounding_box(maroon_coords)
    orange_min_r, orange_max_r, orange_min_c, orange_max_c = get_bounding_box(orange_coords)

    # --- Determine Alignment ---
    rows_overlap = max(maroon_min_r, orange_min_r) <= min(maroon_max_r, orange_max_r)
    cols_overlap = max(maroon_min_c, orange_min_c) <= min(maroon_max_c, orange_max_c)

    is_horizontal_alignment = False
    is_vertical_alignment = False

    # Determine alignment based on shared rows/columns
    # Prioritize horizontal if rows are identical, vertical if columns are identical
    if maroon_min_r == orange_min_r and maroon_max_r == orange_max_r:
        is_horizontal_alignment = True
    elif maroon_min_c == orange_min_c and maroon_max_c == orange_max_c:
        is_vertical_alignment = True
    # Fallback based on simple overlap (covers cases where one dim overlaps but not identical spans)
    elif rows_overlap and not cols_overlap:
        is_horizontal_alignment = True
    elif cols_overlap and not rows_overlap:
        is_vertical_alignment = True
    # If both overlap but aren't identical spans, default to horizontal (matches example 3 logic implicitly)
    elif rows_overlap and cols_overlap:
         is_horizontal_alignment = True # Default preference or could add more complex logic

    # --- Apply Alignment-Specific Red Pixel Rules ---
    if is_horizontal_alignment:
        # Find shared rows using bounding boxes
        shared_rows = list(range(max(maroon_min_r, orange_min_r), min(maroon_max_r, orange_max_r) + 1))
        
        # Define the column range strictly *between* the objects
        between_start_col = min(maroon_max_c, orange_max_c) + 1
        between_end_col = max(maroon_min_c, orange_min_c) # Exclusive end

        target_cols = set()
        if between_start_col < between_end_col: # Check if there is actually space between
            # Find all white objects in the input
            white_objects = find_objects(input_grid, WHITE)
            
            # Filter for white objects completely within the 'between' columns
            for obj_coords in white_objects:
                w_min_r, w_max_r, w_min_c, w_max_c = get_bounding_box(obj_coords)
                if w_min_c >= between_start_col and w_max_c < between_end_col:
                    # Collect the columns occupied by these objects
                    for r_w, c_w in obj_coords:
                        target_cols.add(c_w)

        # Place Red pixels on shared rows in the target columns
        for r in shared_rows:
            for c in target_cols:
                # Check bounds just in case, though target_cols should be valid
                if 0 <= r < height and 0 <= c < width:
                    output_grid[r, c] = RED

    elif is_vertical_alignment:
        # Find shared columns and the leftmost one
        shared_cols = list(range(max(maroon_min_c, orange_min_c), min(maroon_max_c, orange_max_c) + 1))
        if not shared_cols: 
             # This case indicates alignment detection might be flawed, but proceed assuming vertical
             leftmost_shared_col = min(maroon_min_c, orange_min_c) # Best guess
        else:
             leftmost_shared_col = min(shared_cols)


        # Iterate through rows to find those with >= 2 white segments
        for r in range(height):
            row_slice = input_grid[r, :]
            white_segments = find_white_segments_on_row(row_slice)

            if len(white_segments) >= 2:
                # Find the rightmost white segment (one with the largest start column)
                rightmost_segment = max(white_segments, key=lambda seg: seg[0])
                right_white_left_col = rightmost_segment[0] # Leftmost column of the rightmost segment
                col_left_of_right_white = right_white_left_col - 1

                # Place Red pixel at leftmost shared column
                if 0 <= r < height and 0 <= leftmost_shared_col < width:
                     output_grid[r, leftmost_shared_col] = RED
                     
                # Place Red pixel at column left of the rightmost white segment start
                if 0 <= r < height and 0 <= col_left_of_right_white < width:
                     output_grid[r, col_left_of_right_white] = RED

    return output_grid