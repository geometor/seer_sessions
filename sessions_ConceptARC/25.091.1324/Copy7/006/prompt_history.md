
## train_1

**input:**
```
6 3 6 6 6 6 0 7 7 7 7 7 7
6 0 3 0 0 6 0 7 0 0 0 0 7
6 0 0 3 0 6 0 7 0 0 0 0 7
6 0 0 0 3 6 0 7 0 0 0 0 7
6 0 0 0 0 3 0 7 0 0 0 0 7
6 6 6 6 6 6 0 7 7 7 7 7 7
```


**output:**
```
6 3 6 6 6 6 0 7 3 7 7 7 7
6 0 3 0 0 6 0 7 0 3 0 0 7
6 0 0 3 0 6 0 7 0 0 3 0 7
6 0 0 0 3 6 0 7 0 0 0 3 7
6 0 0 0 0 3 0 7 0 0 0 0 3
6 6 6 6 6 6 0 7 7 7 7 7 7
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
4 4 4 4 1 0 0 0 0 0
4 4 4 1 4 0 0 0 0 0
4 4 1 4 4 0 0 2 2 2
4 1 4 4 4 0 0 2 2 2
1 4 4 4 4 0 0 2 2 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
4 4 4 4 1 0 0 0 0 0
4 4 4 1 4 0 0 0 0 0
4 4 1 4 4 0 0 2 2 1
4 1 4 4 4 0 0 2 1 2
1 4 4 4 4 0 0 1 2 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples.

**Perception of the Elements:**

Both examples seem to involve two distinct primary objects or regions within the grid, separated by the background color (white, 0). In `train_1`, there's a magenta-framed region on the left and an orange-framed region on the right, separated by a white column. In `train_2`, there's a yellow/blue object on the left and a red object on the right, separated by white columns.

Within the first (left) object/region of each example, there's a "pattern" composed of pixels of a specific color that is different from the main color of the object and the background (green within magenta/white in `train_1`, blue within yellow/white in `train_2`).

The transformation appears to copy this pattern from the source (left) region to the target (right) region. The copying mechanism preserves the row position of each pattern pixel but adjusts its column position based on the horizontal shift between the two regions. The copied pattern overwrites the existing pixels in the target region, but only within the bounds of the target object/region. If the translated pattern pixel falls outside the target region's bounds, it is not drawn.

**Facts (YAML):**


```python
import numpy as np
from scipy.ndimage import label, find_objects
import copy

# COLOR_MAP is not used in the logic but helpful for visualization/debugging
COLOR_MAP = {
    0: (238, 238, 238),  # white / background
    1: (30, 147, 255),  # blue
    2: (220, 50, 40),  # red
    3: (79, 204, 48),  # green
    4: (230, 200, 0),  # yellow
    5: (85, 85, 85),  # gray
    6: (229, 58, 163),  # magenta
    7: (230, 120, 20),  # orange
    8: (135, 216, 241),  # azure
    9: (146, 18, 49),  # maroon
}

def find_objects_by_color(grid, exclude_color=0):
    """
    Finds connected components (objects) of non-excluded colors in the grid.
    Returns a list of objects, each represented as a list of (row, col) coordinates.
    """
    objects = []
    mask = grid != exclude_color
    labeled_array, num_features = label(mask) # Uses 8-connectivity by default

    if num_features == 0:
        return objects

    # Extract coordinates for each labeled object
    object_slices = find_objects(labeled_array)
    for i in range(num_features):
        obj_label = i + 1
        obj_coords = np.argwhere(labeled_array == obj_label)
        objects.append(obj_coords.tolist()) # Store as list of [row, col] pairs

    return objects

def get_object_properties(grid, obj_coords):
    """
    Calculates properties for a given object (list of coordinates).
    Returns min_row, min_col, max_row, max_col, and set of colors.
    """
    if not obj_coords:
        return None

    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    colors = set(grid[r, c] for r, c in obj_coords)

    return {
        'min_row': min_row, 'max_row': max_row,
        'min_col': min_col, 'max_col': max_col,
        'colors': colors,
        'coords': obj_coords # Keep coordinates for easy access
    }


