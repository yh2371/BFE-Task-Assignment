.. BFE_Task_Assignment documentation master file, created by
   sphinx-quickstart on Wed May 13 15:58:52 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
  :maxdepth: 1


Classes
=======

This section contains documentation on all classes defined in this project.

Graph
-----

.. class:: Graph

   Representation of a simple graph using an adjacency map.

   .. function:: __init__(self, directed=True, borough=None, daytype=None):

      Creates an empty graph (undirected, by default):, Graph is directed if optional paramter is set to True.

      :param self._vertices: dictionary of vertices in the graph with station names (string) as keys and Station objects as values
      :param self._outgoing: dictionary dictionaries of outgoing edges in the graph with Station objects as keys and Edge objects as values, Edge = dict[origin][destination]
      :param self._incoming: dictionary dictionaries of incoming edges in the graph with Station objects as keys and Edge objects as values, Edge = dict[destination][origin]
      :param self._borough: borough ID associated to the graph
      :type self._borough: string
      :param self._daytype: day type associated to the graph, weekday, saturday, or sunday
      :type self._daytype: string
      :rtype: Graph object

|

   .. function:: get_borough(self):

      :rtype: Borough ID of the graph

|

   .. function:: get_daytype(self):

      :rtype: Day type of the graph

|

   .. function:: _validate_vertex(self, v):

      Validates a vertex

      :param v: vertex
      :raises TypeError: If vertex is not a Station object
      :raises ValueError: If vertex does not belong to the graph

|

   .. function:: is_directed(self):


      :rtype: True if directed, otherwise False

|

   .. function:: vertex_count(self):

      :rtype: Number of vertices in the graph

|

   .. function:: vertices(self):

      :rtype: Iterable of Station objects in the graph

|

   .. function:: edge_count(self):

      :rtype: Number of edges in the graph

|

   .. function:: get_edge(self, u, v):

      Gets the edge starting from u and ending at v

      :param u: origin
      :type u: Station
      :param v: destination
      :type v: Station
      :rtype: Edge going from u to v

|

   .. function:: incident_edges(self, v, outgoing=True):

     Returns an iterable of all outgoing incident edges of v

     :param v: origin
     :type v: Station
     :param outgoing: control whether we are looking for incoming or outgoing incident edges, outgoing by default
     :type outgoing: bool
     :rtype: Iterable of outgoing incident edges of v

|

   .. function:: get_vertex(self, station):

      Retrieves the Station object (vertex) associated to the station name, if there's no such station in the graph, a None type value is returned

      :param station: name of station
      :type station: string
      :rtype: Station object associated to the station name or None

|

   .. function:: insert_vertex(self, station, coord):

      Insert and return a new vertex (Station object):

      :param station: name of station
      :type station: string
      :param coord: [longitude, latitude] list associated to the station
      :type coord: list
      :rtype: New Station object that was inserted into the graph

|

   .. function:: insert_edge(self, u, v, route = None, arrivaltime = None, departuretime = None, sample_id = None):

      Insert and return a new Edge from u to v

      :param u: origin
      :type u: station
      :param v: destination
      :type v: station
      :param arrivaltime: Time of arrival of route [hour, minute]
      :type arrivaltime: list
      :param departuretime: Time of departure of route[hour, minute]
      :type departuretime: list
      :param sample_id: Sample ID
      :type sample_id: String
      :rtype: New Edge object going from u to v

|

   .. function:: remove_vertex(self, v):

      Remove vertex from graph

      :param v: vertex
      :param type: Station
      :rtype: None

|

   .. function:: remove_edge(self, u, v):

      Remove edge starting from u and ending at v

      :param u: origin
      :type u: Station
      :param v: destination
      :type v: Station
      :rtype: None

