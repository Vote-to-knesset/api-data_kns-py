def containsNearbyAlmostDuplicate( nums, indexDiff, valueDiff):
    dict_nums = {}
    for i in range(len(nums)):
        if nums[i] not in dict_nums:
            dict_nums[nums[i]] = [i]
        else:
            dict_nums[nums[i]].append(i)
    for x in dict_nums:
        val = abs(x - valueDiff)
        for j in range(val + 1):
            if j or -j in dict_nums:
                k = []
                if x != j:
                    if j in dict_nums:
                        k = dict_nums[j]
                    elif -j in dict_nums:
                        k = dict_nums[-j]
                c = sorted(dict_nums[x] + k)
                min_diff = float('inf')

                pair = ()

                for i in range(len(c) - 1):
                    diff = c[i + 1] - c[i]
                    if diff < min_diff:
                        min_diff = diff
                        pair = abs(c[i]-c[i + 1])
                        if pair <= indexDiff:
                            return True
    return False

print(containsNearbyAlmostDuplicate([1,5,9,1,5,9],2,3))