import numpy as np
from collections import Counter

"""
Identify all separate contiguous regions (objects) of non-white pixels in the input grid, considering orthogonal and diagonal adjacency.
For each region, calculate the frequency of each color within it and determine the maximum frequency of any single color.
Select the region(s) with the highest maximum color frequency across all regions.
If there is a tie (multiple regions share the same highest maximum color frequency), select the region among the tied ones that extends furthest to the right (has the largest maximum column index).
Create an output grid of the same dimensions as the input, filled with the background color (white, 0).
Copy the pixels of the finally selected region onto the output grid at their original positions.
"""

def find_regions(grid, background_color=0):
    """
    Finds all contiguous regions of non-background colors in the grid.

    Args:
        grid (np.ndarray): The input grid.
        background_color (int): The value representing the background.

    Returns:
        list: A list of regions, where each region is a list of
              (row, col, color) tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    regions = []

    for r in range(rows):
        for c in range(cols):
            # If the pixel is not background and not visited yet
            if grid[r, c] != background_color and not visited[r, c]:
                current_region = []
                q = [(r, c)]  # Queue for BFS
                visited[r, c] = True

                while q:
                    row, col = q.pop(0)
                    color = grid[row, col]
                    current_region.append((row, col, color))

                    # Check all 8 neighbors (orthogonal and diagonal)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue  # Skip self

                            nr, nc = row + dr, col + dc

                            # Check bounds
                            if 0 <= nr < rows and 0 <= nc < cols:
                                # Check if neighbor is part of the object and not visited
                                if grid[nr, nc] != background_color and not visited[nr, nc]:
                                    visited[nr, nc] = True
                                    q.append((nr, nc))
                
                if current_region:
                    regions.append(current_region)
    return regions

def calculate_region_properties(region):
    """
    Calculates properties for a single region.

    Args:
        region (list): A list of (row, col, color) tuples for the region.

    Returns:
        dict: A dictionary containing properties:
              'pixels': the input region list,
              'max_color_frequency': highest frequency of a single color,
              'rightmost_column': the maximum column index.
              Returns None if region is empty.
    """
    if not region:
        return None

    colors = [pixel[2] for pixel in region]
    cols = [pixel[1] for pixel in region]

    if not colors: # Should not happen if region is not empty, but safety check
         return {'pixels': region, 'max_color_frequency': 0, 'rightmost_column': -1}


    color_counts = Counter(colors)
    max_color_frequency = 0
    if color_counts:
        max_color_frequency = max(color_counts.values())

    rightmost_column = -1
    if cols:
        rightmost_column = max(cols)

    return {
        'pixels': region,
        'max_color_frequency': max_color_frequency,
        'rightmost_column': rightmost_column
    }


def transform(input_grid):
    """
    Applies the described transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape
    background_color = 0

    # Initialize output grid with background color
    output_array = np.full_like(input_array, background_color)

    # 1. Identify all non-background regions
    regions = find_regions(input_array, background_color)

    # If no regions found, return the empty grid
    if not regions:
        return output_array.tolist()

    # 2. Calculate properties for each region
    region_properties = [calculate_region_properties(r) for r in regions]
    
    # Handle potential None values if empty regions were somehow generated
    region_properties = [prop for prop in region_properties if prop is not None]
    
    if not region_properties:
        return output_array.tolist()


    # 3. Find the overall highest maximum color frequency
    overall_max_freq = 0
    if region_properties:
      overall_max_freq = max(prop['max_color_frequency'] for prop in region_properties)


    # 4. Identify primary candidates (those with the overall highest frequency)
    primary_candidates = [prop for prop in region_properties if prop['max_color_frequency'] == overall_max_freq]

    # 5. Select the final region
    selected_region_prop = None
    if len(primary_candidates) == 1:
        # a. If only one region has the max frequency, select it
        selected_region_prop = primary_candidates[0]
    elif len(primary_candidates) > 1:
        # b. If multiple regions tie, use the tie-breaker (rightmost column)
        max_rightmost_col = -1
        # Find the maximum rightmost column among the tied candidates
        max_rightmost_col = max(prop['rightmost_column'] for prop in primary_candidates)
        
        # Select the candidate(s) that match this max rightmost column
        # Although the prompt implies a single winner, we'll handle potential further ties by picking the first one.
        # In practice, based on examples, it seems a unique winner is expected after the tiebreaker.
        final_candidates = [prop for prop in primary_candidates if prop['rightmost_column'] == max_rightmost_col]
        selected_region_prop = final_candidates[0] # Pick the first one if there's still a tie

    # 6. Create the output grid
    if selected_region_prop:
        selected_region_pixels = selected_region_prop['pixels']
        # 7. Copy selected region pixels to the output grid
        for r, c, color in selected_region_pixels:
            output_array[r, c] = color

    return output_array.tolist()