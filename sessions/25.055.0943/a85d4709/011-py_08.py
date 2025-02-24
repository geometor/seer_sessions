"""
1.  **Identify Objects:** The input consists of five distinct black objects of varying rectangular shapes and one yellow object.
2.  **Combine Black Objects:** The transformation combines vertically-adjacent and horizontally-adjacent black objects into the smallest bounding rectangle.
3. **Preserve Yellow object:** The yellow object does not combine or change
4.  **Output:** The output consists of the two combined black rectangles and the original yellow square.
"""

import numpy as np
from skimage.measure import label, regionprops

def get_objects(grid):
    """Identifies objects and extracts their properties."""
    labeled_grid = label(grid, connectivity=1)  # Use 4-connectivity
    objects = []
    for region in regionprops(labeled_grid):
        # skimage regionprops identifies background, so we ignore that.
        if region.label == 0: continue # added

        min_row, min_col, max_row, max_col = region.bbox
        objects.append({
            "label": region.label, # added
            "color": grid[min_row, min_col],  # All pixels in region have same color
            "bbox": (min_row, min_col, max_row, max_col),
            "size": (max_row - min_row, max_col - min_col),
            "area": region.area,
            "centroid": region.centroid,
            "is_square": region.extent == 1
        })
    return objects

def combine_black_objects(objects):
    """Combines adjacent black objects."""
    black_objects = [obj for obj in objects if obj["color"] == 0]
    other_objects = [obj for obj in objects if obj["color"] != 0]
    if not black_objects:  # Handle cases with no black objects
        return other_objects
    
    combined_black = []
    processed = [False] * len(black_objects)

    for i in range(len(black_objects)):
        if processed[i]:
            continue

        current_bbox = list(black_objects[i]["bbox"])
        processed[i] = True
        
        # Iteratively expand the bounding box
        expansion_occurred = True
        while expansion_occurred:
            expansion_occurred = False
            for j in range(len(black_objects)):
                if processed[j]:
                    continue
                other_bbox = black_objects[j]["bbox"]
                
                # Check for adjacency (4-connectivity)
                adjacent = False
                # Check vertical adjacency
                if (current_bbox[1] <= other_bbox[3] and current_bbox[3] >= other_bbox[1] and
                    (current_bbox[0] == other_bbox[2] or current_bbox[2] == other_bbox[0] )):
                  adjacent = True

                # Check horizontal adjacency
                if (current_bbox[0] <= other_bbox[2] and current_bbox[2] >= other_bbox[0] and
                    (current_bbox[1] == other_bbox[3] or current_bbox[3] == other_bbox[1])):
                    adjacent = True

                if adjacent:
                    current_bbox[0] = min(current_bbox[0], other_bbox[0])
                    current_bbox[1] = min(current_bbox[1], other_bbox[1])
                    current_bbox[2] = max(current_bbox[2], other_bbox[2])
                    current_bbox[3] = max(current_bbox[3], other_bbox[3])
                    processed[j] = True
                    expansion_occurred = True
        
        combined_black.append({"color": 0, "bbox": tuple(current_bbox)})
    
    return combined_black + other_objects
    

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # get objects
    objects = get_objects(input_grid)
    
    # combine black objects
    combined_objects = combine_black_objects(objects)
    
    # fill output grid
    for obj in combined_objects:
        min_row, min_col, max_row, max_col = obj["bbox"]
        output_grid[min_row:max_row, min_col:max_col] = obj["color"]

    return output_grid