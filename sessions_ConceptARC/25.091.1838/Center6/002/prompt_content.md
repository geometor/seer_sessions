
Previous Code:
```python
import numpy as np
from collections import Counter

"""
Transformation Rule:
1. Identify the background color (white, 0).
2. Find all contiguous objects not matching the background color.
3. Identify the largest object (the "main shape").
4. Find the single pixel whose color is different from both the background and the main shape's color (the "marker pixel").
5. Determine the bounding box of the main shape.
6. Calculate the geometric center coordinates of the bounding box (floor of the average row/col).
7. Create the output grid by copying the input grid.
8. Set the original location of the marker pixel to the background color in the output grid.
9. Set the calculated center location in the output grid to the color of the marker pixel.
"""

def find_objects(grid, background_color):
    """
    Finds all contiguous objects of non-background colors in the grid.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color to ignore.

    Returns:
        list: A list of tuples, where each tuple contains (color, set_of_coords).
              Returns an empty list if no objects are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                coords = set()
                stack = [(r, c)]
                visited[r, c] = True
                
                while stack:
                    row, col = stack.pop()
                    coords.add((row, col))
                    
                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            stack.append((nr, nc))
                            
                if coords:
                    objects.append((color, coords))
                    
    return objects

def get_bounding_box(object_coords):
    """
    Calculates the bounding box (min/max row/col) for a set of coordinates.

    Args:
        object_coords (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) or None if coords is empty.
    """
    if not object_coords:
        return None
        
    rows = [r for r, c in object_coords]
    cols = [c for r, c in object_coords]
    
    return (min(rows), min(cols), max(rows), max(cols))

def get_center(bounding_box):
    """
    Calculates the geometric center (floor of average) of a bounding box.

    Args:
        bounding_box (tuple): (min_row, min_col, max_row, max_col).

    Returns:
        tuple: (center_row, center_col).
    """
    min_r, min_c, max_r, max_c = bounding_box
    center_r = (min_r + max_r) // 2
    center_c = (min_c + max_c) // 2
    return (center_r, center_c)

def transform(input_grid):
    """
    Applies the transformation rule: moves a unique marker pixel to the 
    center of the largest object in the grid.

    Args:
        input_grid (np.array): The input 2D numpy array.

    Returns:
        np.array: The transformed 2D numpy array.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    # 1. Identify background color (assuming 0 based on examples)
    background_color = 0
    
    # 2. Find all non-background objects
    objects = find_objects(output_grid, background_color)
    if not objects:
        return output_grid # No objects to process

    # 3. Identify the largest object (main shape)
    largest_object = max(objects, key=lambda item: len(item[1]))
    main_shape_color, main_shape_coords = largest_object
    
    # 4. Find the unique marker pixel
    marker_color = None
    marker_location = None
    for r in range(rows):
        for c in range(cols):
            pixel_color = output_grid[r, c]
            if pixel_color != background_color and pixel_color != main_shape_color:
                # Check if this color exists elsewhere - it should be unique
                is_unique = True
                for obj_color, obj_coords in objects:
                    if obj_color == pixel_color and len(obj_coords) > 1:
                         is_unique = False
                         break
                    if obj_color == pixel_color and (r, c) not in obj_coords: # Should not happen with find_objects
                         is_unique = False
                         break
                if is_unique:
                    # Found the single pixel with a unique color
                    marker_color = pixel_color
                    marker_location = (r, c)
                    break # Assumes only one such pixel based on examples
        if marker_location:
            break

    if marker_location is None or marker_color is None:
         # Fallback or error: No unique marker pixel found, maybe logic needs adjustment for edge cases
         # Let's try finding any pixel not part of the main shape or background
         all_pixels = [(r,c) for r in range(rows) for c in range(cols)]
         non_bg_non_main_pixels = [
             (r, c) for r, c in all_pixels 
             if output_grid[r, c] != background_color and (r, c) not in main_shape_coords
         ]
         if len(non_bg_non_main_pixels) == 1:
             marker_location = non_bg_non_main_pixels[0]
             marker_color = output_grid[marker_location]
         else:
             # Still couldn't find a unique marker, return original grid or handle error
             print("Warning: Could not uniquely identify marker pixel.")
             return output_grid # Return unchanged grid if marker is ambiguous/missing


    # 5. Determine the bounding box of the main shape
    bounding_box = get_bounding_box(main_shape_coords)
    
    # 6. Calculate the geometric center of the bounding box
    target_location = get_center(bounding_box)
    
    # 8. Set the original location of the marker pixel to the background color
    output_grid[marker_location] = background_color
    
    # 9. Set the calculated center location to the color of the marker pixel
    output_grid[target_location] = marker_color
    
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 2 0 2 0 0 4 0 0
0 0 0 0 2 0 0 0 2 0 0 0 0
0 0 0 2 0 0 0 0 0 2 0 0 0
0 0 2 0 0 0 0 0 0 0 2 0 0
0 2 0 0 0 0 0 0 0 0 0 2 0
2 0 0 0 0 0 0 0 0 0 0 0 2
0 2 0 0 0 0 0 0 0 0 0 2 0
0 0 2 0 0 0 0 0 0 0 2 0 0
0 0 0 2 0 0 0 0 0 2 0 0 0
0 0 0 0 2 0 0 0 2 0 0 0 0
0 0 0 0 0 2 0 2 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 2 0 2 0 0 0 0 0
0 0 0 0 2 0 0 0 2 0 0 0 0
0 0 0 2 0 0 0 0 0 2 0 0 0
0 0 2 0 0 0 0 0 0 0 2 0 0
0 2 0 0 0 0 0 0 0 0 0 2 0
2 0 0 0 0 0 4 0 0 0 0 0 2
0 2 0 0 0 0 0 0 0 0 0 2 0
0 0 2 0 0 0 0 0 0 0 2 0 0
0 0 0 2 0 0 0 0 0 2 0 0 0
0 0 0 0 2 0 0 0 2 0 0 0 0
0 0 0 0 0 2 0 2 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 2 0 2 0 0 0 0 0
0 0 0 0 2 0 0 0 2 0 0 0 0
0 0 0 2 0 0 0 0 0 2 0 0 0
0 0 2 0 0 0 0 0 0 0 2 0 0
0 2 0 0 0 0 0 0 0 0 0 2 0
2 0 0 0 0 0 0 0 0 0 0 0 2
0 2 0 0 0 0 0 0 0 0 0 2 0
0 0 2 0 0 0 0 0 0 0 2 0 0
0 0 0 2 0 0 0 0 0 2 0 0 0
0 0 0 0 2 0 0 0 2 0 0 0 0
0 0 0 0 0 2 0 2 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 2.366863905325431

## Example 2:
Input:
```
3 3 3 3 3 3 3 3 3 3 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 7
```
Expected Output:
```
3 3 3 3 3 3 3 3 3 3 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 7 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
3 3 3 3 3 3 3 3 3 3 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 7 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 0 0 0 0 0 0 0 0 0 3 0
3 3 3 3 3 3 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0
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
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 4 4 4 4 4 4 4 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0 0 0
0 0 0 4 4 4 8 4 4 4 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0 0 0
0 0 0 4 4 4 8 4 4 4 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
