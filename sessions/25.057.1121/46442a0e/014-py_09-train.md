
## example 1
*input:*
```
8 6
6 8
```
*expected output:*
```
8 6 6 8
6 8 8 6
6 8 8 6
8 6 6 8
```
size: None
palette: None
color count: None
pixels off: None
**ERROR**: ERROR: could not broadcast input array from shape (2,2) into shape (3,3)

## example 2
*input:*
```
7 7 8
7 7 8
8 8 8
```
*expected output:*
```
7 7 8 8 7 7
7 7 8 8 7 7
8 8 8 8 8 8
8 8 8 8 8 8
7 7 8 8 7 7
7 7 8 8 7 7
```
*transformed output:*
```
7 7 8 7 7 7
7 7 7 8 0 8
7 7 7 8 0 8
8 8 8 8 0 7
8 0 0 0 0 7
7 7 7 7 8 7
```
size: True
palette: False
color count: False
pixels off: 18
**FAILED!**

## example 3
*input:*
```
6 9 9
6 4 4
6 4 4
```
*expected output:*
```
6 9 9 6 6 6
6 4 4 4 4 9
6 4 4 4 4 9
9 4 4 4 4 6
9 4 4 4 4 6
6 6 6 9 9 6
```
*transformed output:*
```
6 9 9 6 6 6
6 6 9 9 0 9
6 6 4 4 0 9
9 6 4 4 0 6
9 0 0 0 0 6
6 6 6 9 9 6
```
size: True
palette: False
color count: False
pixels off: 12
**FAILED!**
