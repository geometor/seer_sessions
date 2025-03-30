*   **General Assessment:**
    The initial code implements a basic flood fill algorithm starting from the identified 'fill color' pixels and expanding into adjacent 'background' (white) pixels. The results indicate that the fill operation is not correctly constrained. In all examples, the transformed output shows the fill color spreading beyond the intended areas, often filling the entire outer background region or crossing implied boundaries. The core issue seems to be that the fill process doesn't distinguish between white pixels *inside* the azure-bounded regions (which should be filled if connected to the seed color) and white pixels *outside* these regions or in separate, unconnected compartments (which should remain white). The fill needs to be contained within the specific regions demarcated by the azure boundaries *and* connected to the initial fill color patches.

*   **Strategy for Resolution:**
    1.  Identify the boundary (azure, 8), background (white, 0), and fill colors as before.
    2.  Identify the "external" background region: Perform a flood fill (BFS or DFS) starting from all white pixels located on the absolute border of the grid. Mark all reachable white pixels from these starting points as 'external' or 'unfillable'.
    3.  Perform the main flood fill: Start a BFS from the initial fill-color pixels ('seeds').
    4.  During the main BFS, only fill adjacent white pixels if they are *not* marked as 'external'/'unfillable' and have not already been visited/filled in this step. The fill should naturally stop at azure boundaries because they are not the background color.
    5.  This two-stage process ensures that the fill operation respects both the explicit azure boundaries and the implicit boundary between the enclosed areas and the outer grid background.

*   **Metrics Gathering:**
    Let's analyze the color counts for Example 1 to illustrate the issue.
    Fill Color: Magenta (6)
    Boundary Color: Azure (8)
    Background Color: White (0)

