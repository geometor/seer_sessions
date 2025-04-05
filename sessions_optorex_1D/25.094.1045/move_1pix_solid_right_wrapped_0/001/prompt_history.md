
## train_1

**input:**
```
5 5 5 0 0 0 5 5 5 5 5 5
```


**output:**
```
5 5 5 5 0 0 0 5 5 5 5 5
```


## train_2

**input:**
```
8 8 8 8 0 0 0 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 0 0 0 8 8 8 8
```


## train_3

**input:**
```
2 2 2 0 0 0 2 2 2 2 2 2
```


**output:**
```
2 2 2 2 0 0 0 2 2 2 2 2
```


## train_4

**input:**
```
1 1 1 1 1 1 0 0 0 1 1 1
```


**output:**
```
1 1 1 1 1 1 1 0 0 0 1 1
```


## train_5

**input:**
```
2 0 0 2 2 2 2 2 2 2 2 2
```


**output:**
```
2 2 0 0 2 2 2 2 2 2 2 2
```


## train_6

**input:**
```
7 0 0 0 0 0 0 0 0 0 0 7
```


**output:**
```
7 7 0 0 0 0 0 0 0 0 0 0
```


## train_7

**input:**
```
2 2 2 2 0 0 0 0 0 2 2 2
```


**output:**
```
2 2 2 2 2 0 0 0 0 0 2 2
```

*   **Perception:** The task involves rearranging a sequence of single-digit numbers. The input and output sequences generally contain the same numbers but in a different order. The core operation seems to be moving a specific non-zero number from the end of the sequence to a position earlier in the sequence, specifically just before the first block of zeros. The identity of the non-zero number being moved seems consistently to be the last non-zero digit appearing in the input sequence.

*   **Facts:**
    
```yaml
    objects:
      - sequence: a list of single-digit integers.
      - element: an integer within the sequence.
      - zero_element: an element with the value 0.
      - non_zero_element: an element with a value other than 0.
    properties:
      - position: the index of an element in the sequence.
      - value: the numerical value of an element.
      - is_last_non_zero: boolean property indicating if a non_zero_element is the last one encountered when scanning from the beginning or end of the sequence. (Specifically, the one with the highest index).
      - is_first_zero: boolean property indicating if a zero_element is the first one encountered when scanning from the beginning of the sequence.
    actions:
      - identify: locate elements based on properties (e.g., find the first zero, find the last non-zero).
      - remove: delete an element from the sequence at a specific position.
      - insert: add an element into the sequence at a specific position.
    relationships:
      - order: elements appear in a specific sequence.
      - location_relative_to_zeros: a non-zero element can be before, after, or within a block of zeros.
    transformation:
      - condition: The transformation occurs only if there is at least one zero and at least one non-zero element in the sequence.
      - step_1: Identify the value and original position (index) of the last non-zero element in the input sequence.
      - step_2: Identify the position (index) of the first zero element in the input sequence.
      - step_3: If the original position of the last non-zero element is already before the position of the first zero element, no change is made.
      - step_4: Otherwise, remove the identified last non-zero element from its original position.
      - step_5: Insert the removed element at the position identified as the first zero's location.
    ```


*   **Natural Language Program:**
    1.  Receive the input sequence of numbers.
    2.  Find the index of the *first* occurrence of the number 0 in the sequence. If no 0 is found, return the original sequence unchanged.
    3.  Find the index and value of the *last* non-zero number in the sequence. If no non-zero number is found, return the original sequence unchanged.
    4.  If the index of the last non-zero number is less than the index of the first 0, return the original sequence unchanged.
    5.  Otherwise, remove the last non-zero number from its original position.
    6.  Insert the removed number into the sequence at the index where the first 0 was found.
    7.  Return the modified sequence.
