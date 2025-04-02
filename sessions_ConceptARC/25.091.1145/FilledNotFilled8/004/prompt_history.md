
## train_1

**input:**
```
0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 6 0 0 0 0 0 6 0 0 0 0
0 0 0 6 0 0 0 0 0 6 0 0 0
0 0 0 0 6 0 0 0 0 0 6 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 6 0 0 0 0 0 0 0
0 0 0 0 6 6 6 0 0 0 0 0 0
0 0 0 6 6 6 6 6 0 0 0 0 0
0 0 6 6 6 6 6 6 6 0 0 0 0
0 0 0 6 6 6 6 6 6 6 0 0 0
0 0 0 0 6 6 6 6 6 6 6 0 0
0 0 0 0 0 6 6 6 6 6 0 0 0
0 0 0 0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0
0 0 0 3 3 3 3 3 0 0 0 0
0 0 3 3 3 3 3 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 3 0 0 0 0
0 0 3 0 0 0 3 0 0 0 0 0
0 3 0 0 0 3 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down the perception and logic for this task.

## Perception of Task Elements

1.  **Input Grid Analysis:**
    *   The input grids primarily consist of a background color (`white` - 0).
    *   There is one prominent foreground color in each example (`magenta` - 6 in `train_1`, `green` - 3 in `train_2`).
    *   In `train_1`, the `magenta` pixels are sparsely distributed, forming a disconnected pattern.
    *   In `train_2`, the `green` pixels form a single, connected object – a filled diamond shape.

2.  **Output Grid Analysis:**
    *   The output grids also have a `white` background and use the same foreground color as their corresponding inputs.
    *   In `train_1`, the output shows a solid, filled `magenta` diamond shape. The original input pixels seem to lie on or within the boundary of this output diamond.
    *   In `train_2`, the output shows only the outline or perimeter of the `green` diamond shape seen in the input. The interior pixels of the input diamond have been turned `white`.

3.  **Transformation Pattern:**
    *   The task appears to involve geometric shapes, specifically diamonds aligned with the grid axes (like those defined by Manhattan distance).
    *   There seem to be two distinct modes of operation based on the input's structure:
        *   **Mode 1 (Fill/Complete):** If the input pixels are scattered points, the transformation finds the smallest diamond shape enclosing all these points and fills it completely with the input color. (`train_1` demonstrates this).
        *   **Mode 2 (Hollow/Perimeter):** If the input pixels already form a filled diamond shape, the transformation removes the interior pixels, leaving only the perimeter of the diamond in the input color. (`train_2` demonstrates this).
    *   The key is distinguishing between scattered points and a pre-filled diamond in the input.

## YAML Fact Document


```yaml
task_description: "Transforms input based on whether non-background pixels form scattered points or a filled diamond."
grid_elements:
  - type: background
    color_value: 0
    color_name: white
  - type: shape_pixels
    color_value: non-zero (e.g., 6/magenta, 3/green)
    role: defines or constitutes a diamond shape
input_patterns:
  - type: scattered_points
    description: Non-background pixels are sparse and potentially disconnected.
    example: train_1 input
  - type: filled_diamond
    description: Non-background pixels form a single connected component representing a solid diamond shape (defined by Manhattan distance from a center).
    example: train_2 input
transformations:
  - condition: input pattern is scattered_points
    action: compute and fill bounding diamond
    steps:
      - Identify the non-background color (C).
      - Find all pixels with color C (InputPixels).
      - Calculate the minimal bounding diamond (center (rc, cc), radius k) enclosing InputPixels based on Manhattan distance.
      - Generate the set of all pixels within this diamond (FilledDiamondPixels).
      - Output grid: color pixels in FilledDiamondPixels with C, others white.
  - condition: input pattern is filled_diamond
    action: extract perimeter of the diamond
    steps:
      - Identify the non-background color (C).
      - Identify the set of input pixels forming the diamond (InputPixels). (This set should match the theoretical FilledDiamondPixels calculated as above).
      - Output grid: Keep only those pixels from InputPixels that are adjacent (8-way) to at least one pixel *not* in InputPixels (i.e., background or outside the grid). Color these perimeter pixels C, others white.
