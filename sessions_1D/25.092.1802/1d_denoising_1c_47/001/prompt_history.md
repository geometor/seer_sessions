
## train_1

**input:**
```
0 0 4 0 0 4 0 0 0 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0 4 0 0 0 0 4 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 3 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 3 0 0 3 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0
```

## Perception

The input and output are both single rows of pixels (1D grids).
The input row consists primarily of white (0) pixels, interspersed with segments of a single non-white color. These non-white segments vary in length and color across different examples (yellow, azure, green).
The output row retains only the longest contiguous segment of the non-white color from the input row, placed in its original position. All other pixels in the output row, including the original white background pixels and any shorter non-white segments, are turned white (0).

## Facts


```yaml
Task: Retain the longest contiguous segment of non-white color in a 1D grid.

Input_Components:
  - Type: Grid
    Format: 1D (single row)
    Pixels:
      - Background: White (0)
      - Foreground: Contiguous segments of a single non-white color (e.g., Yellow(4), Azure(8), Green(3))

Output_Components:
  - Type: Grid
    Format: 1D (single row)
    Pixels:
      - Background: White (0)
      - Foreground: The single longest contiguous segment of non-white color from the input grid.

Objects:
  - Name: Non-white segment
    Properties:
      - Color: Any color except White(0)
      - Pixels: A contiguous sequence of pixels of the same non-white color.
      - Length: The number of pixels in the segment.
      - Position: The starting and ending indices within the row.
  - Name: Background
    Properties:
      - Color: White (0)

Relationships:
  - Contiguity: Pixels of the same non-white color are adjacent horizontally.
  - Comparison: Lengths of different non-white segments are compared.

Actions:
  - Identify: Find all contiguous segments of non-white pixels in the input row.
  - Measure: Determine the length of each identified segment.
  - Select: Choose the segment with the maximum length. (Implicit assumption: if multiple segments have the same maximum length, the examples don't specify tie-breaking, but suggest only one is kept. The simplest interpretation is *a* longest segment).
  - Create: Generate an output row of the same length as the input, initially filled with White (0).
  - Copy: Transfer the pixels of the selected longest segment from the input to their original positions in the output row.

Transformation:
  - Isolate the single longest contiguous block of non-white pixels.
  - Replace all other pixels (original background and shorter non-white blocks) with the background color (White, 0).
```


## Natural Language Program

1.  Examine the input row of pixels.
2.  Identify all contiguous segments (runs) of pixels that are not white (0). Keep track of the start index, end index, and color of each segment.
3.  Calculate the length of each identified non-white segment.
4.  Find the segment(s) with the maximum length. If there is only one longest segment, select it. (The examples only show cases with a unique longest segment).
5.  Create a new row of pixels with the same length as the input row, and fill it entirely with white (0) pixels.
6.  Copy the pixels from the selected longest non-white segment (identified in step 4) from their original positions in the input row to the corresponding positions in the new output row.
7.  The resulting row is the final output.
