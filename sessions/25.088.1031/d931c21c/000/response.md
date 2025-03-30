**Perception of Task Elements:**

1.  **Input/Output:** Both are grids of pixels with colors represented by integers 0-9. The primary colors involved are white (0), blue (1), red (2), and green (3).
2.  **Objects:** The salient objects in the input grids are shapes formed by contiguous blue (1) pixels against a white (0) background. These shapes vary in form (rectangles, L-shapes, more complex structures) and can be hollow or solid.
3.  **Transformation:** The core transformation involves identifying specific blue shapes and modifying the pixels inside and immediately outside them.
    *   Shapes that fully enclose a region of white (0) pixels are targeted.
    *   The enclosed white pixels are changed to green (3).
    *   The white pixels immediately adjacent (8-way connectivity) to the *outside* of the enclosing blue shape are changed to red (2).
4.  **Conditionality:** The transformation is conditional. It only applies to blue shapes that form a complete enclosure. Blue shapes that do not enclose a white area (like open shapes or solid shapes) remain unchanged, along with their surrounding pixels.
5.  **Spatial Relationships:** Adjacency (both side-by-side and diagonal) is crucial for defining the enclosed area ("inside") and the immediate exterior boundary ("outside"). Topology (identifying enclosed vs. open regions) is the key concept.
6.  **Consistency:** The blue shapes themselves (the pixels with value 1) are never modified; only the surrounding or enclosed white pixels are changed.

**YAML Fact Document:**


```yaml
task_description: Identify enclosed regions formed by blue shapes and color the interior green and the exterior border red.

elements:
  - element: grid
    description: A 2D array of pixels representing colors 0-9.
  - element: pixel
    properties:
      - color: integer 0-9 (white, blue, red, green are relevant)
      - location: (row, column) coordinates

objects:
  - object: blue_shape
    description: A contiguous region of blue (1) pixels.
    properties:
      - connectivity: 8-way adjacency
      - topology: Can be enclosing (forms a loop) or open.
  - object: white_region
    description: A contiguous region of white (0) pixels.
    properties:
      - connectivity: 8-way adjacency
      - relationship: Can be inside a blue_shape, outside a blue_shape, or unbounded (background).

actions:
  - action: identify_enclosed_regions
    input: input grid
    output: set of white_regions that are fully surrounded by blue_shape pixels (and possibly grid boundaries) and do not reach the grid boundary via other white pixels.
    criteria: A flood fill starting within the white_region does not reach the grid boundary.
  - action: color_interior
    input: enclosed white_region
    output: change color of all pixels in the region to green (3).
  - action: identify_exterior_border
    input: blue_shape forming an enclosure
    output: set of white (0) pixels in the original grid adjacent (8-way) to the blue_shape pixels, excluding pixels inside the enclosure.
  - action: color_exterior_border
    input: exterior_border pixel set
    output: change color of all pixels in the set to red (2).

relationships:
  - relationship: adjacency
    between: [pixel, pixel]
    type: 8-way connectivity (includes diagonals)
  - relationship: enclosure
    between: [blue_shape, white_region]
    description: The blue_shape completely surrounds the white_region.
  - relationship: boundary
    between: [blue_shape, white_region]
    description: Pixels of the blue_shape are adjacent to pixels of the white_region.

transformation_rule:
  - step: Find all connected components of white (0) pixels.
  - step: For each white component, check if it is bounded (a flood fill starting within it does not reach the grid edge).
  - step: If a white component is bounded, identify it as an 'interior' region and the adjacent blue (1) pixels as its 'border'.
  - step: Color all pixels in the 'interior' region green (3).
  - step: Find all white (0) pixels adjacent to the 'border' blue pixels, excluding those already colored green. Color these 'exterior border' pixels red (2).
  - step: All other pixels retain their original color from the input grid.
```


**Natural Language Program:**

1.  Create a copy of the input grid to serve as the output grid.
2.  Identify all distinct connected regions of white (0) pixels using 8-way adjacency.
3.  For each white region found:
    a.  Determine if this region is "enclosed". An enclosed region is one where a search (like flood fill or BFS) starting from any pixel within the region cannot reach the boundary of the grid by only moving through other white pixels in the *same* region.
    b.  If the white region is enclosed:
        i.  Identify all the blue (1) pixels that are directly adjacent (8-way) to any pixel in this enclosed white region. Call this set the "border blue pixels".
        ii. Change the color of all pixels within the enclosed white region to green (3) in the output grid.
        iii. Identify all pixels in the *original input grid* that were white (0) and are adjacent (8-way) to any of the "border blue pixels".
        iv. For each such adjacent white pixel identified in step (iii), if its color in the *current output grid* is still white (0), change its color to red (2). (This avoids overwriting pixels already colored green).
4.  Return the modified output grid.