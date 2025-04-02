
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0
0 1 1 1 0 0 0 0 0
0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0
0 1 1 1 0 0 0 0 0
0 1 1 1 0 0 0 0 0
0 0 0 0 0 1 1 1 0
0 0 0 0 0 1 1 1 0
0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 3 0 3
2 2 2 0 0 0 0 3 0
0 2 0 0 0 0 3 0 3
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 2 0 0 0 0 0
0 0 2 2 2 0 0 0 0
0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 3 0 3
2 2 2 0 0 0 0 3 0
0 2 0 0 0 0 3 0 3
0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 3 0 0
0 0 0 0 0 3 0 0 0
0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 6 0
0 8 0 8 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 6 6 6
0 8 8 8 0 0 0 0 0 6 0
0 8 0 8 0 0 0 0 6 6 6
0 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 0 0 0
0 0 0 0 0 8 0 8 0 0 0
0 0 0 0 0 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 6 0 0 0 0
0 0 0 0 0 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The task involves identifying specific "marker" pixels and larger "source" objects of the same color within the input grid.
    *   The transformation copies the largest source object of a given color and places it onto the grid, centered at the location of the corresponding single marker pixel of the same color.
    *   Multiple colors can be processed independently within the same grid.
    *   Objects that are neither markers nor the largest source object for a marker remain unchanged.
    *   The original source objects also remain unchanged.

*   **YAML Facts:**
    
```yaml
    elements:
      - role: grid
        description: A 2D array of pixels with integer values 0-9 representing colors.
      - role: object
        description: A contiguous block of pixels of the same non-white color.
        properties:
          - color: The color value (1-9) of the pixels in the object.
          - size: The number of pixels comprising the object.
          - shape: The spatial arrangement of the pixels.
          - position: The coordinates (row, col) of the pixels.
          - bounding_box: The smallest rectangle enclosing the object.
          - center: The calculated center coordinate of the bounding box.
      - role: marker_pixel
        description: An object with a size of exactly one pixel.
        relationship: Corresponds to a source object of the same color.
      - role: source_object
        description: The largest object (by pixel count) of a specific color, excluding any marker pixels of that color.
        relationship: Is copied and centered onto the location of a marker pixel of the same color.

    actions:
      - name: identify_objects
        description: Find all distinct contiguous objects of non-white colors in the input grid.
      - name: classify_objects
        description: For each color present, categorize objects into single-pixel markers and potential source objects (size > 1).
      - name: find_largest_source
        description: For each color with exactly one marker pixel, identify the largest object (by pixel count) among the potential source objects of that same color.
      - name: calculate_center
        description: Determine the center coordinates for the bounding box of the largest source object and the coordinates of the marker pixel.
      - name: copy_and_place
        description: Create a copy of the largest source object's pixels. Calculate the offset required to align the center of the source object's copy with the marker pixel's location. Place the copied pixels onto the output grid at the calculated offset positions, overwriting existing pixels including the marker.
      - name: preserve_others
        description: Ensure all original pixels/objects not involved in the copy/place operation (i.e., not markers that were replaced, and not the pixels newly placed) are present in the output grid in their original positions.

    flow:
      - Input grid is analyzed to identify all colored objects.
      - For each color, objects are checked. If a color has exactly one single-pixel object (marker) and one or more larger objects, proceed.
      - The largest object of that color (the source object) is identified.
      - The source object is copied.
      - The copy is positioned on the grid such that its center aligns with the location of the marker pixel, overwriting the marker.
      - This process is repeated for all colors meeting the criteria.
      - The final grid state forms the output.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify all distinct contiguous objects (groups of same-colored, adjacent pixels) for each non-white color in the input grid.
    3.  For each color present in the grid:
        a.  Count how many objects of this color consist of exactly one pixel (these are "marker pixels").
        b.  Count how many objects of this color consist of more than one pixel (these are potential "source objects").
        c.  If there is exactly one marker pixel and at least one potential source object of this color:
            i.  Identify the source object with the largest number of pixels (the "largest source object").
            ii. Find the coordinates of the single marker pixel.
            iii. Determine the bounding box of the largest source object.
            iv. Calculate the relative coordinates of each pixel within the largest source object relative to its top-left corner of the bounding box.
            v. Calculate the center position of the largest source object's bounding box.
            vi. Calculate the top-left coordinate where the copied object should be placed so that its calculated center aligns with the marker pixel's coordinates. Handle fractional centers by rounding or truncation consistently (e.g., floor).
            vii. For each pixel in the largest source object, calculate its target position in the output grid by adding its relative coordinates (from step iv) to the calculated top-left placement coordinate (from step vi).
            viii. Place the color of the source object at these target coordinates in the *output* grid, overwriting any existing pixels at those locations (including the original marker pixel).
    4.  Return the modified output grid.
```python
import numpy as np
from scipy.ndimage import label, find_objects
import math

