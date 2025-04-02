import numpy as np
from collections import deque

"""
Transforms the input grid by performing a conditional flood fill. 
It identifies an 'outer' or 'container' color (often touching the grid edges) 
and an 'inner' color (fully enclosed). It then fills any white (0) pixels 
reachable from the inner shape's pixels without crossing the container color pixels, 
using the inner color as the fill color. Original non-white pixels retain their color.
"""

def find_colors_and_roles(grid):
    """
    Identifies the container color, inner/fill color, and inner shape pixels.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (container_color, fill_color, inner_shape_pixels, error_message)
               Returns None for colors/pixels and an error message if identification fails.
    """
    rows, cols = grid.shape
    unique_colors = np.unique(grid[grid != 0]) # Find all non-white colors

    if len(unique_colors) < 2:
        return None, None, None, "Requires at least two non-background colors."

    colors_touching_edge = set()
    all_non_white_pixels = {} # Store coordinates for each color

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0:
                # Store coordinates
                if color not in all_non_white_pixels:
                    all_non_white_pixels[color] = set()
                all_non_white_pixels[color].add((r, c))

                # Check edge touching
                if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                    colors_touching_edge.add(color)

    # Determine container and fill colors
    inner_colors = [c for c in unique_colors if c not in colors_touching_edge]
    
    # Handle edge case where container is not touching the edge (padded grid)
    if not colors_touching_edge and len(unique_colors) == 2:
         # Assume the color with more pixels is the container if neither touches edge
         # This is heuristic and might fail in complex cases
         color1, color2 = unique_colors
         if len(all_non_white_pixels[color1]) > len(all_non_white_pixels[color2]):
             container_color = color1
             fill_color = color2
         else:
             container_color = color2
             fill_color = color1
         inner_shape_pixels = all_non_white_pixels[fill_color]
         return container_color, fill_color, inner_shape_pixels, None
             
    elif len(colors_touching_edge) == 1 and len(inner_colors) == 1:
        container_color = list(colors_touching_edge)[0]
        fill_color = inner_colors[0]
        if fill_color not in all_non_white_pixels:
             return None, None, None, f"Identified inner color {fill_color} has no pixels."
        inner_shape_pixels = all_non_white_pixels[fill_color]
        return container_color, fill_color, inner_shape_pixels, None
    else:
        # Fallback or more complex logic might be needed if heuristics fail
        # Let's try the largest component by pixel count is container, next is inner
        if len(unique_colors) >= 2:
             components = []
             for color in unique_colors:
                 if color in all_non_white_pixels:
                     components.append({'color': color, 'coords': all_non_white_pixels[color], 'count': len(all_non_white_pixels[color])})
             components.sort(key=lambda x: x['count'], reverse=True)
             container_color = components[0]['color']
             fill_color = components[1]['color']
             inner_shape_pixels = components[1]['coords']
             # Warning: This fallback contradicts the edge-touching logic if that failed ambiguously
             # print(f"Warning: Using fallback component size logic. Container={container_color}, Fill={fill_color}")
             return container_color, fill_color, inner_shape_pixels, None # Use with caution
        
        return None, None, None, f"Ambiguous roles: Edge colors {colors_touching_edge}, Inner colors {inner_colors}"


def transform(input_grid):
    """
    Applies the conditional flood fill transformation.
    """
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    output_grid = grid.copy()

    # 1. Identify Container Color, Fill Color, and Inner Shape Pixels
    container_color, fill_color, inner_shape_pixels, error = find_colors_and_roles(grid)

    if error:
        # print(f"Error identifying roles: {error}")
        # Return original grid if roles cannot be determined
        return output_grid.tolist() 
        
    if not inner_shape_pixels:
        # print("Error: No inner shape pixels found.")
        return output_grid.tolist()

    # 2. Perform Conditional Flood Fill (BFS)
    start_pixel = next(iter(inner_shape_pixels)) # Get one pixel from the inner shape
    q = deque([start_pixel])
    visited = set(inner_shape_pixels) # Start visit set with all inner pixels

    while q:
        r, c = q.popleft()

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is valid and unvisited
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                
                neighbor_color_original = grid[nr, nc]

                # Check if the neighbor is NOT part of the container boundary
                if neighbor_color_original != container_color:
                    visited.add((nr, nc)) # Mark as visited regardless of color (if not container)
                    
                    # If the neighbor was originally white, color it in the output grid
                    if neighbor_color_original == 0:
                        output_grid[nr, nc] = fill_color
                    
                    # Add neighbor to the queue to explore from it
                    q.append((nr, nc))
                # else: # Neighbor is container color, stop fill in this direction but mark visited
                     # Mark container pixels encountered as visited so we don't re-evaluate them
                     # Note: we could pre-populate visited with all container pixels if needed
                     # visited.add((nr, nc)) 
                     # No - only mark if visited *from* a non-container pixel
                     pass # Explicitly do nothing if it's a container pixel


    return output_grid.tolist()