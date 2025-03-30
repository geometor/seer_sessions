Okay, let's analyze the transformation.

**Perception:**

1.  **Input/Output Structure:** Both input and output are grids of pixels with various colors. The primary background color is white (0).
2.  **Color Palette:** The input grids use white (0) and one dominant color (yellow-4, red-2, or green-3), sometimes with scattered gray (5) pixels. The output grids are identical to the inputs except for the addition of azure (8) pixels.
3.  **Key Change:** A rectangular block of azure (8) pixels appears in the output grid. This block did not exist in the input.
4.  **Location of Change:** The azure rectangle appears in an area that was entirely white (0) in the input grid.
5.  **Identifying the Area:** Comparing the input and output grids across the examples, the azure rectangle consistently fills the largest contiguous rectangular area composed solely of white (0) pixels in the input grid.
    *   Example 1: A 3x4 white rectangle at (row 5, col 5) becomes azure.
    *   Example 2: A 2x2 white rectangle at (row 4, col 6) becomes azure.
    *   Example 3: A 2x4 white rectangle at (row 11, col 8) becomes azure.
6.  **Transformation Logic:** The core transformation seems to be identifying the largest "empty" (all white) rectangle within the input grid and then "filling" that specific rectangle with the color azure (8) in the output, leaving all other pixels unchanged. "Largest" refers to the area (height * width) of the rectangle.

**YAML Facts:**


```yaml
task_description: Identify the largest rectangular area composed entirely of white pixels in the input grid and fill that area with azure pixels in the output grid.
grid_properties:
  - background_color: white (0)
input_elements:
  - type: pixel
    color: white (0)
    role: background / potential area for transformation
  - type: pixel
    color: various (non-white)
    role: foreground / boundary definition
output_elements:
  - type: pixel
    color: white (0)
    source: copied from input
  - type: pixel
    color: various (non-white)
    source: copied from input
  - type: object
    shape: rectangle
    color: azure (8)
    location: position of the largest all-white rectangle found in the input
    size: dimensions of the largest all-white rectangle found in the input
transformation:
  - action: find_largest_rectangle
    criteria:
      - all pixels within the rectangle must be white (0)
      - maximize area (height * width)
    target: input_grid
    tie_breaking: (Implicit) Assume unique largest or use top-leftmost if needed.
  - action: fill_rectangle
    target_area: the identified largest all-white rectangle
    fill_color: azure (8)
    destination: output_grid
  - action: copy_pixels
    source: input_grid
    destination: output_grid
    condition: pixels not part of the identified largest all-white rectangle
```


**Natural Language Program:**

1.  Create a copy of the input grid to serve as the initial output grid.
2.  Search the input grid to find all possible rectangular areas that contain only white (0) pixels.
3.  Calculate the area (height multiplied by width) of each all-white rectangle found.
4.  Identify the rectangle(s) with the maximum area.
5.  If there is only one rectangle with the maximum area, select it. If there are multiple rectangles with the same maximum area, select the one whose top-left corner is uppermost (smallest row index). If there is still a tie, select the one whose top-left corner is leftmost (smallest column index).
6.  Locate the coordinates (top-row, left-col, bottom-row, right-col) of the selected largest all-white rectangle.
7.  Modify the output grid by changing the color of all pixels within these coordinates (inclusive) to azure (8).
8.  The final modified grid is the result.