# --- Helper Functions ---

def find_all_objects_by_color(grid):
    """
    Finds all contiguous objects (connected components including diagonals) 
    of non-background colors in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        dict: A dictionary where keys are colors (int > 0) and values are lists
              of objects. Each object is represented as a set of coordinates
              {(r1, c1), (r2, c2), ...}. Returns an empty dict if no 
              non-background objects are found.
    """
    objects_by_color = {}
    # Find unique non-background colors present in the grid
    unique_colors = np.unique(grid[grid > 0])
    if unique_colors.size == 0:
        return {} # Return empty if only background color exists

    for color in unique_colors:
        # Create a binary mask for the current color
        mask = (grid == color)
        
        # Label connected components in the mask. 
        # structure=np.ones((3,3)) ensures diagonal connectivity is considered.
        labeled_array, num_features = label(mask, structure=np.ones((3,3)))

        if num_features > 0:
            # find_objects returns a list of slices corresponding to the bounding box of each feature
            coords_slices = find_objects(labeled_array)
            color_objects = []
            
            for i in range(num_features):
                # Get the slice for the current feature (object)
                loc = coords_slices[i]
                
                # Basic validation for the slice object
                if loc is None or not isinstance(loc, tuple) or len(loc) != 2:
                    continue 
                
                # Extract the portion of the labeled array corresponding to this object's bounding box
                object_slice = labeled_array[loc]
                
                # Find the coordinates within the slice where the label matches the current feature index + 1
                obj_mask_in_slice = (object_slice == (i + 1))
                obj_coords_in_slice = np.argwhere(obj_mask_in_slice)

                # If no coordinates were found (e.g., issues with labeling), skip
                if obj_coords_in_slice.size == 0:
                    continue

                # Convert slice-relative coordinates (r, c) to absolute grid coordinates
                # by adding the starting row and column of the slice.
                obj_coords_global = set(
                    (r + loc[0].start, c + loc[1].start)
                    for r, c in obj_coords_in_slice
                )
                
                # Add the set of global coordinates for this object to the list
                if obj_coords_global: # Ensure we don't add empty sets
                    color_objects.append(obj_coords_global)
            
            # If any objects were found for this color, add them to the main dictionary
            if color_objects: 
                 objects_by_color[color] = color_objects
                 
    return objects_by_color

