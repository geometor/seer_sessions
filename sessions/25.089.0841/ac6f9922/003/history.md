
## train_1

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 2 2 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 2 2 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 3 3 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 3 3 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 2
3 8
```


## train_2

**input:**
```
4 4 4 4 4 4 4 4 4 4 4 4 4
4 1 1 1 1 1 1 1 1 1 1 1 4
4 1 1 1 1 1 1 1 1 1 1 1 4
4 1 1 4 4 4 4 1 4 4 4 1 4
4 1 1 4 2 2 4 1 4 4 4 1 4
4 1 1 4 2 2 4 1 4 4 4 1 4
4 1 1 4 4 4 4 1 4 4 4 1 4
4 1 1 1 1 1 1 1 1 1 1 1 4
4 1 1 4 4 4 4 1 4 4 4 1 4
4 1 1 4 4 4 4 1 4 4 4 1 4
4 1 1 4 4 4 4 1 4 4 4 1 4
4 1 1 1 1 1 1 1 1 1 1 1 4
4 4 4 4 4 4 4 4 4 4 4 4 4
```


**output:**
```
2 4
4 4
```


## train_3

**input:**
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1
1 2 1 1 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 1 3 1 2 1 4 4 1 2 1 1 1 2 2 1
1 2 1 3 1 2 1 4 4 1 2 1 1 1 2 2 1
1 2 1 3 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 1 1 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 1 1 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1
1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1
1 2 1 1 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 1 1 1 2 1 6 6 1 2 1 8 1 2 2 1
1 2 1 1 1 2 1 6 6 1 2 1 8 1 2 2 1
1 2 1 1 1 2 1 6 6 1 2 1 8 1 2 2 1
1 2 1 1 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```


**output:**
```
3 4 1
1 6 8
```

*   **Perception:** The task involves identifying distinct 'target' objects within a larger defined area in the input grid and representing their relative spatial arrangement in a smaller output grid. The colors of the frame, the main inner area, and the internal structures play roles in defining the context and identifying the target objects. The output grid seems to capture the essence of the target objects' layout, discarding the exact shapes, sizes, and the surrounding context from the input.

*   **Facts:**
    
```yaml
    task_elements:
      - Input Grid: A 2D array of pixels with integer values representing colors.
      - Output Grid: A smaller 2D array representing a distilled spatial relationship.
    
    grid_properties:
      - Frame Color (B1): The color forming the outer border of the input grid.
      - Main Area Color (C1): The dominant color filling the region inside the frame.
      - Internal Structure Color (B2): The color used for patterns/shapes within the C1 area. Observed that B1 == B2 in examples.
    
    objects:
      - Frame: The outermost border of the grid, defined by B1.
      - Main Area: The region enclosed by the frame, primarily filled with C1.
      - Internal Structures: Shapes within the Main Area, colored B1/B2.
      - Target Objects: Contiguous blocks of pixels within the Main Area whose color is neither C1 nor B1/B2. These are the objects of interest.
    
    object_properties:
      - Target Object Color: The color of a target object.
      - Target Object Position: The location (e.g., centroid) of a target object within the input grid.
      - Target Object Relative Position: The spatial location of a target object relative to others or a reference point (like the center of the Main Area).
    
    relationships:
      - Containment: Target Objects are contained within the Main Area.
      - Spatial Arrangement: Target Objects have relative positions (e.g., top-left, bottom-right) with respect to each other or a reference point.
      - Color Exclusion: Target Objects are defined by colors different from the Main Area (C1) and the Frame/Internal Structure (B1/B2).
    
    transformation:
      - Identification: Locate the Frame (B1), Main Area (C1), and Target Objects.
      - Abstraction: Extract the color and relative position of each Target Object.
      - Mapping: Create a new, smaller grid.
      - Placement: Arrange the Target Object colors in the output grid based on their relative spatial positions identified in the input.
      - Filling: Fill the remaining cells of the output grid with the Frame/Internal Structure color (B1/B2).
      - Size Determination: The output grid size depends on the number and arrangement of target objects (specifically, the number of unique relative rows and columns they occupy, with a special case for single objects resulting in a 2x2 grid).
    ```


