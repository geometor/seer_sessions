
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 0
0 1 1 1 0 2 0 2 0 0
0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 6 0 0 0 0
0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 6 0 0 0 0
0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 7 7 7 0
0 3 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 2 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 2 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0 0
4 0 4 0 0 0 0 0 0 0
4 4 4 0 0 0 8 8 8 0
3 3 3 0 0 0 8 0 8 0
3 0 3 0 0 0 8 8 8 0
3 3 3 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0 0
3 0 3 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0 0
```

Okay, let's break down this task.

**Perception**

The input grids contain multiple distinct geometric shapes, each made of a single solid color, placed on a white background. The shapes seem to generally fall into two categories: 'L' shapes and 'T' shapes (or variations thereof). The output grid isolates and retains only one specific shape from the input, while removing all others and leaving the background white. The key transformation involves identifying objects based on their shape ('T' shapes specifically) and then applying a selection criterion based on their vertical position if multiple qualifying shapes exist. The shape that is retained in the output is always the 'T' shape whose highest point is lowest on the grid compared to other 'T' shapes.

**Facts**


```yaml
Task: Shape Selection based on Type and Position

Input_Features:
  - Grid: 2D array of pixels (0-9) representing colors.
  - Background_Color: white (0).
  - Objects:
    - Composed of contiguous pixels of a single non-white color.
    - Can have different shapes and colors.
    - Shapes observed:
      - 'L' shape (or variations)
      - 'T' shape (5 pixels: a 3-pixel line segment with a 2-pixel perpendicular stem attached to the center)

Output_Features:
  - Grid: Same dimensions as input.
  - Background_Color: white (0).
  - Objects:
    - Contains at most one object from the input.
    - If an object is present, it's a 'T' shape from the input.

Transformation_Rules:
  - Identify_Objects: Find all distinct colored objects in the input grid.
  - Classify_Shapes: Determine the shape type for each identified object. Focus on identifying 'T' shapes.
  - Filter_Objects: Select only the objects classified as 'T' shapes.
  - Positional_Selection:
    - If multiple 'T' shapes are found:
      - Find the highest pixel (minimum row index) for each 'T' shape.
      - Select the 'T' shape whose highest pixel has the maximum row index (i.e., is located lowest on the grid).
    - If only one 'T' shape is found, select it.
    - If no 'T' shapes are found, select none.
  - Construct_Output:
    - Create a new grid of the same size as the input, filled with the background color (white).
    - If a 'T' shape was selected, draw it onto the new grid in its original position and color.

Relationships:
  - Input objects are filtered based on their shape ('T' shape).
  - Selection among filtered objects ('T' shapes) is based on vertical position (lowest starting point).
  - The output grid preserves the dimensions of the input grid and the position/color of the single selected object.
```


**Natural Language Program**

1.  Initialize an empty output grid with the same dimensions as the input grid, filled with the background color (white, 0).
2.  Scan the input grid to identify all distinct objects, where an object is a contiguous group of pixels of the same non-white color.
3.  For each identified object, determine if it matches the specific structure of a 'T' shape (a 5-pixel shape composed of a 3-pixel line and a 2-pixel line attached perpendicularly to the center of the 3-pixel line).
4.  Create a list of all objects identified as 'T' shapes.
5.  If the list of 'T' shapes is empty, return the initialized empty output grid.
6.  If the list contains one or more 'T' shapes, find the 'T' shape whose topmost pixel (the pixel with the minimum row index within that shape) has the maximum row index compared to the topmost pixels of all other 'T' shapes in the list. This identifies the 'T' shape that starts lowest on the grid.
7.  Take the selected 'T' shape (the lowest one) and draw its pixels (preserving their original color and coordinates) onto the initially empty output grid.
8.  Return the final output grid.
```python
import numpy as np
from collections import deque

"""
Identifies all distinct colored objects in the input grid. 
Filters these objects to find only those that match a 'T' shape pattern (5 pixels: a 3-pixel line and a 2-pixel perpendicular stem attached to the center).
If multiple 'T' shapes are found, selects the one whose highest point (minimum row index) is lowest on the grid (maximum row index).
Constructs an output grid of the same dimensions as the input, initially filled with the background color (white, 0).
Draws the selected 'T' shape (if any) onto the output grid in its original position and color.
If no 'T' shapes are found, returns the empty grid.
"""

