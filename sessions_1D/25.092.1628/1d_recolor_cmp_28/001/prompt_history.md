
## train_1

**input:**
```
0 4 4 0 0 0 4 4 0 0 4 4 4 0 4 4 4 0 0 0 4 4 4 4 4 0 4 4 0 4 0 0 0
```


**output:**
```
0 4 4 0 0 0 4 4 0 0 4 4 4 0 4 4 4 0 0 0 7 7 7 7 7 0 4 4 0 4 0 0 0
```


## train_2

**input:**
```
0 0 4 4 4 4 4 4 4 0 0 0 4 4 4 4 4 0 0 4 4 4 4 4 4 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 7 7 7 7 7 7 7 0 0 0 4 4 4 4 4 0 0 4 4 4 4 4 4 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 4 0 0 4 0 0 0 4 4 4 0 0 0 4 4 4 4 0 0 4 0 0 4 4 4 4 0 0 4 0 0
```


**output:**
```
0 0 4 0 0 4 0 0 0 4 4 4 0 0 0 7 7 7 7 0 0 4 0 0 7 7 7 7 0 0 4 0 0
```

## Perception

The input and output are single-row grids (or effectively 1D arrays) containing pixels of primarily white (0) and yellow (4). The output grid is largely identical to the input grid, with the key difference being that some yellow (4) pixels are changed to orange (7) pixels.

Observing the examples provided:
1.  **train_1:** The input has contiguous horizontal groups of yellow pixels with lengths [2, 2, 3, 3, 5, 2, 1]. The maximum length is 5. The group of 5 yellow pixels in the input is changed to orange in the output.
2.  **train_2:** The input has contiguous horizontal groups of yellow pixels with lengths [7, 5, 6]. The maximum length is 7. The group of 7 yellow pixels in the input is changed to orange in the output.
3.  **train_3:** The input has contiguous horizontal groups of yellow pixels with lengths [1, 1, 3, 4, 1, 4, 1]. The maximum length is 4. Both groups of 4 yellow pixels in the input are changed to orange in the output.

The core transformation involves identifying horizontal segments of yellow pixels, determining their lengths, finding the maximum length among these segments, and then changing the color of all yellow pixels that belong to segments of that maximum length to orange. Pixels not meeting this criterion (white pixels or yellow pixels in shorter segments) remain unchanged.

## Facts


```yaml
Grid:
  - type: 1D array or single-row 2D array
  - colors_present: white (0), yellow (4) in input; white (0), yellow (4), orange (7) in output

Objects:
  - type: contiguous horizontal segments
  - color: yellow (4)
  - property: length (number of pixels in the segment)

Relationships:
  - Segments are separated by white (0) pixels.
  - Multiple segments can exist within a single grid.

Actions:
  - Identify all yellow (4) segments.
  - Calculate the length of each segment.
  - Determine the maximum length among all identified segments.
  - For every segment whose length equals the maximum length:
    - Change the color of all pixels within that segment from yellow (4) to orange (7).
  - Pixels not part of a maximum-length yellow segment remain unchanged.
```


## Natural Language Program

1.  Scan the input grid horizontally to identify all contiguous segments composed entirely of yellow (4) pixels.
2.  For each identified yellow segment, calculate its length (the number of pixels it contains).
3.  Find the maximum length among all calculated segment lengths. If no yellow segments exist, the maximum length is 0.
4.  Create the output grid as a copy of the input grid.
5.  Iterate through the input grid again, identifying the yellow segments.
6.  If a yellow segment's length matches the maximum length found in step 3, change the color of all pixels corresponding to that segment in the output grid from yellow (4) to orange (7).
7.  Leave all other pixels in the output grid unchanged from their input values (white pixels remain white, yellow pixels in segments shorter than the maximum length remain yellow).
