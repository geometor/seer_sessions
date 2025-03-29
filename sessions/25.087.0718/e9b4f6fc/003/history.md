
Previous Code:
```python
import numpy as np
from collections import deque

"""
Identifies a specific target object within the input grid, characterized by a 
uniform, single-color border enclosing an interior region. Extracts this target 
object. Transforms the colors of the interior pixels based on the color of the 
border (Border Color, BC), while keeping the border pixels unchanged. The 
transformation rules depend on the BC:
- If BC=Azure(8): Swap Red(2)<->Green(3), Swap Blue(1)<->Yellow(4).
- If BC=Green(3): Blue(1)->Red(2), Gray(5)->Yellow(4), Azure(8)->Magenta(6).
- If BC=Blue(1): Yellow(4)->Red(2), Azure(8)->Green(3).
Other interior colors or colors matching the BC remain unchanged. 
The output grid contains only the transformed target object, cropped to its 
bounding box.
"""

def find_objects(grid):
    """Finds all connected components of non-background pixels."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and not visited[r, c]:
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                color = grid[r, c]
                
                while q:
                    row, col = q.popleft()
                    if grid[row, col] == color: # Only include pixels of the same color initially found
                        obj_pixels.add((row, col))
                        # Check 8 neighbors
                        for dr in [-1, 0, 1]:
                            for dc in [-1, 0, 1]:
                                if dr == 0 and dc == 0:
                                    continue
                                nr, nc = row + dr, col + dc
                                if 0 <= nr < height and 0 <= nc < width and \
                                   grid[nr, nc] != 0 and not visited[nr, nc]:
                                     # Check if neighbor has same color before adding to queue
                                     if grid[nr,nc] == color:
                                         visited[nr, nc] = True
                                         q.append((nr, nc))
                
                # Re-evaluate connectivity for multi-colored objects later
                # For now, let's group by initial color found. This might need adjustment.
                # Let's refine find_objects to find connected non-zero regions regardless of color first.
                
    # --- Revised find_objects to find connected non-zero regions ---
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and not visited[r, c]:
                current_object_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                current_object_pixels.add((r,c))

                while q:
                    row, col = q.popleft()
                    
                    # Check 8 neighbors for any non-zero color
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid[nr, nc] != 0 and not visited[nr, nc]:
                                visited[nr, nc] = True
                                current_object_pixels.add((nr, nc))
                                q.append((nr, nc))
                if current_object_pixels:
                     objects.append(current_object_pixels)
                     
    return objects

def get_bounding_box(obj_pixels):
    """Calculates the bounding box of a set of pixels."""
    if not obj_pixels:
        return None
    rows = [r for r, c in obj_pixels]
    cols = [c for r, c in obj_pixels]
    return min(rows), min(cols), max(rows), max(cols)

def find_target_object(grid):
    """Identifies the target object with a uniform border."""
    height, width = grid.shape
    objects = find_objects(grid)
    
    target_object = None
    target_border_color = -1
    target_pixels = set()
    target_bb = None

    for obj_pixels in objects:
        if not obj_pixels: continue

        min_r, min_c, max_r, max_c = get_bounding_box(obj_pixels)
        
        border_pixels = set()
        interior_pixels = set()
        potential_border_colors = set()
        
        is_candidate = True
        
        # Identify potential border and interior pixels
        for r, c in obj_pixels:
            is_on_border = False
            # Check 8 neighbors
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    # If neighbor is outside bounds or is background (0), it's a border pixel
                    if not (0 <= nr < height and 0 <= nc < width) or \
                       (0 <= nr < height and 0 <= nc < width and grid[nr, nc] == 0) or \
                       (nr < min_r or nr > max_r or nc < min_c or nc > max_c): # Consider bounding box edge
                        is_on_border = True
                        break
                    # Also check if neighbor is outside the current object pixel set
                    elif (nr, nc) not in obj_pixels:
                         is_on_border = True
                         break
                         
            if is_on_border:
                border_pixels.add((r, c))
                potential_border_colors.add(grid[r,c])
            else:
                # Check if it's truly interior (all neighbours are part of the object)
                all_neighbors_in_object = True
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                         if dr == 0 and dc == 0: continue
                         nr, nc = r + dr, c + dc
                         if not (0 <= nr < height and 0 <= nc < width) or (nr, nc) not in obj_pixels:
                             all_neighbors_in_object = False
                             break
                if all_neighbors_in_object:
                    interior_pixels.add((r, c))
                else: # It touches background or outside, so it's border
                     border_pixels.add((r, c))
                     potential_border_colors.add(grid[r,c])


        # Check conditions: uniform border color and non-empty interior
        if len(potential_border_colors) == 1 and interior_pixels:
             border_color = potential_border_colors.pop()
             # Final check: Ensure all border pixels actually have the border_color
             all_border_correct_color = all(grid[r,c] == border_color for r,c in border_pixels)
             
             if all_border_correct_color:
                 # Found the target object
                 target_object = obj_pixels
                 target_border_color = border_color
                 target_pixels = obj_pixels # Use all pixels for cropping
                 target_bb = (min_r, min_c, max_r, max_c)
                 break # Assume only one such object per input based on examples

    if target_object is None:
         # Fallback or error handling if no suitable object found
         # Based on examples, assume one always exists.
         # If this happens, the logic needs refinement.
         print("Warning: No target object found!")
         return None, -1, None, None, None

    # Refine interior/border based on the confirmed border color
    final_border_pixels = {p for p in target_pixels if grid[p] == target_border_color}
    final_interior_pixels = target_pixels - final_border_pixels
    
    # Check if the border pixels truly enclose the interior pixels
    # A simple check: ensure all interior pixels have neighbors ONLY within the target_pixels set
    truly_enclosed = True
    for r, c in final_interior_pixels:
        all_neighbors_in_obj = True
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = r + dr, c + dc
                if not (0 <= nr < height and 0 <= nc < width) or (nr, nc) not in target_pixels:
                     all_neighbors_in_obj = False
                     break
        if not all_neighbors_in_obj:
             # This interior pixel touches the outside - implies border isn't fully enclosing or is malformed
             # Reclassify this pixel as border for safety? Or is object definition wrong?
             # Let's stick with the color based separation for now.
             pass


    return target_pixels, target_border_color, target_bb, final_border_pixels, final_interior_pixels


def transform_color(original_color, border_color):
    """Applies color transformation based on border color."""
    if border_color == 8: # Azure border
        if original_color == 2: return 3 # Red -> Green
        if original_color == 3: return 2 # Green -> Red
        if original_color == 1: return 4 # Blue -> Yellow
        if original_color == 4: return 1 # Yellow -> Blue
    elif border_color == 3: # Green border
        if original_color == 1: return 2 # Blue -> Red
        if original_color == 5: return 4 # Gray -> Yellow
        if original_color == 8: return 6 # Azure -> Magenta
    elif border_color == 1: # Blue border
        if original_color == 4: return 2 # Yellow -> Red
        if original_color == 8: return 3 # Azure -> Green
        
    # If no specific rule applies, return the original color
    return original_color


def transform(input_grid):
    """
    Transforms the input grid by identifying a target object with a uniform border,
    extracting it, and applying color transformations to its interior pixels based
    on the border color.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    
    # 1. Find the target object, its border color, bounding box, and pixel sets
    target_pixels, border_color, bb, border_pixel_set, interior_pixel_set = find_target_object(input_grid_np)

    if target_pixels is None or bb is None:
        # Handle error case: Maybe return input or empty grid? 
        # Based on examples, expecting one object. Let's return empty for now.
        return np.array([[]], dtype=int) 

    min_r, min_c, max_r, max_c = bb
    
    # 2. Create the output grid based on the bounding box size
    output_height = max_r - min_r + 1
    output_width = max_c - min_c + 1
    # Initialize with background color (0), though it will be overwritten
    output_grid = np.zeros((output_height, output_width), dtype=int) 

    # 3. Populate the output grid, applying transformations
    for r_idx, r in enumerate(range(min_r, max_r + 1)):
        for c_idx, c in enumerate(range(min_c, max_c + 1)):
            # Check if the original grid coordinate (r, c) is part of the target object
            if (r, c) in target_pixels:
                original_color = input_grid_np[r, c]
                
                # 4. Check if it's an interior pixel
                if (r, c) in interior_pixel_set:
                     # Apply transformation rule
                     output_grid[r_idx, c_idx] = transform_color(original_color, border_color)
                else: 
                     # It's a border pixel (or wasn't classified as interior), keep original color
                     output_grid[r_idx, c_idx] = original_color
            # else: # If the pixel wasn't part of the object, it remains 0 (background) - cropping effect
            #    pass # Already initialized to 0

    return output_grid.tolist() # Return as list of lists
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 0 0 0
0 0 0 0 8 8 4 8 8 8 0 0 0
0 0 0 0 8 4 4 4 8 8 0 0 0
0 0 0 0 8 3 4 3 8 8 0 0 0
0 0 0 0 8 3 3 3 8 8 0 0 0
0 0 0 0 8 8 8 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
8 8 8 8 8 8
8 8 1 8 8 8
8 1 1 1 8 8
8 2 1 2 8 8
8 2 2 2 8 8
8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8
8 8 1 8 8 8
8 1 1 1 8 8
8 2 1 2 8 8
8 2 2 2 8 8
8 8 8 8 8 8
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
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 3 0 4 5 0 0
0 3 5 5 5 5 3 3 0 0 0 0 0
0 3 3 1 1 5 3 3 0 0 0 0 0
0 3 8 1 1 3 3 3 0 0 0 0 0
0 3 8 8 8 8 3 3 0 0 0 0 0
0 3 3 3 3 3 3 3 0 0 0 0 0
0 3 3 3 3 3 3 3 0 0 0 0 0
```
Expected Output:
```
3 3 3 3 3 3 3
3 4 4 4 4 3 3
3 3 2 2 4 3 3
3 6 2 2 3 3 3
3 6 6 6 6 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
```
Transformed Output:
```
3 3 3 3 3 3 3
3 4 4 4 4 3 3
3 3 2 2 4 3 3
3 6 2 2 3 3 3
3 6 6 6 6 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
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
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0
0 0 8 8 2 4 8 8 8 0 0 0 0
0 0 8 2 2 4 4 4 8 0 0 0 0
0 0 8 8 8 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
8 8 8 8 8 8 8
8 8 3 1 8 8 8
8 3 3 1 1 1 8
8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8
8 8 3 1 8 8 8
8 3 3 1 1 1 8
8 8 8 8 8 8 8
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 4:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 4 4 1 0 0 0 0 0 0 0 0
0 8 8 4 1 0 0 0 0 0 0 0 0
0 8 8 1 1 0 0 0 0 0 0 0 0
0 1 1 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
1 2 2 1
3 3 2 1
3 3 1 1
1 1 1 1
```
Transformed Output:
```

```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
Color Count Correct: False
Score: None
## General Assessment

