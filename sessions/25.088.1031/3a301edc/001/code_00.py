import numpy as np

"""
Fill the bounding box of the non-white object(s) with the 'inner' color.

1. Find all non-white pixels (value > 0) in the input grid. If none are found, return the input grid unchanged.
2. Determine the minimum bounding box that encloses all these non-white pixels.
3. Identify the set of unique non-white colors present within the object(s).
4. Determine the 'inner' color:
   a. If there's only one unique non-white color, that color is the 'inner' color.
   b. If there are multiple unique non-white colors, identify the set of 'outer' colors. An 'outer' color is any non-white color that has at least one pixel directly adjacent (including diagonals) to a background (white, 0) pixel.
   c. The 'inner' color is the unique non-white color that is present in the object but is NOT in the set of 'outer' colors.
   d. Handle potential ambiguity (e.g., if all colors are 'outer' or multiple colors are 'inner') by selecting the most frequent non-white color as a fallback.
5. Create a new grid, initially as a copy of the input grid.
6. Iterate through each pixel position (row, column) within the calculated bounding box.
7. For each position within the bounding box, if the corresponding pixel in the *input* grid is white (0), change the pixel at the same position in the *output* grid to the determined 'inner' color.
8. Return the modified output grid.
"""

def find_non_white_pixels(grid):
    """Finds coordinates (row, col) of all pixels with value > 0."""
    non_white_coords = np.argwhere(grid > 0)
    if non_white_coords.size == 0:
        return None
    return non_white_coords

def find_bounding_box(non_white_coords):
    """Calculates the min/max row/col for the bounding box."""
    if non_white_coords is None:
        return None
    min_r = np.min(non_white_coords[:, 0])
    max_r = np.max(non_white_coords[:, 0])
    min_c = np.min(non_white_coords[:, 1])
    max_c = np.max(non_white_coords[:, 1])
    return min_r, max_r, min_c, max_c

def get_neighbors(r, c, height, width):
    """Gets valid 8-directional neighbor coordinates within grid bounds."""
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue # Skip self
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def find_inner_color(grid, non_white_coords):
    """Determines the inner color based on adjacency to the background."""
    height, width = grid.shape

    # Find all unique non-white colors present in the identified pixels
    unique_colors = set(grid[r, c] for r, c in non_white_coords)

    if not unique_colors:
        # Should not happen if called after non_white_coords check
        return None 
        
    if len(unique_colors) == 1:
        # If only one non-white color, it's the inner color
        return list(unique_colors)[0]

    # Identify 'outer' colors: those adjacent to any white pixel (0)
    outer_colors = set()
    for r, c in non_white_coords:
        color = grid[r, c]
        if color in outer_colors: 
            continue # Already confirmed as outer

        # Check neighbors for white pixels
        for nr, nc in get_neighbors(r, c, height, width):
             if grid[nr, nc] == 0:
                 outer_colors.add(color)
                 break # This color touches the background

    # Inner colors are those present but not 'outer'
    inner_candidates = unique_colors - outer_colors

    if len(inner_candidates) == 1:
        # Expected case: one unique inner color
        return list(inner_candidates)[0]
    
    # Handle ambiguity / unexpected cases (fallback)
    # Calculate frequency of all non-white colors
    counts = {c: 0 for c in unique_colors}
    for r, c in non_white_coords:
        counts[grid[r, c]] += 1

    if len(inner_candidates) == 0:
        # All colors touch the background. Fallback: most frequent overall non-white color.
        most_frequent_color = max(counts, key=counts.get)
        # print(f"Warning: No strictly inner color found. Defaulting to most frequent: {most_frequent_color}")
        return most_frequent_color
    else: # len(inner_candidates) > 1
        # Multiple inner candidates. Fallback: most frequent among the candidates.
        candidate_counts = {c: counts[c] for c in inner_candidates}
        most_frequent_inner = max(candidate_counts, key=candidate_counts.get)
        # print(f"Warning: Multiple inner colors found ({inner_candidates}). Defaulting to most frequent inner: {most_frequent_inner}")
        return most_frequent_inner

def transform(input_grid):
    """
    Transforms the input grid by finding the non-white object(s), determining
    the bounding box and the 'inner' color, and filling the white space 
    within the bounding box with that inner color.
    """
    # Convert input to numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    
    # 1. Find non-white pixels
    non_white_coords = find_non_white_pixels(input_np)
    
    # If no object pixels found, return the original grid
    if non_white_coords is None:
        return input_grid

    # 2. Determine bounding box
    bbox = find_bounding_box(non_white_coords)
    if bbox is None: # Should not happen if non_white_coords is not None
         return input_grid 
    min_r, max_r, min_c, max_c = bbox

    # 3. & 4. Determine the inner color
    inner_color = find_inner_color(input_np, non_white_coords)
    
    # Check if inner color determination failed (shouldn't with fallbacks)
    if inner_color is None:
        print("Error: Could not determine inner color.")
        return input_grid # Return original grid on error

    # 5. Create a copy of the input grid for modification
    output_np = np.copy(input_np)

    # 6. & 7. Iterate within bounding box and fill white pixels
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            # Check original pixel color at this location
            if input_np[r, c] == 0:
                # If it was white, fill with inner color in the output
                output_np[r, c] = inner_color

    # 8. Return the result, converted back to list of lists format
    return output_np.tolist()