
Previous Code:
```python
import numpy as np

"""
Identifies 5x5 square objects in the input grid, characterized by a 1-pixel thick frame of either Azure (8) or Red (2) and a 3x3 filled center of a different color.
The transformation rule translates these objects horizontally based on their frame color:
- Objects with an Azure (8) frame are shifted left by 1 column.
- Objects with a Red (2) frame are shifted right by 5 columns.
The output grid is initialized with the background color of the input, and then the translated objects are drawn onto it, preserving their original frame and center colors. Pixels moved outside the grid boundaries are clipped.
"""

def find_objects(input_grid, background_color):
    """
    Finds all 5x5 frame/center objects in the grid.
    """
    objects = []
    height, width = input_grid.shape
    visited = np.zeros_like(input_grid, dtype=bool) # Keep track of visited pixels to avoid re-identifying parts of objects

    for r in range(height - 4):
        for c in range(width - 4):
            if visited[r, c]:
                continue

            # Check if the top-left pixel could be the start of an Azure or Red frame
            potential_frame_color = input_grid[r, c]
            if potential_frame_color != 8 and potential_frame_color != 2:
                continue
            
            # Check if the 5x5 area matches the expected pattern
            is_object = True
            potential_center_color = -1 # Initialize center color

            for i in range(5):
                for j in range(5):
                    current_r, current_c = r + i, c + j
                    
                    # Frame check
                    if i == 0 or i == 4 or j == 0 or j == 4:
                        if input_grid[current_r, current_c] != potential_frame_color:
                            is_object = False
                            break
                    # Center check
                    else:
                        if potential_center_color == -1:
                           potential_center_color = input_grid[current_r, current_c]
                           # Center color should not be the same as frame or background
                           if potential_center_color == potential_frame_color or potential_center_color == background_color:
                               is_object = False
                               break
                        elif input_grid[current_r, current_c] != potential_center_color:
                            is_object = False
                            break
                if not is_object:
                    break
            
            # If a valid 5x5 object is found
            if is_object and potential_center_color != -1:
                objects.append({
                    'top_left': (r, c),
                    'frame_color': potential_frame_color,
                    'center_color': potential_center_color
                })
                # Mark the area as visited
                visited[r:r+5, c:c+5] = True

    return objects

def draw_object(output_grid, top_left, frame_color, center_color):
    """
    Draws a 5x5 object at the specified top_left coordinates on the output grid.
    Handles boundary clipping.
    """
    new_r, new_c = top_left
    height, width = output_grid.shape

    for i in range(5):
        for j in range(5):
            tr, tc = new_r + i, new_c + j

            # Check grid boundaries
            if 0 <= tr < height and 0 <= tc < width:
                # Determine if it's a frame or center pixel
                if i == 0 or i == 4 or j == 0 or j == 4:
                    output_grid[tr, tc] = frame_color
                else:
                    output_grid[tr, tc] = center_color

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape

    # Determine background color (assuming it's the color at 0,0)
    background_color = input_grid[0, 0]

    # Initialize output grid with background color
    output_grid = np.full_like(input_grid, background_color)

    # Find all relevant objects in the input grid
    objects = find_objects(input_grid, background_color)

    # Translate and draw each object onto the output grid
    for obj in objects:
        r, c = obj['top_left']
        frame_color = obj['frame_color']
        center_color = obj['center_color']
        
        new_r = r # Row remains the same
        new_c = c # Initialize new column with old column

        # Apply translation based on frame color
        if frame_color == 8: # Azure
            new_c = c - 1
        elif frame_color == 2: # Red
            new_c = c + 5
            
        # Draw the translated object onto the output grid
        draw_object(output_grid, (new_r, new_c), frame_color, center_color)

    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 5 5 5 8 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 8 5 5 5 8 0 0 0 2 1 1 1 2 0 8 8 8 8 8 0 0
0 8 5 5 5 8 0 0 0 2 1 1 1 2 0 8 3 3 3 8 0 0
0 8 8 8 8 8 0 0 0 2 1 1 1 2 0 8 3 3 3 8 0 0
0 0 0 0 0 0 0 0 0 2 2 2 2 2 0 8 3 3 3 8 0 0
0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 0 0 2 3 3 3 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 3 3 3 2 0 0 0 0 2 2 2 2 2 0 0 0 0
0 0 0 0 2 3 3 3 2 0 0 0 0 2 9 9 9 2 0 0 0 0
0 0 0 0 2 2 2 2 2 0 0 0 0 2 9 9 9 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 2 9 9 9 2 0 0 0 0
2 2 2 2 2 0 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0
2 6 6 6 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 6 6 6 2 0 0 0 0 0 0 0 8 8 8 8 8 0 0 0 0 0
2 6 6 6 2 2 2 2 2 2 0 0 8 4 4 4 8 0 0 0 0 0
2 2 2 2 2 2 4 4 4 2 0 0 8 4 4 4 8 0 0 0 0 0
0 0 0 0 0 2 4 4 4 2 0 0 8 4 4 4 8 0 0 0 0 0
0 0 0 0 0 2 4 4 4 2 0 0 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 5 5 5 8 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2
8 5 5 5 8 8 8 8 8 8 0 0 0 0 0 0 0 2 1 1 1 2
8 5 5 5 8 8 3 3 3 8 0 0 0 0 0 0 0 2 1 1 1 2
8 8 8 8 8 8 3 3 3 8 0 0 0 0 0 0 0 2 1 1 1 2
0 0 0 0 0 8 3 3 3 8 0 0 0 0 0 0 0 2 2 2 2 2
0 0 0 0 0 8 8 8 8 8 0 0 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 2 2 9 9 9 2
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 9 9 9 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 9 9 9 2
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 2 6 6 6 2 0 0 0 0 0
8 8 8 8 8 0 0 0 0 0 0 0 2 6 6 6 2 0 0 0 0 0
8 4 4 4 8 0 0 0 0 0 0 0 2 6 6 6 2 2 2 2 2 2
8 4 4 4 8 0 0 0 0 0 0 0 2 2 2 2 2 2 4 4 4 2
8 4 4 4 8 0 0 0 0 0 0 0 0 0 0 0 0 2 4 4 4 2
8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 2 4 4 4 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 5 5 5 8 0 0 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0
8 5 5 5 8 0 0 0 0 0 0 0 0 0 8 8 8 8 8 0 0 0
8 5 5 5 8 0 0 0 0 0 0 0 0 0 8 3 3 3 8 0 0 0
8 8 8 8 8 0 0 0 0 0 0 0 0 0 8 3 3 3 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 3 3 3 8 0 0 0
0 0 0 0 0 0 0 0 0 2 2 2 2 2 8 8 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 2 3 3 3 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 3 3 3 2 0 0 0 0 2 2 2 2
0 0 0 0 0 0 0 0 0 2 3 3 3 2 0 0 0 0 2 9 9 9
0 0 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0 2 9 9 9
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 9 9 9
0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 2 2 2 2
0 0 0 0 0 2 6 6 6 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 6 6 6 2 0 8 8 8 8 8 0 0 0 0 0 0
0 0 0 0 0 2 6 6 6 2 2 2 2 2 2 8 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 2 4 4 4 2 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 4 4 4 2 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 4 4 4 2 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 231
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 95.45454545454545

## Example 2:
Input:
```
4 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 2 5 5 5 2 4 4 4 4 4 4 4 4 4
4 4 8 8 8 8 8 4 2 5 5 5 2 4 2 2 2 2 2 4 4 4
4 4 8 9 9 9 8 4 2 5 5 5 2 4 2 3 3 3 2 4 4 4
4 4 8 9 9 9 8 4 2 2 2 2 2 4 2 3 3 3 2 4 4 4
4 4 8 9 9 9 8 4 4 4 4 4 4 4 2 3 3 3 2 4 4 4
4 4 8 8 8 8 8 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 4
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2 4
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2 4
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2 4
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 8 8 8 8 8 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4
4 4 8 1 1 1 8 4 4 4 4 4 4 4 2 1 1 1 2 4 4 4
4 4 8 1 1 1 8 4 8 8 8 8 8 4 2 1 1 1 2 4 4 4
4 4 8 1 1 1 8 4 8 6 6 6 8 4 2 1 1 1 2 4 4 4
4 4 8 8 8 8 8 4 8 6 6 6 8 4 2 2 2 2 2 4 4 4
4 4 4 4 4 4 4 4 8 6 6 6 8 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 8 8 8 8 8 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Expected Output:
```
4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 2 5 5 5 2 4 4 4 4 4
8 8 8 8 8 4 4 4 4 4 4 4 2 5 5 5 2 2 2 2 2 2
8 9 9 9 8 4 4 4 4 4 4 4 2 5 5 5 2 2 3 3 3 2
8 9 9 9 8 4 4 4 4 4 4 4 2 2 2 2 2 2 3 3 3 2
8 9 9 9 8 4 4 4 4 4 4 4 4 4 4 4 4 2 3 3 3 2
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
8 1 1 1 8 4 4 4 4 4 4 4 4 4 4 4 4 2 1 1 1 2
8 1 1 1 8 8 8 8 8 8 4 4 4 4 4 4 4 2 1 1 1 2
8 1 1 1 8 8 6 6 6 8 4 4 4 4 4 4 4 2 1 1 1 2
8 8 8 8 8 8 6 6 6 8 4 4 4 4 4 4 4 2 2 2 2 2
4 4 4 4 4 8 6 6 6 8 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Transformed Output:
```
4 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 2 5 5 5 2 4 4 4 4
4 8 8 8 8 8 4 4 4 4 4 4 4 2 5 5 5 2 4 2 2 2
4 8 9 9 9 8 4 4 4 4 4 4 4 2 5 5 5 2 4 2 3 3
4 8 9 9 9 8 4 4 4 4 4 4 4 2 2 2 2 2 4 2 3 3
4 8 9 9 9 8 4 4 4 4 4 4 4 4 4 4 4 4 4 2 3 3
4 8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 2
3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 2
3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 2
3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 2
8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 2
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2
4 8 1 1 1 8 4 4 4 4 4 4 4 4 4 4 4 4 4 2 1 1
4 8 1 1 1 8 4 8 8 8 8 8 4 4 4 4 4 4 4 2 1 1
4 8 1 1 1 8 4 8 6 6 6 8 4 4 4 4 4 4 4 2 1 1
4 8 8 8 8 8 4 8 6 6 6 8 4 4 4 4 4 4 4 2 2 2
4 4 4 4 4 4 4 8 6 6 6 8 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 8 8 8 8 8 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Match: False
Pixels Off: 125
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 51.652892561983464

