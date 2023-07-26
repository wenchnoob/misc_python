start, end, buses = [int(x) for x in input().split()]

# walk time, ride time, intervals,
walks_times = [int(x) for x in input().split()]
ride_times = [int(x) for x in input().split()]
intervals = [int(x) for x in input().split()]
ride_times.insert(0, 0)
intervals.insert(0, 0)

pos = 0
while pos < len(walks_times) - 1:
    start += walks_times[pos]
    pos += 1
    while start % (intervals[pos]) != 0:
        start += 1
    start += ride_times[pos]
start += walks_times[pos]

if start <= end:
    print("yes")
else:
    print("no")