|

   .. class:: Station

      Nested class in Graph. Vertex structure for the graph, representing a bus station in the field

      .. function:: __init__(self, station, coord):

         Creates a Station object

         :param self._station: station name
         :type self._station: string
         :param self._coord: [long, lat] coordinates of station
         :type self._coord: list
         :param self._samples=[]: list of Sample objects, representing samples that can be done at this station
         :type self._samples=[]: list
         :rtype: Station object

  |

      .. function:: get_lat(self):

            Return latitude of station

            :rtype: Latitude of station

  |

      .. function:: get_long(self):

            Return longitude of station

            :rtype: Longitude of station

  |

      .. function:: station(self):

            Return station name

            :rtype: Station name string

  |

      .. function:: samples(self):

            Returns iterable over all samples that can be taken at this station

            :rtype: List of Sample Objects

  |

      .. function:: insert_sample(self, routename, arrival_time, departure_time, sample_id):

            Creates a new sample object and adds it to the samples list of the Station

            :param routename: name of route taken in the sample
            :type routename: string
            :param arrival_time: arrival time of sample (round trip) [hour,minute]
            :type arrival_time: list
            :param departure_time: departure time of sample (round trip) [hour, minute]
            :type departure_time: list
            :param sample_id: Sample ID
            :type sample_id: string
            :rtype: None

  |

      .. class:: Sample

          Nested Class in Station. Representation of a roundtrip sample

          .. function:: __init__(self, routename, arrivaltime, departuretime, sample_id):

                Creates new Sample object

                :param self._routename: name of route taken in the sample
                :type self._routename: string
                :param self._arrivalTime: arrival time of sample (round trip) [hour,minute]
                :type self._arrivalTime: list
                :param self._departureTime: departure time of sample (round trip) [hour, minute]
                :type self._departureTime: list
                :param self._sample_id: Sample ID
                :type self._sample_id: string
                :param self._roundtripTime: round trip duration in minutes
                :type self._roundtripTime: int
                :rtype: New Sample object

      |

          .. function:: routename(self):

                Get route name

                :rtype: Route name string

      |

         .. function:: roundtriptime(self):

                Get round trip time in minutes

                :rtype: Round trip time in minutes

      |

         .. function:: departuretime(self):

                Get departure time

                :rtype: [hour, minute] departure time of round trip

      |

         .. function:: arrivaltime(self):

                Get arrival time

                :rtype: [hour, minute] arrival time of round trip

      |

          .. function::sample_id(self):

                Get sample ID

                :rtype: Sample ID string

      |

         .. function:: calculateroundtrip(self, t1, t2):

                Compute time difference in minutes between time t1 = [h1, m1] and t2 = [h2, m2], t1 later than t2

                :param t1: starting time [hour, minute]
                :type t1: list
                :param t2: ending time [hour, minute]
                :type t2: list
                :rtype: Number of minutes, or -1 if t1 is earlies than t2

|

  .. class:: Edge

      Nested class in Graph. Edge structure for Graph

      .. function:: __init__(self, u, v):

         Create a new Edge object

         :param self._origin=u: origin
         :type self._origin=u: Station
         :param self._destination=v: destination
         :type self._destination=v: Station
         :param self._weight: dictionary holding the traveling time between the origin and destination stations for two time periods, morning and evening
         :type: dictionary
         :rtype: New Edge object

  |

      .. function:: endpoints(self):

         Return end points of the directed edge

         :rtype: (origin, destination) tuple

  |

      .. function:: opposite(self, v):

         Return the vertex on the opposite end of the edge connected to v

         :param v: vertex
         :type v: Station
         :rtype: Station object connected to v by the Edge

  |

      .. function:: weight(self, curr_time):

         Return traveling time on the edge, if its before noon, return the morning summarized traveling time, otherwise return the evening summarized traveling time

         :param curr_time: current time of day [hour, minute]
         :type curr_time: list
         :rtype: Traveling time in minutes

  |

      .. function:: set_weight(self, morning, evening):

         Set the weight of the edge

         :param morning: summarized traveling time before noon in minutes
         :type morning: int
         :param evening: summarized traveling time after noon in minutes
         :type afternoon: int
         :rtype: None

|

Minimum Binary Heap
-------------------