def _get_neighbors(r, c, height, width):
    """ Helper to get valid neighbors of a cell """
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def _find_objects(grid: np.ndarray) -> list[dict]:
    """ Finds all contiguous objects of non-background color (0) """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r = r

                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    min_r = min(min_r, row) # Keep track of the topmost row

                    for nr, nc in _get_neighbors(row, col, height, width):
                        if not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                objects.append({'color': color, 'pixels': obj_pixels, 'top_row': min_r})
    
    return objects

def _is_t_shape(pixels: set) -> bool:
    """ Checks if a set of pixels forms a T-shape (5 pixels) """
    if len(pixels) != 5:
        return False

    rows = sorted([r for r, c in pixels])
    cols = sorted([c for r, c in pixels])
    
    min_r, max_r = rows[0], rows[-1]
    min_c, max_c = cols[0], cols[-1]
    
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # Check bounding box dimensions and pixel relative positions
    # Normalize coordinates relative to the top-left of the bounding box
    normalized_pixels = set((r - min_r, c - min_c) for r, c in pixels)

    # Define the 4 canonical T shapes relative to a 0,0 origin within their bounding box
    t_shapes = [
        # T (3x2)
        set([(0,0), (0,1), (0,2), (1,1), (2,1)]), # Correction: T stem is 2 pixels, shape is 3x2 or 2x3
        # Corrected T (3 wide, 2 high) - stem down
        set([(0,0), (0,1), (0,2), (1,1)]), # Missing one pixel.. let's redefine
        
        # Let's define by structure: 3 collinear, 2 collinear perpendicular from middle of the 3
        
        # Possible T shapes (relative coordinates)
        # 1. T (stem down) BBox: W=3, H=2
        set([(0,0), (0,1), (0,2), (1,1)]), # Still 4 pixels... T is 5 pixels.
        # A 3-pixel line segment with a 2-pixel perpendicular stem attached to the center pixel.

        # Canonical T shapes (5 pixels) normalized to top-left
        # T (stem down): 3 horizontal, 1 vertical from center
        # xxx
        #  x
        #  x  <-- No, stem is 2 pixels total (1 base + 1 extension)
        # xxx
        #  x
        set([(0,0), (0,1), (0,2), (1,1)]), # 4 pixels... hmm. Let's check the examples again.
        
        # Example 1: Blue T
        # (1,1), (1,3) -> (0,0), (0,2)
        # (2,1), (2,2), (2,3) -> (1,0), (1,1), (1,2)  -> This is inverted T
        # {(0,0), (0,2), (1,0), (1,1), (1,2)} normalized -> {(0,0), (0,2), (1,0), (1,1), (1,2)} NO
        # Pixels: (1,1), (1,3), (2,1), (2,2), (2,3). Color 1. Min R=1.
        # Pixels: (1,5), (1,7), (2,5), (2,6), (2,7). Color 2. Min R=1.
        # Pixels: (6,3), (6,5), (7,3), (7,4), (7,5). Color 6. Min R=6. <-- This is the one kept. Lowest top_row.

        # Let's manually define the shapes again based on example 1's magenta shape:
        # (6,3) (6,5)
        # (7,3) (7,4) (7,5)
        # Relative coords (min_r=6, min_c=3):
        # (0,0) (0,2)
        # (1,0) (1,1) (1,2)
        # This is an inverted T shape. BBox: W=3, H=2. 
        inv_t = set([(0,0), (0,2), (1,0), (1,1), (1,2)])

        # T (stem up): 3 horizontal, 1 vertical up from center
        #  x
        # xxx
        # BBox: W=3, H=2
        t_up = set([(0,1), (1,0), (1,1), (1,2)]) # Still 4.. Ah, T has 5 pixels total.
        #  x  -> (0,1)
        # xxx -> (1,0), (1,1), (1,2)
        # Plus the center pixel itself (1,1) is part of both lines.
        
        # Let's retry the definition: 5 pixels total.
        # Central pixel.
        # Two pixels extending in one direction (left/right or up/down).
        # Two pixels extending perpendicularly from the center.

        # Let's use the examples again.
        # Example 1, Blue (color 1): (1,1), (2,1), (2,2), (2,3), (1,3).  Looks like an inverted T.
        #   Relative coords (min_r=1, min_c=1): (0,0), (1,0), (1,1), (1,2), (0,2). Set: {(0,0), (0,2), (1,0), (1,1), (1,2)}. Matches inv_t.
        # Example 1, Red (color 2): (1,5), (2,5), (2,6), (2,7), (1,7). Looks like an inverted T.
        #   Relative coords (min_r=1, min_c=5): (0,0), (1,0), (1,1), (1,2), (0,2). Set: {(0,0), (0,2), (1,0), (1,1), (1,2)}. Matches inv_t.
        # Example 1, Magenta (color 6): (6,3), (7,3), (7,4), (7,5), (6,5). Looks like an inverted T.
        #   Relative coords (min_r=6, min_c=3): (0,0), (1,0), (1,1), (1,2), (0,2). Set: {(0,0), (0,2), (1,0), (1,1), (1,2)}. Matches inv_t.

        # Example 2, Green (color 3): (2,1), (2,2), (2,3), (3,1). This is 4 pixels. Not a T. (It's an L shape)
        # Example 2, Orange (color 7): (2,6), (2,7), (2,8), (3,6). 4 pixels. L shape.
        # Example 2, Azure (color 8): (5,3), (5,4), (5,5), (6,3). 4 pixels. L shape.
        # Example 2, Red (color 2): (8,7), (8,8), (8,9), (9,7). 4 pixels. L shape. --> Output is this Red L shape??
        # Output 2 is: Red shape (8,7), (8,8), (8,9), (9,7).
        # Wait, the description says T shape, but example 2 output is an L shape. Let's re-read the prompt and look at the examples again.

        # Re-evaluating Example 2:
        # Input: Green L, Orange L, Azure L, Red L.
        # Output: Only the Red L.
        # Why red L? It's the lowest one vertically based on its highest point.
        # Green L: top_row = 2
        # Orange L: top_row = 2
        # Azure L: top_row = 5
        # Red L: top_row = 8 <-- Lowest top_row.

        # Re-evaluating Example 3:
        # Input: Yellow L, Azure T, Green T.
        # Yellow L: top_row = 4
        # Azure T: (6,7),(6,9), (7,7),(7,8),(7,9). top_row = 6. Shape: Inverted T.
        # Green T: (7,0),(7,2), (8,0),(8,1),(8,2). top_row = 7. Shape: Inverted T.
        # Output: Only the Green T.
        # Why Green T? It's the lowest T shape.
        # Azure T top_row = 6
        # Green T top_row = 7 <-- Lowest T.

        # Re-evaluating Example 1:
        # Input: Blue T, Red T, Magenta T.
        # Blue T: top_row = 1
        # Red T: top_row = 1
        # Magenta T: top_row = 6
        # Output: Only Magenta T.
        # Why Magenta T? It's the lowest T shape.

        # Okay, the rule seems to be:
        # 1. Find all objects.
        # 2. Identify which objects are 'T' shapes (inverted T in the examples shown).
        # 3. If there are any 'T' shapes, select the 'T' shape whose top_row is maximum (lowest on the grid).
        # 4. If there are NO 'T' shapes, identify which objects are 'L' shapes (4 pixels).
        # 5. If there are any 'L' shapes (and no T shapes), select the 'L' shape whose top_row is maximum.
        # 6. If there are no T or L shapes, return empty grid.

        # Let's define the L shape (4 pixels) based on Example 2, Red:
        # (8,7) (8,8) (8,9)
        # (9,7)
        # Relative coords (min_r=8, min_c=7):
        # (0,0) (0,1) (0,2)
        # (1,0)
        # This is one L shape. There are 8 possible L shapes (4 rotations, 2 mirror images).
        
        # Let's redefine the helper functions:
        # `is_t_shape(pixels)` -> returns True if 5 pixels form an inverted T.
        # `is_l_shape(pixels)` -> returns True if 4 pixels form an L shape.
        # `get_shape_type(pixels)` -> returns 'T', 'L', or 'Other'.

        # Define the canonical inverted T shape (relative coords):
        inv_t_shape = set([(0,0), (0,2), (1,0), (1,1), (1,2)]) # Width=3, Height=2

        # Define the 4 rotated versions of inverted T
        # T (stem up) W=3, H=2: set([(0,1), (1,0), (1,1), (1,2)]) -- No, this is 4 pix again.
        
        # Let's simplify. Check if the shape, when normalized and potentially rotated/flipped, matches the canonical inverted T.

        # Check for inverted T specifically first, as seen in examples 1 & 3.
        if width == 3 and height == 2:
            if normalized_pixels == inv_t_shape:
                return True
        elif width == 2 and height == 3:
            # Check rotated versions
            # T (stem right)
            # x 0 -> (0,0)
            # x x -> (1,0), (1,1)
            # x 0 -> (2,0)
            # Normalized: set([(0,0), (1,0), (1,1), (2,0)]) <-- 4 pixels again.
            
            # Let's just stick to the specific inverted T seen.
            # Maybe the task only considers this specific orientation? It's common in ARC.
            
            # Okay, let's assume ONLY the inverted T counts as 'T'.
            # Bbox W=3, H=2
            if width == 3 and height == 2 and normalized_pixels == set([(0,0), (0,2), (1,0), (1,1), (1,2)]):
                 return True
            # Bbox W=2, H=3 (rotated 90 deg)
            # x x  -> (0,0), (0,1)
            # 0 x  -> (1,1)
            # 0 x  -> (2,1)
            if width == 2 and height == 3 and normalized_pixels == set([(0,0),(0,1),(1,1),(2,1)]): # 4 pixels..
                 pass # This isn't the 5 pixel T

            # Recheck Example 3 Green T: (7,0),(7,2), (8,0),(8,1),(8,2). Pixels: {(7, 0), (7, 2), (8, 0), (8, 1), (8, 2)}
            # min_r=7, max_r=8, min_c=0, max_c=2. H=2, W=3.
            # Normalized: {(0,0), (0,2), (1,0), (1,1), (1,2)}. Matches `inv_t_shape`. Okay.

            # Recheck Example 3 Azure T: (6,7),(6,9), (7,7),(7,8),(7,9). Pixels: {(6, 7), (6, 9), (7, 7), (7, 8), (7, 9)}
            # min_r=6, max_r=7, min_c=7, max_c=9. H=2, W=3.
            # Normalized: {(0,0), (0,2), (1,0), (1,1), (1,2)}. Matches `inv_t_shape`. Okay.
            
            # It seems only the inverted T shape counts.
            
            # If a shape is W=3, H=2 or W=2, H=3 and has 5 pixels, check if it matches any rotation of the base T.
            # Base T: {(0,1), (1,0), (1,1), (1,2), (2,1)}  (Stem down, W=3, H=3 - center at 1,1) No, 5 pixels.
            # Base T can be defined as center + 4 neighbors where 2 pairs are collinear.
            
            # Let's try center-based definition.
            # Find center pixel (average row/col often not integer).
            # Find centroid (median row/col)?
            rows = [r for r,c in pixels]
            cols = [c for r,c in pixels]
            center_r = sorted(rows)[2]
            center_c = sorted(cols)[2]
            center_pixel = None
            # Check if median pixel exists in the set
            if (center_r, center_c) in pixels:
                 center_pixel = (center_r, center_c)
            else: # If median is not in the set, the shape is likely asymmetric -> not a T
                 return False # Or maybe the median point isn't the geometric center for T?

            # Try bounding box center approx
            center_r_bb = min_r + (max_r - min_r) / 2
            center_c_bb = min_c + (max_c - min_c) / 2
            
            # Find pixel closest to bounding box center
            min_dist_sq = float('inf')
            potential_center = None
            for r,c in pixels:
                dist_sq = (r - center_r_bb)**2 + (c - center_c_bb)**2
                if dist_sq < min_dist_sq:
                    min_dist_sq = dist_sq
                    potential_center = (r,c)
                elif dist_sq == min_dist_sq: # Ambiguous center
                    potential_center = None # Mark as ambiguous, might not be T
                    # break # Or maybe allow multiple potential centers? Unlikely for T.
            
            if potential_center is None: return False

            pr, pc = potential_center
            neighbors = 0
            # Check neighbors relative to potential center
            has_up = (pr-1, pc) in pixels
            has_down = (pr+1, pc) in pixels
            has_left = (pr, pc-1) in pixels
            has_right = (pr, pc+1) in pixels
            
            # A T shape has the center pixel connected to 3 other pixels
            if sum([has_up, has_down, has_left, has_right]) != 3:
                 return False

            # The 3 connected neighbors must form one straight line and one perpendicular
            # Case 1: Up, Left, Right neighbors -> T shape (stem down)
            if has_up and has_left and has_right:
                # Need the 5th pixel down from the center: (pr+1, pc)
                return (pr+1, pc) in pixels # Check stem
            # Case 2: Down, Left, Right neighbors -> Inverted T shape (stem up)
            elif has_down and has_left and has_right:
                 # Need the 5th pixel up from the center: (pr-1, pc)
                 return (pr-1, pc) in pixels # Check stem
            # Case 3: Up, Down, Left neighbors -> T shape (stem right)
            elif has_up and has_down and has_left:
                 # Need the 5th pixel right from the center: (pr, pc+1)
                 return (pr, pc+1) in pixels # Check stem
            # Case 4: Up, Down, Right neighbors -> T shape (stem left)
            elif has_up and has_down and has_right:
                 # Need the 5th pixel left from the center: (pr, pc-1)
                 return (pr, pc-1) in pixels # Check stem
            else:
                 # Should not happen if neighbor count was 3
                 return False
                 
        # Fallthrough if not 5 pixels
        return False


def _is_l_shape(pixels: set) -> bool:
    """ Checks if a set of pixels forms an L-shape (4 pixels) """
    if len(pixels) != 4:
        return False
        
    rows = sorted([r for r, c in pixels])
    cols = sorted([c for r, c in pixels])
    
    min_r, max_r = rows[0], rows[-1]
    min_c, max_c = cols[0], cols[-1]
    
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # An L shape (4 pixels) has bounding box 3x2 or 2x3.
    if not ((width == 3 and height == 2) or (width == 2 and height == 3)):
        return False

    # Check for the corner pixel. An L shape has one pixel with 2 neighbors within the shape.
    corner_pixel = None
    for r, c in pixels:
        neighbor_count = 0
        # Check 4 cardinal neighbors
        if (r+1, c) in pixels: neighbor_count += 1
        if (r-1, c) in pixels: neighbor_count += 1
        if (r, c+1) in pixels: neighbor_count += 1
        if (r, c-1) in pixels: neighbor_count += 1
        
        if neighbor_count == 2:
            if corner_pixel is not None: # More than one pixel has 2 neighbors -> not L
                 return False
            corner_pixel = (r, c)
        elif neighbor_count > 2: # Not possible for L shape exterior pixels
             return False
             
    # Exactly one pixel must have 2 neighbors (the corner).
    # The other 3 pixels must have 1 neighbor within the shape.
    return corner_pixel is not None

def _get_shape_type(pixels: set) -> str:
    """ Determines if the shape is T, L, or Other """
    if _is_t_shape(pixels):
        return 'T'
    elif _is_l_shape(pixels):
        return 'L'
    else:
        return 'Other'

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Identifies T or L shapes in the input grid. 
    If T shapes exist, selects the lowest one (max top_row).
    If no T shapes exist but L shapes exist, selects the lowest L shape.
    Draws the selected shape onto an empty grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output grid with background color (0)
    output_grid = np.zeros_like(input_np, dtype=int)

    # Find all distinct objects in the grid
    objects = _find_objects(input_np)
    
    t_shapes = []
    l_shapes = []

    # Classify shapes
    for obj in objects:
        shape_type = _get_shape_type(obj['pixels'])
        if shape_type == 'T':
            t_shapes.append(obj)
        elif shape_type == 'L':
            l_shapes.append(obj)

    selected_shape = None

    # Priority 1: Find the lowest T shape
    if t_shapes:
        # Sort by top_row descending (lowest first)
        t_shapes.sort(key=lambda x: x['top_row'], reverse=True)
        selected_shape = t_shapes[0]
    # Priority 2: If no T shapes, find the lowest L shape
    elif l_shapes:
        # Sort by top_row descending (lowest first)
        l_shapes.sort(key=lambda x: x['top_row'], reverse=True)
        selected_shape = l_shapes[0]

    # Draw the selected shape onto the output grid
    if selected_shape:
        color = selected_shape['color']
        for r, c in selected_shape['pixels']:
            if 0 <= r < height and 0 <= c < width: # Bounds check just in case
                 output_grid[r, c] = color

    # Convert back to list of lists for the required output format
    return output_grid.tolist()

```
