def find_duplicate(nums):
    if len(nums) == 0:
        return False
    duplicate_count = []
    for num in nums:
        if num in duplicate_count:
            return num
        else:
            duplicate_count.append(num)
    return False