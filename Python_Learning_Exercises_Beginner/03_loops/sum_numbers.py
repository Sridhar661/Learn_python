"""Add numbers from 1 through n."""

n = int(input("Add numbers from 1 to: "))
total = 0

for number in range(1, n + 1):
    total += number

print("Total:", total)
