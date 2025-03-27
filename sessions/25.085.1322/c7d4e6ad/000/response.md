Okay, let's break down this task.

## Perception

1.  **Input Grid Structure**: The input grids contain a background of white (0) pixels. There are distinct colored objects (maroon, magenta, yellow in the first example; azure, red in the second) positioned primarily towards the left side of the grid. Additionally, there's a distinct object or pattern composed of gray (5) pixels located roughly in the central area, potentially slightly offset to the right.
2.  **Output Grid Structure**: The output grids retain the background and the colored objects from the left side of the input grid in their exact positions. The gray (5) pixels present in the input are replaced in the output.
3.  **Transformation Observation**: The core transformation appears to involve the gray (5) pixels. Each gray pixel in the input grid is recolored in the output grid. The new color assigned to a former gray pixel corresponds to the color of the first non-white object encountered in the *same row*, scanning from the left edge.
4.  **Row-based Logic**: The transformation seems to operate independently on each row. If a row contains a non-white, non-gray color (e.g., maroon, magenta, yellow, azure, red) starting from the left, this color dictates the replacement color for any gray pixels found *anywhere* within that specific row.
5.  **Conditional Replacement**: Gray pixels are only replaced if there is a non-gray, non-white "source" color present earlier in the same row. If a row only contains white and gray pixels, or starts with gray, the gray pixels in that row remain unchanged (though this specific edge case isn't explicitly shown in the examples, it's implied by the observed pattern). Rows containing only white pixels remain unchanged.

## Facts


```yaml
elements:
  - type: background
    color: white (0)
    description: The predominant color, filling empty space.
  - type: source_object
    description: Contiguous or single pixels of non-white, non-gray color, typically found near the left edge of the grid within certain rows.
    properties:
      - color: Varies (maroon, magenta, yellow, azure, red in examples). Excludes white (0) and gray (5).
      - position: Appears as the first non-white pixel when scanning a row from left to right.
  - type: target_pixel
    description: Pixels to be recolored.
    properties:
      - color: gray (5)
      - position: Can appear anywhere within a row.

actions:
  - name: identify_row_source_color
    description: For each row, find the color of the first pixel that is not white (0).
    input: row
    output: source_color (or null/white if none exists or the first is gray)
  - name: replace_gray_pixels
    description: Change the color of specific pixels in the grid.
    condition: Only applies to pixels with the target color (gray). The replacement occurs only if a valid source_color (non-white, non-gray) was identified for the row.
    input: target_pixel (gray), source_color (from the same row)
    output: pixel with source_color

relationships:
  - type: spatial
    description: The transformation is row-dependent. The color used to replace gray pixels in a specific row is determined by the first non-white, non-gray color found within that same row.
```


## Natural Language Program

1.  Create a copy of the input grid to serve as the output grid.
2.  Iterate through each row of the input grid, from top to bottom.
3.  For the current row, determine the `source_color`:
    a.  Scan the row from the leftmost pixel to the rightmost.
    b.  Identify the color of the first pixel that is not white (0).
    c.  If no non-white pixel is found, the `source_color` is white (0).
4.  Check if the identified `source_color` is neither white (0) nor gray (5).
5.  If a valid `source_color` (non-white, non-gray) was found for the row:
    a.  Iterate through each pixel in that same row of the grid copy (the one being modified).
    b.  If a pixel in the *original* input grid at this position (same row, same column) is gray (5), change the color of the corresponding pixel in the output grid copy to the identified `source_color`.
6.  If the `source_color` for the row is white (0) or gray (5), make no changes to that row in the output grid copy (gray pixels remain gray, other pixels remain as they were).
7.  After processing all rows, the modified grid copy is the final output.