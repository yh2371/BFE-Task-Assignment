Valid Task Gathering
====================

.. toctree::
   :maxdepth: 1

This section includes documentation for the Path Algorithm used to gather valid paths as well as other functions used to complete the gathering process in bulk.

Time Constrained K Shortest Path Algorithm
------------------------------------------

.. function:: time_constrained_shortest_path(G, valid_paths, start_station, end_station, start_time, fulltime, minimum_task, maximum_task):

   Gathers all valid paths for a given graph by repeating the process of extending the shortest path from one node to the all possible next nodes first, evaluating the extended paths, then storing those that have yet reached the destination, discarding those that violate constraints, and outputting those that are valid and have reached the destination

   :param graph: graph of all samples for a given borough for a given day type
   :type graph: Graph
   :param valid_paths: minimum binary heap for storing the valid paths
   :type valid_paths: MinBinaryHeap
   :param start_station: name of station where the path starts, "LIC"
   :type start_station: string
   :param end_station: name of station where the path ends, "LIC"
   :type end_station: string
   :param start_time: [hour, minute] shift starting time
   :type start_time: list
   :param fulltime: 1 if full-time, 0 if part-time
   :type fulltime: int
   :param minimum_task: minimum number of tasks that have to be performed in a day
   :type minimum_task: int
   :param maximum_task: maxmimum number of tasks that have to be performed in a day
   :type maximum_task: int
   :rtype: A minimum binary heap updated with valid paths

|

Valid Path Gathering
--------------------

.. function:: setup_graphs(filename, boroughs, gui = None):

  Builds graphs for each day type using the graph of each borough and stores the elements as a dictionary of dictionaries with day types, and boroughs as the key and corresponding graphs as the value.

  :param filename: name of file that stores all samples
  :type filename: string
  :param boroughs: list containing all five boroughs abbreviations
  :type boroughs: list
  :param gui: gui object for gui output
  :type: tkinter.Text or None
  :rtype: Dictionary of dictionaries with day types, and boroughs as keys and the corresponding graphs as values

|

.. function:: get_checker_tasks(graphs, start_station, end_station, minimum_task, maximum_task, checker, daytype, time_increment, time_range):

   Retrieves valid paths for a given checker from the graph and updates the checker's valid path heaps

   :param graphs: graphs of the given day type for all boroughs
   :type graphs: dictionary
   :param start_station: station checker starts at
   :type start_station: string
   :param end_station: station checker ends at
   :type end_station: string
   :param minimum_task: minimum number of tasks that a checker must complete in a day
   :type minimum_task: int
   :param maximum_task: maximum number of tasks a checker is allowed to complete in a day, constrains path lengths to make runtime shorter
   :type maximum_task: int
   :param checker: checker ID
   :type checker: string
   :param daytype: weekday, saturday or sunday
   :type daytype: string
   :param time_increment: increments of the checker starting time in hours
   :type time_increment: float
   :param time_range: allowed starting time window duration in hours
   :type time_range: float
   :rtype: None

|

.. function:: get_allchecker_tasks(checkerlist, filename, start_station, end_station, minimum_task, maximum_task, boroughs, time_increment, time_range, gui=None):

   Retrieves all valid paths for all checkers

   :param checkerlist: CheckerList object
   :type checkerlist: CheckerList
   :param filename: name of sample file
   :type filename: string
   :param start_station: station checker starts at
   :type start_station: string
   :param end_station: station checker ends at
   :type end_station: string
   :param minimum_task: minimum number of tasks that a checker must complete in a day
   :type minimum_task: int
   :param maximum_task: maximum number of tasks a checker is allowed to complete in a day, constrains path lengths to make runtime shorter
   :type maximum_task: int
   :param boroughs: list of all boroughs
   :type boroughs: list
   :param time_increment: increments of the checker starting time in hours
   :type time_increment: float
   :param time_range: allowed starting time window duration in hours
   :type time_range: float
   :rtype: None
