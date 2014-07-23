from itertools import combinations

def highest_affinity(site_list, user_list, time_list):
	unique_sites = []
	unique_users = []
	site_user_list = []
	storing_dict = {}
	user_dict = {}
	    
	# Create list of unique sites
	unique_sites = list(set(site_list))
	    
	    # Create list of unique users
	unique_users = list(set(user_list))

	for i in range(len(site_list)):
	    site_user_list.append([site_list[i], user_list[i]])
	    
	# Create all combinations of unique site names and put in site_combinations_list  
	site_combinations_list = list(combinations(unique_sites, 2))

	for user in unique_users:
	    for i in range(len(site_user_list)):
	        if site_user_list[i][1] == user:
	            user_dict.setdefault(user, [])
	            user_dict[user].append(site_user_list[i][0])

	for pair in site_combinations_list:
	    pair_list = list(pair)
	    storing_dict.setdefault(pair,0)
	    for key in user_dict:
	        if pair_list[0] in user_dict[key] and pair_list[1] in user_dict[key]:
	            storing_dict[pair] += 1

	return tuple(sorted(max(storing_dict, key=storing_dict.get)))
