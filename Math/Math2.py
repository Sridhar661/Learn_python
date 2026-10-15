import statistics

numbers = [10, 20, 30, 40, 50]

# 66. Mean (average)
print(statistics.mean(numbers))

# 67. Median
print(statistics.median(numbers))

# 68. Mode
print(statistics.mode([1, 2, 2, 3, 4]))

# 69. Population variance
print(statistics.pvariance(numbers))

# 70. Population standard deviation
print(statistics.pstdev(numbers))

# 71. Find the range
print(max(numbers) - min(numbers))

# 72. Count elements
print(len(numbers))

# 73. Sum of all elements
print(sum(numbers))

# 74. Average of three subjects
math_mark, science_mark, english_mark = 90, 85, 95
print((math_mark + science_mark + english_mark) / 3)

# 75. Total marks percentage
obtained, maximum = 450, 500
print(obtained / maximum * 100)

# 76. Weighted average
marks = [80, 90, 70]
weights = [0.5, 0.3, 0.2]
print(sum(m*w for m, w in zip(marks, weights)))

# 77. Find the second-largest distinct number
numbers = [10, 50, 30, 50, 40]
print(sorted(set(numbers))[-2])

# 78. Sort numbers in ascending order
print(sorted(numbers))

# 79. Sort numbers in descending order
print(sorted(numbers, reverse=True))

# 80. Count even numbers
numbers = [1, 2, 3, 4, 5, 6, 8]
print(sum(1 for n in numbers if n % 2 == 0))