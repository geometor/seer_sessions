
## example 1
*input:*
```
3 0 0 5 7 0 6 5 8 5 7
0 0 9 5 5 3 0 5 0 6 0
7 2 0 5 5 0 2 5 0 3 0
5 5 5 5 5 5 5 5 5 5 5
7 5 2 5 8 7 5 5 5 2 3
0 0 6 5 5 0 3 5 0 5 7
3 0 0 5 2 0 0 5 0 6 0
5 5 5 5 5 5 5 5 5 5 5
0 3 4 5 5 2 0 5 2 5 7
7 5 5 5 7 5 3 5 5 5 1
0 0 2 5 5 6 0 5 0 3 0
```
*expected output:*
```
0 0 0 5 0 0 0 5 0 3 4
0 0 0 5 0 0 0 5 7 0 0
0 0 0 5 0 0 0 5 0 0 2
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
```
*transformed output:*
```
3 0 0 5 7 0 6 5 8 5 7
0 0 9 5 5 3 0 5 0 6 0
7 2 0 5 5 0 2 5 0 3 0
5 5 5 5 5 5 5 5 5 5 5
7 5 2 5 8 7 5 5 5 2 3
0 0 6 5 5 0 3 5 0 5 7
3 0 0 5 2 0 0 5 0 6 0
5 5 5 5 5 5 5 5 5 5 5
0 3 4 5 5 2 0 5 2 5 7
7 5 5 5 7 5 3 5 5 5 1
0 0 2 5 5 6 0 5 0 3 0
```
size: True
palette: False
color count: False
pixels off: 54
**FAILED!**

## example 2
*input:*
```
3 0 0 5 0 2 0 5 0 6 0
0 0 7 5 0 0 0 5 0 0 9
0 6 0 5 0 1 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 3 0 5 0 0 0 5 0 0 0
1 0 9 5 0 0 6 5 0 7 3
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
9 0 0 5 0 9 0 5 0 9 0
0 6 0 5 0 0 4 5 0 0 1
0 0 0 5 7 0 0 5 0 0 0
```
*expected output:*
```
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 9 0
0 0 0 5 0 0 0 5 0 0 4
0 0 0 5 0 0 0 5 7 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
```
*transformed output:*
```
3 0 0 5 0 2 0 5 0 6 0
0 0 7 5 0 0 0 5 0 0 9
0 6 0 5 0 1 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 3 0 5 0 0 0 5 0 0 0
1 0 9 5 0 0 6 5 0 7 3
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
9 0 0 5 0 9 0 5 0 9 0
0 6 0 5 0 0 4 5 0 0 1
0 0 0 5 7 0 0 5 0 0 0
```
size: True
palette: False
color count: False
pixels off: 22
**FAILED!**

## example 3
*input:*
```
0 7 0 5 0 6 0 5 7 0 0
8 3 6 5 0 0 0 5 0 8 0
0 0 0 5 0 3 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 8 7 5 0 3 0 5 0 0 7
0 0 0 5 8 0 0 5 0 8 6
0 0 6 5 0 0 0 5 3 0 0
5 5 5 5 5 5 5 5 5 5 5
0 6 0 5 0 8 0 5 0 0 0
8 0 0 5 3 0 0 5 4 0 8
0 7 0 5 0 6 0 5 0 6 7
```
*expected output:*
```
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
4 0 8 5 0 0 0 5 0 0 0
0 6 7 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
```
*transformed output:*
```
0 7 0 5 0 6 0 5 7 0 0
8 3 6 5 0 0 0 5 0 8 0
0 0 0 5 0 3 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 8 7 5 0 3 0 5 0 0 7
0 0 0 5 8 0 0 5 0 8 6
0 0 6 5 0 0 0 5 3 0 0
5 5 5 5 5 5 5 5 5 5 5
0 6 0 5 0 8 0 5 0 0 0
8 0 0 5 3 0 0 5 4 0 8
0 7 0 5 0 6 0 5 0 6 7
```
size: True
palette: False
color count: False
pixels off: 30
**FAILED!**

## example 4
*input:*
```
3 0 0 5 0 1 0 5 0 0 2
0 2 0 5 0 3 0 5 0 6 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 1 0 5 0 0 0 5 0 3 0
7 0 6 5 2 0 7 5 0 7 0
0 0 0 5 0 0 0 5 0 6 0
5 5 5 5 5 5 5 5 5 5 5
7 0 0 5 0 4 0 5 0 0 3
0 0 0 5 0 7 0 5 2 0 0
0 3 0 5 0 3 0 5 0 0 6
```
*expected output:*
```
0 0 0 5 0 4 0 5 0 0 0
0 0 0 5 0 7 0 5 0 0 0
0 0 0 5 0 3 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
0 0 0 5 0 0 0 5 0 0 0
```
*transformed output:*
```
3 0 0 5 0 1 0 5 0 0 2
0 2 0 5 0 3 0 5 0 6 0
0 0 0 5 0 0 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5
0 1 0 5 0 0 0 5 0 3 0
7 0 6 5 2 0 7 5 0 7 0
0 0 0 5 0 0 0 5 0 6 0
5 5 5 5 5 5 5 5 5 5 5
7 0 0 5 0 4 0 5 0 0 3
0 0 0 5 0 7 0 5 2 0 0
0 3 0 5 0 3 0 5 0 0 6
```
size: True
palette: False
color count: False
pixels off: 23
**FAILED!**