``` python
import numpy as np

# Example 1 Data
input_1 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,0,0,0],
    [0,0,8,0,0,0,8,0,0,0,8,0,0,0,8,0,0,0,8,6,6,6,8,0,0,0],
    [0,0,8,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,6,6,6,8,0,0,0],
    [0,0,8,0,0,0,8,0,0,0,8,0,0,0,8,0,0,0,8,6,6,6,8,0,0,0],
    [0,0,8,8,8,8,8,8,0,8,8,8,8,8,8,8,8,8,8,8,8,8,8,0,0,0],
    [0,0,0,0,0,0,8,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,8,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,8,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,8,8,0,8,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,8,8,0,8,8,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,8,0,0,0,8,0,0,0,8,0,0,0,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,8,0,0,0,8,0,0,0,8,0,0,0,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,8,8,8,8,8,8,8,8,8,8,0,8,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,8,6,6,6,8,0,0,0,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,8,6,6,6,0,0,0,0,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,8,6,6,6,8,0,0,0,8,0,0,0,0,0,0,0]
]

expected_1 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,0,0,0],
    [0,0,8,0,0,0,8,6,6,6,8,6,6,6,8,6,6,6,8,6,6,6,8,0,0,0],
    [0,0,8,0,0,0,8,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,8,0,0,0],
    [0,0,8,0,0,0,8,6,6,6,8,6,6,6,8,6,6,6,8,6,6,6,8,0,0,0],
    [0,0,8,8,8,8,8,8,6,8,8,8,8,8,8,8,8,8,8,8,8,8,8,0,0,0],
    [0,0,0,0,0,0,8,6,6,6,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,8,6,6,6,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,8,6,6,6,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,8,8,6,8,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,8,8,6,8,8,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,8,6,6,6,8,6,6,6,8,6,6,6,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,8,6,6,6,6,6,6,6,6,6,6,6,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,8,6,6,6,8,6,6,6,8,6,6,6,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,8,8,8,8,8,8,8,8,8,8,6,8,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,8,6,6,6,8,6,6,6,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,8,6,6,6,6,6,6,6,8,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,8,6,6,6,8,6,6,6,8,0,0,0,0,0,0,0]
]

transformed_1 = [
    [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],
    [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],
    [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],
    [6,6,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,6,6,6],
    [6,6,8,0,0,0,8,6,6,6,8,6,6,6,8,6,6,6,8,6,6,6,8,6,6,6],
    [6,6,8,0,0,0,8,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,8,6,6,6],
    [6,6,8,0,0,0,8,6,6,6,8,6,6,6,8,6,6,6,8,6,6,6,8,6,6,6],
    [6,6,8,8,8,8,8,8,6,8,8,8,8,8,8,8,8,8,8,8,8,8,8,6,6,6],
    [6,6,6,6,6,6,8,6,6,6,8,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],
    [6,6,6,6,6,6,8,6,6,6,8,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],
    [6,6,6,6,6,6,8,6,6,6,8,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],
    [6,6,6,6,6,6,8,8,6,8,8,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],
    [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],
    [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6],
    [6,6,6,6,6,6,8,8,6,8,8,8,8,8,8,8,8,8,8,6,6,6,6,6,6,6],
    [6,6,6,6,6,6,8,6,6,6,8,6,6,6,8,6,6,6,8,6,6,6,6,6,6,6],
    [6,6,6,6,6,6,8,6,6,6,6,6,6,6,6,6,6,6,8,6,6,6,6,6,6,6],
    [6,6,6,6,6,6,8,6,6,6,8,6,6,6,8,6,6,6,8,6,6,6,6,6,6,6],
    [6,6,6,6,6,6,8,8,8,8,8,8,8,8,8,8,6,8,8,6,6,6,6,6,6,6],
    [6,6,6,6,6,6,6,6,6,6,8,6,6,6,8,6,6,6,8,6,6,6,6,6,6,6],
    [6,6,6,6,6,6,6,6,6,6,8,6,6,6,6,6,6,6,8,6,6,6,6,6,6,6],
    [6,6,6,6,6,6,6,6,6,6,8,6,6,6,8,6,6,6,8,6,6,6,6,6,6,6]
]

input_grid = np.array(input_1)
expected_grid = np.array(expected_1)
transformed_grid = np.array(transformed_1)

unique_input, counts_input = np.unique(input_grid, return_counts=True)
unique_expected, counts_expected = np.unique(expected_grid, return_counts=True)
unique_transformed, counts_transformed = np.unique(transformed_grid, return_counts=True)

print("Example 1 Metrics:")
print("Input Counts:", dict(zip(unique_input, counts_input)))
print("Expected Counts:", dict(zip(unique_expected, counts_expected)))
print("Transformed Counts:", dict(zip(unique_transformed, counts_transformed)))

# Quantify the difference (focus on background 0 and fill 6)
expected_0 = dict(zip(unique_expected, counts_expected)).get(0, 0)
transformed_0 = dict(zip(unique_transformed, counts_transformed)).get(0, 0)
expected_6 = dict(zip(unique_expected, counts_expected)).get(6, 0)
transformed_6 = dict(zip(unique_transformed, counts_transformed)).get(6, 0)

print(f"White (0) Pixels: Expected={expected_0}, Transformed={transformed_0}, Difference={transformed_0 - expected_0}")
print(f"Magenta (6) Pixels: Expected={expected_6}, Transformed={transformed_6}, Difference={transformed_6 - expected_6}")

# Count white pixels on the border of the input grid
border_mask = np.zeros_like(input_grid, dtype=bool)
border_mask[0, :] = True
border_mask[-1, :] = True
border_mask[:, 0] = True
border_mask[:, -1] = True
border_white_pixels = np.sum((input_grid == 0) & border_mask)
print(f"White pixels on input grid border: {border_white_pixels}")
```
```
Example 1 Metrics:
Input Counts: {np.int64(0): np.int64(446), np.int64(6): np.int64(18), np.int64(8): np.int64(108)}
Expected Counts: {np.int64(0): np.int64(362), np.int64(6): np.int64(102), np.int64(8): np.int64(108)}
Transformed Counts: {np.int64(0): np.int64(9), np.int64(6): np.int64(455), np.int64(8): np.int64(108)}
White (0) Pixels: Expected=362, Transformed=9, Difference=-353
Magenta (6) Pixels: Expected=102, Transformed=455, Difference=353
White pixels on input grid border: 86

```
*   **Observations from Metrics (Example 1):**
    *   Input: 446 White (0), 18 Magenta (6), 108 Azure (8)
    *   Expected: 362 White (0), 102 Magenta (6), 108 Azure (8)
    *   Transformed: 9 White (0), 455 Magenta (6), 108 Azure (8)
    *   The transformation correctly identifies the fill (6) and boundary (8) colors.
    *   It correctly keeps all boundary (8) pixels.
    *   It incorrectly fills 353 white pixels that should have remained white. This difference (353) exactly matches the increase in magenta pixels.
    *   The number of white pixels on the input border is 86. The transformation fills almost all white pixels, including those connected to the border.