def transform(input_grid):
    """
    Identifies two primary objects (source and target) separated horizontally by the background color (0).
    Finds a 'pattern' within the source object, defined as the pixels matching the numerically lowest non-background color present in the source object.
    Copies this pattern to the target location by translating each pattern pixel horizontally.
    The horizontal shift is determined by the difference in the minimum column index between the source and target objects.
    The copied pattern pixels overwrite the existing pixels in the output grid at the translated coordinates, provided they are within the grid bounds.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = input_np.shape
    background_color = 0

    # Find all distinct non-background objects
    # We use scipy.ndimage.label for connected components
    mask = input_np != background_color
    labeled_array, num_features = label(mask)

    if num_features < 2:
        # Need at least two objects for source and target
        return output_grid.tolist() # Return the original grid if condition not met

    # Get properties for each object and determine their horizontal order
    object_properties = []
    object_slices = find_objects(labeled_array)
    for i in range(num_features):
        obj_label = i + 1
        obj_slice = object_slices[i]
        # Extract coordinates ONLY for this object's label within its slice
        obj_coords_relative = np.argwhere(labeled_array[obj_slice] == obj_label)
        # Convert relative coordinates back to absolute grid coordinates
        obj_coords_absolute = [(r + obj_slice[0].start, c + obj_slice[1].start) for r, c in obj_coords_relative]

        if not obj_coords_absolute: continue # Should not happen if find_objects worked correctly

        props = get_object_properties(input_np, obj_coords_absolute)
        if props:
            object_properties.append(props)

    if len(object_properties) < 2:
         # Check again after potential filtering
        return output_grid.tolist()

    # Sort objects based on their minimum column index (left-to-right)
    object_properties.sort(key=lambda x: x['min_col'])

    # Assume the first is the source, the second is the target
    source_obj = object_properties[0]
    target_obj = object_properties[1]

    # Identify the pattern color in the source object
    # Rule: The pattern color is the numerically lowest color within the source object, excluding the background color.
    source_colors = source_obj['colors']
    if background_color in source_colors:
         source_colors = source_colors - {background_color} # Use set difference

    if not source_colors:
        # Source object has no non-background colors? (Shouldn't happen with current finding logic)
        return output_grid.tolist()

    pattern_color = min(source_colors)

    # Find all pixels in the source object that have the pattern color
    pattern_pixels = []
    for r, c in source_obj['coords']:
        if input_np[r, c] == pattern_color:
            pattern_pixels.append((r, c))

    # Calculate the horizontal shift required to move pattern from source to target
    # Based on the difference in the minimum column index of the two objects
    min_col_source = source_obj['min_col']
    min_col_target = target_obj['min_col']
    delta_col = min_col_target - min_col_source

    # Apply the transformation: copy pattern pixels to the target location
    for r, c in pattern_pixels:
        # Calculate the target coordinates
        target_r = r
        target_c = c + delta_col

        # Check if the target coordinates are within the grid bounds
        if 0 <= target_r < height and 0 <= target_c < width:
            # Overwrite the pixel in the output grid with the pattern color
            output_grid[target_r, target_c] = pattern_color

    # Convert back to list of lists for the final output
    return output_grid.tolist()
```
```python
"""
Transforms the input grid by identifying a source region (leftmost non-background object) and a target region (rightmost non-background object). It then identifies a "pattern color" within the source region, which is the numerically smallest color different from the most frequent color (frame color) in that region. This pattern (pixels of the pattern color) is then copied/translated horizontally from the source to the target region. The horizontal shift is determined by the difference in the minimum column indices of the two regions. The pattern pixels only overwrite pixels within the boundaries of the target region's identified coordinates.
"""

import numpy as np
from scipy.ndimage import label, find_objects
from collections import Counter
import copy

def find_regions(grid_np, background_color=0):
    """
    Finds connected regions of non-background pixels.

    Args:
        grid_np (np.array): The input grid as a NumPy array.
        background_color (int): The color value considered background.

    Returns:
        list: A list of dictionaries, where each dictionary represents a region
              and contains 'coords' (set of (row, col) tuples), 'min_col',
              'max_col', 'min_row', 'max_row'. Returns an empty list if no
              non-background regions are found.
    """
    mask = grid_np != background_color
    labeled_array, num_features = label(mask) # Default 8-connectivity

    regions = []
    if num_features == 0:
        return regions

    # Use find_objects to quickly get bounding boxes, but extract exact coords
    # object_slices = find_objects(labeled_array) # Less efficient for exact coords

    for i in range(1, num_features + 1): # Labels are 1-based
        coords_array = np.argwhere(labeled_array == i)
        if coords_array.size == 0:
            continue

        coords_set = set(tuple(coord) for coord in coords_array)
        rows = coords_array[:, 0]
        cols = coords_array[:, 1]

        regions.append({
            'coords': coords_set,
            'min_row': np.min(rows),
            'max_row': np.max(rows),
            'min_col': np.min(cols),
            'max_col': np.max(cols),
            'label': i # Keep track of the label if needed later
        })

    return regions

def get_region_colors_and_counts(grid_np, region_coords, background_color=0):
    """
    Counts the occurrences of non-background colors within a region.

    Args:
        grid_np (np.array): The grid.
        region_coords (set): A set of (row, col) tuples for the region.
        background_color (int): The background color to ignore.

    Returns:
        collections.Counter: A Counter object mapping non-background colors
                             to their counts within the region.
    """
    color_counts = Counter()
    for r, c in region_coords:
        color = grid_np[r, c]
        if color != background_color:
            color_counts[color] += 1
    return color_counts


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Initialize output grid as a copy of the input
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = input_np.shape
    background_color = 0

    # 1. Find all connected non-background regions
    regions = find_regions(input_np, background_color)

    # 2. Need at least two regions (source and target)
    if len(regions) < 2:
        return output_grid.tolist() # Return original if not enough regions

    # 3. Identify Source (leftmost) and Target (rightmost) regions
    # Sort regions by their minimum column index
    regions.sort(key=lambda r: r['min_col'])
    source_region = regions[0]
    target_region = regions[-1] # Assume rightmost is target

    # 4. Get colors and counts in the source region
    source_colors_counts = get_region_colors_and_counts(input_np, source_region['coords'], background_color)

    if not source_colors_counts:
         return output_grid.tolist() # Source region only has background? unlikely but safe

    # 5. Determine Source Frame Color (most frequent non-background color)
    # Handle cases with only one color or ties (take the first one from most_common)
    most_common = source_colors_counts.most_common(1)
    source_frame_color = most_common[0][0] if most_common else None # color value

    # 6. Determine Pattern Color (smallest non-background color != frame color)
    pattern_color = None
    sorted_unique_colors = sorted(source_colors_counts.keys())

    # Check if there's more than one unique non-bg color first
    if len(sorted_unique_colors) > 1:
        for color in sorted_unique_colors:
            if color != source_frame_color:
                pattern_color = color
                break
    # If only one color, or if loop didn't find a different one (e.g., tie logic resulted in smallest being frame), no pattern
    # OR if source_frame_color is None (only background found)
    if pattern_color is None:
         return output_grid.tolist() # No pattern color found to copy

    # 7. Find Pattern Pixels in the source region
    pattern_pixels = []
    for r, c in source_region['coords']:
        if input_np[r, c] == pattern_color:
            pattern_pixels.append((r, c))

    if not pattern_pixels:
        return output_grid.tolist() # No pixels of pattern color found

    # 8. Calculate the horizontal translation vector
    delta_col = target_region['min_col'] - source_region['min_col']

    # 9. Get target region coordinates as a set for efficient checking
    target_coords_set = target_region['coords']

    # 10. Copy pattern pixels to the target region if applicable
    for r_s, c_s in pattern_pixels:
        # Calculate potential target coordinates
        target_r = r_s
        target_c = c_s + delta_col

        # Check if target coordinate is within grid bounds
        if 0 <= target_r < height and 0 <= target_c < width:
            # Check if the target coordinate falls within the target region's pixels
            if (target_r, target_c) in target_coords_set:
                # Update the output grid
                output_grid[target_r, target_c] = pattern_color

    # Return the modified grid as a list of lists
    return output_grid.tolist()

```
```python
import numpy as np
from scipy.ndimage import label, find_objects
from collections import Counter

"""
Transforms the input grid based on the following rules:
1. Identify all connected groups of non-background (0) pixels (objects).
2. If there are fewer than two objects, return the original grid.
3. Identify the leftmost object as the source and the rightmost object as the target (based on minimum column index).
4. Determine the most frequent non-background color in the source object (frame color).
5. Determine the numerically smallest non-background color in the source object that is different from the frame color (pattern color). If none exists, return the original grid.
6. Find all pixels in the source object matching the pattern color (pattern pixels).
7. Calculate the horizontal shift required to align the start of the source object with the start of the target object.
8. Create a copy of the input grid.
9. For each pattern pixel, calculate its potential target position by applying the horizontal shift.
10. If the target position is within the grid bounds AND within the bounding box of the target object, update the copied grid at that position with the pattern color.
11. Return the modified grid.
"""

def find_regions(grid_np, background_color=0):
    """
    Finds connected regions (objects) of non-background pixels.

    Args:
        grid_np (np.array): The input grid as a NumPy array.
        background_color (int): The color value considered background.

    Returns:
        list: A list of dictionaries, where each dictionary represents a region
              and contains 'coords' (set of (row, col) tuples), 'min_col',
              'max_col', 'min_row', 'max_row'. Returns an empty list if no
              non-background regions are found.
    """
    mask = grid_np != background_color
    # Use 8-way connectivity (default for label)
    labeled_array, num_features = label(mask) 

    regions = []
    if num_features == 0:
        return regions

    # Use find_objects to get bounding slices, then extract exact coordinates
    object_slices = find_objects(labeled_array) 
    
    for i in range(num_features): # Labels are 1-based, index is 0-based
        obj_label = i + 1
        obj_slice = object_slices[i]
        
        # Extract coordinates ONLY for this object's label within its slice
        coords_relative = np.argwhere(labeled_array[obj_slice] == obj_label)
        
        # Convert relative coordinates back to absolute grid coordinates
        coords_absolute = [(r + obj_slice[0].start, c + obj_slice[1].start) for r, c in coords_relative]
        
        if not coords_absolute: 
            continue # Should not happen if find_objects worked correctly but good practice

        coords_set = set(coords_absolute)
        rows = [r for r, c in coords_absolute]
        cols = [c for r, c in coords_absolute]

        regions.append({
            'coords': coords_set,
            'min_row': np.min(rows),
            'max_row': np.max(rows),
            'min_col': np.min(cols),
            'max_col': np.max(cols),
            'label': obj_label # Keep track of the label if needed later
        })

    return regions

def get_region_colors_and_counts(grid_np, region_coords, background_color=0):
    """
    Counts the occurrences of non-background colors within a region's coordinates.

    Args:
        grid_np (np.array): The grid.
        region_coords (set): A set of (row, col) tuples for the region.
        background_color (int): The background color to ignore.

    Returns:
        collections.Counter: A Counter object mapping non-background colors
                             to their counts within the region.
    """
    color_counts = Counter()
    for r, c in region_coords:
        # Ensure coordinates are within bounds (should be, but defensive check)
        if 0 <= r < grid_np.shape[0] and 0 <= c < grid_np.shape[1]:
            color = grid_np[r, c]
            if color != background_color:
                color_counts[color] += 1
    return color_counts


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original input
    output_grid = np.copy(input_np)
    height, width = input_np.shape
    background_color = 0

    # 1. Identify all connected non-background regions (objects)
    regions = find_regions(input_np, background_color)

    # 2. Check if there are at least two objects (source and target)
    if len(regions) < 2:
        return output_grid.tolist() # Return original if not enough regions

    # 3. Identify Source (leftmost) and Target (rightmost) regions
    # Sort regions based on their minimum column index (left-to-right)
    regions.sort(key=lambda r: r['min_col'])
    source_region = regions[0]
    # Assume the one with the largest min_col is the target, even if there are > 2 objects
    target_region = regions[-1] 

    # 4. Get colors and counts in the source region
    source_colors_counts = get_region_colors_and_counts(input_np, source_region['coords'], background_color)

    # Check if the source region actually contains non-background colors
    if not source_colors_counts:
         return output_grid.tolist() 

    # 5. Determine Source Frame Color (most frequent non-background color)
    # Handle cases with only one color or ties (take the first one from most_common)
    most_common = source_colors_counts.most_common(1)
    source_frame_color = most_common[0][0] if most_common else None # color value

    # Check if a frame color was identified
    if source_frame_color is None:
         return output_grid.tolist() # Should not happen if source_colors_counts is not empty

    # 6. Determine Pattern Color (smallest non-background color != frame color)
    pattern_color = None
    # Get unique non-background colors present and sort them numerically
    sorted_unique_colors = sorted(source_colors_counts.keys())

    # Iterate through sorted colors to find the smallest one that isn't the frame color
    for color in sorted_unique_colors:
        if color != source_frame_color:
            pattern_color = color
            break # Found the smallest different color

    # If no pattern color found (e.g., only one non-bg color exists in source)
    if pattern_color is None:
         return output_grid.tolist() 

    # 7. Find Pattern Pixels in the source region
    pattern_pixels = []
    for r, c in source_region['coords']:
        # Check the color at the coordinate in the original input grid
        if input_np[r, c] == pattern_color:
            pattern_pixels.append((r, c))

    # If no pixels of the pattern color were found
    if not pattern_pixels:
        return output_grid.tolist() 

    # 8. Calculate the horizontal translation vector (difference in starting columns)
    delta_col = target_region['min_col'] - source_region['min_col']

    # 9. Get target region bounding box for efficient checking
    target_min_r, target_max_r = target_region['min_row'], target_region['max_row']
    target_min_c, target_max_c = target_region['min_col'], target_region['max_col']

    # 10. Copy pattern pixels to the target area if applicable
    for r_s, c_s in pattern_pixels:
        # Calculate potential target coordinates
        target_r = r_s
        target_c = c_s + delta_col

        # Check if target coordinate is within the overall grid bounds
        if 0 <= target_r < height and 0 <= target_c < width:
            # Check if the target coordinate falls within the target region's BOUNDING BOX
            if target_min_r <= target_r <= target_max_r and \
               target_min_c <= target_c <= target_max_c:
                # Update the output grid with the pattern color, overwriting original
                output_grid[target_r, target_c] = pattern_color

    # Return the modified grid as a standard Python list of lists
    return output_grid.tolist()
```