relationships:
  - The output shape is directly derived from the spatial arrangement of the input's non-background pixels.
  - The transformation applied depends on the classification of the input pattern (scattered vs. filled diamond).
```


## Natural Language Program

1.  Identify the single non-`white` color (let's call it `ShapeColor`) present in the input grid. If no such color exists, return the input grid unchanged.
2.  Locate all pixels having `ShapeColor`. Let the set of their coordinates be `InputShapePixels`.
3.  Calculate the parameters (center `(rc, cc)` and radius `k`) of the smallest diamond shape (defined using Manhattan distance: `|row - rc| + |col - cc| <= k`) that perfectly encloses all coordinates in `InputShapePixels`.
    *   *Detail: Calculate center `(rc, cc)` based on the midpoint of the bounding box of `InputShapePixels`. Calculate radius `k` as the maximum Manhattan distance from `(rc, cc)` to any pixel in `InputShapePixels`.*
4.  Generate the set of all coordinates (`TheoreticalDiamondPixels`) that fall within the calculated diamond (`|row - rc| + |col - cc| <= k`).
5.  Compare the set `InputShapePixels` with the set `TheoreticalDiamondPixels`.
6.  **If** `InputShapePixels` is *not* identical to `TheoreticalDiamondPixels` (i.e., the input was scattered or incomplete):
    a. Create a new output grid of the same size, filled with `white`.
    b. For each coordinate in `TheoreticalDiamondPixels`, set the corresponding pixel in the output grid to `ShapeColor`.
7.  **Else** (i.e., `InputShapePixels` *is* identical to `TheoreticalDiamondPixels`, meaning the input was a filled diamond):
    a. Create a new output grid of the same size, filled with `white`.
    b. Iterate through each coordinate `(r, c)` in `TheoreticalDiamondPixels`.
    c. Check if `(r, c)` has at least one 8-directionally adjacent neighbor `(nr, nc)` such that `(nr, nc)` is *not* in `TheoreticalDiamondPixels` (or is outside the grid bounds).
    d. If such a neighbor exists (meaning `(r, c)` is on the perimeter), set the pixel `(r, c)` in the output grid to `ShapeColor`.
8.  Return the final output grid.
```python
import numpy as np
from typing import Tuple, Set, List

"""
This code solves ARC task a8c383ab.
The transformation identifies the non-background color pixels in the input.
It calculates the minimal bounding diamond (using Manhattan distance) that encloses all these pixels.
It then determines if the input pixels perfectly match all pixels within this theoretical diamond.
If the input pixels DO NOT match the theoretical filled diamond (e.g., they are scattered points), the output is the complete, filled diamond using the identified color.
If the input pixels DO match the theoretical filled diamond, the output is the perimeter of that diamond, keeping only the pixels that are adjacent (8-way) to a background pixel or the grid edge.
"""

def _find_shape_pixels(grid: np.ndarray) -> Tuple[int, Set[Tuple[int, int]]]:
    """Finds the non-background color and coordinates of shape pixels."""
    non_background_pixels = np.where(grid != 0)
    if len(non_background_pixels[0]) == 0:
        return 0, set()  # No shape found, return background color and empty set

    # Assume only one non-background color
    shape_color = int(grid[non_background_pixels[0][0], non_background_pixels[1][0]])
    
    pixel_coords = set(zip(non_background_pixels[0], non_background_pixels[1]))
    return shape_color, pixel_coords

