import numpy as np
from collections import Counter

"""
Identifies sparse 'special' pixels against a background, modifies grid boundaries based on the distance of these pixels to the boundaries, and adds connecting lines of pixels between the special pixel and the modified boundary.

Transformation Steps:
1.  **Initialization:** Create a copy of the input grid.
2.  **Identify Background:** Find the most frequent color (background color).
3.  **Identify Special Pixels:**
    *   Find all non-background pixels.
    *   Count occurrences of each non-background color.
    *   Identify colors with the minimum count ("special" colors).
    *   For each special color, find the representative location (top-most, then left-most pixel).
4.  **Apply Transformation based on Count:**
    *   **One Special Pixel (P, C):**
        a. Find the furthest boundary (FB) from P (Tiebreak: T > B > L > R).
        b. Modify FB with color C.
        c. Add internal pixels of color C every two steps from P towards FB (excluding P and FB).
    *   **Two Special Pixels (P1, C1; P2, C2):**
        a. Calculate distances, furthest boundaries (FB1, FB2), max distances (MaxD1, MaxD2), and closest boundaries (CB1, CB2) for both P1 and P2 (Tiebreak: T > B > L > R).
        b. **If MaxD1 > MaxD2:** P1 is primary (furthest), P2 is secondary (closest). Modify FB1 with C1, add internals from P1 towards FB1. Modify CB2 with C2, add internals from P2 towards CB2.
        c. **If MaxD2 > MaxD1:** P2 is primary, P1 is secondary. Modify FB2 with C2, add internals from P2 towards FB2. Modify CB1 with C1, add internals from P1 towards CB1.
        d. **If MaxD1 == MaxD2:** Both are secondary. Modify CB1 with C1, add internals from P1 towards CB1. Modify CB2 with C2, add internals from P2 towards CB2.
        e. **Intersection Check:** If one modified boundary was horizontal (T/B) and the other vertical (L/R), set their intersection pixel to White (0).
5.  **Return:** Return the modified grid.
"""


def get_background_color(grid):
    """Finds the most frequent color in the grid."""
    counts = Counter(grid.flatten())
    if not counts:
        return 0 # Default to white if grid is empty
    # Find the color with the maximum count
    background_color = counts.most_common(1)[0][0]
    return background_color

def find_special_pixels(grid, background_color):
    """
    Finds the least frequent non-background color(s) and one representative location for each.
    Returns a list of tuples: [(color, (row, col)), ...], sorted by color index.
    """
    non_background_pixels = []
    locations = {} # Store locations for each color: {color: [(r,c), ...]}
    height, width = grid.shape

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != background_color:
                non_background_pixels.append(color)
                if color not in locations:
                    locations[color] = []
                locations[color].append((r, c))

    if not non_background_pixels:
        return [] # No non-background pixels found

    counts = Counter(non_background_pixels)
    if not counts: # Handles case where grid might only have background
         return []
    min_count = min(counts.values())

    special_pixels_info = []
    # Ensure consistent order by sorting colors
    sorted_colors = sorted(locations.keys())
    for color in sorted_colors:
        if counts[color] == min_count:
            # Get the first location found (top-left most)
            first_location = min(locations[color], key=lambda x: (x[0], x[1]))
            special_pixels_info.append((color, first_location))

    return special_pixels_info

def calculate_distances(point, height, width):
    """Calculates distances from a point (r, c) to the boundaries."""
    r, c = point
    return {
        'T': r,
        'B': height - 1 - r,
        'L': c,
        'R': width - 1 - c
    }

def get_furthest_boundary(distances):
    """
    Finds the boundary type ('T', 'B', 'L', 'R') with the maximum distance.
    Tie-breaking order: T > B > L > R.
    """
    max_dist = -1
    furthest = None
    # Check in tie-breaking order
    for boundary in ['T', 'B', 'L', 'R']:
        # Use >= to ensure the first encountered max in tie-break order is kept
        # No, use >. If T=5, B=5, we want T. If T=5, B=4, we want T.
        # If T=4, B=5, we want B.
        # The logic is: Check T. If B > T's dist, B becomes candidate. If B == T's dist, T remains.
        if distances[boundary] > max_dist:
            max_dist = distances[boundary]
            furthest = boundary
    # Example: T=5, B=5, L=3, R=2 -> max_dist=5, furthest=T
    # Example: T=3, B=5, L=5, R=2 -> max_dist=5, furthest=B
    # Example: T=3, B=4, L=5, R=5 -> max_dist=5, furthest=L
    return furthest, max_dist


def get_closest_boundary(distances):
    """
    Finds the boundary type ('T', 'B', 'L', 'R') with the minimum distance.
    Tie-breaking order: T > B > L > R.
    """
    min_dist = float('inf')
    closest = None
    # Find the minimum distance value
    min_dist_val = min(distances.values())

    # Find all boundaries matching the minimum distance
    candidates = [b for b, d in distances.items() if d == min_dist_val]

    # Apply tie-breaking order
    if 'T' in candidates: return 'T', min_dist_val
    if 'B' in candidates: return 'B', min_dist_val
    if 'L' in candidates: return 'L', min_dist_val
    if 'R' in candidates: return 'R', min_dist_val
    return None, None # Should not happen if distances is valid