*   **Natural Language Program:**
    1.  Identify the color of the outer frame (B1) and the color of the large central area (C1) in the input grid. Note that B1 is also used for structures within C1.
    2.  Find all contiguous shapes ("target objects") located within the C1 area whose color is neither C1 nor B1.
    3.  If there are no target objects, the process result is undefined by these examples (likely an empty grid or a grid filled with B1).
    4.  If there is exactly one target object:
        a.  Determine the center coordinates of the C1 area.
        b.  Determine the position of the single target object's centroid relative to the C1 center (top-left, top-right, bottom-left, or bottom-right quadrant).
        c.  Create a 2x2 output grid filled with color B1.
        d.  Place the target object's color into the cell corresponding to its relative quadrant.
    5.  If there are multiple target objects:
        a.  Calculate the centroid coordinates for each target object.
        b.  Create a sorted list of unique row coordinates from the centroids.
        c.  Create a sorted list of unique column coordinates from the centroids.
        d.  Determine the output grid dimensions: height = number of unique rows, width = number of unique columns.
        e.  Create the output grid of the determined size, filling it entirely with color B1.
        f.  For each target object, find the index of its centroid's row coordinate in the sorted unique row list (this is its relative row index).
        g.  For each target object, find the index of its centroid's column coordinate in the sorted unique column list (this is its relative column index).
        h.  Place the target object's color into the output grid at the cell specified by its (relative row index, relative column index).
    6.  Return the constructed output grid.