.. class:: MinBinaryHeap

   Array representation of a minimum binary heap

   .. function:: __init__(self, idle, start_time):

       Create an initially empty binary heap

       :param self._nodes = []: list of Node objects in the heap
       :type self._nodes = []: list
       :param self._idle: 1 if ranked by idle time value, 0 if ranked by total time value
       :type self._idle: int
       :param self._start_time:  fixed starting time of all paths in the heap  [hour, minute]
       :type self._start_time: list
       :rtype: New MinBinaryHeap object

|

   .. function:: get_min(self):

      Return Node with minimum value (i.e. root Node):

      :rtype: Node object

|

   .. function:: insert(self, path, unique = None):

      Creates a node to hold the Path object and inserts the new Node into the heap

      :param path: a set of sequential tasks
      :type path: Path
      :param unique: uniqueness score, so that the node sets uniqueness score as the value, if None, uniqueness score is not considered in the value
      :type unique: float or None
      :rtype: None

|

  .. function:: is_empty(self):

     Checks status of heap

     :rtype: True if the heap is empty, False otherwise

|

  .. function:: extract_min(self):

     Removes the Node with minimum value in the heap and returns the Path object stored in that Node

     :rtype: Path object with smallest value (shortest idle time or total time):

|

  .. function:: get_starttime(self):

     Returns start time of the heap in [hour, minute] form

     :rtype: List [hour, minute] representing the start time

|

  .. function:: is_idle(self):

     Checks whether the heap is sorted by idle time or total time

     :rtype: True if sorted by idle time, False otherwise

|

  .. function:: get_node(self, i):

     Returns the node at the ith index in the heap array

     :param i: index
     :type i: int
     :rtype: Node object at the ith index of the heap array

|

  .. function:: get_value(self, node):

     Return the value of the Node

     :param node: Node object from the heap
     :type node: Node
     :rtype: Int value of the node

|

  .. function:: swap_nodes(self, i, j):

      Swap the two nodes at the indexes i and j in the heap array

      :param i: index of the first node
      :type i: int
      :param j: index of the second node
      :type j: int
      :rtype: None

|

  .. function:: upheap(self):

     Update heap after inserting new node in order to maintain min-heap structure

     :rtype: None

|

  .. function:: downheap(self):

     Update heap after removing min node in order to maintain min-heap structure

     :rtype: None

|

  .. class:: Node

      Nested class in MinBinaryHeap for storing a single path

      .. function:: __init__(self, path, position):

          Create a new Node object for storing a Path Object

          :param self._path: Path object stored in the node
          :type self._path: Path
          :param self._position: index of the Node in the heap array
          :type self._position: int
          :param self._unique: uniqueness score
          :type self._unique: float or 0 by default
          :rtype: New Node object

  |

      .. function:: get_path(self):

         Return Path object stored in the Node

         :rtype: Path object stored in the Node

  |

      .. function:: get_parent(self):

         Return index of parent node

        :rtype: int

  |

      .. function:: get_leftchild(self):

         Return index of left child node

         :rtype:int

  |

      .. function:: get_rightchild(self):

         Return index of right child node

         :rtype: int

  |

      .. function:: get_position(self):

         Return index of the Node

         :rtype: int

  |

      .. function:: set_position(self, i):

         Set the index of the Node

         :param i: index
         :type i: int
         :rtype: None

  |

      .. function:: get_unique(self):

         Get uniqueness score of path associated to the Node

         :rtype: float or 0 by default

  |

      .. function:: set_unique(self, value):

         Set uniqueness score of the Node

         :param value: uniqueness score
         :type: float
         :rtype: None

|

Path
----

