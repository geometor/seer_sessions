
## train_1

**input:**
```
3 3 3 3 0 0 0 0 0 0 2 0
```


**output:**
```
3 3 3 3 3 3 3 3 3 3 2 0
```


## train_2

**input:**
```
6 6 6 6 6 6 2 0 0 0 0 0
```


**output:**
```
6 6 6 6 6 6 2 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 7 0 0 2 0 0 0 0 0
```


**output:**
```
0 0 0 7 7 7 2 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 9 0 2 0 0
```


**output:**
```
0 0 0 0 0 0 0 9 9 2 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 0 0 0 8 8 2
```


**output:**
```
0 0 0 0 0 0 0 0 0 8 8 2
```


## train_6

**input:**
```
0 2 0 0 8 8 8 8 0 0 0 0
```


**output:**
```
0 2 8 8 8 8 8 8 0 0 0 0
```


## train_7

**input:**
```
0 0 2 0 0 0 1 1 1 1 1 1
```


**output:**
```
0 0 2 1 1 1 1 1 1 1 1 1
```

**Perception of Task Elements:**

The task operates on sequences of 12 integers. The core elements appear to be:
1.  **The Number 2:** This number acts as a central pivot or boundary marker within the sequence.
2.  **Other Non-Zero Numbers:** These numbers (e.g., 1, 3, 6, 7, 8, 9) serve as "fill" values.
3.  **Zeros (0):** These are the elements subject to modification (filling).
4.  **Position/Sequence:** The relative positions of the numbers, specifically their proximity to the number 2, are crucial.

The transformation involves propagating a non-zero "fill" value into adjacent zeros, bounded by the position of the number 2.

**Facts:**


```yaml
objects:
  - sequence: a list of 12 integers.
  - marker: the integer value 2.
  - fill_value: any non-zero integer in the sequence other than 2.
  - target_element: the integer value 0.
properties:
  - sequence_length: 12
  - marker_presence: the number 2 is always present exactly once.
  - fill_value_location: relative position to the marker (left or right).
  - target_element_location: relative position to the marker and the fill_value.
actions:
  - locate: find the index of the marker (2).
  - search_left: find the nearest non-zero fill_value to the left of the marker.
  - search_right: find the nearest non-zero fill_value to the right of the marker.
  - fill: replace target_elements (0) between a fill_value and the marker with that fill_value.
relationships:
  - adjacency: zeros located between a fill_value and the marker.
  - boundary: the marker (2) limits the fill operation.
```


**Natural Language Program:**

1.  Identify the index of the number `2` in the input sequence.
2.  Find the index of the rightmost non-zero number located *before* the index of `2`. Let this number be `left_fill_value`. If such a number exists, replace all zeros between its index and the index of `2` with `left_fill_value`.
3.  Find the index of the leftmost non-zero number located *after* the index of `2`. Let this number be `right_fill_value`. If such a number exists, replace all zeros between the index of `2` and its index with `right_fill_value`.
4.  Return the modified sequence.
