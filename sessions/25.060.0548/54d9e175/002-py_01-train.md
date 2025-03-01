
## example 1
*input:*
```
0 0 0 5 0 0 0 5 0 0 0
0 1 0 5 0 2 0 5 0 1 0
0 0 0 5 0 0 0 5 0 0 0
```
*expected output:*
```
6 6 6 5 7 7 7 5 6 6 6
6 6 6 5 7 7 7 5 6 6 6
6 6 6 5 7 7 7 5 6 6 6
```
*transformed output:*
```
6 6 6 5 8 8 8 5 9 9 9
6 6 8 5 8 7 8 5 8 6 9
6 6 6 5 8 8 8 5 9 9 9
```
size: True
palette: False
color count: False
pixels off: 17
**FAILED!**

## example 2
*input:*
```
0 0 0 5 0 0 0 5 0 0 0
0 2 0 5 0 3 0 5 0 1 0
0 0 0 5 0 0 0 5 0 0 0
```
*expected output:*
```
7 7 7 5 8 8 8 5 6 6 6
7 7 7 5 8 8 8 5 6 6 6
7 7 7 5 8 8 8 5 6 6 6
```
*transformed output:*
```
6 6 6 5 8 8 8 5 9 9 9
6 7 8 5 8 8 8 5 8 6 9
6 6 6 5 8 8 8 5 9 9 9
```
size: True
palette: False
color count: False
pixels off: 16
**FAILED!**

## example 3
*input:*
```
0 0 0 5 0 0 0 5 0 0 0
0 3 0 5 0 1 0 5 0 4 0
0 0 0 5 0 0 0 5 0 0 0
```
*expected output:*
```
8 8 8 5 6 6 6 5 9 9 9
8 8 8 5 6 6 6 5 9 9 9
8 8 8 5 6 6 6 5 9 9 9
```
*transformed output:*
```
6 6 6 5 8 8 8 5 9 9 9
6 8 8 5 8 6 8 5 8 9 9
6 6 6 5 8 8 8 5 9 9 9
```
size: True
palette: True
color count: False
pixels off: 16
**FAILED!**

## example 4
*input:*
```
0 0 0 5 0 0 0 5 0 0 0
0 4 0 5 0 1 0 5 0 2 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
0 2 0 5 0 3 0 5 0 4 0
0 0 0 5 0 0 0 5 0 0 0
```
*expected output:*
```
9 9 9 5 6 6 6 5 7 7 7
9 9 9 5 6 6 6 5 7 7 7
9 9 9 5 6 6 6 5 7 7 7
5 5 5 5 5 5 5 5 5 5 5
7 7 7 5 8 8 8 5 9 9 9
7 7 7 5 8 8 8 5 9 9 9
7 7 7 5 8 8 8 5 9 9 9
```
*transformed output:*
```
6 6 6 5 8 8 8 5 9 9 9
6 9 8 5 8 6 8 5 8 7 9
6 6 6 5 8 8 8 5 9 9 9
5 5 5 5 5 5 5 5 5 5 5
6 6 6 5 8 8 8 5 9 9 9
6 7 8 5 8 8 8 5 8 9 9
6 6 6 5 8 8 8 5 9 9 9
```
size: True
palette: True
color count: False
pixels off: 33
**FAILED!**
