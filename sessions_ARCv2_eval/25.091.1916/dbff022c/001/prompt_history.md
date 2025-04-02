
## train_1

**input:**
```
0 4 4 4 4 4 0 3 4 6 9 5
0 4 0 4 0 4 0 3 6 7 2 9
0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 0 0 3 0 0 0 0 0 0 0
0 3 0 0 3 0 0 7 7 7 7 0
0 3 0 0 3 0 0 7 0 7 7 0
0 0 3 0 3 0 0 7 0 0 7 0
0 0 0 3 0 0 0 7 7 0 7 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 4 4 4 4 4 0 3 4 6 9 5
0 4 6 4 6 4 0 3 6 7 2 9
0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 3 3 3 0 0 7 7 7 7 0
0 3 3 3 3 0 0 7 0 7 7 0
0 0 3 3 3 0 0 7 0 0 7 0
0 0 0 3 0 0 0 7 7 0 7 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
2 6 0 0 8 8 8 8 0 0
4 5 0 0 8 0 0 8 0 0
6 8 0 0 8 0 0 8 0 0
8 1 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 4 4 4
0 5 0 0 0 5 0 4 0 4
0 0 5 5 5 5 0 4 4 4
0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 4 4 4
```


**output:**
```
2 6 0 0 8 8 8 8 0 0
4 5 0 0 8 1 1 8 0 0
6 8 0 0 8 1 1 8 0 0
8 1 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 4 4 4
0 5 0 0 0 5 0 4 5 4
0 0 5 5 5 5 0 4 4 4
0 0 0 0 0 0 0 4 5 4
0 0 0 0 0 0 0 4 4 4
```


## train_3

**input:**
```
0 2 6 0 4 4 4 4 4 0 2 2 2 2 0
0 7 1 0 4 0 0 0 4 0 2 0 2 2 0
0 0 0 0 4 0 0 0 4 0 2 2 0 2 0
0 0 0 0 4 4 4 4 4 0 2 2 2 2 0
```


**output:**
```
0 2 6 0 4 4 4 4 4 0 2 2 2 2 0
0 7 1 0 4 0 0 0 4 0 2 7 2 2 0
0 0 0 0 4 0 0 0 4 0 2 2 7 2 0
0 0 0 0 4 4 4 4 4 0 2 2 2 2 0
```

Okay, let's analyze the task examples.

**Perception of Elements:**

1.  **Input/Output Structure:** Both input and output are grids of colored pixels. The output grid largely mirrors the input grid, with specific modifications.
2.  **Objects:** The grids contain distinct shapes (objects) formed by contiguous pixels of the same non-white color. Some shapes are single-colored (like the yellow 'U', green 'H', orange 'C' in example 1), while others are multi-colored conglomerates.
3.  **Key Feature:** The core transformation involves filling enclosed white (0) areas within single-colored shapes. Multi-colored shapes seem unaffected by this filling process.
4.  **Enclosed Areas:** These are regions of white pixels completely surrounded by pixels of a single non-white color or other enclosed white pixels. They do not touch the grid boundary or larger background white areas.
5.  **Fill Color Logic:** The color used to fill these enclosed white areas seems determined by a rule involving the color of the enclosing shape and potentially the colors of adjacent shapes.
    *   In some cases (e.g., the green 'H' and orange 'C' in example 1), the fill color matches the color of the enclosing shape itself.
    *   In other cases (e.g., the yellow 'U' in example 1 fills with magenta; the azure 'H' in example 2 fills with blue), the fill color is *different* from the enclosing shape.
    *   Observing the cases where the fill color differs, it appears to be influenced by the color of pixels from *other* shapes that are directly adjacent (orthogonally) to the enclosed white region. If such "foreign" colored pixels touch the white hole, the most frequent *foreign* color seems to be chosen. If there's a tie in frequency, the lowest color index among the tied foreign colors seems to be selected (e.g., Example 1, Yellow U: Magenta(6) and Orange(7) both touch the hole once, Magenta(6) is chosen). If no foreign colors touch the hole, the shape's own color is used.

