
## train_1

**input:**
```
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0
```


**output:**
```
0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0
```


## train_2

**input:**
```
0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 4 4 4 4 4 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 0 0 0 0
```

*   **Perception:** The input and output are 1D sequences (arrays) of colored pixels. Each sequence contains a contiguous block of a single non-white color (orange, green, or yellow in the examples) surrounded by white pixels (color 0). The length of the sequence remains constant between input and output. The transformation involves rearranging the positions of the pixels within the sequence. Specifically, the entire sequence appears to be shifted cyclically to the right by a fixed amount. Comparing input and output sequences reveals that the last three elements of the input sequence move to the beginning of the output sequence, and the rest of the elements shift three positions to the right. This consistent shift amount (3 positions) across all examples suggests a circular right rotation.

*   **Facts:**
    
```yaml
    task_type: sequence_transformation
    input_format: 1D array of integers (colors)
    output_format: 1D array of integers (colors)
    element_colors:
      - white (0) - acts as background/empty space
      - one non-white color per example (e.g., orange (7), green (3), yellow (4))
    structure:
      - Input contains a single contiguous block of a non-white color.
      - The length of the input array equals the length of the output array.
    transformation:
      - The entire input sequence is modified positionally.
      - The transformation is consistent across examples.
    action:
      type: circular_shift
      direction: right
      amount: 3 positions
    relationships:
      - The output sequence is a result of applying a circular right shift of 3 positions to the input sequence.
    ```


*   **Natural Language Program:**
    1.  Take the input 1D array.
    2.  Perform a circular shift (rotation) of all elements in the array 3 positions to the right.
    3.  The element at the last position moves to the third position from the beginning.
    4.  The element at the second-to-last position moves to the second position from the beginning.
    5.  The element at the third-to-last position moves to the first position from the beginning.
    6.  All other elements shift 3 positions to the right.
    7.  The resulting array is the output.
