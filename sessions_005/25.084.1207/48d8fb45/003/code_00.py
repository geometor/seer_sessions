"""
Identifies a single gray marker pixel and the most frequent non-white, non-gray 'pattern color'. Finds all connected components (8-way adjacency) of the pattern color. Calculates the minimum Manhattan distance from each component to the marker. Selects the component with the smallest minimum distance (tie-breaking by top-left corner of bounding box). Determines the top-left corner of the bounding box of this selected component. Extracts a 3x3 subgrid from the input, starting at this corner, padding with white (0) if the extraction goes out of bounds.
"""

import numpy as np
from collections import Counter, deque

# Helper function to find the first pixel of a specific color
def _find_pixel(grid, color):
    """Finds the coordinates (row, col) of the first pixel with the specified color."""
    coords = np.argwhere(grid == color)
    if len(coords) > 0:
        return tuple(coords[0])
    return None

# Helper function to find the most frequent pattern color
def _find_pattern_color(grid):
    """Finds the most frequent color excluding white (0) and gray (5)."""
    counts = Counter(grid.flatten())
    counts.pop(0, None)  # Remove white
    counts.pop(5, None)  # Remove gray
    if not counts:
        return None # No pattern color found
    # Tie-breaking for most frequent color: lower color index wins (inherent in most_common)
    return counts.most_common(1)[0][0]

# Helper function for Manhattan distance
def _manhattan_distance(p1, p2):
    """Calculates the Manhattan distance between two points (row, col tuples)."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# Helper function to find connected components using BFS (replaces scipy.label)
def _find_connected_components(grid, target_color):
    """
    Finds all connected components of target_color using 8-way adjacency (BFS).
    Returns a list of components, where each component is a set of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = set()
    components = []
    
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == target_color and (r, c) not in visited:
                # Start BFS for a new component
                component = set()
                q = deque([(r, c)])
                visited.add((r, c))
                
                while q:
                    row, col = q.popleft()
                    component.add((row, col))
                    
                    # Check 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self
                            
                            nr, nc = row + dr, col + dc
                            
                            # Check bounds and target color
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == target_color and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                q.append((nr, nc))
                                
                if component:
                    components.append(component)
                    
    return components

# Helper function to calculate bounding box (replaces scipy.find_objects concept)
def _get_bounding_box(component_pixels):
    """
    Calculates the bounding box for a component.
    Returns (min_row, min_col, max_row, max_col).
    Returns None if component_pixels is empty.
    """
    if not component_pixels:
        return None
        
    min_row = min(r for r, c in component_pixels)
    min_col = min(c for r, c in component_pixels)
    max_row = max(r for r, c in component_pixels)
    max_col = max(c for r, c in component_pixels)
    
    return (min_row, min_col, max_row, max_col)

# Helper function to calculate min distance from component to marker
def _calculate_min_distance_to_marker(component_pixels, marker_coords):
    """Calculates the minimum Manhattan distance from component pixels to the marker."""
    min_dist = float('inf')
    if not component_pixels:
        return min_dist
        
    for pixel_coords in component_pixels:
        dist = _manhattan_distance(pixel_coords, marker_coords)
        if dist < min_dist:
            min_dist = dist
            
    return min_dist

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # 1. Identify Marker
    marker_coords = _find_pixel(input_np, 5)
    if marker_coords is None:
        # If no marker, return default 3x3 white grid
        return np.zeros((3, 3), dtype=int).tolist()

    # 2. Determine Pattern Color
    pattern_color = _find_pattern_color(input_np)
    if pattern_color is None:
        # If no pattern color, return default 3x3 white grid
        return np.zeros((3, 3), dtype=int).tolist()

    # 3. Find Pattern Components
    components = _find_connected_components(input_np, pattern_color)
    if not components:
        # If no components found, return default 3x3 white grid
        return np.zeros((3, 3), dtype=int).tolist()

    # 4 & 5. Calculate Distances, Find BBoxes, and Select Target Component
    target_component_info = None # Will store (min_dist, top_left_corner, component_pixels)
    min_overall_distance = float('inf')

    for component_pixels in components:
        if not component_pixels: continue # Should not happen with _find_connected_components logic

        # Calculate min distance for this component
        min_dist_for_component = _calculate_min_distance_to_marker(component_pixels, marker_coords)
        
        # Calculate bounding box and get top-left corner
        bbox = _get_bounding_box(component_pixels)
        component_origin = (bbox[0], bbox[1]) # top-left corner

        # Compare with the current best
        update_target = False
        if min_dist_for_component < min_overall_distance:
            update_target = True
        elif min_dist_for_component == min_overall_distance:
            # Tie-breaking: compare top-left corners (row first, then column)
            current_target_origin = target_component_info[1]
            if component_origin[0] < current_target_origin[0]:
                update_target = True
            elif component_origin[0] == current_target_origin[0] and component_origin[1] < current_target_origin[1]:
                update_target = True

        if update_target:
            min_overall_distance = min_dist_for_component
            target_component_info = (min_dist_for_component, component_origin, component_pixels)

    if target_component_info is None:
        # Should not happen if components were found, but handle defensively
        return np.zeros((3, 3), dtype=int).tolist()

    # 6. Determine Extraction Origin
    extraction_origin = target_component_info[1] # Top-left corner of the target component's bbox

    # 7. Extract 3x3 Output
    output_grid = np.zeros((3, 3), dtype=int) # Initialize with white (0)
    start_row, start_col = extraction_origin

    for r_out in range(3):
        for c_out in range(3):
            # Calculate corresponding input coordinates
            r_in = start_row + r_out
            c_in = start_col + c_out

            # Check if input coordinates are within bounds
            if 0 <= r_in < rows and 0 <= c_in < cols:
                output_grid[r_out, c_out] = input_np[r_in, c_in]
            # else: leave as 0 (white padding) - already initialized

    return output_grid.tolist()
