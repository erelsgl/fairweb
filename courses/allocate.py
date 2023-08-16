"""
Utilities for computing the allocation.
"""

import fairpy.courses
import numpy as np
import logging

logger = logging.getLogger(__name__)

def allocate(agent_capacities, item_capacities, valuations)->dict:
	"""
	Compute a course allocation to students.

	>>> agent_capacities = {'s1': 6, 's2': 4, 's3': 4, 's4': 6, 's5': 3}
	>>> item_capacities = {'c1': 40, 'c2': 40, 'c3': 40, 'c4': 20}
	>>> valuations = {'s1': {'c1': 161, 'c2': 85, 'c3': 420, 'c4': 332}, 's2': {'c1': 285, 'c2': 141, 'c3': 486, 'c4': 86}, 's3': {'c1': 153, 'c2': 353, 'c3': 278, 'c4': 215}, 's4': {'c1': 99, 'c2': 122, 'c3': 759, 'c4': 18}, 's5': {'c1': 382, 'c2': 257, 'c3': 8, 'c4': 351}}
	>>> allocate(agent_capacities, item_capacities, valuations)
	{'s1': ['c1', 'c2', 'c3', 'c4'], 's2': ['c1', 'c2', 'c3', 'c4'], 's3': ['c1', 'c2', 'c3', 'c4'], 's4': ['c1', 'c2', 'c3', 'c4'], 's5': ['c1', 'c2', 'c4']}
	"""
	instance = fairpy.courses.Instance(agent_capacities=agent_capacities, item_capacities=item_capacities, valuations=valuations)
	agents = agent_capacities.keys()
	string_explanation_logger = fairpy.courses.explanations.StringsExplanationLogger(agents)
	map_agent_name_to_bundle = fairpy.courses.divide(fairpy.courses.iterated_maximum_matching, instance=instance, explanation_logger=string_explanation_logger, adjust_utilities=True)
	logger.info("map_agent_name_to_bundle: %s", map_agent_name_to_bundle)
	return map_agent_name_to_bundle, string_explanation_logger.map_agent_to_explanation()


if __name__=="__main__":
	# logger.addHandler(logging.StreamHandler())
	# logger.setLevel(logging.INFO)
	import doctest
	print(doctest.testmod())