```python
import numpy as np
from scipy.ndimage import label, center_of_mass, find_objects

"""
Identifies target objects within a framed area in the input grid and maps their 
colors to a smaller output grid based on their relative spatial positions.

1.  Identify the frame color (B1) - typically the outermost border color.
2.  Identify the main area color (C1) - typically the most frequent color within the frame.
3.  Find all contiguous shapes ("target objects") located within the input grid 
    whose color is neither C1 nor B1.
4.  Calculate the centroid for each target object.
5.  If no target objects are found, return a 1x1 grid filled with B1.
6.  If exactly one target object is found:
    a.  Determine the bounding box of the area inside the frame.
    b.  Calculate the center of this inner bounding box.
    c.  Determine which quadrant (top-left, top-right, bottom-left, bottom-right) 
        the target object's centroid falls into relative to the inner area center.
    d.  Create a 2x2 output grid filled with B1.
    e.  Place the target object's color in the corresponding quadrant cell.
7.  If multiple target objects are found:
    a.  Extract the row and column coordinates from each target object's centroid.
    b.  Create sorted lists of unique row and column coordinates.
    c.  Determine output grid dimensions: height = number of unique rows, width = number of unique columns.
    d.  Create the output grid of the determined size, filled with B1.
    e.  For each target object, find the index of its centroid's row in the unique sorted row list 
        and the index of its centroid's column in the unique sorted column list.
    f.  Place the target object's color at these indices (row_index, col_index) in the output grid.
8.  Return the constructed output grid.
"""

def find_target_objects(grid, frame_color, main_area_color):
    """Finds contiguous objects not matching frame or main area colors."""
    target_mask = (grid != frame_color) & (grid != main_area_color)
    
    # Ensure target_mask contains only valid target colors if needed,
    # but current logic works if frame/main area colors are correctly identified.
    
    labeled_array, num_features = label(target_mask)
    objects = []
    if num_features > 0:
        slices = find_objects(labeled_array)
        for i in range(num_features):
            obj_slice = slices[i]
            obj_coords_local = np.argwhere(labeled_array[obj_slice] == (i + 1))
            obj_coords_global = obj_coords_local + np.array([obj_slice[0].start, obj_slice[1].start])
            
            # Use the color from the original grid at the first coordinate of the object
            obj_color = grid[obj_coords_global[0, 0], obj_coords_global[0, 1]]
            
            centroid = center_of_mass(target_mask, labeled_array, i + 1)
            objects.append({'color': obj_color, 'centroid': centroid, 'pixels': obj_coords_global})
            
    return objects

def get_inner_bounding_box(grid, frame_color):
    """Finds the bounding box of the area inside the frame."""
    non_frame_coords = np.argwhere(grid != frame_color)
    if non_frame_coords.size == 0:
        # Handle cases where grid is all frame color or empty
        return 0, grid.shape[0] -1 , 0, grid.shape[1] - 1 
        
    min_row = np.min(non_frame_coords[:, 0])
    max_row = np.max(non_frame_coords[:, 0])
    min_col = np.min(non_frame_coords[:, 1])
    max_col = np.max(non_frame_coords[:, 1])
    return min_row, max_row, min_col, max_col


def transform(input_grid):
    """
    Transforms the input grid based on the spatial arrangement of target objects.
    """
    input_np = np.array(input_grid)
    
    # 1. Identify frame color (B1) - Assuming it's the border color
    # Check corners and edges; often the most frequent on border
    border_colors, counts = np.unique(np.concatenate([
        input_np[0, :], input_np[-1, :], input_np[1:-1, 0], input_np[1:-1, -1]
    ]), return_counts=True)
    frame_color = border_colors[np.argmax(counts)] # B1

    # 2. Identify main area color (C1) - Most frequent non-frame color inside
    min_r, max_r, min_c, max_c = get_inner_bounding_box(input_np, frame_color)
    inner_area = input_np[min_r:max_r+1, min_c:max_c+1]
    # Consider only pixels NOT equal to frame_color for C1 identification
    inner_colors_non_frame, counts_non_frame = np.unique(inner_area[inner_area != frame_color], return_counts=True)
    
    if len(counts_non_frame) > 0:
         main_area_color = inner_colors_non_frame[np.argmax(counts_non_frame)] # C1
    else:
         # If inner area only contains frame color, perhaps C1 = B1 ?
         # Or maybe there's no distinct C1. Let's assume C1 cannot be B1 for target finding.
         # Use a placeholder or handle error - for now assume B1 and find targets != B1
         main_area_color = frame_color # If no other color is dominant inside, treat frame color as main color too?


    # 3. Find target objects
    # Exclude B1 and C1. If C1 ended up being same as B1, only exclude B1.
    exclude_colors = {frame_color}
    if main_area_color != frame_color:
         exclude_colors.add(main_area_color)
         
    target_mask = np.isin(input_np, list(exclude_colors), invert=True)
    # Need to restrict search to within the inner bounding box potentially?
    # Let's try finding anywhere first, the examples seem contained.
    labeled_array, num_features = label(target_mask)
    target_objects = []
    if num_features > 0:
        slices = find_objects(labeled_array)
        for i in range(num_features):
            obj_slice = slices[i]
            # Ensure we are processing parts of the grid that were originally target_mask=True
            # Take the first pixel within the labeled component to get the original color
            coords_in_comp = np.argwhere(labeled_array[obj_slice] == (i + 1))
            first_coord_local = tuple(coords_in_comp[0])
            first_coord_global = (obj_slice[0].start + first_coord_local[0], obj_slice[1].start + first_coord_local[1])
            obj_color = input_np[first_coord_global]
            
            # Filter out objects that might be part of frame or main area if identification was imperfect
            if obj_color in exclude_colors:
                continue
                
            centroid = center_of_mass(target_mask, labeled_array, i + 1)
            target_objects.append({'color': obj_color, 'centroid': centroid})
            
    num_targets = len(target_objects)

    # 5. Handle no target objects
    if num_targets == 0:
        return np.array([[frame_color]]) # Return 1x1 grid with frame color

    # 6. Handle one target object
    if num_targets == 1:
        target = target_objects[0]
        obj_r, obj_c = target['centroid']
        
        # Use inner bounding box for center calculation
        center_r = (min_r + max_r) / 2.0
        center_c = (min_c + max_c) / 2.0
        
        output_grid = np.full((2, 2), frame_color, dtype=int)
        
        if obj_r < center_r and obj_c < center_c: # Top-left
            output_grid[0, 0] = target['color']
        elif obj_r < center_r and obj_c >= center_c: # Top-right
            output_grid[0, 1] = target['color']
        elif obj_r >= center_r and obj_c < center_c: # Bottom-left
            output_grid[1, 0] = target['color']
        else: # Bottom-right
            output_grid[1, 1] = target['color']
            
        return output_grid.tolist() # Convert back to list of lists if required by framework

    # 7. Handle multiple target objects
    else:
        centroids = [obj['centroid'] for obj in target_objects]
        rows = sorted(list(set([c[0] for c in centroids])))
        cols = sorted(list(set([c[1] for c in centroids])))
        
        # Create mapping from centroid coordinate to output index
        row_map = {r: i for i, r in enumerate(rows)}
        col_map = {c: j for j, c in enumerate(cols)}
        
        output_rows = len(rows)
        output_cols = len(cols)
        
        output_grid = np.full((output_rows, output_cols), frame_color, dtype=int)
        
        for target in target_objects:
            obj_r, obj_c = target['centroid']
            # Find the *closest* unique row/col if centroid isn't exactly on a unique value
            # Or simpler: just map directly using the created maps
            # Note: if multiple objects map to the same relative coordinate, the last one processed wins.
            # This seems consistent with the examples provided (no overlaps in output)
            out_r = row_map[obj_r]
            out_c = col_map[obj_c]
            output_grid[out_r, out_c] = target['color']
            
        return output_grid.tolist() # Convert back to list of lists if required

```

