
## train_1

**input:**
```
0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 0 0 8 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 2
0 0 0 8 8 8 0 0 0 0
3 0 0 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0
```


**output:**
```
0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 0 0 6 7 8 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 8 8 2 0 0 0 2
0 0 0 8 8 8 0 0 0 0
3 0 0 3 8 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 0 0 0 0
0 0 0 0 8 8 0 0 0 0
0 0 0 0 8 8 0 0 0 0
6 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
```


**output:**
```
0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 9 8 0 0 0 0
0 0 0 0 8 8 0 0 0 0
0 0 0 0 8 8 0 0 0 0
6 0 0 0 6 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
```


## train_3

**input:**
```
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 6
3 0 0 8 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 0
2 0 0 8 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
```


**output:**
```
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 8 6 0 0 0 6
3 0 0 3 8 8 0 0 0 0
0 0 0 8 8 8 0 0 0 0
2 0 0 2 8 8 0 0 0 0
0 0 0 7 8 2 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
```

Okay, let's analyze the provided examples.

**Perception:**

1.  **Grid Structure:** Both input and output grids are 10x10.
2.  **Background Color:** The predominant background color is 'white' (0).
3.  **Central Object:** Each input grid features a central, contiguous block of 'azure' (8) pixels. The shape and size of this block vary between examples (3x5, 4x2, 5x3).
4.  **Scattered Pixels:** Outside the 'azure' block, there are several isolated, single pixels of various colors (non-'white', non-'azure'). These pixels are often located near the edges or corners of the grid.
5.  **Transformation:** The output grid is mostly identical to the input grid. The key difference is that some specific pixels within the central 'azure' block have their color changed.
6.  **Color Source:** The new colors appearing within the 'azure' block in the output correspond exactly to the colors of the scattered pixels found in the input grid.
7.  **Mechanism:** It appears that each scattered, non-'azure', non-'white' pixel "projects" its color onto the 'azure' block. The projection follows a straight horizontal or vertical line from the scattered pixel towards the 'azure' block. The path of projection seems to travel only through 'white' pixels. The first 'azure' pixel encountered along this path has its color changed to match the scattered pixel's color.
8.  **Persistence:** The original scattered pixels remain unchanged in their positions in the output grid. The 'azure' pixels that are not hit by any projection also remain unchanged.

**YAML Facts:**


```yaml
task_elements:
  - type: grid
    properties:
      size: 10x10
      background_color: 'white' (0)
  - type: object
    id: central_block
    description: A contiguous block of 'azure' (8) pixels, varying in size and position slightly near the center.
    role: target_area
  - type: object_set
    id: projector_pixels
    description: Isolated single pixels of various colors (not 'white' and not 'azure').
    location: Scattered, often near edges, outside the central_block.
    role: source_colors
relationship:
  - type: projection
    source: projector_pixels
    target: central_block
    condition: Orthogonal projection (horizontal or vertical) from a projector_pixel through only 'white' (0) pixels.
    effect: The first 'azure' (8) pixel encountered on the projection path within the central_block changes its color to match the source projector_pixel's color.
    persistence: Source projector_pixels and unaffected 'azure' pixels remain unchanged.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the largest contiguous block of 'azure' (8) pixels in the input grid.
3.  Find all pixels in the input grid that are *not* 'white' (0) and *not* part of the identified 'azure' (8) block. Call these "projector pixels".
4.  For each projector pixel located at `(row, col)` with color `C`:
    a.  Check the four orthogonal directions (up, down, left, right) starting from the pixel *adjacent* to the projector pixel.
    b.  Trace a path in each direction. Continue tracing as long as the pixels encountered are 'white' (0).
    c.  If the path stops by encountering a pixel that belongs to the 'azure' (8) block identified in step 2, located at `(target_row, target_col)`:
        i.  Modify the output grid by changing the color of the pixel at `(target_row, target_col)` to the projector pixel's color `C`.
    d.  (Assumption based on examples: Each projector pixel will successfully project onto exactly one 'azure' pixel following these rules).
5.  Return the modified output grid.
