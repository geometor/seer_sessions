
## train_1

**input:**
```
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0
```


**output:**
```
0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:** The input and output are both 1-dimensional arrays (or grids of height 1). Each input contains a single contiguous block of a non-white color surrounded by white pixels (color 0). The output shows the same block of non-white color shifted 3 positions to the right, with the surrounding white pixels rearranged accordingly. The length of the array and the counts of each color remain the same.

*   **Facts:**
    
```yaml
    task_type: array_transformation
    dimensionality: 1D
    input_elements:
      - type: background
        color: white (0)
        count: variable
      - type: object
        description: A single contiguous block of a non-white color.
        color: variable (red, orange, blue in examples)
        count: 1
        length: variable
        position: variable start index
    output_elements:
      - type: background
        color: white (0)
        count: same as input
      - type: object
        description: The same object from the input.
        color: same as input object
        count: 1
        length: same as input object
        position: original start index + 3
    transformation:
      - action: identify
        target: non-white object block (color, start index, length)
      - action: shift
        target: non-white object block
        direction: right
        distance: 3 positions
      - action: maintain
        target: array length
      - action: maintain
        target: pixel colors and counts
      - action: fill
        target: vacated and surrounding space
        color: white (0)
    constraints:
      - Only one non-white object exists per input.
      - The object is always a contiguous horizontal block.
      - The shift distance is always 3.
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous block of non-white pixels in the input 1D array. Determine its color, starting position (index), and length.
    2.  Create a new 1D array of the same length as the input array, filled entirely with white pixels (0).
    3.  Calculate the new starting position for the block by adding 3 to its original starting position.
    4.  Copy the identified non-white block (using its original color and length) into the new array, starting at the calculated new position.
    5.  The resulting new array is the output.