.. class:: Path

   Representation of a sequential set of tasks (samples):

   .. function:: __init__(self, path, idleTime, pathTime, time_of_day, lunchbreak = 0, start_time = None):

      Initiate a new Path object

      :param self._idleTime: total idle time of the path in minutes
      :type self._idleTime: int
      :param self._pathTime: total time of the path in minutes
      :type self._pathTime: int
      :param self._path: list of Task objects in the path
      :type self._path: list
      :param self._timeofday: [hour, minute] time of day tracker used when extending paths
      :type self._timeofday: list
      :param self._lunchbreak: 1 if scheduled, 0 if not scheduled
      :type self._lunchbreak: int
      :param self._uniqueness: uniqueness score of the path
      :type self._uniqueness: float
      :param self._starttime: starting time of the path [hour, minute]
      :type self._starttime: list
      :param self._assigned: 0 if the Path has been assigned, 1 otherwise
      :type self._assigned: int
      :rtype: New Path object

|

  .. function:: toggle_assigned(self, e):

     Change the assigned state of the Path

     :param e: state value to change to
     :type e: int
     :rtype: None

|

  .. function:: is_assigned(self):

     Check if the Path has been assigned

     :rtype: 0 if assigned, 1 otherwise

|

  .. function:: get_starttime(self):

     Get starting time of the Path

     :rtype: [hour, minute] starting time

|

  .. function:: get_uniqueness(self):

     Get uniqueness score of the Path

     :rtype: Uniqueness score

|

   .. function:: set_uniqueness(self, value):

      Set uniqueness score of the Path

      :param value: new uniqueness score
      :type value: float
      :rtype: None

|

   .. function:: get_idleTime(self):

      Return idle time of the Path

      :rtype: Idle time in minutes

|

  .. function:: get_pathTime(self):

     Return total time of the Path

     :rtype: Total time in minutes

|

  .. function:: get_tasklist(self):

     Return a list of Task objects stored in the Path

     :rtype: List of Task objects

|

  .. function:: get_startnode(self):

     Return first task in the Path

     :rtype: Task object

|

  .. function:: get_endnode(self):

     Return last task in the Path

     :rtype: Task object

|

  .. function:: get_timeofday(self):

     Return the time of day when the last Task in the Path is completed

     :rtype: [hour, minute]

|

  .. function:: updatetime(self, t):

     Update the time of day once t time has passed, t = [hour, minute]

     :param t: time passed in the form [hour, minute]
     :type t: list
     :rtype: None

|

   .. function:: updatetotaltime(self, t):

      Update total time of the Path

      :param t: increased total time in minutes
      :type t: int
      :rtype: None

|

   .. function:: updateidletime(self, t):

      Update idle time of the Path

      :param t: increased idle time in minutes
      :type t: int
      :rtype: None

|

   .. function:: hadlunchbreak(self):

      Check if a lunchbreak has been included in the Path

      :rtype: 1 if lunchbreak is included, 0 otherwise

|

   .. function:: addlunchbreak(self, next_stop, timeofday):

      Add a lunch break at a station to the Path

      :param next_stop: location of lunch lunchbreak
      :type next_stop: Station
      :param timeofday: starting time of lunchbreak [hour, minute]
      :type: list
      :rtype: None

|

   .. function:: extend(self, next_stop, sample):

      Extend the Path by adding a new Task of completing a certain Sample at a certain Station

      :param next_stop: location of extended Task
      :type next_stop: Station
      :param sample: sample to complete in extended Task, if its "LIC" or lunchbreak, then a string is assigned, otherwise a Sample object is assigned
      :type sample: string or Sample
      :rtype: New extended Path object

|

   .. function:: numoftasks(self):

      Return the number of Tasks in the Path, excluding the starting and ending points at "LIC"

      :rtype: Number of Tasks

|

   .. class:: Task

      Nested class of Path, containing information on one Sample that needs to be checked

      .. function:: __init__(self, station, sample):

        Initiate new Task object

        :param self._station: location of Task
        :type self._station: Station
        :param self._sample: Sample to be checked in the Task or a string representing start, end, or lunchbreak
        :type self._sample: String or Sample
        :rtype: New Task object

   |

      .. function:: get_station(self):

         Get Station where the Task is performed

         :rtype: Station object

   |

      .. function:: get_sample(self):

         Get Sample done through the Task

         :rtype: Sample object or string representing start, end, or lunchbreak



Checker and CheckerList
-----------------------

