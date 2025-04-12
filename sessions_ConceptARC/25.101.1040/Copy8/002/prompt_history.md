
## train_1

**input:**
```
0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 2 2 0 0 0 0 0 0 0 2 2 0 0 0
0 0 2 2 2 2 0 0 0 0 0 2 2 2 2 0 0
0 2 2 2 2 2 2 0 0 0 2 2 2 2 2 2 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 1 1 1 1 1 1 0 0 0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 4 4 4 4 4 0 4 4 4 4 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 4 4 4 4 0 4 4 4 4 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 4 4 4 4 0 4 4 4 4 4 0
0 3 0 0 0 3 0 0 0 0 0 0 0
0 0 3 0 3 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 4 4 4 4 4 0 4 4 4 4 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 4 4 4 4 0 4 4 4 4 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0
0 4 4 4 4 4 0 4 4 4 4 4 0
0 3 0 0 0 3 0 3 0 0 0 3 0
0 0 3 0 3 0 0 0 3 0 3 0 0
0 0 0 3 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples.

**Perception of Elements:**

*   **Example 1:**
    *   Input contains a red shape above a blue rectangle on the left, and just a blue rectangle on the right. The blue rectangles appear identical in shape and size. The background is white.
    *   Output retains all elements from the input and adds a copy of the red shape above the right blue rectangle. The position of the copied red shape relative to the right blue rectangle mirrors the position of the original red shape relative to the left blue rectangle.
*   **Example 2:**
    *   Input contains a yellow '8' shape above a green 'T' shape on the left, and just a yellow '8' shape on the right. The yellow '8' shapes appear identical. The background is white.
    *   Output retains all elements from the input and adds a copy of the green 'T' shape below the right yellow '8'. The position of the copied green shape relative to the right yellow '8' mirrors the position of the original green shape relative to the left yellow '8'.

**Common Pattern:**
The core idea seems to be pattern completion based on symmetry or repetition. The grid contains pairs of identical "anchor" objects (blue rectangles in Ex1, yellow '8's in Ex2). One anchor object has an associated object ("source" object - red shape in Ex1, green shape in Ex2) positioned vertically relative to it. If the other anchor object ("target" anchor) is missing this associated object in the same relative position, the source object is copied and placed there. The relative vertical and horizontal positioning between the source and anchor is preserved during the copy operation relative to the target anchor.

**YAML Fact Document:**


```yaml
task_description: Complete vertical patterns based on paired anchor objects.

elements:
  - type: grid
    description: A 2D array of pixels with integer values 0-9 representing colors.
  - type: background
    color: white (0)
    description: The default color filling empty space.
  - type: object
    description: A contiguous block of non-background colored pixels.
    properties:
      - color: The integer value (1-9) of the pixels.
      - shape: The spatial arrangement of the pixels.
      - size: The height and width of the object's bounding box.
      - position: The row and column coordinates of the object (e.g., top-left corner or bounding box).

relationships:
  - type: spatial
    description: Relative positioning between objects.
    properties:
      - above: Object A is vertically higher than Object B.
      - below: Object A is vertically lower than Object B.
      - aligned: Objects share some vertical or horizontal coordinates.
      - vertical_offset: The difference in row indices between two objects.
      - horizontal_offset: The difference in column indices between two objects.
  - type: identity
    description: Two objects being identical.
    properties:
      - same_color: Objects have the same color value.
      - same_shape: Objects have the same pixel arrangement relative to their top-left corners.
      - same_size: Objects have the same bounding box dimensions.

actions:
  - type: identify_objects
    description: Find all contiguous blocks of non-background colors.
  - type: find_pairs
    description: Identify pairs of objects that are identical (same color, shape, size) but in different locations. These are 'anchor' pairs.
  - type: find_associated_object
    description: For one anchor ('reference'), find another object ('source') positioned directly above or below it.
  - type: calculate_relative_position
    description: Determine the row and column offset between the source object and the reference anchor (e.g., top-left to top-left).
  - type: check_completion
    description: Verify if the other anchor ('target') already has an identical object in the same relative position.
  - type: copy_object
    description: Create a duplicate of the source object's pixels.
  - type: place_object
    description: Position the copied object relative to the target anchor using the calculated relative position, overwriting only background pixels.

example_1_specifics:
  - anchor_pair: Blue rectangles (color 1).
  - reference_anchor: Left blue rectangle.
  - target_anchor: Right blue rectangle.
  - source_object: Red shape (color 2).
  - relative_position: Source is above reference.
  - completion_check: Target does not have a red shape above it.
  - action: Copy red shape and place it above the target anchor.

