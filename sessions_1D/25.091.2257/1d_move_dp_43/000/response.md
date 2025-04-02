*   **Perception:** The input is a 1D array (or a single-row grid) of pixels. Each example contains a contiguous block of a single non-white, non-green color, a single green pixel (3), and several white pixels (0). The output is a rearrangement of the input pixels. The main colored block appears shifted to the right. The green pixel and any trailing white pixels seem to maintain their positions relative to the end of the grid or the shifted block. The amount of shift seems related to the number of white pixels between the main block and the green pixel.

*   **YAML Facts:**
    
```yaml
    task_type: rearrangement
    grid_dimensionality: 1D
    input_elements:
      - object_type: block
        description: A contiguous sequence of pixels of the same color, excluding white (0) and green (3). There is one such block per input.
        properties:
          - color: Varies (azure, yellow, magenta in examples)
          - length: Varies
          - start_index: Varies
          - end_index: Varies
      - object_type: marker
        description: A single green (3) pixel. Acts as a reference point.
        properties:
          - color: green (3)
          - index: Varies
      - object_type: background
        description: White (0) pixels.
        properties:
          - color: white (0)
          - location: Can be before the block, between the block and the marker, or after the marker.
    relationships:
      - type: spatial
        description: The block, the white pixels, and the marker appear sequentially in the 1D grid.
      - type: functional
        description: The number of white pixels located strictly between the end of the block and the green marker determines the transformation applied to the block.
    transformation:
      - action: identify
        target: The main colored block (non-white, non-green). Record its color, start index, end index, and length.
      - action: identify
        target: The green marker pixel. Record its index.
      - action: calculate
        description: Determine the number of white pixels between the end index of the block and the index of the green marker. Call this 'shift_amount'.
        formula: shift_amount = green_marker_index - block_end_index - 1
      - action: shift
        target: The main colored block.
        direction: right
        amount: shift_amount positions.
      - action: rearrange
        target: White pixels.
        description: White pixels originally before the block and between the block and the green marker are moved to fill the space vacated by the block's shift at the beginning of the relevant section. White pixels after the green marker remain in place relative to the end.
      - action: maintain_position
        target: Green marker pixel.
        description: The green marker's position relative to the shifted block is maintained, effectively keeping its absolute position in the grid if only the block and preceding/intermediate white pixels are considered rearranged.
    output_elements:
      - object_type: grid
        description: A 1D grid of the same size as the input, containing the rearranged elements.
        properties:
          - White pixels fill the initial positions up to the new start index of the shifted block.
          - The main colored block appears starting at its original start index plus the calculated shift_amount.
          - The green marker appears at its original index.
          - Any white pixels originally after the green marker appear at their original indices.

    ```


*   **Natural Language Program:**
    1.  Identify the contiguous block of pixels having the same color, ensuring this color is not white (0) or green (3). Record its color, start index, end index, and length.
    2.  Identify the index of the single green (3) pixel.
    3.  Count the number of white (0) pixels located strictly between the end index of the identified block and the index of the green pixel. This count is the `shift_amount`.
    4.  Create a new grid of the same size as the input, filled with white (0) pixels.
    5.  Copy the identified block into the new grid, starting at the position `original_start_index + shift_amount`.
    6.  Place the green (3) pixel in the new grid at its original index.
    7.  Place any white (0) pixels that were originally located *after* the green pixel in the input grid into the new grid at their original indices.
    8.  The resulting grid is the output.