.. class:: CheckerList

   Representation of a list of Checker objects

   .. function:: __init__(self):

      Initialize empty CheckerList object

      :param self._checkerlist: List of Checker objects
      :type self._checkerlist: list
      :rtype: New CheckerList object

|

   .. function:: get_checker(self, i):

      Get the ith Checker in the CheckerList

      :param i: index
      :type i: int
      :rtype: Checker object or None Type if index is out of range

|

   .. function:: get_checkerlist(self):

      Return a iterable containing all Checker objects

      :rtype: Iterable containing all Checker objects

|

   .. function:: shuffle_checkerlist(self):

      Randomly reorder Checker objects

      :rtype: None

|

   .. function:: add_checker(self, checkerid, startshift, endshift, daysoff, workstatus):

      Create a new Checker object and add it to the list stored in the CheckerList

      :param checkerid: checker ID
      :type checkerid: string
      :param startshift: checker earliest shift starting time [hour, minute]
      :type startshift: list
      :param endshift: checker latest shift ending time [hour, minute]
      :type endshift: list
      :param daysoff: list of days off indexes, e.g. [5,6] means Saturday and Sunday are days off
      :type daysoff: list
      :param workstatus: 0 if part-time, 1 if full-time
      :type workstatus: int
      :rtype: None

|

   .. function:: select_checkers(self, num):

      Randomly select a number of checkers and return them in the form of a new CheckerList

      :param num: number of checkers to select
      :type num: int
      :rtype: CheckerList object

|

   .. function:: get_uniqueness_score(self, filename):

      Calculate and set the uniqueness score for all valid paths of each Checker

      :param filename: filename of sample data file
      :type filename: string
      :rtype: None

|

   .. function:: restructure(self):

      Reorder valid paths of each checker based on uniqueness score

      :rtype: None

|

   .. function:: reorder_checkers(self)

      Reorder checkers based on the total number of valid paths

      :rtype: None

|

   .. class:: Checker

      Nested class in CheckerList representing each Checker

      .. function:: __init__(self, checkerid, startshift, endshift, daysoff, workstatus):

          Initialize Checker object

          :param self._checkerid: checker ID
          :type self._checkerid: string
          :param self._startshift: checker earliest shift starting time [hour, minute]
          :type self._startshift: list
          :param self._endshift: checker latest shift ending time [hour, minute]
          :type self._endshift: list
          :param self._daysoff: list of days off indexes, e.g. [5,6] means Saturday and Sunday are days off
          :type self._daysoff: list
          :param self._workstatus: 0 if part-time, 1 if full-time
          :type self._workstatus: int
          :param self._validpaths: dictionary of dictionaries with day types and starting times as keys and valid path queue s as values
          :type self._validpaths: dictionary
          :param self._taskcount: number of tasks covered by the valid path heaps
          :type self._taskcount: int
          :param self._uniqueness: uniqueness score of the Checker
          :type self._uniqueness: float
          :rtype: New Checker object

   |

     .. function:: set_uniqueness(self, value):

        Set uniqueness score

        :param value: uniqueness score
        :type value: float
        :rtype: None

   |

     .. function:: get_uniqueness(self):

        Get uniqueness score

        :rtype: Uniqueness score float

   |

     .. function:: checkerid(self):

        Get checker ID

        :rtype: Checker ID string

   |

     .. function:: startshift(self):

        Get earliest shift starting time

        :rtype: [hour,minute] list

   |

     .. function:: endshift(self):

        Get latest shift ending time

        :rtype: [hour,minute] list

   |

     .. function:: daysoff(self):

        Get days off

        :rtype: List of day type indexes e.g [0,6] means Monday and Sunday off

   |

     .. function:: workstatus(self):

        Get work status

        :rtype: 0 if part-time, 1 if full-time

   |

     .. function:: validpaths(self):

        Get all valid paths of the Checker

        :rtype: Dictionary of dictionaries, with day types, starting times as keys and valid path queues as values

   |

     .. function:: update_validpaths(self, heap, daytype):

        Add a heap of valid paths to the valid paths dictionary in the form of a queue based on daytype and shift starting time

        :param heap: minimum binary heap containing valid paths
        :type heap: MinBinaryHeap
        :param daytype: day type associated to the paths in the heap
        :type daytype: string

   |

     .. function:: set_taskcount(self, value):

        Set task count of the Checker

        :param value: new number of tasks
        :type value: int
        :rtype: None

   |

     .. function:: get_taskcount(self):

        Get task count of the Checker

        :rtype: Int value representing the number of tasks covered by all the valid paths of the Checker