**YAML Facts:**


```yaml
task_description: Fill enclosed white regions within single-colored shapes based on adjacent colors.

elements:
  - element: grid
    description: A 2D array of pixels with integer values 0-9 representing colors.
  - element: pixel
    description: A single cell in the grid with a color value. White (0) is the background. Non-zero values represent colors.
  - element: shape
    description: A contiguous region of pixels of the same non-white color.
    properties:
      - color: The single color of the shape's pixels.
      - boundary: Pixels of the shape adjacent to white pixels or pixels of a different color.
      - interior: Pixels of the shape not on the boundary.
  - element: enclosed_region
    description: A contiguous region of white (0) pixels that cannot reach the grid boundary by moving only through white pixels.
    properties:
      - size: Number of pixels in the region.
      - location: Coordinates of the pixels.
      - adjacent_shape_color: The color of the shape immediately surrounding the region.
      - adjacent_foreign_colors: List of colors (and their counts) from pixels of *other* shapes that are orthogonally adjacent to any pixel in the enclosed region.

actions:
  - action: identify_enclosed_regions
    description: Find all connected components of white pixels that are not reachable from the grid boundary via other white pixels.
    using: Flood fill from boundary white pixels.
  - action: determine_fill_color
    description: For each enclosed region, determine the color to fill it with.
    logic: >
      1. Identify the primary color (C_primary) of the surrounding shape.
      2. Find all orthogonal neighboring pixels to the region that are non-white AND not C_primary.
      3. If no such neighbors exist, the fill color is C_primary.
      4. If such neighbors exist, count the frequency of each color among them.
      5. The fill color is the color with the highest frequency. If there's a tie for the highest frequency, choose the color with the lowest index among the tied colors.
  - action: fill_region
    description: Change the color of all pixels within an enclosed region to the determined fill color.

relationships:
  - relationship: adjacency
    description: Pixels are adjacent if they share an edge (orthogonal adjacency). Used for defining shapes, regions, and determining fill colors.
  - relationship: enclosure
    description: A white region is enclosed by a shape if all paths from the region to the grid boundary must pass through non-white pixels.
  - relationship: influence
    description: The colors of shapes adjacent to an enclosed white region can influence the color used to fill that region.

input_output_relationship:
  - The output grid is identical to the input grid, except that identified enclosed white regions within single-colored shapes are filled with a color determined by the adjacency rules. Multi-colored shapes and shapes without enclosed regions remain unchanged.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all white pixels (color 0) in the input grid that are "enclosed". An enclosed white pixel is one that cannot reach any boundary pixel of the grid by traveling only through adjacent (up, down, left, right) white pixels. This can be found by performing a flood fill starting from all white pixels on the grid's border; any white pixel not reached by this flood fill is enclosed.
3.  Group the identified enclosed white pixels into connected regions (where connectivity is defined by orthogonal adjacency).
4.  For each distinct enclosed white region:
    a.  Determine the single primary color (`C_primary`) of the shape that immediately surrounds this region (i.e., the color of the non-white pixels orthogonally adjacent to the region's pixels).
    b.  Examine all non-white pixels that are orthogonally adjacent to *any* pixel within the current enclosed white region.
    c.  Create a list of colors from these adjacent non-white pixels, excluding any pixels that have the color `C_primary`. Let this list be `Foreign_Colors`.
    d.  If the `Foreign_Colors` list is empty, set the `Fill_Color` for this region to `C_primary`.
    e.  If the `Foreign_Colors` list is not empty:
        i.  Count the occurrences of each distinct color in the `Foreign_Colors` list.
        ii. Find the maximum occurrence count.
        iii. Identify all colors that have this maximum count.
        iv. Select the color with the *lowest* numerical index value among these most frequent colors. Set this as the `Fill_Color`.
    f.  Change the color of all pixels in the output grid corresponding to the current enclosed white region to the determined `Fill_Color`.
5.  Return the modified output grid.
