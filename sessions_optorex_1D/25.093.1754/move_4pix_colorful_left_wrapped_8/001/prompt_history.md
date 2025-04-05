
## train_1

**input:**
```
1 3 1 4 0 0 0 0 0 0 9 7
```


**output:**
```
0 0 0 0 0 0 9 7 1 3 1 4
```


## train_2

**input:**
```
2 9 6 0 7 2 4 9 2 8 9 9
```


**output:**
```
7 2 4 9 2 8 9 9 2 9 6 0
```


## train_3

**input:**
```
0 0 0 0 0 0 7 1 4 0 0 0
```


**output:**
```
0 0 7 1 4 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 3 4 4 7 9 1 0
```


**output:**
```
0 3 4 4 7 9 1 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 2 8 9 6 4 0 0
```


**output:**
```
0 2 8 9 6 4 0 0 0 0 0 0
```


## train_6

**input:**
```
8 8 8 2 1 4 9 2 0 0 9 7
```


**output:**
```
1 4 9 2 0 0 9 7 8 8 8 2
```


## train_7

**input:**
```
0 5 4 8 2 2 6 1 1 4 0 0
```


**output:**
```
2 2 6 1 1 4 0 0 0 5 4 8
```

*   **Perception of Task Elements:**
    *   The input and output are sequences of numbers represented as strings, separated by spaces.
    *   All input sequences have a length of 12 elements.
    *   All output sequences also have a length of 12 elements.
    *   The transformation appears to be a rearrangement of the input sequence elements.
    *   Specifically, the input sequence seems to be split into two segments, and these segments are swapped in the output.

*   **Facts:**
    
```yaml
    task_type: sequence_manipulation
    input:
      type: string
      format: space-separated numbers
      length: 12
      elements:
        type: number (represented as string character)
    output:
      type: string
      format: space-separated numbers
      length: 12
      elements:
        type: number (represented as string character)
    transformation:
      action: split_and_swap
      split_point: after the 4th element
      segments:
        - segment_1: first 4 elements of the input
        - segment_2: last 8 elements of the input
      output_construction: concatenate segment_2 followed by segment_1
    constraints:
      - Input sequence length is always 12.
      - Element order within each segment is preserved.
    ```


*   **Natural Language Program:**
    1.  Parse the input string into a list of 12 number strings.
    2.  Extract the first 4 elements into a 'first segment' list.
    3.  Extract the elements from index 4 to the end (the last 8 elements) into a 'second segment' list.
    4.  Create the output list by concatenating the 'second segment' followed by the 'first segment'.
    5.  Join the elements of the output list with spaces to form the final output string.