|

Simple Queue
------------

.. class:: Queue

   Simple Queue structure for storing and accessing tasks quickly

   .. function:: __init__(self):

      Initialize empty Queue

      :param self._queue: list used for retrieving, changes size when retrieving elements
      :type self._queue: list
      :param self._data: list used for tracking data stored in the Queue, does not change once insertion is complete
      :type self._data: list
      :rtype: Queue object

|

   .. function:: add(self, e):

      Add element to the Queue

      :param e: element
      :rtype: None

|

   .. function:: get_first(self):

      Retrieve first element inserted into the Queue

|

   .. function:: get_data(self):

      Get iterable of all data previously stored in the Queue

      :rtype: Iterable

|

   .. function:: replenish(self):

      Used to fill up the Queue with the data originally stored, once the Queue is empty, i.e. returning the Queue to its original state

      :rtype: None

|


   .. function:: length(self):

      Return the length of the Queue, note that this is not the length of the data

      :rtype: Int

|

Schedule
--------

.. class:: Schedule

   Monthly schedule, also representing a chromosome

   .. function:: __init__(self, checkerlist, onoff, mutationRate = None, schedule = [], month = None, year = None):

      Initialize empty Schedule

      :param self._schedule: list of lists of Week Objects
      :type self._schedule: list
      :param self._checkerlist: CheckerList object
      :type self._checkerlist: CheckerList
      :param self._fitness: fitness score
      :type self._fitness: int
      :param self._onoff: on/off switch dictionary with sample ids as keys and 0 or 1 as values
      :type self._onoff: dictionary
      :param self._month: month of schedule
      :type self._month: int
      :param self._year: year of schedule
      :type self._year: int
      :param self._mutationRate: probability to mutate
      :type self._mutationRate: float

|

  .. function:: get_fitness(self):

     Return fitness score

     :rtype: Fitness score of schedule

|

  .. function:: set_fitness(self):

    Use Score = 1 + (-total_idle + total)/total + (- overlap + covered - empty)/total_paths to calculate and update fitness score

    :rtype: Updated fitness score of schedule

|

  .. function:: mutate(self):

     Go through each day in the schedule, based on mutation rate perform mutation on day tasks, swapping previous day tasks with those in the gene pool (valid path collection)

     :rtype: None

|

  .. function:: crossover(self, other):

     Perform crossover (with weeks as units) between self and other to create crossover offspring

     :param other: the other parent schedule participating in crossover
     :type other: Schedule
     :rtype: New Schedule object

|

  .. function:: update_onoff(self):

     Goes through the Schedule and updates the onoff switches based on changes that occured in the Schedule

     :rtype: None

|

  .. function:: initialize(self):

    Randomly create a schedule. Note that the schedule initialize function will create 6 weeks for each checker and call week.initialize(month, year) to initialize each week

    :rtype: None

|

  .. function:: export(self, filename):

     Export schedule to .xls file, with each Checker's full month schedule located in separate sheets of the workbook

     :param filename: name of output file
     :type filename: string
     :rtype: None

|

  .. function:: display(self):

     Display Schedule in the terminal. Prints out day schedules assigned and displays idle time and total time of shifts for each working day

     :rtype: None

|

  .. function:: evaluate(self, gui=None)

     Calculate and display the total number of samples assigned, total number of samples covered, total number of overlaps and total number of empty days. Display is done in the terminal if the gui object is None

     :param gui: gui object for displaying the info in the gui
     :type gui: tkinter.Text or None
     :rtype: None