*   **YAML Documentation Block:**

    
```yaml
    task_description: Flood fill operation within bounded regions.
    
    grid_properties:
      - size: Variable (up to 30x30)
      - colors: White (0), Azure (8), and one other 'fill_color' (e.g., Magenta 6, Yellow 4, Green 3).
    
    objects:
      - object: boundary
        color: Azure (8)
        shape: Forms closed or partially open shapes, lines, or frames.
        role: Defines regions, acts as a barrier to the fill operation.
      - object: background
        color: White (0)
        distribution: Occupies areas inside and outside the boundaries. Some background areas are connected to the grid edge, others are fully enclosed by boundaries.
        role: The target for the fill operation, but only specific regions of it.
      - object: fill_seed
        color: The unique color that is not White (0) or Azure (8).
        distribution: Appears as one or more contiguous patches, usually within the regions defined by boundaries.
        role: The starting points for the flood fill.
    
    actions:
      - action: identify_colors
        inputs: input_grid
        outputs: boundary_color (8), background_color (0), fill_color (variable)
      - action: identify_external_background
        description: Find all background (0) pixels connected to the grid's absolute border without crossing a boundary (8) pixel.
        inputs: input_grid, background_color (0), boundary_color (8)
        outputs: a set or mask of 'external' background pixel coordinates.
      - action: flood_fill_internal
        description: Starting from 'fill_seed' pixels, fill adjacent background (0) pixels with the 'fill_color', but only if they are NOT 'external' background pixels.
        inputs: input_grid, fill_seed_pixels, external_background_mask, fill_color (variable), background_color (0)
        outputs: output_grid
    
    constraints:
      - The flood fill must not cross boundary (8) pixels.
      - The flood fill must not fill 'external' background (0) pixels (those connected to the grid edge).
      - The flood fill only affects background (0) pixels reachable from the initial fill_seed pixels under the above constraints.
    ```


*   **Natural Language Program:**

    1.  **Initialization:** Create a copy of the input grid, which will become the output grid.
    2.  **Identify Colors:** Determine the boundary color (Azure, 8), the background color (White, 0), and the fill color (the unique color present that is neither White nor Azure).
    3.  **Identify External White Pixels:**
        a. Initialize a queue for BFS and a 'visited_external' set/mask.
        b. Add all White (0) pixels located on the very edge (first/last row or first/last column) of the grid to the queue and mark them as visited_external.
        c. While the queue is not empty:
            i. Dequeue a pixel location (r, c).
            ii. Check its four adjacent neighbors (nr, nc).
            iii. If a neighbor is within bounds, is White (0) in the input grid, and has not been visited_external:
                - Mark it as visited_external.
                - Enqueue the neighbor (nr, nc).
    4.  **Identify Fill Seeds:** Find all pixels in the input grid that have the fill color.
    5.  **Perform Internal Flood Fill:**
        a. Initialize a new queue for the main BFS and a 'visited_fill' set/mask.
        b. Add all fill seed locations to this queue and mark them as visited_fill. Ensure these locations retain the fill color in the output grid.
        c. While the fill queue is not empty:
            i. Dequeue a pixel location (r, c).
            ii. Check its four adjacent neighbors (nr, nc).
            iii. If a neighbor is within bounds, has the background color (White, 0) in the *input* grid, has *not* been visited_fill, AND was *not* marked as visited_external in step 3:
                - Mark the neighbor as visited_fill.
                - Change the neighbor's color in the *output* grid to the fill color.
                - Enqueue the neighbor's location (nr, nc).
    6.  **Return:** Return the modified output grid.