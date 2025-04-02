*   **Perception**: The task operates on 1-dimensional arrays (or single-row grids) of colored pixels. Each input array contains a contiguous block of a single color (other than white or azure), followed by some white pixels, and then a single azure pixel. The transformation involves extending the colored block to the right, overwriting the intermediate white pixels until it reaches the azure pixel. The azure pixel itself and any pixels preceding the colored block or following the azure pixel remain unchanged. The color used for filling is the color of the original contiguous block.

*   **Facts YAML**:
    
```yaml
    task_type: array_manipulation
    dimensionality: 1D
    objects:
      - object: fill_block
        description: A contiguous sequence of identical pixels with a color other than white (0) or azure (8). There is only one such block per input.
        properties:
          - color: The color of the pixels in the block (e.g., yellow, gray, orange).
          - start_index: The index of the first pixel in the block.
          - end_index: The index of the last pixel in the block.
      - object: boundary_pixel
        description: An azure (8) pixel that appears after the fill_block.
        properties:
          - color: azure (8).
          - index: The position of this pixel in the array.
      - object: gap_pixels
        description: White (0) pixels located between the end of the fill_block and the boundary_pixel.
        properties:
          - color: white (0).
          - location: Indices strictly greater than the fill_block's end_index and strictly less than the boundary_pixel's index.
    actions:
      - action: fill
        description: Change the color of specific pixels.
        target: gap_pixels
        details: All gap_pixels (white pixels between the fill_block and the boundary_pixel) are changed to the color of the fill_block.
    relationships:
      - relationship: spatial_order
        description: The fill_block appears first, followed by zero or more gap_pixels, followed by the boundary_pixel. All other pixels either precede the fill_block or follow the boundary_pixel.
    invariants:
      - Pixels before the start of the fill_block remain unchanged.
      - The fill_block itself remains unchanged (though it becomes part of a larger block of the same color).
      - The boundary_pixel (azure) remains unchanged in color and position.
      - Pixels after the boundary_pixel remain unchanged.
    ```


*   **Natural Language Program**:
    1.  Identify the contiguous block of pixels having the same color, where the color is not white (0) and not azure (8). Record its color (let's call it `fill_color`) and the index of its last pixel (`end_fill_index`).
    2.  Find the index of the first azure (8) pixel that occurs after `end_fill_index`. Let this be `azure_index`.
    3.  Iterate through the array from the index immediately following `end_fill_index` up to (but not including) `azure_index`.
    4.  For each pixel in this range, if its color is white (0), change its color to `fill_color`.
    5.  Leave all other pixels in the array unchanged.
    6.  The resulting array is the output.