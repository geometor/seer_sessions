## Perception

The input and output are both single-row grids (1D arrays).
Each input grid contains:
1.  Optional leading white pixels (0).
2.  A contiguous sequence of pixels of a single color (e.g., red '2' in train_1, magenta '6' in train_2, green '3' in train_3). Let's call this the "main color".
3.  A sequence of white pixels (0).
4.  A single yellow pixel (4).
5.  Optional trailing white pixels (0).

The transformation involves identifying the main color and the position of the yellow pixel. The white pixels located *between* the end of the main color sequence and the yellow pixel are replaced with the main color. All other pixels (leading white pixels, the original main color sequence, the yellow pixel, and trailing white pixels) remain unchanged. The yellow pixel acts as a right-hand boundary for the fill operation.

## Facts


```yaml
Task: Fill a gap between a colored sequence and a boundary marker.
Input:
  Type: Single-row grid (1D array).
  Elements:
    - Leading_White_Pixels: Optional sequence of white pixels (0) at the beginning.
    - Main_Color_Sequence: Contiguous sequence of a single non-white, non-yellow color.
    - Intermediate_White_Pixels: Sequence of white pixels (0) following the Main_Color_Sequence.
    - Boundary_Marker: Single yellow pixel (4) following the Intermediate_White_Pixels.
    - Trailing_White_Pixels: Optional sequence of white pixels (0) at the end.
Output:
  Type: Single-row grid (1D array).
  Relationship_to_Input: Modified version of the input grid.
Transformation:
  Action: Fill.
  Target: Intermediate_White_Pixels.
  Fill_Color: The color of the Main_Color_Sequence.
  Condition: The filling occurs only in the segment between the end of the Main_Color_Sequence and the position of the Boundary_Marker (yellow pixel).
  Preserved_Elements:
    - Leading_White_Pixels
    - Main_Color_Sequence
    - Boundary_Marker
    - Trailing_White_Pixels
```


## Natural Language Program

1.  Iterate through the input grid from left to right to find the first non-white pixel. This pixel's color is the "main color".
2.  Continue iterating to find the end of the contiguous sequence of the main color. Record this end position.
3.  Continue iterating from the end position to find the first occurrence of the yellow pixel (4). Record this position.
4.  Create a copy of the input grid to serve as the output grid.
5.  Iterate through the output grid from the position immediately after the end of the main color sequence up to (but not including) the position of the yellow pixel.
6.  For each pixel in this range, if its color is white (0), change it to the main color.
7.  Return the modified output grid.