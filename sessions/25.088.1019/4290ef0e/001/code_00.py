import numpy as np
from collections import Counter

"""
Identifies the background color (most frequent) in the input grid.
Finds all non-background objects (contiguous pixels of the same color).
Determines a central alignment point:
  - If a unique non-background pixel exists, its location is the center, and its color overrides the output center.
  - Otherwise, the center of the single 'plus' shaped object is the center.
Calculates the relative positions of all non-background pixels to this center.
Overlays these pixels onto a conceptual canvas based on relative positions.
Determines the bounding box of the overlaid pixels.
Creates the output grid sized to the bounding box, initialized with the background color.
Copies the overlaid pixels from the canvas to the output grid.
If a unique center pixel determined alignment, sets the corresponding output pixel to its color.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    counts = Counter(grid.flatten())
    if not counts:
        return 0 # Default to black/white if grid is empty, though ARC constraints prevent this.
    # Find the color with the maximum count
    background_color = counts.most_common(1)[0][0]
    return background_color

def find_objects(grid, background_color):
    """Finds all contiguous objects of non-background colors."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != background_color and not visited[r, c]:
                obj_coords = []
                q = [(r, c)]
                visited[r, c] = True
                obj_color = color
                
                while q:
                    row, col = q.pop(0)
                    obj_coords.append((row, col))
                    
                    # Check 4 orthogonal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == obj_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if obj_coords:
                    objects.append({'color': obj_color, 'coords': obj_coords})
    return objects

def find_center(grid, background_color):
    """
    Finds the alignment center.
    Returns ((center_row, center_col), center_color_override)
    center_color_override is None if alignment is based on the plus shape.
    """
    height, width = grid.shape
    counts = Counter(grid.flatten())
    
    # 1. Check for unique non-background pixel
    unique_pixel_color = None
    unique_pixel_coords = None
    for color, count in counts.items():
        if color != background_color and count == 1:
            unique_pixel_color = color
            break
            
    if unique_pixel_color is not None:
        # Find its coordinates
        for r in range(height):
            for c in range(width):
                if grid[r, c] == unique_pixel_color:
                    unique_pixel_coords = (r, c)
                    return unique_pixel_coords, unique_pixel_color

    # 2. If no unique pixel, find the center of the plus shape
    plus_center_coords = None
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            center_color = grid[r, c]
            if center_color != background_color:
                # Check N, S, E, W neighbors
                if (grid[r-1, c] == center_color and
                        grid[r+1, c] == center_color and
                        grid[r, c-1] == center_color and
                        grid[r, c+1] == center_color):
                    # Basic check assumes only one such shape per problem constraints
                    # More robust check could ensure corners are different, etc.
                    plus_center_coords = (r, c)
                    return plus_center_coords, None # No color override

    # Should not happen based on examples, but return geometric center as fallback?
    # Or raise error? For now, assume one of the above conditions is met.
    if plus_center_coords is None:
         raise ValueError("Could not determine alignment center (no unique pixel or plus shape found).")

    return plus_center_coords, None


def transform(input_grid):
    """
    Transforms the input grid by overlaying non-background shapes centered
    according to specific rules.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. Analyze Input: Identify background color
    background_color = find_background_color(input_np)

    # 2. Identify Objects
    objects = find_objects(input_np, background_color)
    if not objects:
        # Handle cases with no non-background objects if necessary
        # (e.g., return empty grid or grid with only background)
        # For ARC, likely means returning a minimal grid of background color.
        # Let's assume 1x1 background based on usual ARC patterns if no objects.
         return np.array([[background_color]], dtype=int)


    # 3. Find Center
    center_coords, center_color_override = find_center(input_np, background_color)
    center_r, center_c = center_coords

    # 4. Perform Overlay (conceptually)
    # Store pixels relative to the center: {(rel_r, rel_c): color}
    relative_pixels = {}
    for obj in objects:
        obj_color = obj['color']
        for r, c in obj['coords']:
            rel_r = r - center_r
            rel_c = c - center_c
            relative_pixels[(rel_r, rel_c)] = obj_color
            
    if not relative_pixels:
         # This case should ideally be caught by the 'objects' check earlier
         return np.array([[background_color]], dtype=int)


    # 5. Determine Output Bounds
    min_r = min(r for r, c in relative_pixels)
    max_r = max(r for r, c in relative_pixels)
    min_c = min(c for r, c in relative_pixels)
    max_c = max(c for r, c in relative_pixels)

    out_height = max_r - min_r + 1
    out_width = max_c - min_c + 1

    # 6. Create Output Grid
    output_grid = np.full((out_height, out_width), background_color, dtype=int)

    # Copy pixels from relative map to output grid
    for (rel_r, rel_c), color in relative_pixels.items():
        # Calculate output coordinates based on top-left corner (min_r, min_c)
        out_r = rel_r - min_r
        out_c = rel_c - min_c
        # Ensure coords are within bounds (should always be, but good practice)
        if 0 <= out_r < out_height and 0 <= out_c < out_width:
             output_grid[out_r, out_c] = color

    # 7. Set Center Color (if applicable)
    if center_color_override is not None:
        # Calculate the output grid coordinates corresponding to the relative center (0, 0)
        center_out_r = 0 - min_r
        center_out_c = 0 - min_c
        
        # Check if the calculated center falls within the output grid bounds
        if 0 <= center_out_r < out_height and 0 <= center_out_c < out_width:
            output_grid[center_out_r, center_out_c] = center_color_override

    # 8. Return Output Grid
    return output_grid.tolist() # Return as list of lists per ARC standard