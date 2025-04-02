import numpy as np
from collections import Counter, deque

"""
Identify distinct contiguous non-white regions (blobs) in the input grid using 
8-way adjacency. For each blob, determine if it consists of exactly two 
non-white colors where one color (the center color) is topologically enclosed 
by the other color (the frame color). A color is considered topologically 
enclosed if all its pixels within the blob only have neighbors (8-connectivity) 
that are either the frame color or the center color itself; specifically, no 
neighbor of a center pixel can be the background color (0) or any other color 
not belonging to the blob. Collect all identified center colors from all such 
valid frame/center blobs. The final output is a 1x1 grid containing the center 
color that appears most frequently across all identified blobs. If there is a 
tie in frequency, the color with the highest numerical value is chosen. If no 
such frame/center blobs are found, the output is white (0).
"""

def get_neighbors(r, c, height, width, connectivity=8):
    """
    Gets valid neighbor coordinates for a given pixel.

    Args:
        r (int): Row index of the pixel.
        c (int): Column index of the pixel.
        height (int): Grid height.
        width (int): Grid width.
        connectivity (int): 4 or 8 for neighbor connectivity.

    Returns:
        list: A list of (row, col) tuples for valid neighbors.
    """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip self
            if dr == 0 and dc == 0: 
                continue
            # Skip diagonals for 4-connectivity if specified
            if connectivity == 4 and abs(dr) + abs(dc) != 1: 
                continue
            nr, nc = r + dr, c + dc
            # Check grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def find_blobs(grid):
    """
    Finds all distinct contiguous regions (blobs) of non-white pixels using BFS.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list where each element is a set of (row, col) tuples 
              representing the coordinates of a single blob's pixels.
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    blobs = []

    for r in range(height):
        for c in range(width):
            # Start BFS from a non-white, unvisited pixel
            if grid[r, c] != 0 and not visited[r, c]:
                current_blob_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    curr_r, curr_c = q.popleft()
                    current_blob_coords.add((curr_r, curr_c))
                    
                    # Explore neighbors (using 8-connectivity for blob definition)
                    for nr, nc in get_neighbors(curr_r, curr_c, height, width, connectivity=8):
                        # Add neighbor if it's non-white and not visited
                        if grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Add the found blob to the list
                if current_blob_coords:
                     blobs.append(current_blob_coords)
    return blobs

def is_topologically_enclosed(center_pixels, center_color, frame_color, grid, height, width):
    """
    Checks if the set of center_pixels is topologically enclosed by the frame_color.
    A pixel is enclosed if all its 8 neighbors are either the center_color or the frame_color.
    
    Args:
        center_pixels (set): Set of (r, c) coordinates for the candidate center pixels.
        center_color (int): The color value of the candidate center.
        frame_color (int): The color value of the candidate frame.
        grid (np.array): The input grid.
        height (int): Grid height.
        width (int): Grid width.

    Returns:
        bool: True if all center_pixels are enclosed, False otherwise.
    """
    for r, c in center_pixels:
        # Check all 8 neighbors
        for nr, nc in get_neighbors(r, c, height, width, connectivity=8):
            neighbor_color = grid[nr, nc]
            # If any neighbor is NOT the center color and NOT the frame color, it's not enclosed.
            if neighbor_color != center_color and neighbor_color != frame_color:
                return False # Found a neighbor that breaks the enclosure rule
    return True # All neighbors of all center pixels are valid

def analyze_blob_for_center(blob_coords, grid):
    """
    Analyzes a blob to find if it has a valid frame/center structure 
    based on topological enclosure and returns the center color.

    Args:
        blob_coords (set): Set of (row, col) tuples for the blob pixels.
        grid (np.array): The input grid.

    Returns:
        int or None: The center color if found, otherwise None.
    """
    if not blob_coords:
        return None

    height, width = grid.shape
    pixel_map = {} # color -> set of coords
    
    # Collect colors and their pixel locations within the blob
    for r, c in blob_coords:
        color = grid[r, c]
        # Should always be non-white based on find_blobs logic
        if color not in pixel_map:
            pixel_map[color] = set()
        pixel_map[color].add((r,c))

    # A valid frame/center blob must have exactly two distinct non-white colors
    non_white_colors = list(pixel_map.keys())
    if len(non_white_colors) != 2:
        return None 

    c1, c2 = non_white_colors[0], non_white_colors[1]
    c1_pixels = pixel_map[c1]
    c2_pixels = pixel_map[c2]
    
    # Check if c1 is enclosed by c2
    c1_is_enclosed = is_topologically_enclosed(c1_pixels, c1, c2, grid, height, width)
    
    # Check if c2 is enclosed by c1
    c2_is_enclosed = is_topologically_enclosed(c2_pixels, c2, c1, grid, height, width)

    # Return the center color if exactly one color is enclosed by the other
    if c1_is_enclosed and not c2_is_enclosed:
        return c1 
    elif c2_is_enclosed and not c1_is_enclosed:
        return c2
    else:
        # Ambiguous or invalid structure (e.g., adjacent, neither enclosed, or both enclosed)
        return None

def transform(input_grid):
    """
    Transforms the input grid by finding frame/center objects, identifying 
    their center colors based on topological enclosure, and returning the 
    most frequent center color (highest value in case of ties).

    Args:
        input_grid (np.array): The 2D input grid.

    Returns:
        np.array: A 1x1 grid containing the most frequent center color.
    """
    
    # Step 1: Find all distinct contiguous non-white blobs
    blobs = find_blobs(input_grid)
    
    # Step 2: Analyze each blob to identify center colors based on enclosure
    center_colors_found = []
    for blob_coords in blobs:
        center_color = analyze_blob_for_center(blob_coords, input_grid)
        # If a valid center color was identified for this blob, add it to the list
        if center_color is not None:
            center_colors_found.append(center_color)

    # Step 3: Count frequencies of the identified center colors
    output_color = 0 # Default to white (0) if no valid centers found
    if center_colors_found:
        color_counts = Counter(center_colors_found)
        
        # Step 4: Find the maximum frequency
        max_freq = 0
        # Check if counter is not empty before finding max
        if color_counts: 
             max_freq = max(color_counts.values())

        # Step 5: Find all colors that have this maximum frequency
        most_frequent_colors = [color for color, count in color_counts.items() if count == max_freq]

        # Step 6: Apply tie-breaking rule: select the color with the highest numerical value
        if most_frequent_colors:
            output_color = max(most_frequent_colors)

    # Step 7: Create the 1x1 output grid
    output_grid = np.array([[output_color]], dtype=int)

    return output_grid