example_2_specifics:
  - anchor_pair: Yellow '8' shapes (color 4).
  - reference_anchor: Left yellow '8'.
  - target_anchor: Right yellow '8'.
  - source_object: Green 'T' shape (color 3).
  - relative_position: Source is below reference.
  - completion_check: Target does not have a green shape below it.
  - action: Copy green shape and place it below the target anchor.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct non-background colored objects in the input grid, noting their color, shape, size, and bounding box position.
3.  Search for pairs of objects ("anchor pairs") that are identical in color, shape, and size but are located at different positions within the grid.
4.  For each identified anchor pair:
    a.  Designate one anchor as the "reference anchor" and the other as the "target anchor". (Consistency is needed, e.g., always pick the top-most or left-most as reference).
    b.  Search for a "source object" that is located immediately above or immediately below the reference anchor (potentially separated by background pixels, but vertically aligned).
    c.  If a source object is found:
        i.  Calculate the relative position (row offset, column offset) between the top-left corner of the source object's bounding box and the top-left corner of the reference anchor's bounding box.
        ii. Check if an object identical to the source object already exists in the output grid at the calculated relative position with respect to the *target* anchor's top-left corner.
        iii. If no such object exists at the target location, copy the source object's pixels and paste them onto the output grid at the calculated relative position with respect to the target anchor's top-left corner. Ensure pasting only overwrites background (white) pixels in the target area.