def get_bounding_box(obj_coords):
    """
    Calculates the bounding box (min_row, min_col, max_row, max_col) 
    for a set of object coordinates.

    Args:
        obj_coords (set): A set of (row, col) tuples representing the object's pixels.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) or None if obj_coords is empty.
    """
    if not obj_coords:
        return None
    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]
    # Return the min/max row and column values
    return (min(rows), min(cols), max(rows), max(cols))

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Identifies all distinct objects (contiguous blocks of the same color) in the input grid.
    For each color:
      - Finds objects that are single pixels ("markers").
      - Finds objects that are larger than one pixel ("potential sources").
      - If there is exactly one marker and at least one potential source of the same color:
        - Identifies the potential source object with the largest number of pixels (the "largest source object").
        - Determines the coordinates of the single marker pixel.
        - Calculates the bounding box of the largest source object.
        - Calculates the placement position for a copy of the largest source object so that its 
          calculated center (using floor division on bounding box dimensions) aligns with the marker pixel's position.
        - Places the copied object's pixels onto an output grid at the calculated positions, 
          overwriting existing pixels (including the original marker).
    Repeats this process for all applicable colors. Pixels not involved in any copy/placement 
    operation retain their original values.

    Args:
        input_grid (np.ndarray): The input grid as a 2D NumPy array.

    Returns:
        np.ndarray: The transformed grid.
    """
    # Initialize the output grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # Step 1: Find all objects in the input grid, grouped by their color
    objects_by_color = find_all_objects_by_color(input_grid)

    # Step 2: Iterate through each color found
    for color, objects in objects_by_color.items():
        markers = []
        potential_sources = []
        
        # Step 3a: Classify objects into markers (size 1) and potential sources (size > 1)
        for obj_coords in objects:
            if len(obj_coords) == 1:
                markers.append(obj_coords)
            elif len(obj_coords) > 1:
                potential_sources.append(obj_coords)

        # Step 3b: Check if the condition is met: exactly one marker and at least one source
        if len(markers) == 1 and len(potential_sources) >= 1:
            
            # Step 3c.i: Identify the single marker pixel coordinate
            # markers[0] is a set containing one tuple, e.g., {(r, c)}
            marker_coord = list(markers[0])[0] 
            marker_r, marker_c = marker_coord

            # Step 3c.i: Find the source object with the largest number of pixels
            largest_source_obj = max(potential_sources, key=len)

            # Step 3c.iii: Get the bounding box of the largest source object
            source_bbox = get_bounding_box(largest_source_obj)
            if source_bbox is None:
                continue # Should not happen if largest_source_obj is valid
            src_min_r, src_min_c, src_max_r, src_max_c = source_bbox

            # Step 3c.v & 3c.vi: Calculate placement coordinates
            # Calculate the dimensions (height, width) of the source object's bounding box
            src_height = src_max_r - src_min_r + 1
            src_width = src_max_c - src_min_c + 1

            # Calculate the offset from the top-left of the bounding box to its conceptual center.
            # Using floor ensures integer coordinates and consistent alignment.
            # This offset represents the relative coordinate (dr, dc) within the bounding box shape 
            # that should align with the marker pixel.
            center_offset_r = math.floor((src_height - 1) / 2)
            center_offset_c = math.floor((src_width - 1) / 2)

            # Calculate the target top-left corner (target_min_r, target_min_c) for placing 
            # the *bounding box* of the source object copy. This ensures that the pixel at 
            # (center_offset_r, center_offset_c) relative to this top-left corner lands 
            # exactly on the marker position (marker_r, marker_c).
            target_min_r = marker_r - center_offset_r
            target_min_c = marker_c - center_offset_c

            # Step 3c.vii & 3c.viii: Place the copied object onto the output grid
            # Iterate through each pixel coordinate (src_r, src_c) of the actual largest source object
            for src_r, src_c in largest_source_obj:
                # Calculate the pixel's relative position within its original bounding box
                relative_r = src_r - src_min_r
                relative_c = src_c - src_min_c

                # Calculate the absolute target position in the output grid by adding the
                # relative position to the calculated target top-left corner.
                target_r = target_min_r + relative_r
                target_c = target_min_c + relative_c

                # Check if the calculated target position is within the grid boundaries
                if 0 <= target_r < height and 0 <= target_c < width:
                    # If within bounds, update the output grid with the object's color
                    output_grid[target_r, target_c] = color

    # Step 4: Return the modified output grid
    return output_grid
```
```python
import numpy as np
from scipy.ndimage import label, find_objects
import math

"""
Identifies all distinct objects (contiguous blocks of the same color, including diagonals) in the input grid.
For each color:
  - Finds objects that are single pixels ("markers").
  - Finds objects that are larger than one pixel ("potential sources").
  - If there is exactly one marker and at least one potential source of the same color:
    - Identifies the potential source object with the largest number of pixels (the "largest source object").
    - Determines the coordinates of the single marker pixel.
    - Calculates the bounding box of the largest source object.
    - Calculates the conceptual center of the bounding box (using floor division on dimensions).
    - Calculates the placement position for a copy of the largest source object so that its conceptual center aligns with the marker pixel's position.
    - Iterates through ONLY the actual pixel coordinates of the largest source object. For each source pixel, calculates its corresponding target position on the output grid based on the alignment.
    - Places the source object's color at these calculated target coordinates on an output grid, overwriting existing pixels (including the original marker). Pixels within the calculated placement area but NOT part of the original source object's shape are NOT drawn.
