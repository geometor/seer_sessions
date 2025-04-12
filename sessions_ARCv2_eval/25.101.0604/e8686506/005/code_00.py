import numpy as np
from collections import Counter
from scipy.ndimage import label, find_objects
import math

"""
Transforms an input grid based on the following rules:
1. Determine the background color (most frequent pixel value).
2. Identify all connected non-background objects (8-way connectivity), storing the pixels for each.
3. Calculate the bounding box and area for each object.
4. Find the object(s) with the maximum bounding box area ("frame objects").
5. Determine the combined bounding box enclosing all frame objects. This defines the output grid's frame.
6. Identify all non-background objects that are NOT frame objects ("non-frame objects") and collect all pixels belonging to them.
7. Create the output grid with the dimensions of the combined frame bounding box.
8. Populate the output grid:
    - If a pixel within the frame corresponds to a non-background pixel in the input, copy its color.
    - If a pixel within the frame corresponds to a background pixel in the input:
        - Find the pixel among all non-frame pixels that is closest (Euclidean distance) to the input pixel's coordinates.
        - Tie-breaking for closest pixel: minimum distance -> minimum color -> minimum row -> minimum column.
        - Fill the output pixel with the color of this closest non-frame pixel.
    - Handle the case where no non-frame pixels exist (e.g., fill with background color).
"""

def find_background_color(grid: np.ndarray) -> int:
    """Finds the most frequent value in the grid."""
    counts = Counter(grid.flatten())
    if not counts:
        return -1 # Indicate error or empty grid
    # Find the value with the highest count.
    background_color = counts.most_common(1)[0][0]
    return background_color

def find_objects_and_pixels(grid: np.ndarray, background_color: int) -> tuple[dict, np.ndarray, int]:
    """
    Finds connected non-background objects, calculates their properties,
    and returns the labeled array and number of features.
    Properties: bbox, area, color, list of pixels (r, c).
    """
    non_bg_mask = grid != background_color
    # Define 8-way connectivity
    structure = np.ones((3, 3), dtype=bool)
    labeled_array, num_features = label(non_bg_mask, structure=structure)

    if num_features == 0:
        return {}, labeled_array, num_features

    object_properties = {}
    object_slices = find_objects(labeled_array)

    for i in range(num_features):
        label_id = i + 1
        obj_slice = object_slices[i]
        
        # Bounding Box and Area
        min_r, max_r = obj_slice[0].start, obj_slice[0].stop
        min_c, max_c = obj_slice[1].start, obj_slice[1].stop
        bbox = (min_r, min_c, max_r, max_c)
        height = max_r - min_r
        width = max_c - min_c
        area = height * width

        # Coordinates and Color
        obj_coords = np.argwhere(labeled_array == label_id)
        if obj_coords.size == 0:
            continue 

        # Get color from the first pixel of the object (assuming monochromatic objects)
        obj_color = grid[obj_coords[0][0], obj_coords[0][1]]
        
        # Store pixel coordinates (r, c) directly, color is stored once per object
        pixel_list = [(r, c) for r, c in obj_coords]

        object_properties[label_id] = {
            'bbox': bbox,
            'area': area,
            'color': obj_color,
            'pixels': pixel_list # List of (r, c) tuples
        }
        
    return object_properties, labeled_array, num_features