The previous code successfully solved the first three examples but failed on the fourth. The failure occurred because the code assumed the target object must have a *uniform, single-color border*. Example 4 presented an input where the relevant object has multiple colors along its border.

The transformed output for Example 4 being empty indicates that the `find_target_object` function returned `None`, failing to identify any object meeting the strict criteria. However, comparing the input and expected output for Example 4 reveals:
1.  The output corresponds to a specific, largest connected object in the input.
2.  The color transformations applied to this object match the rules previously defined for a *Blue (1)* border, even though the actual border has multiple colors (Blue (1), Yellow (4), Azure (8)).

This suggests the core transformation logic based on a single "characteristic" color is likely correct, but the method for determining that characteristic color needs revision. Instead of requiring a uniform border, the characteristic color seems to be derived from the border pixels in a different way, potentially the *most frequent* color among the pixels adjacent to the background or grid edges.

## Strategy for Resolution

1.  **Modify Object Identification:** Remove the requirement for a uniform border color. Instead, identify all connected non-background objects and select the "target" object, likely the one with the largest pixel count.
2.  **Determine Characteristic Color:** For the selected target object, identify its "border pixels" (those adjacent to background/edge). Calculate the frequency of each color among these border pixels. The color with the highest frequency will be considered the "characteristic color" that dictates the transformation rules. Handle ties if necessary (e.g., lowest color value, though ties don't occur in the examples).
3.  **Apply Transformation:** Use the determined characteristic color and the existing `transform_color` function logic to transform *all* pixels within the target object (not just interior ones as previously interpreted, as Example 4 transforms border pixels too).
4.  **Crop and Output:** Extract the transformed target object based on its bounding box.

## Metrics and Analysis

Let's analyze each example using the new strategy.



*code_execution:*
```python
import numpy as np
from collections import Counter, deque

def find_objects(grid_np):
    """Finds all connected components of non-background pixels."""
    height, width = grid_np.shape
    visited = np.zeros_like(grid_np, dtype=bool)
    objects = []
    for r in range(height):
        for c in range(width):
            if grid_np[r, c] != 0 and not visited[r, c]:
                current_object_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                current_object_pixels.add((r, c))
                min_r, min_c, max_r, max_c = r, c, r, c

                while q:
                    row, col = q.popleft()
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 8 neighbors for any non-zero color
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid_np[nr, nc] != 0 and not visited[nr, nc]:
                                visited[nr, nc] = True
                                current_object_pixels.add((nr, nc))
                                q.append((nr, nc))
                if current_object_pixels:
                    objects.append({
                        'pixels': current_object_pixels,
                        'size': len(current_object_pixels),
                        'bb': (min_r, min_c, max_r, max_c)
                    })
    return objects

def get_border_pixels(grid_np, obj_pixels):
    """Finds pixels in obj_pixels adjacent to background (0) or grid edge."""
    height, width = grid_np.shape
    border_pixels = set()
    for r, c in obj_pixels:
        is_border = False
        # Check 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                # Check if neighbor is outside grid or is background
                if not (0 <= nr < height and 0 <= nc < width) or \
                   grid_np[nr, nc] == 0:
                    is_border = True
                    break
                # Check if neighbor is outside the object pixel set itself
                # This handles cases where object has holes or touches another object
                # Let's refine this: only consider adjacency to TRUE background (0) or edge.
        if is_border:
             border_pixels.add((r, c))
        else: # Check again specifically for adjacency to 0 or edge
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0: continue
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < height and 0 <= nc < width) or grid_np[nr, nc] == 0:
                         border_pixels.add((r,c))
                         break # Found one reason, it's a border pixel

    return border_pixels


def get_characteristic_color(grid_np, border_pixels):
    """Finds the most frequent color among border pixels."""
    if not border_pixels:
        return -1 # Or handle appropriately
    
    border_colors = [grid_np[r, c] for r, c in border_pixels]
    if not border_colors:
        return -1

    color_counts = Counter(border_colors)
    # Find the most common color, handle ties by choosing smallest color index
    most_common = sorted(color_counts.items(), key=lambda item: (-item[1], item[0]))
    return most_common[0][0]

# --- Inputs ---
inputs = [
    [[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,2,3,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,1,4,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,8,8,8,8,8,8,0,0,0],[0,0,0,0,8,8,4,8,8,8,0,0,0],[0,0,0,0,8,4,4,4,8,8,0,0,0],[0,0,0,0,8,3,4,3,8,8,0,0,0],[0,0,0,0,8,3,3,3,8,8,0,0,0],[0,0,0,0,8,8,8,8,8,8,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0]],
    [[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,6,8,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,2,1,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,3,3,3,3,3,3,3,0,4,5,0,0],[0,3,5,5,5,5,3,3,0,0,0,0,0],[0,3,3,1,1,5,3,3,0,0,0,0,0],[0,3,8,1,1,3,3,3,0,0,0,0,0],[0,3,8,8,8,8,3,3,0,0,0,0,0],[0,3,3,3,3,3,3,3,0,0,0,0,0],[0,3,3,3,3,3,3,3,0,0,0,0,0]],
    [[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,8,8,8,0,0,0,0],[0,0,8,8,2,4,8,8,8,0,0,0,0],[0,0,8,2,2,4,4,4,8,0,0,0,0],[0,0,8,8,8,8,8,8,8,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,1,4,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,3,2,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0]],
    [[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,2,4,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,1,4,4,1,0,0,0,0,0,0,0,0],[0,8,8,4,1,0,0,0,0,0,0,0,0],[0,8,8,1,1,0,0,0,0,0,0,0,0],[0,1,1,1,1,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,3,8,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0]]
]

results = []
for i, input_grid in enumerate(inputs):
    grid_np = np.array(input_grid, dtype=int)
    objects = find_objects(grid_np)
    
    if not objects:
        results.append(f"Example {i+1}: No objects found.")
        continue
        
    # Find largest object
    largest_obj = max(objects, key=lambda obj: obj['size'])
    
    # Get border pixels of the largest object
    border_pixels = get_border_pixels(grid_np, largest_obj['pixels'])
    
    # Get characteristic color
    char_color = get_characteristic_color(grid_np, border_pixels)
    
    results.append(f"Example {i+1}: Found {len(objects)} object(s). Largest object size: {largest_obj['size']}. Border pixels count: {len(border_pixels)}. Characteristic (most frequent border) color: {char_color}.")

print("\n".join(results))
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Example 1: Found 3 object(s). Largest object size: 36. Border pixels count: 20. Characteristic (most frequent border) color: 8.
Example 2: Found 4 object(s). Largest object size: 49. Border pixels count: 24. Characteristic (most frequent border) color: 3.
Example 3: Found 3 object(s). Largest object size: 28. Border pixels count: 18. Characteristic (most frequent border) color: 8.
Example 4: Found 3 object(s). Largest object size: 16. Border pixels count: 12. Characteristic (most frequent border) color: 1.

```
The code execution confirms the revised strategy:
*   It correctly identifies the largest object in each example.
*   It calculates the set of border pixels (adjacent to 0 or edge) for that largest object.
*   It determines the most frequent color among these border pixels.
*   The resulting characteristic colors (8, 3, 8, 1) perfectly match the transformation rules needed for each example (Azure, Green, Azure, Blue rules respectively).

This provides strong evidence for the updated understanding of the task.

## Facts (YAML)


```yaml
task_context:
  problem_description: "Transform the largest connected non-background object found in the input grid based on a characteristic color derived from its border."
  input_grid_description: "A 2D grid containing colored pixels (0-9), where 0 represents the background. May contain multiple distinct non-background objects."
  output_grid_description: "A 2D grid representing the transformed target object, cropped to its bounding box."

objects:
  - object_type: background
    description: "Pixels with value 0."
    properties: {}
  - object_type: non_background_component
    description: "A connected component of pixels with values 1-9. Connectivity includes diagonals (8 neighbors)."
    properties:
      - pixels: "Set of (row, col) coordinates."
      - size: "Number of pixels in the component."
      - bounding_box: "Tuple (min_row, min_col, max_row, max_col)."
      - border_pixels: "Subset of pixels adjacent (8 neighbors) to background (0) or the grid edge."
      - border_color_counts: "Frequency map of colors appearing in border_pixels."
  - object_type: target_object
    description: "The non_background_component with the largest size (pixel count)."
    properties:
      - characteristic_color: "The most frequent color among its border_pixels. Ties broken by choosing the lower color index."

actions:
  - action: FIND_OBJECTS
    description: "Identify all distinct non_background_component objects in the input grid."
    inputs: [input_grid]
    outputs: [list_of_non_background_components]
  - action: SELECT_TARGET_OBJECT
    description: "Choose the object from list_of_non_background_components with the maximum size."
    inputs: [list_of_non_background_components]
    outputs: [target_object]
  - action: DETERMINE_CHARACTERISTIC_COLOR
    description: "Identify the border_pixels of the target_object and find the most frequent color among them."
    inputs: [target_object, input_grid]
    outputs: [characteristic_color]
  - action: TRANSFORM_PIXELS
    description: "Iterate through each pixel of the target_object. Apply a color transformation based on the pixel's original color and the characteristic_color."
    inputs: [target_object, characteristic_color]
    outputs: [transformed_target_object_pixels]
    transformation_rules:
      - condition: "characteristic_color == Azure (8)"
        rules: ["Red(2) <-> Green(3)", "Blue(1) <-> Yellow(4)"]
      - condition: "characteristic_color == Green (3)"
        rules: ["Blue(1) -> Red(2)", "Gray(5) -> Yellow(4)", "Azure(8) -> Magenta(6)"]
      - condition: "characteristic_color == Blue (1)"
        rules: ["Yellow(4) -> Red(2)", "Azure(8) -> Green(3)"]
      - condition: "Otherwise"
        rules: ["Pixel color remains unchanged"]
  - action: CROP_OUTPUT
    description: "Create a new grid based on the target_object's bounding_box dimensions. Place the transformed pixels from transformed_target_object_pixels into this new grid, relative to the bounding box origin."
    inputs: [transformed_target_object_pixels, target_object.bounding_box]
    outputs: [output_grid]

```


## Natural Language Program

1.  Identify all distinct connected objects composed of non-background pixels (colors 1-9) in the input grid. Consider pixels connected if they touch horizontally, vertically, or diagonally.
2.  Select the object with the largest number of pixels as the "target object". If there's a tie in size, the selection criteria don't matter based on the examples, but a tie-breaking rule (e.g., object with the top-most, left-most bounding box corner) could be used if needed.
3.  Determine the "border pixels" of the target object. These are the pixels within the target object that are adjacent (horizontally, vertically, or diagonally) to any background pixel (color 0) or the edge of the grid.
4.  Find the "characteristic color" by identifying the color that appears most frequently among these border pixels. If there's a tie in frequency, choose the color with the lowest numerical value (though ties are not observed in the examples).
5.  Create a new output grid whose dimensions match the bounding box of the target object.
6.  Iterate through each pixel coordinate within the bounding box of the target object.
7.  For each coordinate, check if it belongs to the target object in the original input grid.
8.  If it belongs to the target object, determine its original color. Apply a color transformation based on the characteristic color found in step 4:
    *   If the characteristic color is Azure (8): Swap Red (2) and Green (3); Swap Blue (1) and Yellow (4).
    *   If the characteristic color is Green (3): Change Blue (1) to Red (2); Change Gray (5) to Yellow (4); Change Azure (8) to Magenta (6).
    *   If the characteristic color is Blue (1): Change Yellow (4) to Red (2); Change Azure (8) to Green (3).
    *   For any other characteristic color, or if the pixel's original color is not mentioned in the rules for the current characteristic color, the pixel's color remains unchanged.
9.  Place the resulting (potentially transformed) color into the corresponding position in the output grid (relative to the target object's bounding box).
10. If a coordinate within the bounding box does *not* belong to the target object (e.g., if the object is not rectangular), leave the corresponding pixel in the output grid as background (color 0) - although this doesn't happen in the examples as the target object completely fills its bounding box after transformation. The initialization to background (step 5) handles this implicitly if the object were non-rectangular *within* its bounding box.
11. The final output grid contains the cropped, transformed target object.
