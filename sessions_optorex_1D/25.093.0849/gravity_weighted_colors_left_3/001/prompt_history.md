
## train_1

**input:**
```
2 2 0 1 0 0 0 1 2 2 2 2
```


**output:**
```
0 0 0 0 1 1 2 2 2 2 2 2
```


## train_2

**input:**
```
0 2 2 2 0 0 1 0 2 1 2 1
```


**output:**
```
0 0 0 0 1 1 1 2 2 2 2 2
```


## train_3

**input:**
```
0 0 1 2 2 0 0 1 2 0 2 1
```


**output:**
```
0 0 0 0 0 1 1 1 2 2 2 2
```


## train_4

**input:**
```
0 0 1 0 0 2 1 0 0 2 2 2
```


**output:**
```
0 0 0 0 0 0 1 1 2 2 2 2
```


## train_5

**input:**
```
2 0 0 1 0 2 1 2 2 0 1 0
```


**output:**
```
0 0 0 0 0 1 1 1 2 2 2 2
```


## train_6

**input:**
```
1 1 2 1 0 1 0 0 0 0 0 1
```


**output:**
```
0 0 0 0 0 0 1 1 1 1 1 2
```


## train_7

**input:**
```
0 0 0 0 2 0 2 0 2 2 2 2
```


**output:**
```
0 0 0 0 0 0 2 2 2 2 2 2
```

*   **Perception:**
    *   The input consists of a sequence of integers (specifically 0, 1, and 2).
    *   The output is also a sequence of integers of the same length as the input.
    *   The integers present in the output sequence are the same as those in the input sequence, just rearranged.
    *   Observing the output sequences across all examples, they appear to be sorted in non-decreasing (ascending) order.

*   **Facts:**
    
```yaml
    Task: Sort a sequence of numbers.
    Objects:
      - InputSequence:
          Type: List of Integers
          Properties:
            - Contains integers 0, 1, or 2.
            - Fixed length (12 in examples).
      - OutputSequence:
          Type: List of Integers
          Properties:
            - Contains the same integers as InputSequence.
            - Same length as InputSequence.
            - Elements are sorted in ascending order.
    Relationships:
      - OutputSequence is a sorted version of InputSequence.
    Action:
      - Sort: Rearrange the elements of the InputSequence in non-decreasing order to produce the OutputSequence.
    ```


*   **Natural Language Program:**
    1.  Take the input sequence of numbers.
    2.  Sort the numbers in the sequence in ascending order.
    3.  Return the sorted sequence as the output.