def find_closest_non_frame_pixel_color(target_r: int, target_c: int, non_frame_pixels: list[tuple[int, int, int]], background_color: int) -> int:
    """
    Finds the color of the closest pixel from the non_frame_pixels list to the target coordinates.
    Tie-breaking: min distance -> min color -> min row -> min col.
    non_frame_pixels: List of (row, col, color) tuples.
    """
    if not non_frame_pixels:
        # Fallback if there are no non-frame pixels
        return background_color 

    min_dist_sq = float('inf')
    closest_candidates = [] # Stores (dist_sq, color, r, c) for tie-breaking

    for pr, pc, p_color in non_frame_pixels:
        dist_sq = (target_r - pr)**2 + (target_c - pc)**2
        
        if dist_sq < min_dist_sq:
            min_dist_sq = dist_sq
            closest_candidates = [(dist_sq, p_color, pr, pc)]
        elif dist_sq == min_dist_sq:
            closest_candidates.append((dist_sq, p_color, pr, pc))

    if not closest_candidates:
         # Should not happen if non_frame_pixels is not empty
        return background_color

    # Apply tie-breaking rules by sorting
    # Sort by: dist_sq (implicitly same), color, row, col
    closest_candidates.sort(key=lambda x: (x[1], x[2], x[3]))

    # The first element after sorting is the winner
    return closest_candidates[0][1] # Return the color


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    # Convert input to numpy array
    if not input_grid or not input_grid[0]:
        return []
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape

    # 1. Determine the background color
    background_color = find_background_color(input_grid_np)
    if background_color == -1:
        return [] # Handle empty or problematic input

    # 2 & 3. Find objects, their properties (including pixels), and bounding box areas
    object_properties, _, num_features = find_objects_and_pixels(input_grid_np, background_color)
    
    if num_features == 0:
         return [] # No non-background objects found

    # 4. Find the maximum bounding box area
    max_area = 0
    if object_properties: # Check if dictionary is not empty
        max_area = max(props['area'] for props in object_properties.values()) if object_properties else 0
    
    # 5. Identify frame objects (those with max area)
    frame_object_labels = {label_id for label_id, props in object_properties.items() if props['area'] == max_area}

    # 6. Identify non-frame objects and collect all their pixels
    non_frame_pixels = [] # List of (r, c, color)
    for label_id, props in object_properties.items():
        if label_id not in frame_object_labels:
            obj_color = props['color']
            for r, c in props['pixels']:
                non_frame_pixels.append((r, c, obj_color))

    # 7. Determine the combined bounding box for frame objects
    if not frame_object_labels:
        # Handle case where only non-frame objects exist, or no objects
        # Based on problem description, frame must be defined by max area objects.
        # If no frame objects (e.g., all objects have area 0?), return empty or handle differently.
        # For now, assume max_area > 0 if num_features > 0.
        # If frame_object_labels is empty despite num_features > 0, it implies an issue.
         return []

    combined_min_r, combined_min_c = rows, cols
    combined_max_r, combined_max_c = 0, 0 

    for label_id in frame_object_labels:
        min_r, min_c, max_r, max_c = object_properties[label_id]['bbox']
        combined_min_r = min(combined_min_r, min_r)
        combined_min_c = min(combined_min_c, min_c)
        combined_max_r = max(combined_max_r, max_r) # max_r is exclusive stop index
        combined_max_c = max(combined_max_c, max_c) # max_c is exclusive stop index
        
    frame_r0, frame_c0 = combined_min_r, combined_min_c
    frame_height = combined_max_r - combined_min_r
    frame_width = combined_max_c - combined_min_c

    if frame_height <= 0 or frame_width <= 0:
        return [] # Invalid frame dimensions calculated

    # 8. Create the output grid
    output_grid_np = np.full((frame_height, frame_width), background_color, dtype=int) # Initialize with background

    # 9. Check if non_frame_pixels exist (handled within the fill function)
    
    # 10 & 11 & 12. Populate the output grid
    for out_r in range(frame_height):
        for out_c in range(frame_width):
            # Corresponding input coordinates
            in_r = frame_r0 + out_r
            in_c = frame_c0 + out_c

            # Check bounds just in case
            if 0 <= in_r < rows and 0 <= in_c < cols:
                 input_val = input_grid_np[in_r, in_c]
            else:
                 # Should not happen with correct frame calculation
                 continue # Keep background color

            if input_val != background_color:
                # Copy non-background color from input frame
                output_grid_np[out_r, out_c] = input_val
            else:
                # Find the color of the closest non-frame pixel
                fill_color = find_closest_non_frame_pixel_color(in_r, in_c, non_frame_pixels, background_color)
                output_grid_np[out_r, out_c] = fill_color

    # Convert back to list of lists and return
    output_grid = output_grid_np.tolist()
    return output_grid