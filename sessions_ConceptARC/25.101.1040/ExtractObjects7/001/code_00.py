import numpy as np
from scipy.ndimage import label, find_objects

"""
Identifies all connected components (objects) of non-white pixels in the input grid.
Determines which object serves as the separator, typically a line or bar shape (vertical or horizontal) that partitions the grid.
Notes the orientation of the separator (vertical or horizontal).
Isolates the non-separator primary objects.
For each primary object, extracts the subgrid corresponding to its minimal bounding box.
Sorts the extracted subgrids based on their original spatial position relative to the separator (left-to-right for a vertical separator, top-to-bottom for a horizontal separator).
Concatenates the sorted subgrids along the axis orthogonal to the separator's orientation (horizontally for vertical separator, vertically for horizontal separator).
Returns the resulting concatenated grid.
"""

def get_objects(grid: np.ndarray) -> list[dict]:
    """
    Finds all connected components of non-background pixels.

    Args:
        grid: Input grid as a numpy array.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains its color, coordinates, and bounding box slice.
    """
    objects = []
    unique_colors = np.unique(grid)
    non_background_colors = unique_colors[unique_colors != 0]

    for color in non_background_colors:
        # Create a binary mask for the current color
        binary_mask = (grid == color)
        
        # Label connected components for this color
        labeled_array, num_features = label(binary_mask)
        
        # Find the location (slices) of each labeled feature
        object_slices = find_objects(labeled_array)

        for i in range(num_features):
            obj_slice = object_slices[i]
            # Extract coordinates within the bounding box slice
            coords = np.argwhere(labeled_array[obj_slice] == (i + 1))
            # Offset coordinates to be relative to the original grid
            absolute_coords = coords + np.array([obj_slice[0].start, obj_slice[1].start])
            
            min_row, min_col = np.min(absolute_coords, axis=0)
            max_row, max_col = np.max(absolute_coords, axis=0)

            objects.append({
                'color': color,
                'coords': absolute_coords.tolist(),
                'slice': obj_slice,
                'bbox': (min_row, min_col, max_row, max_col) # top, left, bottom, right
            })
            
    return objects

def extract_subgrid(grid: np.ndarray, obj_slice: tuple[slice, slice]) -> np.ndarray:
    """Extracts the subgrid defined by the slice."""
    return grid[obj_slice]

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by identifying a separator, extracting other objects,
    and concatenating them based on the separator's orientation.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    
    # 1. Identify all connected components (objects) of non-white pixels
    all_objects = get_objects(grid)

    separator = None
    separator_orientation = None # 'vertical' or 'horizontal'
    primary_objects = []

    # 2. Determine which object serves as the separator
    potential_separators = []
    for obj in all_objects:
        min_r, min_c, max_r, max_c = obj['bbox']
        obj_h = max_r - min_r + 1
        obj_w = max_c - min_c + 1

        # Heuristic: Separator is often a line spanning most of the grid dimension
        # Check vertical line possibility (thin and tall)
        if obj_w <= 2 and obj_h >= height * 0.8:
            potential_separators.append({'object': obj, 'orientation': 'vertical'})
        # Check horizontal line possibility (flat and wide)
        elif obj_h <= 2 and obj_w >= width * 0.8:
             potential_separators.append({'object': obj, 'orientation': 'horizontal'})

    # Refined Check: A separator must partition the *other* objects
    if not potential_separators:
         # Fallback or alternative separator detection needed if simple lines fail
         # For this task, the line heuristic seems sufficient based on examples
         # If needed, implement the partitioning check described in thought process
         raise ValueError("Could not identify a clear separator object based on shape.")

    # Assume the first potential separator found is the correct one (simplification)
    # A more complex task might require choosing the 'best' partitioner
    if potential_separators:
        separator_info = potential_separators[0] # Simplistic choice
        separator = separator_info['object']
        separator_orientation = separator_info['orientation']
        
        # 3. Note the orientation (done above)

        # 4. Isolate the non-separator primary objects
        primary_objects = [obj for obj in all_objects if obj != separator]
    else:
         # If no separator found via heuristics, maybe all objects are primary?
         # Or the logic needs extension. For now, assume separator exists.
         raise ValueError("Separator identification failed.")


    if not primary_objects:
        # Handle cases where there are no objects other than the separator (unlikely in ARC)
        return [] 
        
    # 5. For each primary object, extract its subgrid
    extracted_subgrids = []
    for obj in primary_objects:
        subgrid = extract_subgrid(grid, obj['slice'])
        # Important: Ensure extracted subgrid only contains the object's color + background
        # This avoids including parts of other objects if bounding boxes overlap slightly
        mask = np.zeros_like(subgrid, dtype=bool)
        relative_coords = np.array(obj['coords']) - np.array([obj['slice'][0].start, obj['slice'][1].start])
        mask[tuple(relative_coords.T)] = True
        
        final_subgrid = np.zeros_like(subgrid)
        final_subgrid[mask] = subgrid[mask] # Keep only the object's pixels
        
        extracted_subgrids.append({
            'subgrid': final_subgrid,
            'original_bbox': obj['bbox'] 
        })

    # 6 & 7. Sort and Concatenate based on separator orientation
    output_grid_np = None
    if separator_orientation == 'vertical':
        # Sort left-to-right based on min column index
        extracted_subgrids.sort(key=lambda x: x['original_bbox'][1])
        # Concatenate horizontally
        output_grid_np = np.hstack([item['subgrid'] for item in extracted_subgrids])

    elif separator_orientation == 'horizontal':
        # Sort top-to-bottom based on min row index
        extracted_subgrids.sort(key=lambda x: x['original_bbox'][0])
        # Concatenate vertically
        output_grid_np = np.vstack([item['subgrid'] for item in extracted_subgrids])
    else:
         # Should not happen if separator was identified
         raise ValueError("Separator orientation not determined.")

    # 8. Convert back to list of lists and return
    return output_grid_np.tolist()
