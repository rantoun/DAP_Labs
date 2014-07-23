import bear_matching

computed_result = bear_matching.matching_bears("medium-2.dat")
expected_result = [("child2", "child1")]

computed_result.sort()
expected_result.sort()

print computed_result
assert computed_result == expected_result
print "Successfully passed test3!"