def _manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    """Calculates Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def _calculate_diamond_params(pixels: Set[Tuple[int, int]]) -> Tuple[Tuple[float, float], int]:
    """Calculates the center and radius of the minimal bounding diamond."""
    if not pixels:
        return (0, 0), -1 # Indicate no pixels

    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]

    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)

    # Calculate center based on the bounding box midpoints
    center_r = (min_r + max_r) / 2.0
    center_c = (min_c + max_c) / 2.0
    center = (center_r, center_c)
    
    # Find the maximum Manhattan distance from the *integer* pixel coordinates
    # closest to the calculated center to any pixel in the set.
    # Test the four potential integer centers around the float center.
    potential_centers = [
        (int(np.floor(center_r)), int(np.floor(center_c))),
        (int(np.floor(center_r)), int(np.ceil(center_c))),
        (int(np.ceil(center_r)), int(np.floor(center_c))),
        (int(np.ceil(center_r)), int(np.ceil(center_c))),
    ]

    best_center = None
    min_max_dist = float('inf')

    # Refined approach: Find the tightest diamond.
    # The center must be the average of the extrema in row+col and row-col coordinates.
    # Let u = r + c, v = r - c
    u_coords = [r + c for r, c in pixels]
    v_coords = [r - c for r, c in pixels]
    min_u, max_u = min(u_coords), max(u_coords)
    min_v, max_v = min(v_coords), max(v_coords)
    
    # Center calculation from u,v extrema:
    # center_r + center_c = (min_u + max_u) / 2
    # center_r - center_c = (min_v + max_v) / 2
    # Adding: 2 * center_r = (min_u + max_u + min_v + max_v) / 2
    # Subtracting: 2 * center_c = (min_u + max_u - min_v - max_v) / 2
    center_r = (min_u + max_u + min_v + max_v) / 4.0
    center_c = (min_u + max_u - min_v - max_v) / 4.0
    center = (center_r, center_c)
    
    # The radius k is related to the span of u and v
    # k = max(|r - center_r| + |c - center_c|)
    # This can also be expressed as:
    radius = (max(max_u - min_u, max_v - min_v)) / 2.0

    # Find the max distance from the *closest integer coordinate* center
    # Need to handle float centers and radii carefully. Check integer grid points.
    int_center_r = round(center_r)
    int_center_c = round(center_c)
    int_center = (int_center_r, int_center_c)
    
    max_dist = 0
    for pixel in pixels:
         dist = _manhattan_distance(pixel, int_center)
         max_dist = max(max_dist, dist)

    # It's possible the true center is slightly offset, affecting radius.
    # A more robust radius calculation is needed if center is float.
    # Let's stick to the max distance from the rounded integer center for now.
    radius_k = max_dist 

    return int_center, radius_k


def _generate_diamond_pixels(center: Tuple[int, int], radius: int, grid_shape: Tuple[int, int]) -> Set[Tuple[int, int]]:
    """Generates all pixel coordinates within the diamond defined by center and radius."""
    diamond_pixels = set()
    center_r, center_c = center
    rows, cols = grid_shape
    
    # Iterate through a bounding box around the diamond
    min_r_bound = max(0, center_r - radius)
    max_r_bound = min(rows, center_r + radius + 1)
    min_c_bound = max(0, center_c - radius)
    max_c_bound = min(cols, center_c + radius + 1)

    for r in range(min_r_bound, max_r_bound):
        for c in range(min_c_bound, max_c_bound):
            if _manhattan_distance((r, c), center) <= radius:
                diamond_pixels.add((r, c))
    return diamond_pixels

def _is_perimeter(r: int, c: int, grid_shape: Tuple[int, int], diamond_pixels: Set[Tuple[int, int]]) -> bool:
    """Checks if a pixel (r, c) within the diamond is adjacent to a non-diamond pixel."""
    rows, cols = grid_shape
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue # Skip self
            
            nr, nc = r + dr, c + dc

            # Check if neighbor is outside grid bounds
            if not (0 <= nr < rows and 0 <= nc < cols):
                return True # Adjacent to edge
            
            # Check if neighbor is not part of the diamond
            if (nr, nc) not in diamond_pixels:
                return True # Adjacent to background or other shape
                
    return False # All neighbors are within the diamond

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on the diamond fill/hollow logic.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    output_np = np.zeros_like(input_np) # Initialize with background color 0

    # 1. Identify Shape Pixels
    shape_color, input_shape_pixels = _find_shape_pixels(input_np)

    if not input_shape_pixels:
        return input_grid # Return original if no shape found

    # 2. Determine Bounding Diamond Parameters
    center, radius = _calculate_diamond_params(input_shape_pixels)
    
    # Check if valid parameters were found
    if radius < 0:
         return input_grid # Should not happen if pixels were found, but safety check

    # 3. Generate Theoretical Diamond Pixels
    theoretical_diamond_pixels = _generate_diamond_pixels(center, radius, (rows, cols))

    # 4. Compare Input Pixels with Theoretical Diamond
    is_filled_diamond_input = (input_shape_pixels == theoretical_diamond_pixels)

    # 5. Apply Transformation based on comparison
    if not is_filled_diamond_input:
        # Mode 1: Fill the diamond (Input was scattered/incomplete)
        for r, c in theoretical_diamond_pixels:
             if 0 <= r < rows and 0 <= c < cols:
                 output_np[r, c] = shape_color
    else:
        # Mode 2: Hollow the diamond (Input was already a filled diamond)
        for r, c in theoretical_diamond_pixels:
             # Keep pixel if it's on the perimeter
             if _is_perimeter(r, c, (rows, cols), theoretical_diamond_pixels):
                 if 0 <= r < rows and 0 <= c < cols: # Redundant check, but safe
                     output_np[r, c] = shape_color

    return output_np.tolist()
```
```python
import numpy as np
from typing import Tuple, Set, List, Optional
import math

"""
This code solves ARC task a8c383ab.
The transformation identifies the non-background color pixels in the input grid.
It determines the parameters (center and radius) of a diamond shape based on the bounding box of these input pixels.
It then generates all pixels that would belong to a perfect diamond with these parameters.
If the set of input pixels is identical to the set of pixels in the generated theoretical diamond, the output is the perimeter (hollow diamond) of this shape.
Otherwise (if the input pixels are scattered or form an incomplete diamond), the output is the completely filled theoretical diamond.
The background color is assumed to be 0. Only one non-background color is expected per input grid.
"""

def _find_shape_pixels(grid: np.ndarray) -> Tuple[Optional[int], Set[Tuple[int, int]]]:
    """Finds the non-background color and coordinates of shape pixels."""
    # Find coordinates where the grid is not equal to the background color (0)
    non_background_indices = np.where(grid != 0)
    
    # If no non-background pixels are found, return None for color and an empty set
    if len(non_background_indices[0]) == 0:
        return None, set()

    # Extract the coordinates as a set of (row, col) tuples
    pixel_coords = set(zip(non_background_indices[0], non_background_indices[1]))
    
    # Get the color of the first non-background pixel found (assuming only one color)
    shape_color = int(grid[non_background_indices[0][0], non_background_indices[1][0]])
    
    return shape_color, pixel_coords

def _calculate_diamond_params_from_bbox(pixels: Set[Tuple[int, int]]) -> Tuple[Tuple[int, int], int]:
    """
    Calculates the center and radius of a diamond based on the bounding box of the pixels.
    Returns ((center_r, center_c), radius).
    """
    if not pixels:
        # Should not happen if called after checking for pixels, but defensive check
        return (0, 0), -1 

    # Extract row and column coordinates
    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]

    # Find the min/max row and column to define the bounding box
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)

    # Calculate the center coordinates by averaging the min/max and rounding
    # Using integer division // for robustness if sum is odd
    center_r = (min_r + max_r) // 2
    center_c = (min_c + max_c) // 2
    center = (center_r, center_c)

    # Calculate the radius based on the larger dimension of the bounding box
    # This defines the 'size' of the diamond related to the bbox extent
    # Using integer division // 2
    radius = max(max_r - min_r, max_c - min_c) // 2
    
    # Alternative center calculation: check if averaging produces .5
    # center_r_float = (min_r + max_r) / 2.0
    # center_c_float = (min_c + max_c) / 2.0
    # center_r = int(round(center_r_float)) # Round to nearest int
    # center_c = int(round(center_c_float)) # Round to nearest int
    # We use the integer division approach first as it seemed to work for examples.

    return center, radius

def _generate_diamond_pixels(center: Tuple[int, int], radius: int, grid_shape: Tuple[int, int]) -> Set[Tuple[int, int]]:
    """Generates all pixel coordinates within the diamond defined by center and radius."""
    diamond_pixels = set()
    center_r, center_c = center
    rows, cols = grid_shape
    
    # Iterate through potential pixels within the grid boundaries
    # No need to calculate tight bounds, just check distance for all grid cells
    # (Optimization possible by iterating only within bounding box of diamond)
    min_r_bound = max(0, center_r - radius)
    max_r_bound = min(rows, center_r + radius + 1)
    min_c_bound = max(0, center_c - radius)
    max_c_bound = min(cols, center_c + radius + 1)

    for r in range(min_r_bound, max_r_bound):
        for c in range(min_c_bound, max_c_bound):
            # Calculate Manhattan distance from the pixel to the center
            distance = abs(r - center_r) + abs(c - center_c)
            # If the distance is within the radius, add it to the set
            if distance <= radius:
                diamond_pixels.add((r, c))
                
    return diamond_pixels

def _is_perimeter(r: int, c: int, grid_shape: Tuple[int, int], diamond_pixels: Set[Tuple[int, int]]) -> bool:
    """Checks if a pixel (r, c) within the diamond is adjacent (8-way) to a non-diamond pixel or grid edge."""
    rows, cols = grid_shape
    # Iterate through all 8 neighbors and self (checking self is redundant but harmless)
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue # Skip self

            nr, nc = r + dr, c + dc

            # Check if the neighbor is outside the grid boundaries
            if not (0 <= nr < rows and 0 <= nc < cols):
                return True # Pixel is adjacent to the grid edge

            # Check if the neighbor is NOT part of the diamond pixel set
            if (nr, nc) not in diamond_pixels:
                return True # Pixel is adjacent to a background/non-diamond pixel

    # If none of the neighbors were outside the diamond or grid, it's an interior pixel
    return False

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on detecting a diamond shape.
    If the input perfectly matches a filled diamond derived from its bounding box,
    the output is the hollow perimeter of that diamond.
    Otherwise, the output is the filled diamond derived from the bounding box.
    """
    # Convert the input list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # Initialize the output grid with the background color (0)
    output_np = np.zeros_like(input_np)

    # 1. Find the shape's color and the coordinates of its pixels
    shape_color, input_shape_pixels = _find_shape_pixels(input_np)

    # If no shape pixels are found, return the original grid
    if shape_color is None:
        return input_grid

    # 2. Calculate the diamond parameters (center, radius) based on the bounding box
    center, radius = _calculate_diamond_params_from_bbox(input_shape_pixels)

    # If radius calculation failed (e.g., no pixels), return original grid
    if radius < 0:
         return input_grid 

    # 3. Generate the set of pixels for a theoretical perfect diamond with these parameters
    theoretical_diamond_pixels = _generate_diamond_pixels(center, radius, (rows, cols))

    # 4. Compare the actual input pixels with the theoretical diamond pixels
    is_perfect_diamond_input = (input_shape_pixels == theoretical_diamond_pixels)

    # 5. Determine the output based on whether the input was a perfect diamond
    if not is_perfect_diamond_input:
        # Mode 1: Input was scattered or incomplete. Output is the filled theoretical diamond.
        for r, c in theoretical_diamond_pixels:
             # Ensure coordinates are within grid bounds (should be, but safety check)
             if 0 <= r < rows and 0 <= c < cols:
                 output_np[r, c] = shape_color
    else:
        # Mode 2: Input was a perfect filled diamond. Output is the perimeter.
        for r, c in theoretical_diamond_pixels:
             # Check if the current pixel is on the perimeter
             if _is_perimeter(r, c, (rows, cols), theoretical_diamond_pixels):
                 # Ensure coordinates are within grid bounds
                 if 0 <= r < rows and 0 <= c < cols:
                     output_np[r, c] = shape_color

    # Convert the final NumPy array back to a list of lists and return
    return output_np.tolist()
```
