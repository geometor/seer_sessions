```python
import numpy as np # numpy isn't used in the current code but often useful
from collections import deque

"""
The transformation identifies pairs of identical objects (anchors) based on shape 
and color within the input grid. For each anchor pair, it searches for any 
other object (source) located spatially relative to one anchor (reference). 
It then calculates the corresponding relative position for the second anchor 
(target). If an identical source object is not already present at this target 
location in the grid (specifically, if the area is background or incomplete), 
the source object is copied and pasted into that location. The pasting process 
only overwrites background pixels (color 0). This procedure is applied 
symmetrically, considering each anchor in a pair as both a potential reference 
and target.
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
        if not self.pixels:
             # Handle case of potentially finding an empty object (shouldn't happen with BFS start condition)
             self.bbox = (0, 0, -1, -1)
             self.shape = []
             self.height = 0
             self.width = 0
             self.top_left = (-1, -1)
        else:
            # Calculate bbox first
            min_r = min(r for r, c in self.pixels)
            max_r = max(r for r, c in self.pixels)
            min_c = min(c for r, c in self.pixels)
            max_c = max(c for r, c in self.pixels)
            self.bbox = (min_r, min_c, max_r, max_c)

            # Calculate dimensions
            self.height = self.bbox[2] - self.bbox[0] + 1
            self.width = self.bbox[3] - self.bbox[1] + 1
            self.top_left = (self.bbox[0], self.bbox[1])

            # Now extract shape using calculated dimensions
            self.shape = self._extract_shape(grid) # list of lists relative to bbox top-left

    def _extract_shape(self, grid):
        # Extracts the object's shape relative to its top-left corner.
        # Represents shape as a grid filled with 0 or the object's color.
        if not self.pixels:
            return []
        min_r, min_c, _, _ = self.bbox
        # Initialize shape grid with background color (0)
        shape_grid = [[0] * self.width for _ in range(self.height)]
        for r, c in self.pixels:
            # Calculate relative coordinates within the shape grid
            rel_r, rel_c = r - min_r, c - min_c
            # Ensure relative coordinates are within the bounds of the shape grid
            if 0 <= rel_r < self.height and 0 <= rel_c < self.width:
                 shape_grid[rel_r][rel_c] = self.color
        return shape_grid

    def __eq__(self, other):
        # Defines equality based on color and shape.
        if not isinstance(other, ObjectInfo):
            return NotImplemented
        return self.color == other.color and self.shape == other.shape

    def __hash__(self):
        # Allows objects to be used in sets/dictionaries based on color and shape.
        shape_tuple = tuple(tuple(row) for row in self.shape)
        return hash((self.color, shape_tuple))
    
    def __repr__(self):
        # String representation for debugging.
        return f"Object(color={self.color}, top_left={self.top_left}, shape={self.shape})"


def find_objects(grid: list[list[int]], ignore_color: int = 0) -> list[ObjectInfo]:
    """
    Finds all contiguous objects of colors other than ignore_color in the grid.
    Uses Breadth-First Search (BFS) with 8-way connectivity.
    Returns a list of ObjectInfo instances.
    """
    height = len(grid)
    width = len(grid[0])
    visited = set()
    objects = []
    
    for r in range(height):
        for c in range(width):
            # If pixel is not visited and not the ignored color, start BFS
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
                                continue # Skip self
                            nr, nc = row + dr, col + dc
                            
                            # Check bounds and if neighbor has same color and not visited
                            if 0 <= nr < height and 0 <= nc < width and \
                               (nr, nc) not in visited and grid[nr][nc] == color:
                                visited.add((nr, nc))
                                q.append((nr, nc))
                                
                # Create ObjectInfo instance if pixels were found
                if obj_pixels:
                    objects.append(ObjectInfo(color, obj_pixels, grid))
                    
    return objects

def check_if_present(grid: list[list[int]], target_top_left: tuple[int, int], 
                     source_shape: list[list[int]], source_color: int) -> bool:
    """
    Checks if an object identical to the source (shape and color) exists 
    at the target_top_left position in the grid by checking pixel values.
    Note: This checks for the *presence* of the exact pixels, not necessarily
          if it forms a complete, isolated object identical to the source.
    """
    shape_h = len(source_shape)
    if shape_h == 0: return True # An empty shape is considered present.
    shape_w = len(source_shape[0])
    grid_h = len(grid)
    grid_w = len(grid[0])
    start_r, start_c = target_top_left

    for r in range(shape_h):
        for c in range(shape_w):
            # Only check pixels that are part of the source object's shape
            if source_shape[r][c] == source_color: 
                gr, gc = start_r + r, start_c + c
                # Check bounds: if the source pixel position is outside the grid, it's not present
                if not (0 <= gr < grid_h and 0 <= gc < grid_w):
                    return False 
                # Check color match: if the grid color doesn't match, it's not present
                if grid[gr][gc] != source_color:
                    return False
                    
    # If all source pixels were found at the target location with correct color and within bounds
    return True


def paste_object(grid: list[list[int]], target_top_left: tuple[int, int], 
                 source_shape: list[list[int]], source_color: int):
    """
    Pastes the source_shape onto the grid at target_top_left.
    Only overwrites pixels with color 0 (background).
    Modifies the grid in place.
    """
    shape_h = len(source_shape)
    if shape_h == 0: return # Nothing to paste for an empty shape
    shape_w = len(source_shape[0])
    grid_h = len(grid)
    grid_w = len(grid[0])
    start_r, start_c = target_top_left

    for r in range(shape_h):
        for c in range(shape_w):
            # If the current position in the shape belongs to the object
            if source_shape[r][c] == source_color: 
                gr, gc = start_r + r, start_c + c
                # Check if the target grid coordinates are within bounds
                if 0 <= gr < grid_h and 0 <= gc < grid_w:
                    # Only overwrite if the target pixel is background (color 0)
                    if grid[gr][gc] == 0:
                        grid[gr][gc] = source_color


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    # Initialize output_grid as a deep copy of the input grid
    output_grid = [row[:] for row in input_grid]
    
    # Find all distinct objects in the input grid
    objects = find_objects(input_grid)
    
    # --- Identify pairs of identical anchor objects ---
    anchor_pairs = []
    num_objects = len(objects)
    # Use indices to avoid redundant checks and comparing an object to itself
    for i in range(num_objects):
        for j in range(i + 1, num_objects):
            # Check for identity using ObjectInfo.__eq__ (color and shape)
            # The find_objects ensures pixel sets are different if they are different objects
            if objects[i] == objects[j]: 
                 # Store the actual ObjectInfo instances
                 anchor_pairs.append((objects[i], objects[j]))

    # --- Process each anchor pair to find and potentially copy relative objects ---
    processed_sources_targets = set() # Keep track of (source_hash, target_top_left) to avoid redundant pastes

    for anchor1, anchor2 in anchor_pairs:
        # Iterate through all identified objects to check if they are 'source' objects relative to anchors
        for source_obj in objects:
            # A source object cannot be one of the anchors in the current pair
            if source_obj == anchor1: # Equality check handles both shape and color
                continue

            # -- Check relative position: anchor1 -> anchor2 --
            # Calculate relative offset of source_obj's top-left wrt anchor1's top-left
            dr1 = source_obj.top_left[0] - anchor1.top_left[0]
            dc1 = source_obj.top_left[1] - anchor1.top_left[1]
            
            # Calculate the potential target top-left position relative to anchor2
            target_r1 = anchor2.top_left[0] + dr1
            target_c1 = anchor2.top_left[1] + dc1
            target_top_left1 = (target_r1, target_c1)
            
            # Create a unique key for this potential paste operation
            paste_key1 = (hash(source_obj), target_top_left1)

            # Check if this source object is already present at the target location relative to anchor2
            # Check against the potentially modified output_grid
            # Also check if we've already processed this exact paste operation
            if paste_key1 not in processed_sources_targets and \
               not check_if_present(output_grid, target_top_left1, source_obj.shape, source_obj.color):
                 # If not present, paste the object onto the output grid
                 paste_object(output_grid, target_top_left1, source_obj.shape, source_obj.color)
                 processed_sources_targets.add(paste_key1) # Mark as processed


            # -- Check relative position: anchor2 -> anchor1 (Symmetry) --
            # Calculate relative offset of source_obj's top-left wrt anchor2's top-left
            dr2 = source_obj.top_left[0] - anchor2.top_left[0]
            dc2 = source_obj.top_left[1] - anchor2.top_left[1]

            # Calculate the potential target top-left position relative to anchor1
            target_r2 = anchor1.top_left[0] + dr2
            target_c2 = anchor1.top_left[1] + dc2
            target_top_left2 = (target_r2, target_c2)

            # Create a unique key for this potential paste operation
            paste_key2 = (hash(source_obj), target_top_left2)
            
            # Check if this source object is already present at the target location relative to anchor1
            # Check against the potentially modified output_grid
            # Also check if we've already processed this exact paste operation
            if paste_key2 not in processed_sources_targets and \
               not check_if_present(output_grid, target_top_left2, source_obj.shape, source_obj.color):
                 # If not present, paste the object onto the output grid
                 paste_object(output_grid, target_top_left2, source_obj.shape, source_obj.color)
                 processed_sources_targets.add(paste_key2) # Mark as processed

    # Return the modified grid
    return output_grid
```