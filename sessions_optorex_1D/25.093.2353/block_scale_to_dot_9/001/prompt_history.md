
## train_1

**input:**
```
0 0 0 0 2 0 7 7 7 7 7 7
```


**output:**
```
0 0 0 0 2 7 7 7 7 7 7 7
```


## train_2

**input:**
```
0 0 0 2 0 0 0 0 3 3 3 3
```


**output:**
```
0 0 0 2 3 3 3 3 3 3 3 3
```


## train_3

**input:**
```
0 2 0 0 0 0 0 0 0 0 0 8
```


**output:**
```
0 2 8 8 8 8 8 8 8 8 8 8
```


## train_4

**input:**
```
0 6 6 6 6 6 6 6 6 2 0 0
```


**output:**
```
0 6 6 6 6 6 6 6 6 2 0 0
```


## train_5

**input:**
```
0 9 9 9 0 0 0 0 0 0 2 0
```


**output:**
```
0 9 9 9 9 9 9 9 9 9 2 0
```


## train_6

**input:**
```
7 7 7 7 7 7 7 2 0 0 0 0
```


**output:**
```
7 7 7 7 7 7 7 2 0 0 0 0
```


## train_7

**input:**
```
0 0 5 5 5 5 5 0 0 2 0 0
```


**output:**
```
0 0 5 5 5 5 5 5 5 2 0 0
```

Okay, let's analyze the transformation.

**Perception of Elements:**

1.  **Input/Output Structure:** Both input and output are sequences (lists or arrays) of 12 single-digit integers.
2.  **Key Digits:** The digits `0` and `2` appear to play special roles. Other non-zero digits (like `3`, `5`, `6`, `7`, `8`, `9` in the examples) act as "fill" values.
3.  **The Role of '2':** The digit `2` seems to function as a fixed boundary or marker within the sequence. Its position does not change.
4.  **The Role of '0':** The digit `0` represents an empty or fillable space. These are the only digits that get replaced.
5.  **The Role of Other Non-Zero Digits (N):** These digits seem to expand or "fill" adjacent `0`s under certain conditions. The expansion originates from an existing block or instance of the digit `N`.
6.  **Transformation Mechanism:** The transformation involves identifying sequences of `0`s that lie *between* the digit `2` and the nearest non-zero digit (`N`) on either side (left or right). These intervening `0`s are then replaced by the digit `N`. If `2` is already adjacent to a non-zero digit, or if there are no non-zero digits on one side, no filling occurs on that side.

**YAML Fact Document:**


```yaml
elements:
  - type: sequence
    properties:
      - length: 12
      - item_type: integer
      - item_range: 0-9
objects:
  - id: marker
    value: 2
    description: A fixed position digit that acts as a boundary. Its own value and position never change.
  - id: fillable_space
    value: 0
    description: Represents positions that can be potentially overwritten.
  - id: fill_value
    value: N (any digit from 1, 3, 4, 5, 6, 7, 8, 9)
    description: A non-zero, non-marker digit that can expand to replace adjacent 'fillable_space' digits.
relationships:
  - type: adjacency
    description: The relative positions of 'marker', 'fillable_space', and 'fill_value' determine the transformation.
  - type: spatial_gap
    description: A sequence of one or more 'fillable_space' digits located between a 'marker' and the nearest 'fill_value' on either side.
actions:
  - name: locate_marker
    actor: system
    target: input_sequence
    description: Find the index of the 'marker' (digit 2).
  - name: locate_nearest_fill_value
    actor: system
    target: input_sequence
    parameters:
      - direction: left_of_marker
      - direction: right_of_marker
    description: Find the index of the nearest non-zero, non-marker digit ('fill_value') to the left and right of the 'marker'.
  - name: fill_gap
    actor: system
    target: sequence (initially a copy of input)
    condition: A 'spatial_gap' exists between the 'marker' and a 'fill_value'.
    effect: Replace all 'fillable_space' (0) digits within the 'spatial_gap' with the corresponding 'fill_value'. This happens independently for the left and right sides of the 'marker'.
```


**Natural Language Program:**

1.  Receive the input sequence of 12 digits.
2.  Create a mutable copy of the input sequence to serve as the potential output.
3.  Find the index (position) of the digit `2` in the sequence. Let this be `marker_index`.
4.  **Left-side Fill:**
    a.  Search the sequence from `marker_index - 1` down to index 0.
    b.  Find the index of the first non-zero digit encountered. Let this be `left_fill_index` and its value be `left_fill_value`.
    c.  If such a digit is found (i.e., `left_fill_index` exists):
        i.  Iterate through the indices from `left_fill_index + 1` up to `marker_index - 1`.
        ii. For each index in this range, if the digit in the sequence copy at that index is `0`, replace it with `left_fill_value`.
5.  **Right-side Fill:**
    a.  Search the sequence from `marker_index + 1` up to the end of the sequence (index 11).
    b.  Find the index of the first non-zero digit encountered. Let this be `right_fill_index` and its value be `right_fill_value`.
    c.  If such a digit is found (i.e., `right_fill_index` exists):
        i.  Iterate through the indices from `marker_index + 1` up to `right_fill_index - 1`.
        ii. For each index in this range, if the digit in the sequence copy at that index is `0`, replace it with `right_fill_value`.
6.  Return the modified sequence copy as the output.
