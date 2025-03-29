```python
import numpy as np
from scipy import ndimage
from typing import List, Tuple, Dict, Any
import math

"""
The transformation identifies distinct non-background objects in the input grid. 
It calculates the relative position of each object's center (centroid) with respect to the overall center of all objects.
These relative positions are then rotated 90 degrees clockwise.
Finally, the original, unmodified objects are placed onto a new grid according to these rotated relative positions, packed tightly together, potentially overwriting each other. 
The output is the minimal bounding box containing the assembled objects.

Note: This implementation currently uses the original objects without the filtering/modification step suspected from the analysis, as the exact rule for pixel reduction is uncertain. It focuses on the object identification, layout rotation, and packing logic. Overlap is handled by overwriting.
"""

# Define colors for clarity if needed (using integer values directly is fine)
# COLOR_MAP = {0: 'white', 1: 'blue', 2: 'red', 3: 'green', ...}


def find_objects(grid: np.ndarray, bg_color: int) -> List[Dict[str, Any]]:
    """
    Finds distinct contiguous objects of non-background colors.

    Args:
        grid: The input grid as a numpy array.
        bg_color: The background color.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains: 'color', 'pixels' (relative coordinates), 
        'bbox' (min_row, min_col, max_row, max_col), 'centroid' (r, c),
        'grid_pixels' (absolute coordinates).
    """
    objects = []
    unique_colors = np.unique(grid)
    
    for color in unique_colors:
        if color == bg_color:
            continue
        
        # Create a mask for the current color
        color_mask = (grid == color)
        
        # Label connected components for the current color
        labeled_mask, num_features = ndimage.label(color_mask)
        
        # Find the locations (slices) of each component
        slices = ndimage.find_objects(labeled_mask)
        
        for i, sl in enumerate(slices):
            # Adjust slice object to get labeled_mask coordinates
            obj_indices = np.where(labeled_mask[sl] == (i + 1))
            
            # Absolute grid coordinates of the object pixels
            abs_coords = (obj_indices[0] + sl[0].start, obj_indices[1] + sl[1].start)
            
            if not abs_coords[0].size: # Should not happen with find_objects slices but check
                continue

            # Calculate bounding box
            min_row, max_row = np.min(abs_coords[0]), np.max(abs_coords[0])
            min_col, max_col = np.min(abs_coords[1]), np.max(abs_coords[1])
            bbox = (min_row, min_col, max_row, max_col)

            # Calculate relative pixel coordinates (relative to bbox top-left)
            rel_coords = (abs_coords[0] - min_row, abs_coords[1] - min_col)
            
            # Store pixels as a set of (r, c) tuples relative to bbox top-left
            pixels = set(zip(rel_coords[0], rel_coords[1]))

            # Calculate centroid (using absolute coordinates)
            centroid = (np.mean(abs_coords[0]), np.mean(abs_coords[1]))
            
            objects.append({
                'color': color,
                'pixels': pixels, # Relative coordinates
                'bbox': bbox, # Absolute coords
                'centroid': centroid, # Absolute coords
                'grid_pixels': set(zip(abs_coords[0], abs_coords[1])) # Absolute coordinates
            })
            
    return objects

def rotate_point_around_center(point: Tuple[float, float], center: Tuple[float, float], angle_deg: float) -> Tuple[float, float]:
    """Rotates a point clockwise around a center point."""
    angle_rad = math.radians(angle_deg)
    cx, cy = center
    px, py = point
    
    # Translate point to origin
    temp_x = px - cx
    temp_y = py - cy
    
    # Rotate point
    # Clockwise rotation: x' = x*cos(a) + y*sin(a), y' = -x*sin(a) + y*cos(a)
    rotated_x = temp_x * math.cos(angle_rad) + temp_y * math.sin(angle_rad)
    rotated_y = -temp_x * math.sin(angle_rad) + temp_y * math.cos(angle_rad)
    
    # Translate point back
    final_x = rotated_x + cx
    final_y = rotated_y + cy
    
    return (final_x, final_y)

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by rearranging objects based on a 90-degree clockwise
    rotation of their relative positions.
    """
    # Convert input to numpy array
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Determine background color
    bg_color = input_grid_np[0, 0]
    
    # Find all non-background objects
    objects = find_objects(input_grid_np, bg_color)
    
    if not objects:
        # Handle case with no objects (e.g., return empty grid or background grid)
        # Based on examples, we expect objects. If none, maybe return 1x1 bg?
        # Returning 1x1 background for now.
         return [[int(bg_color)]]

    # Calculate the overall center of all object centroids
    all_centroids = np.array([obj['centroid'] for obj in objects])
    overall_center = np.mean(all_centroids, axis=0) # (center_r, center_c)

    # Calculate rotated target positions for each object's centroid
    target_centroids = []
    for obj in objects:
        rotated_centroid = rotate_point_around_center(obj['centroid'], overall_center, 90)
        target_centroids.append(rotated_centroid) # (target_r, target_c)

    # --- Packing Stage ---
    # Determine target top-left corners based on rotated centroids
    target_tls = []
    object_dims = []
    for i, obj in enumerate(objects):
        orig_centroid_r, orig_centroid_c = obj['centroid']
        orig_bbox_min_r, orig_bbox_min_c, _, _ = obj['bbox']
        obj_height = obj['bbox'][2] - obj['bbox'][0] + 1
        obj_width = obj['bbox'][3] - obj['bbox'][1] + 1
        object_dims.append({'h': obj_height, 'w': obj_width})

        # Offset from centroid to original top-left
        offset_r = orig_centroid_r - orig_bbox_min_r
        offset_c = orig_centroid_c - orig_bbox_min_c
        
        # Calculate target top-left based on target centroid and original offset
        target_r, target_c = target_centroids[i]
        target_tl_r = target_r - offset_r
        target_tl_c = target_c - offset_c
        target_tls.append({'r': target_tl_r, 'c': target_tl_c})

    # Shift target coordinates to start near (0,0)
    if not target_tls: return [[int(bg_color)]] # Should not happen if objects exist
    
    min_target_r = min(tl['r'] for tl in target_tls)
    min_target_c = min(tl['c'] for tl in target_tls)
    
    shifted_target_tls = []
    max_shifted_r = 0
    max_shifted_c = 0
    for i, tl in enumerate(target_tls):
        shifted_r = round(tl['r'] - min_target_r)
        shifted_c = round(tl['c'] - min_target_c)
        shifted_target_tls.append({'r': shifted_r, 'c': shifted_c})
        # Track max coords needed for canvas size estimation
        max_shifted_r = max(max_shifted_r, shifted_r + object_dims[i]['h'])
        max_shifted_c = max(max_shifted_c, shifted_c + object_dims[i]['w'])

    # Create output canvas (estimate size, add padding)
    # Use a placeholder value different from 0-9, e.g., -1
    canvas_h = int(max_shifted_r + 5) 
    canvas_w = int(max_shifted_c + 5)
    # Fill with a value indicating empty/background (use -1 as placeholder)
    output_canvas = np.full((canvas_h, canvas_w), -1, dtype=int) 

    # Place objects onto the canvas based on shifted target top-lefts
    # Overwrite previous pixels in case of overlap
    # Process objects maybe sorted by target position? (optional, might affect overlap outcome)
    # Sort by target row, then target column
    placement_order = sorted(range(len(objects)), key=lambda k: (shifted_target_tls[k]['r'], shifted_target_tls[k]['c']))

    for i in placement_order:
        obj = objects[i]
        target_tl = shifted_target_tls[i]
        obj_color = obj['color']
        
        for (rel_r, rel_c) in obj['pixels']:
            place_r = target_tl['r'] + rel_r
            place_c = target_tl['c'] + rel_c
            
            # Ensure placement is within canvas bounds
            if 0 <= place_r < canvas_h and 0 <= place_c < canvas_w:
                output_canvas[place_r, place_c] = obj_color

    # Crop the canvas to the content
    # Find rows/cols containing actual objects (non -1)
    content_indices = np.where(output_canvas != -1)
    if content_indices[0].size == 0:
         # If somehow everything was placed out of bounds or no objects placed
         return [[int(bg_color)]] 
         
    min_final_r, max_final_r = np.min(content_indices[0]), np.max(content_indices[0])
    min_final_c, max_final_c = np.min(content_indices[1]), np.max(content_indices[1])
    
    # Final crop
    final_output_np = output_canvas[min_final_r : max_final_r + 1, min_final_c : max_final_c + 1]

    # Replace any remaining -1 placeholders (if any somehow exist within crop) with a default,
    # perhaps the most frequent color in the output? Or just 0? Let's use 0 for now.
    # This shouldn't happen if cropping is correct, but as a safeguard.
    final_output_np[final_output_np == -1] = 0 # Replace placeholder with black/default

    # Convert final numpy array back to list of lists
    output_grid = final_output_np.tolist()

    return output_grid
```