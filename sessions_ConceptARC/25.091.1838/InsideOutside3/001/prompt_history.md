
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 2 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 2 0 4
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 2 0
2 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Perception of the Elements:**

1.  **Grid Structure:** The inputs and outputs are 10x10 grids.
2.  **Colors:** The grids contain white (0) as the background, multiple red pixels (2), and exactly one yellow pixel (4).
3.  **Objects:** The primary objects are the individual red pixels and the single yellow pixel.
4.  **Transformation:** The core transformation involves deciding whether to keep the red pixels or the yellow pixel, removing the other color (changing it to white).
5.  **Key Factor:** The decision seems to depend on the coordinate parity (even/odd) of the yellow pixel and the red pixels. Specifically, there's a special condition when the yellow pixel is at an (odd row, odd column) position.

**YAML Facts:**


```yaml
task_description: Determine whether to keep red pixels or a single yellow pixel based on coordinate parity.
grid_properties:
  size: 10x10 for all examples
colors_present:
  - white (0): background
  - red (2): multiple pixels
  - yellow (4): exactly one pixel
objects:
  - type: pixel
    color: red (2)
    quantity: multiple (variable count)
    attributes:
      - location: (row, column)
      - coordinate_parity: (row % 2, col % 2)
  - type: pixel
    color: yellow (4)
    quantity: 1
    attributes:
      - location: (row, column)
      - coordinate_parity: (row % 2, col % 2)
transformation_rule: Conditional removal based on coordinate parity comparison.
conditions:
  - if yellow pixel coordinates are NOT (odd, odd):
      action: remove yellow pixel (change to white), keep red pixels.
  - if yellow pixel coordinates ARE (odd, odd):
      sub_condition: check if ANY red pixel also has (odd, odd) coordinates.
      sub_action_if_true: remove yellow pixel, keep red pixels.
      sub_action_if_false: remove ALL red pixels, keep yellow pixel.
output_grid: Contains only white background and either the original red pixels OR the original yellow pixel.

```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Find the coordinates (row `y_r`, column `y_c`) of the single yellow pixel (color 4).
3.  Find the coordinates of all red pixels (color 2). Store these locations.
4.  Calculate the parity type of the yellow pixel's coordinates: `y_parity = (y_r % 2, y_c % 2)`. (Use 1 for odd, 0 for even).
5.  **Check if the yellow pixel's parity type is (odd, odd) (i.e., `y_parity == (1, 1)`).**
6.  **Case 1: Yellow pixel parity is NOT (odd, odd).**
    *   Change the yellow pixel at (`y_r`, `y_c`) in the output grid to white (0).
    *   All red pixels remain unchanged.
7.  **Case 2: Yellow pixel parity IS (odd, odd).**
    *   Iterate through the location of each red pixel (`r_r`, `r_c`).
    *   Calculate the parity type for the current red pixel: `r_parity = (r_r % 2, r_c % 2)`.
    *   Check if `r_parity` is also (odd, odd) (i.e., `r_parity == (1, 1)`).
    *   **Subcase 2a: At least one red pixel has (odd, odd) parity.**
        *   Change the yellow pixel at (`y_r`, `y_c`) in the output grid to white (0).
        *   All red pixels remain unchanged. Stop checking other red pixels.
    *   **Subcase 2b: After checking all red pixels, NONE of them have (odd, odd) parity.**
        *   Keep the yellow pixel at (`y_r`, `y_c`) unchanged in the output grid.
        *   Iterate through the saved locations of all red pixels. For each red pixel location (`r_r`, `r_c`), change the corresponding cell in the output grid to white (0).
8.  Return the modified output grid.
