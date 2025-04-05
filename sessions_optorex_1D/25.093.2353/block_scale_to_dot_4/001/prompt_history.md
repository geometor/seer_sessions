
## train_1

**input:**
```
0 0 8 8 0 0 2 0 0 0 0 0
```


**output:**
```
0 0 8 8 8 8 2 0 0 0 0 0
```


## train_2

**input:**
```
0 0 2 1 1 1 1 0 0 0 0 0
```


**output:**
```
0 0 2 1 1 1 1 0 0 0 0 0
```


## train_3

**input:**
```
0 1 1 0 0 0 0 0 0 0 2 0
```


**output:**
```
0 1 1 1 1 1 1 1 1 1 2 0
```


## train_4

**input:**
```
2 0 0 0 0 0 0 0 8 8 8 8
```


**output:**
```
2 8 8 8 8 8 8 8 8 8 8 8
```


## train_5

**input:**
```
0 0 0 0 0 8 8 8 8 0 0 2
```


**output:**
```
0 0 0 0 0 8 8 8 8 8 8 2
```


## train_6

**input:**
```
0 0 0 1 1 1 1 1 1 2 0 0
```


**output:**
```
0 0 0 1 1 1 1 1 1 2 0 0
```


## train_7

**input:**
```
0 0 0 0 2 4 4 4 4 4 4 4
```


**output:**
```
0 0 0 0 2 4 4 4 4 4 4 4
```

*   **Perception:** The task involves transforming a sequence of single-digit integers. The core operation seems to be filling sequences of zeros based on the proximity of a non-zero number to the number `2`. The number `2` acts as a central point or boundary. Zeros located between the number `2` and the nearest non-zero number (either to the left or right) are replaced by that non-zero number. If `2` is adjacent to a non-zero number, or if there are only zeros on one side extending to the end of the sequence, no filling occurs in that direction.

*   **Facts:**
    
```yaml
    task_elements:
      - object: input_sequence
        description: A list of single-digit integers.
      - object: output_sequence
        description: The transformed list of single-digit integers.
      - object: marker_element
        value: 2
        description: Acts as a central reference point for the transformation.
      - object: fill_element
        description: A non-zero integer in the sequence adjacent (or nearest across zeros) to the marker_element.
      - object: zero_element
        value: 0
        description: Elements that are potentially replaced.
      - object: sequence_segment
        description: A contiguous sub-sequence of zeros located between the marker_element (2) and the nearest non-zero element.
    actions:
      - action: locate
        actor: system
        target: marker_element (2)
        result: index of the marker_element
      - action: scan_left
        actor: system
        origin: index of marker_element
        target: first non-zero element encountered
        result: value and index of the left-side non-zero element (if any)
      - action: scan_right
        actor: system
        origin: index of marker_element
        target: first non-zero element encountered
        result: value and index of the right-side non-zero element (if any)
      - action: fill
        actor: system
        target: zero_elements within the identified sequence_segment
        value: value of the corresponding fill_element (left or right)
        condition: A non-zero element is found on that side, and there are zeros between it and the marker_element.
    relationships:
      - type: position
        between: marker_element, fill_element, zero_element
        description: Defines which zeros are candidates for filling based on their location relative to '2' and the nearest non-zero neighbours.
    ```


*   **Natural Language Program:**
    1.  Find the index of the number `2` in the input sequence. If `2` is not present, return the input sequence unchanged.
    2.  Initialize the output sequence as a copy of the input sequence.
    3.  **Left Fill:** Iterate leftwards from the index immediately preceding `2` down to the beginning of the sequence.
        a.  If a non-zero number `L` is encountered at index `idx_L`:
            i.  Iterate from `idx_L + 1` up to (but not including) the index of `2`.
            ii. For each element in this range, if its value is `0`, change its value in the output sequence to `L`.
            iii. Stop the leftward scan.
    4.  **Right Fill:** Iterate rightwards from the index immediately following `2` up to the end of the sequence.
        a.  If a non-zero number `R` is encountered at index `idx_R`:
            i.  Iterate from the index immediately following `2` up to (but not including) `idx_R`.
            ii. For each element in this range, if its value is `0`, change its value in the output sequence to `R`.
            iii. Stop the rightward scan.
    5.  Return the modified output sequence.