5.  Repeat step 4 for all identified anchor pairs and their associated source objects.
6.  Return the modified output grid.
```python
import numpy as np
from collections import deque

"""
The transformation identifies pairs of identical objects (anchors) in the input grid. 
For each anchor pair, it finds any other object (source) that is positioned 
vertically relative to one of the anchors (the reference anchor). 
If the second anchor (the target anchor) does not have an identical source object 
in the same relative position, the source object is copied and placed there. 
The placement only overwrites background pixels (color 0).
"""

class ObjectInfo:
    """
    Helper class to store information about a detected object.
    Includes color, pixel coordinates, bounding box, shape, height, and width.
    Provides equality comparison based on color and shape.
    """
    def __init__(self, color, pixels, grid):
        self.color = color
        self.pixels = set(pixels) # set of (r, c) tuples
        self.bbox = self._calculate_bbox() # (min_r, min_c, max_r, max_c)
        self.shape = self._extract_shape(grid) # list of lists relative to bbox top-left
        self.height = self.bbox[2] - self.bbox[0] + 1
        self.width = self.bbox[3] - self.bbox[1] + 1
        self.top_left = (self.bbox[0], self.bbox[1])

    def _calculate_bbox(self):
        if not self.pixels:
            return (0, 0, -1, -1) # Handle empty object case if necessary
        min_r = min(r for r, c in self.pixels)
        max_r = max(r for r, c in self.pixels)
        min_c = min(c for r, c in self.pixels)
        max_c = max(c for r, c in self.pixels)
        return (min_r, min_c, max_r, max_c)

    def _extract_shape(self, grid):
        if not self.pixels:
            return []
        min_r, min_c, _, _ = self.bbox
        shape_grid = [[0] * self.width for _ in range(self.height)]
        for r, c in self.pixels:
            # Ensure coordinates are within bounds before access
            if 0 <= r - min_r < self.height and 0 <= c - min_c < self.width:
                 shape_grid[r - min_r][c - min_c] = self.color
            # Consider adding error handling or logging if out of bounds
        return shape_grid

    def __eq__(self, other):
        if not isinstance(other, ObjectInfo):
            return NotImplemented
        # Compare based on color and shape (implicitly size)
        return self.color == other.color and self.shape == other.shape

    def __hash__(self):
        # Hash based on color and shape tuple to allow use in sets/dicts
        shape_tuple = tuple(tuple(row) for row in self.shape)
        return hash((self.color, shape_tuple))
    
    def __repr__(self):
         return f"Object(color={self.color}, top_left={self.top_left}, shape={self.shape})"


def find_objects(grid: list[list[int]], ignore_color: int = 0) -> list[ObjectInfo]:
    """
    Finds all contiguous objects of colors other than ignore_color in the grid.
    Uses Breadth-First Search (BFS).
    Returns a list of ObjectInfo instances.
    """
    height = len(grid)
    width = len(grid[0])
    visited = set()
    objects = []
    
    for r in range(height):
        for c in range(width):
            if (r, c) not in visited and grid[r][c] != ignore_color:
                color = grid[r][c]
                obj_pixels = set()
                q = deque([(r, c)])
                visited.add((r, c))
                
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    
                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            
                            if 0 <= nr < height and 0 <= nc < width and \
                               (nr, nc) not in visited and grid[nr][nc] == color:
                                visited.add((nr, nc))
                                q.append((nr, nc))
                                
                if obj_pixels:
                    objects.append(ObjectInfo(color, obj_pixels, grid))
                    
    return objects

def check_if_present(grid: list[list[int]], target_top_left: tuple[int, int], 
                     source_shape: list[list[int]], source_color: int) -> bool:
    """
    Checks if an object identical to the source (shape and color) exists 
    at the target_top_left position in the grid.
    """
    shape_h = len(source_shape)
    if shape_h == 0: return True # Empty shape is technically always present
    shape_w = len(source_shape[0])
    grid_h = len(grid)
    grid_w = len(grid[0])
    start_r, start_c = target_top_left

    for r in range(shape_h):
        for c in range(shape_w):
            if source_shape[r][c] == source_color: # Only check object pixels
                gr, gc = start_r + r, start_c + c
                # Check bounds and color match
                if not (0 <= gr < grid_h and 0 <= gc < grid_w and grid[gr][gc] == source_color):
                    return False
                
    # Check if the area contains *only* the object pixels (no extra pixels of the same color connected)
    # This might be too strict based on examples, let's omit for now and rely on the pixel match.
    # If needed, could run a mini-BFS from the target area to ensure the shape matches exactly.
                    
    return True


def paste_object(grid: list[list[int]], target_top_left: tuple[int, int], 
                 source_shape: list[list[int]], source_color: int):
    """
    Pastes the source_shape onto the grid at target_top_left.
    Only overwrites pixels with color 0 (background).
    Modifies the grid in place.
    """
    shape_h = len(source_shape)
    if shape_h == 0: return
    shape_w = len(source_shape[0])
    grid_h = len(grid)
    grid_w = len(grid[0])
    start_r, start_c = target_top_left

    for r in range(shape_h):
        for c in range(shape_w):
            if source_shape[r][c] == source_color: # If it's part of the object shape
                gr, gc = start_r + r, start_c + c
                # Check bounds before writing
                if 0 <= gr < grid_h and 0 <= gc < grid_w:
                    # Only overwrite background color
                    if grid[gr][gc] == 0:
                        grid[gr][gc] = source_color

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by finding pairs of identical anchor objects,
    identifying associated source objects relative to one anchor, and copying
    the source object to the corresponding relative position of the other anchor
    if it's missing.
    """
    # Initialize output_grid as a deep copy
    output_grid = [row[:] for row in input_grid]
    
    # Find all objects in the input grid
    objects = find_objects(input_grid)
    
    # Identify pairs of identical anchor objects
    anchor_pairs = []
    num_objects = len(objects)
    for i in range(num_objects):
        for j in range(i + 1, num_objects):
            # Check for identity using the overloaded __eq__
            # Also ensure they are not the exact same object instance (though find_objects should prevent this)
            # and that their positions are different.
            if objects[i] == objects[j] and objects[i].pixels != objects[j].pixels:
                 anchor_pairs.append((objects[i], objects[j]))

    # Process each anchor pair
    for anchor1, anchor2 in anchor_pairs:
        # Find source objects associated with anchor1
        for source_obj in objects:
            # Source must be different from the anchors
            if source_obj.pixels == anchor1.pixels or source_obj.pixels == anchor2.pixels:
                continue

            # Calculate relative position of source_obj wrt anchor1
            # Using top-left corners of bounding boxes
            dr = source_obj.top_left[0] - anchor1.top_left[0]
            dc = source_obj.top_left[1] - anchor1.top_left[1]
            
            # Calculate potential target top-left position wrt anchor2
            target_r = anchor2.top_left[0] + dr
            target_c = anchor2.top_left[1] + dc
            target_top_left = (target_r, target_c)

            # Check if the source object already exists at the target location in the *output* grid
            # Crucially check against the potentially modified output_grid
            if not check_if_present(output_grid, target_top_left, source_obj.shape, source_obj.color):
                 # If not present, paste the object onto the output grid
                 paste_object(output_grid, target_top_left, source_obj.shape, source_obj.color)

        # Find source objects associated with anchor2 (Symmetry check)
        # This ensures if the pattern exists around anchor2 but not anchor1, it gets copied too.
        for source_obj in objects:
             if source_obj.pixels == anchor1.pixels or source_obj.pixels == anchor2.pixels:
                continue
             
             dr = source_obj.top_left[0] - anchor2.top_left[0]
             dc = source_obj.top_left[1] - anchor2.top_left[1]

             target_r = anchor1.top_left[0] + dr
             target_c = anchor1.top_left[1] + dc
             target_top_left = (target_r, target_c)

             if not check_if_present(output_grid, target_top_left, source_obj.shape, source_obj.color):
                  paste_object(output_grid, target_top_left, source_obj.shape, source_obj.color)

    return output_grid
```