|

  .. function:: onoff_assignment(self, iterations):

     Assigns day tasks to all checkers for each day of the month. Uses order of CheckerList to assign full month schedules one by one. For each full month schedule, it calls the week.onoff_assignment function to assign tasks for each Week object

     :param iterations: the number of times to repeat the (accumulative) process of assignment over the entire CheckerList (goal is to fill up possible empty days)
     :type iterations: int
     :rtype: None

|

  .. function:: refresh(self, missing_samples, week_num):

      Update schedule based on missing samples. First, switch off missed samples, then call week.refresh for the weeks after the modification point

      :param missing_samples: list of missing sample IDs
      :type missing_samples: list
      :param week_num: modification point, corresponds to the index of the week where the update starts, value between 0 and 5
      :type week_num: int
      :rtype: None

|

  .. function:: evaluate_refresh(self, missing_samples, week_num, gui = None):

     Compare and evaluate refreshed schedule with previous schedule. Print out evaluations in terminal or gui

     :param missing_samples: list of missing sample IDs
     :type missing_samples: list
     :param week_num: modification point, corresponds to the index of the week where the update starts, value between 0 and 5
     :type week_num: int
     :param gui: gui object for displaying evaluations in the gui
     :type gui: tkinter.Text or None

|

Week and Day
------------

.. class:: Week

   Weekly schedule, also represents a part of the chromosome

   .. function:: __init__(self, checker, weeknumber):

      Initializes an empty Week object

      :param self._week: list of Day object, week schedule
      :type self._week: list
      :param self._checker: Checker corresponding to the Week schedule
      :type self._checker: Checker
      :param self._weeknumber: the ith week (values from 1 to 6), is equal to the index of the week + 1
      :type self._weeknumber: int
      :param self._population: a dictionary containing all valid tasks regardless of daytype that begin at the same given starting time window
      :type self._population: dictionary
      :param self._starttime: [hour, minute], the earliest starting time possible in the 3-hour window for the week
      :type self._starttime: list
      :rtype: New Week object

|

  .. function:: initialize(self, month, year):

     Initialize week schedule by creating Day objects and adding them to the week schedule list, block off days off and border days not within the month, i.e. a Thursday that is in March not April, then randomly selects a earliest starting shift time, thus, determining the starting time window and setting the population. Randomly assigns day tasks from population for each Day object

     :param month: month of schedule
     :type month: int
     :param year: year of schedule
     :type year: int
     :rtype: None

|

  .. function:: create_empty(self, month, year):

     Initialize week schedule by creating empty Day objects

     :param month: month of schedule
     :type month: int
     :param year: year of schedule
     :type year: int
     :rtype: None

|

  .. function:: onoff_assignment(self, on_off):

     Use on/off switch to restrict assignment, go through possible shift window selections, checking the windows with a larger valid path set available first. Assign tasks for each day without overlap, assign those with higher uniqueness scores first. If a window does not have enough tasks to assign a full week, we clear the week and proceed to check the next best shift window. If all windows can't assign a full week, we clear the week, end the assignment process

     :param on_off: onoff switch dictionary
     :type on_off: dictionary
     :rtype: None

|

  .. function:: fillup(self, on_off):

     After the full schedule of the month is generated, we go back to the weeks that have been emptied since a full week assignment was not possible and use this function to fill up the weeks as much as possible to achieve a partial week assignment

     :param on_off: onoff switch dictionary
     :type on_off: dictionary
     :rtype: None

|

  .. function:: refresh(self, onoff):

     Clear out the week and update the onoff switch, then call self.onoff_assignment to reassign tasks based on updated on/off switch

     :param onoff: onoff switch dictionary
     :type onoff: dictionary
     :rtype: None

|

  .. function:: get_starttime(self):

     Get earliest shift start time within the 3-hour window

     :rtype: [hour,minute] list

|

  .. function:: get_population(self):

     Get dictionary containing all valid paths of the Checker corresponding to the given start_time window

     :rtype: Dictionary of lists, with day types as keys, and lists of valid path queues, ordered by size (total number of path in the heap)

