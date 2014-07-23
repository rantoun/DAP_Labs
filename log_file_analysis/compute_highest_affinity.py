def highest_affinity(site_list, user_list, time_list):

    # Initialize lists for unique users, unique sites, and [site, user] lists
    unique_sites = []
    unique_users = []
    site_user_list = []
    
    # Create list of unique sites
    for site in site_list:
    	if site not in unique_sites:
    		unique_sites.append(site)
    
    # Create list of unique users
    for user in user_list:
    	if user not in unique_users:
    		unique_users.append(user)
    
    # Create all combinations of unique site names and put in site_combinations_list  
    site_combinations_list = []
    for first in range(len(unique_sites)):
        for second in range(first+1, len(unique_sites)):
            site_combinations_list.append((unique_sites[first], unique_sites[second]))

    # Create list of lists containing site and user who accessed
    for i in range(len(site_list)):
    	site_user_list.append([site_list[i], user_list[i]])
    
    # Initialize list to store counts of combinations to 0
    count_combinations = len(site_combinations_list) * [0]

    for i in range(len(site_combinations_list)):
    	for user in unique_users:
    		if [site_combinations_list[i][0], user] in site_user_list and [site_combinations_list[i][1], user] in site_user_list:
    			count_combinations[i] += 1

    # Find index for maximum number of site pairs and use it to return site pair of maximum affinity
    max_index = count_combinations.index(max(count_combinations))

    max_affinity = sorted(site_combinations_list[max_index])
    return tuple(max_affinity)
