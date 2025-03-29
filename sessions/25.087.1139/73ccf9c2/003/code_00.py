import numpy as np
from collections import deque

"""
The transformation identifies all connected objects of the single non-white color in the input grid.
It categorizes these objects into 'signal' (area > 1) and 'noise' (area = 1).
If the count of noise objects is strictly greater than the count of signal objects, 
the target object is the noise object (single pixel) that is located bottom-most, 
and then right-most in case of a tie in the row coordinate.
Otherwise (if the count of noise objects is less than or equal to the count of signal objects), 
the target object is the signal object whose bounding box's top-left corner is 
located bottom-most (maximum row index), and then right-most (maximum column index) 
in case of a tie.
The final output grid contains only the target object, cropped to its minimal bounding box,
with the remaining space filled with the background color (white, 0).
"""

def find_objects(grid, target_color):
    """
    Finds all connected objects of a specific color in the grid using BFS.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is a set of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == target_color and (r, c) not in visited:
                # Start BFS to find a connected object
                obj_pixels = set()
                q = deque([(r, c)])
                visited.add((r, c))
                obj_pixels.add((r, c))

                while q:
                    row, col = q.popleft()

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == target_color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            obj_pixels.add((nr, nc))
                            q.append((nr, nc))
                
                if obj_pixels:
                    objects.append(obj_pixels)
    return objects

def get_bounding_box(obj_pixels):
    """
    Calculates the bounding box for a set of pixels.

    Args:
        obj_pixels (set): A set of (row, col) tuples representing an object.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) or None if the set is empty.
    """
    if not obj_pixels:
        return None
    
    rows = [r for r, c in obj_pixels]
    cols = [c for r, c in obj_pixels]
    
    min_row = min(rows)
    min_col = min(cols)
    max_row = max(rows)
    max_col = max(cols)
    
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    """
    Identifies a target object based on signal/noise counts and position,
    then extracts it into its bounding box.
    """
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    
    # Find the non-white color present in the grid
    unique_colors = np.unique(grid)
    target_color = -1
    for color in unique_colors:
        if color != 0:
            target_color = color
            break
            
    # Handle cases with no non-white color or empty grid
    if target_color == -1:
        return [[0]] 

    # Find all objects of the target color
    all_objects = find_objects(grid, target_color)
    
    if not all_objects:
        # No objects of the target color found
         return [[0]]

    # Categorize objects into signal (area > 1) and noise (area == 1)
    signal_objects = []
    noise_objects_coords = [] # Store (r, c) for noise objects for sorting
    noise_objects_pixels = [] # Store pixel set for noise objects

    for obj_pixels in all_objects:
        if len(obj_pixels) == 1:
            # It's a noise object, store its coordinate and pixel set
            coord = next(iter(obj_pixels)) # Get the single (r, c) tuple
            noise_objects_coords.append(coord)
            noise_objects_pixels.append(obj_pixels)
        else:
            # It's a signal object
            signal_objects.append(obj_pixels)

    N_signal = len(signal_objects)
    N_noise = len(noise_objects_coords)
    
    selected_object_pixels = None

    # Selection Logic
    if N_noise > N_signal:
        # Case 1: More noise than signal
        # Sort noise objects: bottom-most (max r), then right-most (max c)
        # Combine coordinates and pixels for sorting
        noise_data = sorted(zip(noise_objects_coords, noise_objects_pixels), 
                            key=lambda item: (item[0][0], item[0][1]), 
                            reverse=True) 
        if noise_data:
            selected_object_pixels = noise_data[0][1] # Get the pixel set of the selected noise object
            
    else:
        # Case 2: Noise <= Signal (or no signal objects, which shouldn't happen if N_noise <= N_signal and all_objects is not empty)
        if not signal_objects: 
             # This case might occur if N_noise=0 and N_signal=0, already handled by 'if not all_objects'
             # Or if N_noise > 0 and N_signal=0, handled by the N_noise > N_signal case.
             # If somehow N_noise <= N_signal but N_signal is 0, default to selecting based on noise if any.
             if noise_objects_coords:
                 noise_data = sorted(zip(noise_objects_coords, noise_objects_pixels), 
                                     key=lambda item: (item[0][0], item[0][1]), 
                                     reverse=True)
                 selected_object_pixels = noise_data[0][1]
             else: # Should not be reachable if all_objects was not empty
                 return [[0]] 
        else:
            # Calculate bounding box top-left corners for signal objects
            signal_data = []
            for pixels in signal_objects:
                bbox = get_bounding_box(pixels)
                if bbox:
                    min_r, min_c, _, _ = bbox
                    signal_data.append({'pixels': pixels, 'min_r': min_r, 'min_c': min_c})
            
            # Sort signal objects: bottom-most (max min_r), then right-most (max min_c)
            sorted_signal_data = sorted(signal_data, 
                                        key=lambda item: (item['min_r'], item['min_c']), 
                                        reverse=True)
            
            if sorted_signal_data:
                 selected_object_pixels = sorted_signal_data[0]['pixels']

    # If no object could be selected (edge case, e.g., only signal objects but bbox calculation failed)
    if selected_object_pixels is None:
        return [[0]] # Or handle appropriately

    # Get the bounding box of the selected object
    bbox = get_bounding_box(selected_object_pixels)
    if bbox is None:
         return [[0]] # Should not happen if selected_object_pixels is not None/empty
         
    min_r, min_c, max_r, max_c = bbox
    
    # Calculate output grid dimensions
    output_height = max_r - min_r + 1
    output_width = max_c - min_c + 1
    
    # Initialize output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Copy the selected object pixels to the output grid, adjusting coordinates
    for r, c in selected_object_pixels:
        output_r = r - min_r
        output_c = c - min_c
        # Ensure indices are within bounds (should be by definition of bbox)
        if 0 <= output_r < output_height and 0 <= output_c < output_width:
            output_grid[output_r, output_c] = target_color
        
    # Convert back to list of lists for the required output format
    return output_grid.tolist()