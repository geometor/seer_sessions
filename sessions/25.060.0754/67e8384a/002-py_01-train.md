
## example 1
*input:*
```
5 3 4
3 4 5
3 4 4
```
*expected output:*
```
5 3 4 4 3 5
3 4 5 5 4 3
3 4 4 4 4 3
3 4 4 4 4 3
3 4 5 5 4 3
5 3 4 4 3 5
```
*transformed output:*
```
5 5 3 3 4 4
5 5 3 3 4 4
3 3 4 4 5 5
3 3 4 4 5 5
3 3 4 4 4 4
3 3 4 4 4 4
```
size: True
palette: True
color count: True
pixels off: 23
**FAILED!**

## example 2
*input:*
```
7 1 5
7 7 1
5 3 1
```
*expected output:*
```
7 1 5 5 1 7
7 7 1 1 7 7
5 3 1 1 3 5
5 3 1 1 3 5
7 7 1 1 7 7
7 1 5 5 1 7
```
*transformed output:*
```
7 7 1 1 5 5
7 7 1 1 5 5
7 7 7 7 1 1
7 7 7 7 1 1
5 5 3 3 1 1
5 5 3 3 1 1
```
size: True
palette: True
color count: True
pixels off: 30
**FAILED!**

## example 3
*input:*
```
2 5 2
2 6 4
2 2 2
```
*expected output:*
```
2 5 2 2 5 2
2 6 4 4 6 2
2 2 2 2 2 2
2 2 2 2 2 2
2 6 4 4 6 2
2 5 2 2 5 2
```
*transformed output:*
```
2 2 5 5 2 2
2 2 5 5 2 2
2 2 6 6 4 4
2 2 6 6 4 4
2 2 2 2 2 2
2 2 2 2 2 2
```
size: True
palette: True
color count: True
pixels off: 22
**FAILED!**

## example 4
*input:*
```
1 2 1
2 8 1
8 1 6
```
*expected output:*
```
1 2 1 1 2 1
2 8 1 1 8 2
8 1 6 6 1 8
8 1 6 6 1 8
2 8 1 1 8 2
1 2 1 1 2 1
```
*transformed output:*
```
1 1 2 2 1 1
1 1 2 2 1 1
2 2 8 8 1 1
2 2 8 8 1 1
8 8 1 1 6 6
8 8 1 1 6 6
```
size: True
palette: True
color count: True
pixels off: 27
**FAILED!**
