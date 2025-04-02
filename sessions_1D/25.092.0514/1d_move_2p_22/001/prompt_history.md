
## train_1

**input:**
```
3 3 3 3 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 3 3 3 3 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 7 7 7 7 7 7 7 7 0 0 0 0 0
```


**output:**
```
0 0 0 7 7 7 7 7 7 7 7 0 0 0
```


## train_3

**input:**
```
0 0 0 0 3 3 3 3 3 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 3 3 3 3 3 0 0 0
```

Okay, let's analyze the task based on the provided examples.

## Perception

1.  **Input/Output Format:** The examples are presented as 1D arrays (sequences) of integers representing colors. All examples have a length of 14.
2.  **Key Elements:** Each input sequence contains exactly one contiguous block of a single non-white color (e.g., green '3' or orange '7'). The rest of the sequence consists of white ('0') pixels.
3.  **Transformation:** The transformation involves changing the position of the non-white block within the sequence.
4.  **Observation:** Comparing input and output sequences, the non-white block appears to be shifted horizontally to the right. The amount of shift seems constant across examples.
5.  **Detailed Shift:**
    *   In example 1, the green block `[3, 3, 3, 3]` starts at index 0 and moves to start at index 2 (a shift of +2).
    *   In example 2, the orange block `[7, 7, 7, 7, 7, 7, 7, 7]` starts at index 1 and moves to start at index 3 (a shift of +2).
    *   In example 3, the green block `[3, 3, 3, 3, 3]` starts at index 4 and moves to start at index 6 (a shift of +2).
6.  **Conclusion:** The transformation identifies the single contiguous block of non-white pixels and shifts it exactly 2 positions to the right within the 1D sequence. The pixels originally occupied by the start of the block become white, and the overall length of the sequence remains unchanged.

## Facts


```yaml
Data_Structure:
  - type: 1D array (sequence)
  - element_type: integer (color code 0-9)
  - size: constant length (14 in examples)

Objects:
  - type: Contiguous_Block
    properties:
      - color: non-white (e.g., green, orange)
      - pixels: identical non-white color
      - location: defined by start and end indices in the sequence
      - uniqueness: exactly one such block per sequence
      - context: surrounded by white (0) pixels

Transformation:
  - name: Horizontal_Shift
  - target: Contiguous_Block
  - parameters:
      - direction: right
      - distance: 2 positions
  - effect:
      - The block's start index increases by 2.
      - The block's end index increases by 2.
      - Pixels vacated by the shift become white (0).
      - Pixels outside the original and final block positions remain white (0).
      - The block's color and length remain unchanged.
```


## Natural Language Program

1.  Identify the contiguous sequence (block) of non-white pixels within the input 1D array. Determine its start index, end index, length, and color.
2.  Create a new 1D array of the same length as the input, initialized entirely with white (0) pixels.
3.  Calculate the new start index for the block by adding 2 to its original start index.
4.  Copy the identified block of non-white pixels into the new array, starting at the calculated new start index.
5.  The resulting array is the output.
