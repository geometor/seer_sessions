```python
import numpy as np
from collections import deque

"""
Identifies non-white (0) and non-magenta (6) pixels as 'markers'.
Identifies contiguous shapes made of magenta (6) pixels using 4-way connectivity ('templates').
Associates each marker with its spatially closest template shape based on minimum Manhattan distance between the marker and any pixel of the shape. A one-to-one mapping is ensured by processing the globally closest marker-template pairs first.
For each associated marker-template pair, creates a new small grid containing the template's shape within its bounding box, colored with the marker's color against a white (0) background.
Determines the final arrangement (horizontal or vertical) of these colored shapes based on the spatial range of the original marker positions. If the column range is strictly greater than the row range, arrangement is horizontal; otherwise, it's vertical.
Sorts the colored shapes based on the marker's column index (for horizontal) or row index (for vertical).
Combines the sorted shapes into a final output grid, padding with white (0) as necessary to align shapes (pad bottom for horizontal, pad right for vertical).
"""

# Helper function to find marker pixels
def find_marker_pixels(grid):
    """Finds pixels that are not white (0) or magenta (6)."""
    markers = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Markers are any color other than white (0) and magenta (6)
            if color != 0 and color != 6:
                markers.append({'pos': (r, c), 'color': color})
    return markers

# Helper function for Manhattan distance
def manhattan_distance(p1, p2):
    """Calculates the Manhattan distance between two points (tuples)."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# Helper function to find contiguous shapes using BFS (4-connectivity)
def find_shapes(grid, color):
    """Finds contiguous shapes of a specific color using BFS (4-connectivity)."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    shapes = []

    for r in range(rows):
        for c in range(cols):
            # If it's the target color and not visited yet, start BFS
            if grid[r, c] == color and not visited[r, c]:
                current_shape_coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    curr_r, curr_c = q.popleft()
                    current_shape_coords.append((curr_r, curr_c))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        # Check bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # If neighbor is target color and not visited
                            if grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                
                if current_shape_coords:
                    shapes.append({'coords': current_shape_coords}) # Store coordinates list
                    
    return shapes

# Helper function to get bounding box
def get_bounding_box(coords):
    """Calculates the minimum bounding box for a set of coordinates."""
    if not coords:
        return None, None, None, None
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return min_r, min_c, height, width

# Helper function to calculate min distance from a point to a set of points
def distance_marker_to_shape(marker_pos, shape_coords):
    """Calculates the minimum Manhattan distance from a marker point to any pixel in a shape."""
    min_dist = float('inf')
    for shape_pos in shape_coords:
        dist = manhattan_distance(marker_pos, shape_pos)
        if dist < min_dist:
            min_dist = dist
    return min_dist

# Helper function to extract shape and recolor
def extract_and_recolor(shape_coords, marker_color):
    """Extracts shape within bounding box and recolors magenta to marker color."""
    if not shape_coords:
        return None
        
    min_r, min_c, height, width = get_bounding_box(shape_coords)
    
    # Create the output subgrid, initialized to white (0)
    subgrid = np.zeros((height, width), dtype=np.uint8)
    
    # Fill the subgrid with the marker color where the shape exists
    for r, c in shape_coords:
        subgrid[r - min_r, c - min_c] = marker_color
            
    return subgrid

# Helper function to combine grids with padding
def combine_grids(grids, orientation):
    """Combines multiple grids horizontally or vertically, padding with 0s."""
    if not grids:
        # Return an empty grid if there are no shapes to combine
        return np.array([[]], dtype=np.uint8) 

    if orientation == 'horizontal':
        if not any(g.size > 0 for g in grids): # Check if all grids are empty
            return np.array([[]], dtype=np.uint8)
        # Find max height among non-empty grids
        max_height = max(g.shape[0] for g in grids if g.size > 0) if grids else 0
        padded_grids = []
        for g in grids:
            if g.size == 0: # Handle potentially empty grids if needed
                 # Create an empty grid of correct height to avoid padding errors
                 padded_g = np.zeros((max_height, 0), dtype=np.uint8)
            else:
                 pad_height = max_height - g.shape[0]
                 # Pad at the bottom
                 padded_g = np.pad(g, ((0, pad_height), (0, 0)), mode='constant', constant_values=0)
            padded_grids.append(padded_g)
        # Filter out potentially zero-width padded grids before hstack
        padded_grids = [g for g in padded_grids if g.shape[1] > 0]
        if not padded_grids: return np.array([[]], dtype=np.uint8) # All inputs were empty
        return np.hstack(padded_grids)
    else: # vertical
        if not any(g.size > 0 for g in grids): # Check if all grids are empty
             return np.array([[]], dtype=np.uint8)
        # Find max width among non-empty grids
        max_width = max(g.shape[1] for g in grids if g.size > 0) if grids else 0
        padded_grids = []
        for g in grids:
            if g.size == 0: # Handle potentially empty grids
                # Create an empty grid of correct width
                padded_g = np.zeros((0, max_width), dtype=np.uint8)
            else:
                pad_width = max_width - g.shape[1]
                # Pad on the right
                padded_g = np.pad(g, ((0, 0), (0, pad_width)), mode='constant', constant_values=0)
            padded_grids.append(padded_g)
        # Filter out potentially zero-height padded grids before vstack
        padded_grids = [g for g in padded_grids if g.shape[0] > 0]
        if not padded_grids: return np.array([[]], dtype=np.uint8) # All inputs were empty
        return np.vstack(padded_grids)

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    input_grid_np = np.array(input_grid, dtype=np.uint8)

    # 1. Find marker pixels
    markers = find_marker_pixels(input_grid_np)
    if not markers:
        # If no markers, return empty grid (or input, depending on spec - assume empty)
        return np.array([[]], dtype=np.uint8).tolist()

    # 2. Find template shapes (magenta color = 6) using BFS
    template_shapes = find_shapes(input_grid_np, 6)
    if not template_shapes:
         # If no template shapes, return empty grid
        return np.array([[]], dtype=np.uint8).tolist()

    # 3. Associate each marker with the closest template shape
    marker_shape_distances = []
    for i, marker in enumerate(markers):
        for j, shape in enumerate(template_shapes):
            # Calculate distance only if shape has coordinates
            if shape['coords']:
                 dist = distance_marker_to_shape(marker['pos'], shape['coords'])
                 marker_shape_distances.append({'marker_idx': i, 'shape_idx': j, 'dist': dist})
            
    # Sort distances to prioritize closest pairs globally
    marker_shape_distances.sort(key=lambda x: x['dist'])

    processed_pairs = []
    marker_assigned = [False] * len(markers)
    shape_assigned = [False] * len(template_shapes)

    for M_S_dist in marker_shape_distances:
        marker_idx = M_S_dist['marker_idx']
        shape_idx = M_S_dist['shape_idx']
        
        # If this marker and shape haven't been assigned yet, make the assignment
        if not marker_assigned[marker_idx] and not shape_assigned[shape_idx]:
            marker = markers[marker_idx]
            shape = template_shapes[shape_idx]
            processed_pairs.append({
                'marker': marker,
                'shape_coords': shape['coords']
            })
            marker_assigned[marker_idx] = True
            shape_assigned[shape_idx] = True
            
        # Optimization: Stop if all markers have been assigned
        if all(marker_assigned):
            break
            
    # Check if all markers were successfully associated (optional, for debugging)
    # if len(processed_pairs) != len(markers):
    #     print(f"Warning: Could not associate all {len(markers)} markers. Found {len(processed_pairs)} associations.")

    # 4. Process each pair: Extract and recolor
    output_shapes_data = []
    for pair in processed_pairs:
        marker = pair['marker']
        shape_coords = pair['shape_coords']
        # Recolor the shape based on marker color
        recolored_shape = extract_and_recolor(shape_coords, marker['color'])
        if recolored_shape is not None and recolored_shape.size > 0: # Ensure shape is valid
            output_shapes_data.append({
                'shape': recolored_shape,
                'marker_pos': marker['pos'] # Store original marker position for sorting
            })

    # If no valid shapes were generated (e.g., all markers failed association)
    if not output_shapes_data:
         return np.array([[]], dtype=np.uint8).tolist()

    # 5. Determine arrangement strategy based on marker positions
    marker_rows = [data['marker_pos'][0] for data in output_shapes_data]
    marker_cols = [data['marker_pos'][1] for data in output_shapes_data]

    # Handle case with only one marker/shape
    if len(output_shapes_data) <= 1:
         # Default to vertical if only one, or if ranges are zero (doesn't matter)
         orientation = 'vertical'
    else:
        row_range = max(marker_rows) - min(marker_rows)
        col_range = max(marker_cols) - min(marker_cols)

        # Rule: Horizontal if col_range > row_range, otherwise vertical
        if col_range > row_range:
            orientation = 'horizontal'
        else: # Includes row_range >= col_range (handles ties)
            orientation = 'vertical'

    # 6. Sort the shapes based on the chosen orientation and marker positions
    if orientation == 'horizontal':
        # Sort by marker column index (left-to-right)
        output_shapes_data.sort(key=lambda x: x['marker_pos'][1])
    else: # vertical
        # Sort by marker row index (top-to-bottom)
        output_shapes_data.sort(key=lambda x: x['marker_pos'][0])

    # 7. Assemble the output grid by combining sorted shapes with padding
    final_shapes = [data['shape'] for data in output_shapes_data]
    output_grid = combine_grids(final_shapes, orientation)

    # 8. Return the result as a list of lists
    return output_grid.tolist()

```