def modify_boundary(grid, boundary_type, color):
    """Modifies the specified boundary row or column with the given color."""
    height, width = grid.shape
    if boundary_type == 'T':
        grid[0, :] = color
    elif boundary_type == 'B':
        grid[height - 1, :] = color
    elif boundary_type == 'L':
        grid[:, 0] = color
    elif boundary_type == 'R':
        grid[:, width - 1] = color

def add_internal_pixels(grid, start_point, boundary_type, color):
    """Adds pixels every two steps towards the specified boundary, excluding start and end."""
    height, width = grid.shape
    r, c = start_point

    if boundary_type == 'T':
        # Move up from r-2, r-4, ... stopping *before* row 0
        for i in range(r - 2, 0, -2):
             grid[i, c] = color
    elif boundary_type == 'B':
        # Move down from r+2, r+4, ... stopping *before* row H-1
        for i in range(r + 2, height - 1, 2):
             grid[i, c] = color
    elif boundary_type == 'L':
        # Move left from c-2, c-4, ... stopping *before* col 0
        for j in range(c - 2, 0, -2):
             grid[r, j] = color
    elif boundary_type == 'R':
        # Move right from c+2, c+4, ... stopping *before* col W-1
        for j in range(c + 2, width - 1, 2):
             grid[r, j] = color


def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    """
    # 1. Initialization
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # 2. Identify Background
    background_color = get_background_color(output_grid)

    # 3. Identify Special Pixels
    special_pixels = find_special_pixels(output_grid, background_color)

    # If no special pixels, return the copy
    if not special_pixels:
        return output_grid

    # 4. Apply Transformation based on Count
    modified_boundaries_info = {} # Store {boundary_type: color}

    if len(special_pixels) == 1:
        # Case: One special color
        color, point = special_pixels[0]
        distances = calculate_distances(point, height, width)
        furthest_boundary, _ = get_furthest_boundary(distances)

        # Modify the furthest boundary
        modify_boundary(output_grid, furthest_boundary, color)
        modified_boundaries_info[furthest_boundary] = color
        # Add internal pixels towards the furthest boundary
        add_internal_pixels(output_grid, point, furthest_boundary, color)

    elif len(special_pixels) >= 2:
        # Case: Two or more special colors (use the first two found based on color index)
        c1, p1 = special_pixels[0]
        c2, p2 = special_pixels[1]

        # Calculate properties for P1
        dist1 = calculate_distances(p1, height, width)
        furthest1, max_dist1 = get_furthest_boundary(dist1)
        closest1, _ = get_closest_boundary(dist1)

        # Calculate properties for P2
        dist2 = calculate_distances(p2, height, width)
        furthest2, max_dist2 = get_furthest_boundary(dist2)
        closest2, _ = get_closest_boundary(dist2)

        # Determine actions based on max distances
        if max_dist1 > max_dist2:
            # P1=Primary (furthest), P2=Secondary (closest)
            modify_boundary(output_grid, furthest1, c1)
            add_internal_pixels(output_grid, p1, furthest1, c1)
            modified_boundaries_info[furthest1] = c1

            modify_boundary(output_grid, closest2, c2)
            add_internal_pixels(output_grid, p2, closest2, c2) # ADDED THIS LINE
            modified_boundaries_info[closest2] = c2

        elif max_dist2 > max_dist1:
            # P2=Primary (furthest), P1=Secondary (closest)
            modify_boundary(output_grid, furthest2, c2)
            add_internal_pixels(output_grid, p2, furthest2, c2)
            modified_boundaries_info[furthest2] = c2

            modify_boundary(output_grid, closest1, c1)
            add_internal_pixels(output_grid, p1, closest1, c1) # ADDED THIS LINE
            modified_boundaries_info[closest1] = c1

        else: # max_dist1 == max_dist2
            # Both are Secondary (closest)
            modify_boundary(output_grid, closest1, c1)
            add_internal_pixels(output_grid, p1, closest1, c1) # ADDED THIS LINE
            modified_boundaries_info[closest1] = c1

            modify_boundary(output_grid, closest2, c2)
            add_internal_pixels(output_grid, p2, closest2, c2) # ADDED THIS LINE
            modified_boundaries_info[closest2] = c2

        # Intersection Handling
        row_intersect = None
        col_intersect = None

        # Identify horizontal boundary (if any)
        if 'T' in modified_boundaries_info: row_intersect = 0
        elif 'B' in modified_boundaries_info: row_intersect = height - 1

        # Identify vertical boundary (if any)
        if 'L' in modified_boundaries_info: col_intersect = 0
        elif 'R' in modified_boundaries_info: col_intersect = width - 1

        # Check if exactly one horizontal and one vertical boundary were modified
        if row_intersect is not None and col_intersect is not None:
             # Ensure the boundary modification didn't overwrite the corner first
             # (The modify_boundary calls happened first)
             output_grid[row_intersect, col_intersect] = 0


    # If more than 2 special pixels, the current logic only considers the first two.

    # 5. Return
    return output_grid