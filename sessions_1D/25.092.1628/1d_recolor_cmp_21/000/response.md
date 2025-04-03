## Perception
The input and output are both single rows of pixels. The input contains blocks of azure (8) pixels separated by white (0) pixels. The output is largely the same as the input, except for one specific block of azure pixels. This block, which originally consisted of seven consecutive azure pixels, has been changed to gray (5) pixels in the output. Other blocks of azure pixels, with lengths of five and six respectively, remain unchanged. The white pixels also remain unchanged. This suggests the transformation rule targets contiguous horizontal blocks of azure pixels based on their length. Specifically, blocks of azure pixels with a length of exactly seven are transformed into blocks of gray pixels of the same length.

## Facts


```yaml
elements:
  - type: pixel_grid
    description: A single row of pixels.
  - type: color
    values: [white (0), azure (8), gray (5)]
  - type: object
    identifier: contiguous_horizontal_block
    description: A sequence of one or more pixels of the same color along the row.
    properties:
      - color: azure (8) or gray (5)
      - length: count of pixels in the block

transformation:
  - action: identify
    target: contiguous_horizontal_blocks
    properties:
      - color: azure (8)
  - action: filter
    criteria: length == 7
    target: identified_azure_blocks
  - action: change_color
    target: filtered_azure_blocks
    from_color: azure (8)
    to_color: gray (5)
  - action: keep
    target: all other pixels (white pixels and azure blocks not matching the filter criteria)
    properties:
      - color: unchanged

relationships:
  - type: positional_invariance
    description: The positions of white pixels and unchanged azure blocks are preserved.
  - type: size_invariance
    description: The length of the transformed block remains the same, only the color changes.
```


## Natural Language Program

1.  Identify all contiguous horizontal blocks of azure (8) pixels in the input row.
2.  For each identified azure block, determine its length (number of pixels).
3.  If an azure block has a length exactly equal to 7, change the color of all pixels within that block to gray (5).
4.  Leave all other pixels (white pixels and azure blocks with lengths other than 7) unchanged.
5.  The output row is the result of these changes.