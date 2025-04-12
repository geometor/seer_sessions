import math
import numpy as np
from collections import Counter

"""
Transforms an input grid according to the following rules:
1. Identify foreground colors (non-background, typically non-7).
2. For each foreground color, determine its pixel count, the number of unique grid edges it touches, and the count of pixels touching each specific edge.
3. Select the 'target_color' as the one touching the most unique edges. Tie-break using the highest pixel count.
4. Calculate the optimal rectangle shape (Height R, Width C) for the target_color's pixel count N, minimizing abs(R-C) and preferring smaller R in ties.
5. Determine the 'target_corner' based on edge contact frequency: choose the vertical edge (T/B) with more contacts (T wins tie) and the horizontal edge (L/R) with more contacts (R wins tie). Combine them (e.g., T+R -> TR).
6. Create an output grid, initially a copy of the input.
7. Erase the original pixels of the target_color from the output grid by setting them to the background color.
8. Draw a solid rectangle of the target_color with the calculated shape (R, C) in the determined target_corner.
9. Pixels of other foreground colors remain unchanged.
"""

def get_pixel_locations(grid: np.ndarray, color: int) -> list[tuple[int, int]]:
    """Finds all locations (row, col) of a given color in the grid."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def get_unique_edge_contacts(grid_height: int, grid_width: int, locations: list[tuple[int, int]]) -> int:
    """Counts unique edges (T, B, L, R) contacted by pixels at given locations."""
    edges = set()
    for r, c in locations:
        if r == 0:
            edges.add('T')
        if r == grid_height - 1:
            edges.add('B')
        if c == 0:
            edges.add('L')
        if c == grid_width - 1:
            edges.add('R')
    return len(edges)

def get_edge_contact_counts(grid_height: int, grid_width: int, locations: list[tuple[int, int]]) -> dict[str, int]:
    """Counts how many pixels contact each specific edge."""
    counts = {'T': 0, 'B': 0, 'L': 0, 'R': 0}
    for r, c in locations:
        if r == 0:
            counts['T'] += 1
        if r == grid_height - 1:
            counts['B'] += 1
        if c == 0:
            counts['L'] += 1
        if c == grid_width - 1:
            counts['R'] += 1
    return counts

def find_best_rectangle_shape(n: int) -> tuple[int, int]:
    """Finds factors (R, C) of n minimizing abs(R-C), tie-breaking with smaller R."""
    if n == 0:
        return (0, 0)
    if n == 1:
        return (1, 1)
        
    factors = []
    for r in range(1, int(math.sqrt(n)) + 1):
        if n % r == 0:
            c = n // r
            factors.append((r, c))
            if r * r != n: # Avoid adding square root twice if n is a perfect square
                factors.append((c, r))

    best_shape = (0, 0)
    min_diff = float('inf')

    # Sort factors primarily by difference, secondarily by row (height)
    factors.sort(key=lambda pair: (abs(pair[0] - pair[1]), pair[0]))
    
    if not factors: # Should not happen for n > 0, but as a fallback
         return (1, n)

    best_shape = factors[0]
    return best_shape


def determine_target_corner(edge_counts: dict[str, int]) -> str:
    """Determines the target corner based on the highest vertical and horizontal edge contact counts."""
    # Vertical Edge: T vs B (T preferred on tie: >=)
    vert_edge = 'T' if edge_counts['T'] >= edge_counts['B'] else 'B'
        
    # Horizontal Edge: R vs L (R preferred on tie: >=)
    horiz_edge = 'R' if edge_counts['R'] >= edge_counts['L'] else 'L'

    # Combine
    return vert_edge + horiz_edge


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    # Convert to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape
    
    # Define background color (assuming 7 based on examples)
    background_color = 7

    # 1. Identify foreground colors
    unique_colors, counts = np.unique(input_np, return_counts=True)
    color_counts = dict(zip(unique_colors, counts))
    foreground_colors = [c for c in unique_colors if c != background_color]

    # Handle cases with 0 or 1 foreground color
    if not foreground_colors:
        return input_grid # No foreground colors, return original
    
    target_color = -1
    target_locations = []
    
    if len(foreground_colors) == 1:
        target_color = foreground_colors[0]
        target_locations = get_pixel_locations(input_np, target_color)
    else:
        # 2 & 3. Find target color based on unique edge contacts, tie-breaking with pixel count
        color_data = {}
        for color in foreground_colors:
            locations = get_pixel_locations(input_np, color)
            unique_edges = get_unique_edge_contacts(height, width, locations)
            pixel_count = len(locations) # Use actual locations length
            color_data[color] = {'locations': locations, 'unique_edges': unique_edges, 'count': pixel_count}

        # Sort colors: primary key = unique_edges (desc), secondary key = count (desc)
        sorted_colors = sorted(foreground_colors, key=lambda c: (color_data[c]['unique_edges'], color_data[c]['count']), reverse=True)
        target_color = sorted_colors[0]
        target_locations = color_data[target_color]['locations']

    # 4. Count pixels N of target_color
    n = len(target_locations)
    if n == 0: # If target color somehow has 0 pixels, return original grid
        return input_grid

    # 5. Determine rectangle shape (Height R, Width C)
    rect_height, rect_width = find_best_rectangle_shape(n)

    # 6. Calculate edge contact counts for target_color
    edge_counts = get_edge_contact_counts(height, width, target_locations)

    # 7 & 8. Determine target corner using the revised logic
    target_corner = determine_target_corner(edge_counts)

    # 9. Output grid is already initialized as a copy

    # 10. Change original target_color pixels to background color
    # Use numpy indexing for efficiency
    if target_locations: # Ensure there are locations to change
        rows, cols = zip(*target_locations)
        output_np[rows, cols] = background_color

    # 11. Draw the rectangle in the target corner
    start_row, start_col = 0, 0
    if target_corner == 'TL':
        start_row, start_col = 0, 0
    elif target_corner == 'TR':
        start_row, start_col = 0, width - rect_width
    elif target_corner == 'BL':
        start_row, start_col = height - rect_height, 0
    elif target_corner == 'BR':
        start_row, start_col = height - rect_height, width - rect_width

    # Define the slice for the rectangle
    end_row = start_row + rect_height
    end_col = start_col + rect_width
    
    # Ensure slices are within bounds (although calculations should make this unnecessary)
    start_row = max(0, start_row)
    start_col = max(0, start_col)
    end_row = min(height, end_row)
    end_col = min(width, end_col)

    # Fill the rectangle slice with the target color
    output_np[start_row:end_row, start_col:end_col] = target_color

    # Convert back to list of lists and return
    return output_np.tolist()