|

  .. function:: get_weeknumber(self):

     Get Week Number i meaning the ith week of the month

     :rtype: Integer between 1 and 6

|

  .. function:: get_checker(self):

     Get checker associated to this week

     :rtype: Checker object

|

  .. function:: get_day(self, i):

     Return the corresponding day object to the index i

     :param i: index
     :type i: int
     :rtype: Day object at index i or None if index is out of range

|

  .. function:: get_days(self):

     Iteratable that returns the Day objects in the week

     :rtype: Iterable of Day objects

|

  .. class:: Day

    Nested Day class within Week clas

    .. function:: __init__(self, path, date):

      Initialize empty Day object

      :param self._path: Path object, i.e. the set of samples assigned to be checked on this day
      :type self._path: Path
      :param date: [date, daytype] list representing this day
      :type date: list
      :rtype: New Day object

  |

    .. function:: is_empty(self):

      Checks if a Day task has been assigned to this day or not

      :rtype: True if a Day task is assigned, False otherwise

  |

    .. function:: set_path(self, path):

      Set the path (set of samples) of the day

      :rtype: None

  |

    .. function:: get_path(self):

      Get the path (set of samples) of the day

      :rtype: Path object

  |

    .. function:: get_date(self):

      Get the date of the day

      :rtype: [date,daytype] list

  |

    .. function:: is_sat(self):

       Check if its a Saturday

       :rtype: True if Saturday, False otherwise

  |

    .. function:: is_sun(self):

       Check if its a Sunday

       :rtype: True if Sunday, False otherwise


  |

    .. function:: is_blocked(self):

       Check if the day is blocked, i.e. self._date[0] == 0

       :rtype: True if blocked, False otherwise

  |

    .. function:: is_dayoff(self):

       Check if its a day off

       rtype: True if it is a day off, False otherwise

|

Generation
----------

.. class:: Generation

   Generation of schedules

   .. function:: __init__(self, generationNumber, size, mutationRate, fitnessThreshold, month, year, onoff, checkerlist, generation = []):

      Initiate and empty Generation 0

      :param self._generation: List of schedules in the generation
      :type self._generation: list
      :param self._generationNumber: generation number such as Gen 0
      :type self._generationNumber: int
      :param self._size: number of schedules in the generation
      :type self._size: int
      :param self._mutationRate: the probability of mutation during reproduction for all individuals
      :type self._mutationRate: float
      :param self._fitnessThreshold: the minimum fitness score an individual must have to participate in reproduction (added to the mating pool)
      :type self._fitnessThreshold: float
      :param self._month: month of schedule
      :type self._month: int
      :param self._year: year of schedule
      :type self._year: int
      :param self._onoff: onoff switch dictionary
      :type self._onoff: dictionary
      :param self._checkerlist: CheckerList object
      :type: self._checkerlist: CheckerList
      :param self._mating_pool: list of individuals that are capable of participating in reproduction
      :type self._mating_pool: list
      :param self._elites: list of individuals that are capable of moving directly into the next generation
      :type self._elites: list
      :rtype: New Generation object

|

  .. function:: initialize(self):

     Randomly initialize a generation of schedules --> Gen 0, use self._size to create a fixed number of Schedules then call Schedule.initialize to initialize each Schedule

     :rtype: None

|

  .. function:: natural_selection(self):

     Calculate and normalize fitness scores of the generation. Based on fitness scores, eliminate individuals from reproduction and add those who are capable to the mating pool. Those with higher fitness scores get added a larger number of times, corresponding to a higher possibility of reproducing

     :rtype: None

|

  .. function:: reproduce(self):

     Randomly select two parent schedules from the mating pool to perform crossover, creating one new child schedule, and letting it mutate. The process is repeated until the number of offspring is equal to the required generation size. Return the next generation

     :rtype: Next Generation

|

  .. function:: get_bestIndividual(self):

     Find the schedule with the best fitness score and return it

     :rtype: Schedule object with the best fitness score in the Generation