Previous Code:
```python
import numpy as np
from scipy.ndimage import label, center_of_mass, find_objects

"""
Identifies target objects within a framed area in the input grid and maps their 
colors to a smaller output grid based on their relative spatial positions.

1.  Identify the frame color (B1) - typically the outermost border color.
2.  Identify the main area color (C1) - typically the most frequent color within the frame.
3.  Find all contiguous shapes ("target objects") located within the input grid 
    whose color is neither C1 nor B1.
4.  Calculate the centroid for each target object.
5.  If no target objects are found, return a 1x1 grid filled with B1.
6.  If exactly one target object is found:
    a.  Determine the bounding box of the area inside the frame.
    b.  Calculate the center of this inner bounding box.
    c.  Determine which quadrant (top-left, top-right, bottom-left, bottom-right) 
        the target object's centroid falls into relative to the inner area center.
    d.  Create a 2x2 output grid filled with B1.
    e.  Place the target object's color in the corresponding quadrant cell.
7.  If multiple target objects are found:
    a.  Extract the row and column coordinates from each target object's centroid.
    b.  Create sorted lists of unique row and column coordinates.
    c.  Determine output grid dimensions: height = number of unique rows, width = number of unique columns.
    d.  Create the output grid of the determined size, filled with B1.
    e.  For each target object, find the index of its centroid's row in the unique sorted row list 
        and the index of its centroid's column in the unique sorted column list.
    f.  Place the target object's color at these indices (row_index, col_index) in the output grid.
8.  Return the constructed output grid.
"""

def find_target_objects(grid, frame_color, main_area_color):
    """Finds contiguous objects not matching frame or main area colors."""
    target_mask = (grid != frame_color) & (grid != main_area_color)
    
    # Ensure target_mask contains only valid target colors if needed,
    # but current logic works if frame/main area colors are correctly identified.
    
    labeled_array, num_features = label(target_mask)
    objects = []
    if num_features > 0:
        slices = find_objects(labeled_array)
        for i in range(num_features):
            obj_slice = slices[i]
            obj_coords_local = np.argwhere(labeled_array[obj_slice] == (i + 1))
            obj_coords_global = obj_coords_local + np.array([obj_slice[0].start, obj_slice[1].start])
            
            # Use the color from the original grid at the first coordinate of the object
            obj_color = grid[obj_coords_global[0, 0], obj_coords_global[0, 1]]
            
            centroid = center_of_mass(target_mask, labeled_array, i + 1)
            objects.append({'color': obj_color, 'centroid': centroid, 'pixels': obj_coords_global})
            
    return objects

def get_inner_bounding_box(grid, frame_color):
    """Finds the bounding box of the area inside the frame."""
    non_frame_coords = np.argwhere(grid != frame_color)
    if non_frame_coords.size == 0:
        # Handle cases where grid is all frame color or empty
        return 0, grid.shape[0] -1 , 0, grid.shape[1] - 1 
        
    min_row = np.min(non_frame_coords[:, 0])
    max_row = np.max(non_frame_coords[:, 0])
    min_col = np.min(non_frame_coords[:, 1])
    max_col = np.max(non_frame_coords[:, 1])
    return min_row, max_row, min_col, max_col


def transform(input_grid):
    """
    Transforms the input grid based on the spatial arrangement of target objects.
    """
    input_np = np.array(input_grid)
    
    # 1. Identify frame color (B1) - Assuming it's the border color
    # Check corners and edges; often the most frequent on border
    border_colors, counts = np.unique(np.concatenate([
        input_np[0, :], input_np[-1, :], input_np[1:-1, 0], input_np[1:-1, -1]
    ]), return_counts=True)
    frame_color = border_colors[np.argmax(counts)] # B1

    # 2. Identify main area color (C1) - Most frequent non-frame color inside
    min_r, max_r, min_c, max_c = get_inner_bounding_box(input_np, frame_color)
    inner_area = input_np[min_r:max_r+1, min_c:max_c+1]
    # Consider only pixels NOT equal to frame_color for C1 identification
    inner_colors_non_frame, counts_non_frame = np.unique(inner_area[inner_area != frame_color], return_counts=True)
    
    if len(counts_non_frame) > 0:
         main_area_color = inner_colors_non_frame[np.argmax(counts_non_frame)] # C1
    else:
         # If inner area only contains frame color, perhaps C1 = B1 ?
         # Or maybe there's no distinct C1. Let's assume C1 cannot be B1 for target finding.
         # Use a placeholder or handle error - for now assume B1 and find targets != B1
         main_area_color = frame_color # If no other color is dominant inside, treat frame color as main color too?


    # 3. Find target objects
    # Exclude B1 and C1. If C1 ended up being same as B1, only exclude B1.
    exclude_colors = {frame_color}
    if main_area_color != frame_color:
         exclude_colors.add(main_area_color)
         
    target_mask = np.isin(input_np, list(exclude_colors), invert=True)
    # Need to restrict search to within the inner bounding box potentially?
    # Let's try finding anywhere first, the examples seem contained.
    labeled_array, num_features = label(target_mask)
    target_objects = []
    if num_features > 0:
        slices = find_objects(labeled_array)
        for i in range(num_features):
            obj_slice = slices[i]
            # Ensure we are processing parts of the grid that were originally target_mask=True
            # Take the first pixel within the labeled component to get the original color
            coords_in_comp = np.argwhere(labeled_array[obj_slice] == (i + 1))
            first_coord_local = tuple(coords_in_comp[0])
            first_coord_global = (obj_slice[0].start + first_coord_local[0], obj_slice[1].start + first_coord_local[1])
            obj_color = input_np[first_coord_global]
            
            # Filter out objects that might be part of frame or main area if identification was imperfect
            if obj_color in exclude_colors:
                continue
                
            centroid = center_of_mass(target_mask, labeled_array, i + 1)
            target_objects.append({'color': obj_color, 'centroid': centroid})
            
    num_targets = len(target_objects)

    # 5. Handle no target objects
    if num_targets == 0:
        return np.array([[frame_color]]) # Return 1x1 grid with frame color

    # 6. Handle one target object
    if num_targets == 1:
        target = target_objects[0]
        obj_r, obj_c = target['centroid']
        
        # Use inner bounding box for center calculation
        center_r = (min_r + max_r) / 2.0
        center_c = (min_c + max_c) / 2.0
        
        output_grid = np.full((2, 2), frame_color, dtype=int)
        
        if obj_r < center_r and obj_c < center_c: # Top-left
            output_grid[0, 0] = target['color']
        elif obj_r < center_r and obj_c >= center_c: # Top-right
            output_grid[0, 1] = target['color']
        elif obj_r >= center_r and obj_c < center_c: # Bottom-left
            output_grid[1, 0] = target['color']
        else: # Bottom-right
            output_grid[1, 1] = target['color']
            
        return output_grid.tolist() # Convert back to list of lists if required by framework

    # 7. Handle multiple target objects
    else:
        centroids = [obj['centroid'] for obj in target_objects]
        rows = sorted(list(set([c[0] for c in centroids])))
        cols = sorted(list(set([c[1] for c in centroids])))
        
        # Create mapping from centroid coordinate to output index
        row_map = {r: i for i, r in enumerate(rows)}
        col_map = {c: j for j, c in enumerate(cols)}
        
        output_rows = len(rows)
        output_cols = len(cols)
        
        output_grid = np.full((output_rows, output_cols), frame_color, dtype=int)
        
        for target in target_objects:
            obj_r, obj_c = target['centroid']
            # Find the *closest* unique row/col if centroid isn't exactly on a unique value
            # Or simpler: just map directly using the created maps
            # Note: if multiple objects map to the same relative coordinate, the last one processed wins.
            # This seems consistent with the examples provided (no overlaps in output)
            out_r = row_map[obj_r]
            out_c = col_map[obj_c]
            output_grid[out_r, out_c] = target['color']
            
        return output_grid.tolist() # Convert back to list of lists if required

```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 2 2 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 2 2 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 3 3 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 3 3 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 2
3 8
```
Transformed Output:
```
8 2
3 8
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 2:
Input:
```
4 4 4 4 4 4 4 4 4 4 4 4 4
4 1 1 1 1 1 1 1 1 1 1 1 4
4 1 1 1 1 1 1 1 1 1 1 1 4
4 1 1 4 4 4 4 1 4 4 4 1 4
4 1 1 4 2 2 4 1 4 4 4 1 4
4 1 1 4 2 2 4 1 4 4 4 1 4
4 1 1 4 4 4 4 1 4 4 4 1 4
4 1 1 1 1 1 1 1 1 1 1 1 4
4 1 1 4 4 4 4 1 4 4 4 1 4
4 1 1 4 4 4 4 1 4 4 4 1 4
4 1 1 4 4 4 4 1 4 4 4 1 4
4 1 1 1 1 1 1 1 1 1 1 1 4
4 4 4 4 4 4 4 4 4 4 4 4 4
```
Expected Output:
```
2 4
4 4
```
Transformed Output:
```
2 4
4 4
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 3:
Input:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1
1 2 1 1 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 1 3 1 2 1 4 4 1 2 1 1 1 2 2 1
1 2 1 3 1 2 1 4 4 1 2 1 1 1 2 2 1
1 2 1 3 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 1 1 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 1 1 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1
1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1
1 2 1 1 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 1 1 1 2 1 6 6 1 2 1 8 1 2 2 1
1 2 1 1 1 2 1 6 6 1 2 1 8 1 2 2 1
1 2 1 1 1 2 1 6 6 1 2 1 8 1 2 2 1
1 2 1 1 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Expected Output:
```
3 4 1
1 6 8
```
Transformed Output:
```
1 4 1
3 1 1
1 6 8
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
Color Count Correct: False
Score: None
