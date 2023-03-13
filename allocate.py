"""
Utilities for computing the allocation.
"""

import fairpy
from fairpy.items.bounded_sharing import dominating_allocation_with_bounded_sharing
from typing import *
import numpy as np
import logging

logger = logging.getLogger(__name__)

def allocate(agents, entitlement_normalized_preferences)->Dict:
	"""
	Compute a bounded-sharing leximin allocation.
	Returns the allocation as a dict mapping an agent to an nparray of fractions.

	>>> agents = ['likkud', 'religious', 'shas', 'aguda']
	>>> entitlement_normalized_preferences =     {'likkud': {'foreign': 0.333, 'defence': 0.333, 'finance': 0.333, 'police': 0.167, 'justice': 0.167, 'interior': 0.167, 'health': 0.167, 'educations': 0.333}, 'religious': {'foreign': 0.327, 'defence': 0.653, 'finance': 0.327, 'police': 0.98, 'justice': 0.653, 'interior': 0.327, 'health': 0.653, 'educations': 0.653}, 'shas': {'foreign': 0.253, 'defence': 0.253, 'finance': 1.012, 'police': 0.253, 'justice': 0.506, 'interior': 1.518, 'health': 1.012, 'educations': 1.012}, 'aguda': {'foreign': 0.61, 'defence': 0.61, 'finance': 0.61, 'police': 0.61, 'justice': 0.61, 'interior': 1.219, 'health': 2.438, 'educations': 2.438}}
	>>> allocate(agents, entitlement_normalized_preferences)
	{'likkud': array([1.   , 1.   , 1.   , 0.   , 0.276, 0.043, 0.404, 1.   ]), 'religious': array([0.   , 0.   , 0.   , 1.   , 0.724, 0.   , 0.   , 0.   ]), 'shas': array([0.   , 0.   , 0.   , 0.   , 0.   , 0.957, 0.   , 0.   ]), 'aguda': array([0.   , 0.   , 0.   , 0.   , 0.   , 0.   , 0.596, 0.   ])}
	"""
	leximin_allocation = fairpy.divide(fairpy.items.leximin_optimal_allocation, entitlement_normalized_preferences)
	logger.info("leximin allocation: %s", leximin_allocation)
	leximin_utility_profile = leximin_allocation.utility_profile()
	bounded_sharing_allocation = fairpy.divide(dominating_allocation_with_bounded_sharing, entitlement_normalized_preferences, thresholds=leximin_utility_profile)
	logger.info("bounded sharing allocation: %s", bounded_sharing_allocation)

	def rounded_fractions(fractions):
		new_fractions = np.round(fractions,3)
		new_fractions[new_fractions==0]=0   # remove negative zeros: 	https://stackoverflow.com/a/26786119/827927
		return new_fractions

	map_agent_to_fractions = {
		agents[i]: 
		rounded_fractions(bounded_sharing_allocation.bundles[i].fractions)
		for i in range(len(agents))}
	logger.info("map_agent_to_fractions: %s", map_agent_to_fractions)
	
	return map_agent_to_fractions




if __name__=="__main__":
	# logger.addHandler(logging.StreamHandler())
	# logger.setLevel(logging.INFO)
	import doctest
	print(doctest.testmod())