Repeats this process for all applicable colors. Pixels not involved in any copy/placement operation retain their original values from the input grid.
"""

# --- Helper Functions ---

def find_all_objects_by_color(grid):
    """
    Finds all contiguous objects (connected components including diagonals) 
    of non-background colors in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        dict: A dictionary where keys are colors (int > 0) and values are lists
              of objects. Each object is represented as a set of coordinates
              {(r1, c1), (r2, c2), ...}. Returns an empty dict if no 
              non-background objects are found.
    """
    objects_by_color = {}
    # Find unique non-background colors present in the grid
    unique_colors = np.unique(grid[grid > 0])
    if unique_colors.size == 0:
        return {} # Return empty if only background color exists

    for color in unique_colors:
        # Create a binary mask for the current color
        mask = (grid == color)
        
        # Label connected components in the mask. 
        # structure=np.ones((3,3)) ensures diagonal connectivity is considered.
        labeled_array, num_features = label(mask, structure=np.ones((3,3)))

        if num_features > 0:
            # find_objects returns a list of slices corresponding to the bounding box of each feature
            coords_slices = find_objects(labeled_array)
            color_objects = []
            
            # Iterate through each found feature (object) for this color
            for i in range(num_features):
                # Get the slice defining the bounding box for the current feature
                loc = coords_slices[i]
                
                # Basic validation for the slice object
                if loc is None or not isinstance(loc, tuple) or len(loc) != 2:
                    continue 
                
                # Extract the portion of the labeled array corresponding to this object's bounding box
                object_slice = labeled_array[loc]
                
                # Find the coordinates *within the slice* where the label matches the current feature index + 1
                # This identifies the pixels belonging to this specific object within its bounding box
                obj_mask_in_slice = (object_slice == (i + 1))
                obj_coords_in_slice = np.argwhere(obj_mask_in_slice)

                # If no coordinates were found (e.g., issues with labeling), skip
                if obj_coords_in_slice.size == 0:
                    continue

                # Convert slice-relative coordinates (r, c) to absolute grid coordinates
                # by adding the starting row and column of the slice.
                obj_coords_global = set(
                    (r + loc[0].start, c + loc[1].start)
                    for r, c in obj_coords_in_slice
                )
                
                # Add the set of global coordinates for this object to the list
                if obj_coords_global: # Ensure we don't add empty sets
                    color_objects.append(obj_coords_global)
            
            # If any objects were found for this color, add them to the main dictionary
            if color_objects: 
                 objects_by_color[color] = color_objects
                 
    return objects_by_color

def get_bounding_box(obj_coords):
    """
    Calculates the bounding box (min_row, min_col, max_row, max_col) 
    for a set of object coordinates.

    Args:
        obj_coords (set): A set of (row, col) tuples representing the object's pixels.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) or None if obj_coords is empty.
    """
    if not obj_coords:
        return None
    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]
    # Return the min/max row and column values
    return (min(rows), min(cols), max(rows), max(cols))

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # 1. Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # 2. Identify all distinct contiguous objects for each non-white color.
    objects_by_color = find_all_objects_by_color(input_grid)

    # 3. Iterate through each color found.
    for color, objects in objects_by_color.items():
        markers = []
        potential_sources = []
        
        # 3a. Separate objects into markers (size 1) and potential sources (size > 1).
        for obj_coords in objects:
            if len(obj_coords) == 1:
                markers.append(obj_coords)
            elif len(obj_coords) > 1:
                potential_sources.append(obj_coords)

        # 3b. Check if the condition is met: exactly one marker and at least one source.
        if len(markers) == 1 and len(potential_sources) >= 1:
            
            # 3c.i. Get the coordinate of the single marker pixel.
            marker_coord = list(markers[0])[0] # markers[0] is a set like {(r, c)}
            marker_r, marker_c = marker_coord

            # 3c.ii. Find the largest source object by pixel count.
            largest_source_obj_coords = max(potential_sources, key=len)

            # 3c.iii. Determine the bounding box of the largest source object.
            source_bbox = get_bounding_box(largest_source_obj_coords)
            if source_bbox is None:
                continue # Should not happen if largest_source_obj_coords is valid
            src_min_r, src_min_c, src_max_r, src_max_c = source_bbox

            # 3c.iv. Calculate the dimensions of the source bounding box.
            src_height = src_max_r - src_min_r + 1
            src_width = src_max_c - src_min_c + 1

            # 3c.v. Calculate the center offset relative to the source bounding box's top-left.
            center_offset_r = math.floor((src_height - 1) / 2)
            center_offset_c = math.floor((src_width - 1) / 2)

            # 3c.vi. Calculate the top-left anchor coordinate for placing the object.
            # This is the coordinate where the source object's bounding box's top-left
            # would be placed so that its center aligns with the marker.
            anchor_r = marker_r - center_offset_r
            anchor_c = marker_c - center_offset_c

            # 3c.vii. Iterate through each coordinate *actually belonging* to the largest source object.
            for src_r, src_c in largest_source_obj_coords:
                # 1. Calculate the pixel's relative offset from the source bounding box's top-left.
                relative_r = src_r - src_min_r
                relative_c = src_c - src_min_c

                # 2. Calculate the final target coordinate on the output grid.
                target_r = anchor_r + relative_r
                target_c = anchor_c + relative_c

                # 3. If the target coordinate is within the grid bounds, place the color.
                if 0 <= target_r < height and 0 <= target_c < width:
                    output_grid[target_r, target_c] = color

    # 4. Return the modified output grid.
    return output_grid
```
