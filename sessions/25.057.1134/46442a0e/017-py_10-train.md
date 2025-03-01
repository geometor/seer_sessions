
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
*transformed output:*
```
4 4 4 4
4 4 4 4
4 4 4 4
4 4 4 4
```
size: True
palette: False
color count: False
pixels off: 16
**FAILED!**

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
6 7 6 7 6 7
7 4 4 4 4 6
6 4 4 4 4 7
7 4 4 4 4 6
6 4 4 4 4 7
7 6 7 6 7 6
```
size: True
palette: False
color count: False
pixels off: 30
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
6 6 6 6 6 6
6 4 4 4 4 6
6 4 4 4 4 6
6 4 4 4 4 6
6 4 4 4 4 6
6 6 6 6 6 6
```
size: True
palette: True
color count: False
pixels off: 8
**FAILED!**
