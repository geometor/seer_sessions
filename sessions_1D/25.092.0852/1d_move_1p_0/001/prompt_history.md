
## train_1

**input:**
```
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0
```


**output:**
```
0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0
```

## Perception of the Elements

The input and output are both single rows (1D grids) of pixels.
In each example, the entire sequence of pixels appears to be shifted one position to the right.
The pixel originally at the rightmost end wraps around to become the new leftmost pixel.
The colors of the pixels and the length of the sequence are preserved, only their positions change.

## Documented Facts


```yaml
Task: Row Circular Shift Right

Input:
  Type: 1D grid (row) of pixels
  Properties:
    - Contains pixels of various colors (white=0, red=2, orange=7, azure=8 in examples).
    - Can have contiguous blocks of non-white colors.
    - Can have leading and trailing white pixels.

Output:
  Type: 1D grid (row) of pixels
  Properties:
    - Same length as the input row.
    - Same pixels (colors and count) as the input row.

Transformation:
  Action: Circular shift right
  Description: All pixels in the input row are shifted one position to the right. The pixel originally at the last position moves to the first position.
  Relationship: The output is a result of applying a single circular right shift operation to the entire input row.
```


## Natural Language Program

1.  Take the input row of pixels.
2.  Perform a circular shift of all pixels one position to the right.
3.  Place the pixel originally at the last index (rightmost position) into the first index (leftmost position).
4.  Shift all other pixels one position to the right from their original position.
5.  The resulting row is the output.
