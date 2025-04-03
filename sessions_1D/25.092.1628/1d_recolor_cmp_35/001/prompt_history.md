
## train_1

**input:**
```
0 0 1 1 1 1 0 0 1 1 1 0 0 1 1 0 0 0 0 0
```


**output:**
```
0 0 4 4 4 4 0 0 1 1 1 0 0 1 1 0 0 0 0 0
```


## train_2

**input:**
```
0 1 1 1 1 0 1 1 1 1 1 1 1 0 1 1 0 0 0 0
```


**output:**
```
0 1 1 1 1 0 4 4 4 4 4 4 4 0 1 1 0 0 0 0
```


## train_3

**input:**
```
0 0 0 1 1 1 1 1 0 0 0 1 0 0 1 1 1 0 0 0
```


**output:**
```
0 0 0 4 4 4 4 4 0 0 0 1 0 0 1 1 1 0 0 0
```

*   **Perception:**
    *   The input and output are sequences of integers representing colors.
    *   The primary colors involved are white (0), blue (1), and yellow (4).
    *   The transformation focuses on contiguous segments (blocks) of blue pixels (value 1).
    *   In each example, one specific block of blue pixels is changed to yellow (value 4), while other blue blocks remain unchanged.
    *   By comparing the lengths of the blue blocks in each example, it appears the *longest* contiguous block of blue pixels is the one selected for modification.
    *   If multiple blocks share the maximum length (which doesn't occur in these examples, but is a possibility), the rule likely selects the first one encountered when reading the sequence from left to right.

*   **Facts:**
    
```yaml
    elements:
      - element: sequence
        properties:
          - represents: colors
          - values: [0, 1, 4] # white, blue, yellow
      - element: segment
        properties:
          - type: contiguous block of identical color
          - relevant_color: blue (1)
          - attributes:
              - start_index: position where the segment begins
              - end_index: position where the segment ends
              - length: number of pixels in the segment
    transformation:
      - action: identify_segments
        parameters:
          - color: blue (1)
        output: list of blue segments with their properties (start_index, end_index, length)
      - action: find_longest_segment
        input: list of blue segments
        criteria: maximum length
        tie_breaking: select the segment with the smallest start_index
        output: the target segment to be modified
      - action: modify_segment
        input: target segment
        change: color of pixels within the segment
        from_color: blue (1)
        to_color: yellow (4)
    relationships:
      - The modification applies only to the segment identified as the longest (and earliest, in case of ties).
      - Other segments, even if blue, remain unchanged.
      - The overall length and structure of the sequence remain the same, only pixel values within the target segment are altered.
    ```


*   **Natural Language Program:**
    1.  Scan the input sequence from left to right to identify all contiguous segments (blocks) composed entirely of blue pixels (value 1).
    2.  For each identified blue segment, record its starting position and its length.
    3.  Determine the maximum length among all identified blue segments.
    4.  Identify the blue segment(s) that have this maximum length.
    5.  If there is only one segment with the maximum length, select it as the target segment.
    6.  If there are multiple segments with the same maximum length, select the one that appears earliest in the sequence (i.e., the one with the smallest starting position) as the target segment.
    7.  Create the output sequence by copying the input sequence.
    8.  Change the color of all pixels within the selected target segment from blue (1) to yellow (4) in the output sequence.
