
## train_1

**input:**
```
0 8 8 0 0 0 8 8 8 0 0 0 8 8 8 8 0 8 8 0 0 0
```


**output:**
```
0 8 8 0 0 0 8 8 8 0 0 0 4 4 4 4 0 8 8 0 0 0
```


## train_2

**input:**
```
0 8 8 8 8 8 0 8 8 8 8 0 0 8 8 8 8 8 0 8 8 0
```


**output:**
```
0 4 4 4 4 4 0 8 8 8 8 0 0 4 4 4 4 4 0 8 8 0
```


## train_3

**input:**
```
0 8 8 8 8 8 8 0 0 8 8 0 0 8 8 8 8 8 8 8 0 0
```


**output:**
```
0 8 8 8 8 8 8 0 0 8 8 0 0 4 4 4 4 4 4 4 0 0
```

## Perception

The input is a single row (1D grid) containing pixels of two colors: white (0) and azure (8). The azure pixels form contiguous horizontal blocks separated by white pixels.
The output is also a single row, identical in size to the input.
Comparing the input and output, most pixels remain the same. However, one specific block of azure pixels in the input has changed its color to yellow (4) in the output.
The input has four distinct blocks of azure pixels with lengths 2, 3, 4, and 2 respectively.
In the output, the blocks of length 2, 3, and 2 remain azure (8), while the block of length 4 has become yellow (4).
This suggests a rule related to the properties of the azure blocks, specifically their length. The block whose length (4) matches the numerical value of the yellow color (4) is the one that undergoes the transformation.

## Facts


```yaml
task_description: Change the color of specific horizontal blocks based on their length.

elements:
  - element: pixel
    properties:
      - color: white (0), azure (8), yellow (4)
  - element: block
    definition: A contiguous horizontal sequence of pixels of the same color.
    properties:
      - color: The color of the pixels in the block.
      - length: The number of pixels in the block.
      - location: Start and end indices within the row.

input_features:
  - grid_dimensionality: 1D (single row)
  - colors_present: white (0), azure (8)
  - objects:
      - type: block
        color: azure
        properties_observed:
          - length: 2 (at indices 1-2)
          - length: 3 (at indices 6-8)
          - length: 4 (at indices 12-15)
          - length: 2 (at indices 17-18)

output_features:
  - grid_dimensionality: 1D (single row)
  - colors_present: white (0), azure (8), yellow (4)
  - objects:
      - type: block
        color: azure
        properties_observed:
          - length: 2 (at indices 1-2)
          - length: 3 (at indices 6-8)
          - length: 2 (at indices 17-18)
      - type: block
        color: yellow
        properties_observed:
          - length: 4 (at indices 12-15) # Changed from azure

transformation:
  - action: Identify horizontal blocks of azure (8) pixels.
  - condition: Check if the length of an azure block is exactly 4.
  - consequence: If the condition is met, change the color of all pixels within that block to yellow (4).
  - otherwise: Leave the block unchanged.
```


## Natural Language Program

1.  Scan the input grid row from left to right.
2.  Identify all contiguous horizontal blocks composed entirely of azure (8) pixels.
3.  For each identified azure block, determine its length (number of pixels).
4.  If the length of an azure block is exactly 4, change the color of all pixels in that block to yellow (4).
5.  Leave all other pixels (white pixels and azure blocks of lengths other than 4) unchanged.
6.  The resulting grid is the output.