## Example 3:
Input:
```
1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 1 1 1 1 1
1 1 1 8 8 8 8 8 1 1 1 1 2 3 3 3 2 1 1 1 1 1
1 1 1 8 2 2 2 8 1 1 1 1 2 3 3 3 2 1 1 1 1 1
1 1 1 8 2 2 2 8 1 1 1 1 2 3 3 3 2 1 1 1 1 1
1 1 1 8 2 2 2 8 1 1 1 1 2 2 2 2 2 1 1 1 1 1
1 1 1 8 8 8 8 8 1 1 1 1 8 8 8 8 8 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 8 6 6 6 8 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 8 6 6 6 8 1 1 1 1 1
1 1 2 2 2 2 2 1 1 1 1 1 8 6 6 6 8 1 1 1 1 1
1 1 2 5 5 5 2 1 1 1 1 1 8 8 8 8 8 1 1 1 1 1
1 1 2 5 5 5 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 2 5 5 5 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 2 2 2 2 2 1 1 1 1 1 1 1 2 2 2 2 2 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 2 1 1 1
1 1 1 1 1 1 1 8 8 8 8 8 1 1 2 4 4 4 2 1 1 1
1 1 1 1 1 1 1 8 3 3 3 8 1 1 2 4 4 4 2 1 1 1
1 1 1 1 1 1 1 8 3 3 3 8 1 1 2 2 2 2 2 1 1 1
1 1 1 1 1 1 1 8 3 3 3 8 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Expected Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 2 3 3 3 2
8 2 2 2 8 1 1 1 1 1 1 1 1 1 1 1 1 2 3 3 3 2
8 2 2 2 8 1 1 1 1 1 1 1 1 1 1 1 1 2 3 3 3 2
8 2 2 2 8 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
8 8 8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 8 6 6 6 8 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 8 6 6 6 8 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 8 6 6 6 8 1 1 2 2 2 2 2 1 1 1 1 1
1 1 1 1 1 8 8 8 8 8 1 1 2 5 5 5 2 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 2 5 5 5 2 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 2 5 5 5 2 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 2
8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 2
8 3 3 3 8 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 2
8 3 3 3 8 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
8 3 3 3 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Transformed Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
1 1 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 2 3 3 3 2
1 1 8 2 2 2 8 1 1 1 1 1 1 1 1 1 1 2 3 3 3 2
1 1 8 2 2 2 8 1 1 1 1 1 1 1 1 1 1 2 3 3 3 2
1 1 8 2 2 2 8 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
1 1 8 8 8 8 8 1 1 1 1 8 8 8 8 8 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 8 6 6 6 8 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 8 6 6 6 8 1 1 1 1 1 1
1 1 1 1 1 1 1 2 2 2 2 2 6 6 6 8 1 1 1 1 1 1
1 1 1 1 1 1 1 2 5 5 5 2 8 8 8 8 1 1 1 1 1 1
1 1 1 1 1 1 1 2 5 5 5 2 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 2 5 5 5 2 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 2 2 2 2 2 1 1 1 1 1 1 1 2 2 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4
1 1 1 1 1 1 8 8 8 8 8 1 1 1 1 1 1 1 1 2 4 4
1 1 1 1 1 1 8 3 3 3 8 1 1 1 1 1 1 1 1 2 4 4
1 1 1 1 1 1 8 3 3 3 8 1 1 1 1 1 1 1 1 2 2 2
1 1 1 1 1 1 8 3 3 3 8 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Match: False
Pixels Off: 172
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 71.07438016528926
