"""# Load Packages"""

from onoff import *
from bfehelper import *
import bfehelper
from shortestpath import *

"""# Classes

## Graph
"""

class Graph:
    """Representation of a simple graph using an adjacency map."""

    #------------------------- nested Station class -------------------------
    class Station:
        """Lightweight vertex structure for a graph."""
        __slots__ = '_station', '_samples', '_coord'

        def __init__(self, station, coord):
            """Do not call constructor directly. Use Graph's insert_vertex(x)."""
            self._station = station #station_name
            self._coord = coord
            self._samples = []

        def get_lat(self):
            return self._coord[0]

        def get_long(self):
            return self._coord[1]

        def station(self):
            """Return element associated with this vertex."""
            return self._station

        def samples(self):
            """Return routes associated with this vertex."""
            for sample in self._samples:
                yield sample

        def __hash__(self):         # will allow vertex to be a map/set key
            return hash(id(self))

        def __str__(self):
            return str(self._station)

        def __repr__(self):
            return str(self._station)

        def insert_sample(self, routename, arrival_time, departure_time, sample_id):
            sample = self.Sample(routename, arrival_time, departure_time, sample_id)
            self._samples.append(sample)

      #------------------------- nested Route class -------------------------
        class Sample:
            __slots__ = '_routename', '_arrivalTime', '_departureTime', '_roundtripTime', '_sample_id'
            def __init__(self, routename, arrivaltime, departuretime, sample_id):
              self._routename = routename
              self._arrivalTime = arrivaltime
              self._departureTime = departuretime
              self._roundtripTime = self.calculateroundtrip(arrivaltime, departuretime)
              self._sample_id = sample_id

            def routename(self):
              return self._routename

            def roundtriptime(self):
              return self._roundtripTime

            def departuretime(self):
              return self._departureTime

            def arrivaltime(self):
              return self._arrivalTime

            def sample_id(self):
              return self._sample_id

            def calculateroundtrip(self, t1, t2):
              """Compute time differenct between time t1 = [h1, m1] and t2 = [h2, m2]"""
              hour_diff = (t1[0]-t2[0])*60
              minute_diff = t1[1] - t2[1]
              if hour_diff > 0:
                return hour_diff + minute_diff
              elif hour_diff == 0 and minute_diff >= 0:
                return minute_diff
              elif hour_diff < 0 and t1[0] == 0:
                return (24 - t2[0])*60 + minute_diff
              else:
                print("Error, arrives before departure")
                print(t1, t2)
                return -1

    #------------------------- nested Edge class -------------------------
    class Edge:
        """Lightweight edge structure for a graph."""
        __slots__ = '_origin', '_destination', '_weight'

        def __init__(self, u, v):
            """Do not call constructor directly. Use Graph's insert_edge(u,v,x)."""
            self._origin = u
            self._destination = v
            self._weight = {}

        def endpoints(self):
            """Return (u,v) tuple for vertices u and v."""
            return (self._origin, self._destination)

        def opposite(self, v):
            """Return the vertex that is opposite v on this edge."""
            #if not isinstance(v, Graph.Station):
                #print(type(v))
                #raise TypeError('v must be a Vertex')
            return self._destination if v is self._origin else self._origin
            raise ValueError('v not incident to edge')

        def weight(self, curr_time):
            if curr_time[0]<12:
              return self._weight["morning"]
            return self._weight["evening"]

        def set_weight(self, morning, evening):
            self._weight["morning"] = morning
            self._weight["evening"] = evening

        def __hash__(self):         # will allow edge to be a map/set key
            return hash( (self._origin, self._destination) )

        def __str__(self):
            return '({0},{1},{2})'.format(self._origin,self._destination,self._weight)

        def __repr__(self):
            return '({0},{1},{2})'.format(self._origin,self._destination,self._weight)

    #------------------------- Graph methods -------------------------
    def __init__(self, directed=True, borough=None, daytype=None):
        """Create an empty graph (directed, by default).

        Graph is directed if optional paramter is set to True.
        """
        self._vertices = {}
        self._outgoing = {}
        # only create second map for directed graph; use alias for undirected
        self._incoming = {} if directed else self._outgoing
        self._borough = borough
        self._daytype = daytype

    def get_borough(self):
        return self._borough

    def get_daytype(self):
        return self._daytype

    def _validate_vertex(self, v):
        """Verify that v is a Vertex of this graph."""
        if not isinstance(v, self.Station):
            raise TypeError('Station expected')
        if v not in self._outgoing:
            raise ValueError('Station does not belong to this graph.')

    def is_directed(self):
        """Return True if this is a directed graph; False if undirected.

        Property is based on the original declaration of the graph, not its contents.
        """
        return self._incoming is not self._outgoing # directed if maps are distinct

    def vertex_count(self):
        """Return the number of vertices in the graph."""
        return len(self._outgoing)

    def vertices(self):
        """Return an iterable of all vertices of the graph."""
        return self._outgoing.keys()

    def edge_count(self):
        """Return the number of edges in the graph."""
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        # for undirected graphs, make sure not to double-count edges
        return total if self.is_directed() else total // 2

    def edges(self):
        """Return a set of all edges of the graph."""
        result = set()       # avoid double-reporting edges of undirected graph
        for secondary_map in self._outgoing.values():
          result.update(secondary_map.values())    # add edges to resulting set
        return result

    def get_edge(self, u, v):
        """Return the edge from u to v, or None if not adjacent."""
        self._validate_vertex(u)
        self._validate_vertex(v)
        return self._outgoing[u].get(v)        # returns None if v not adjacent

    def incident_edges(self, v, outgoing=True):
        """Return all (outgoing) edges incident to vertex v in the graph.

        If graph is directed, optional parameter used to request incoming edges.
        """
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge

    def get_vertex(self, station):
        """Get a Vertex."""
        return self._vertices.get(station, None)

    def insert_vertex(self, station, coord):
        """Insert and return a new Vertex."""
        if self._vertices.get(station, 0) == 0:
          v = self.Station(station, coord)
          self._outgoing[v] = {}
          if self.is_directed():
            self._incoming[v] = {}        # need distinct map for incoming edges
          self._vertices[station] = v
        else:
          v = self._vertices[station]
        return v

    def insert_edge(self, u, v, route = None, arrivaltime = None, departuretime = None, sample_id = None):
        """Insert and return a new Edge from u to v.

        Raise a ValueError if u and v are not vertices of the graph.
        Raise a ValueError if u and v are already adjacent.
        """
        e1 = self.Edge(u, v)
        e2 = self.Edge(v, u)
        if route != None:
          u.insert_sample(route, arrivaltime, departuretime, sample_id)
        if self.get_edge(u, v) is None:
          self._outgoing[u][v] = e1
        if self.get_edge(v, u) is None:
          self._incoming[v][u] = e2

    def __str__(self):
        if self._outgoing is self._incoming:
            return str(self._outgoing)
        else:
            return str(self._outgoing) + "\n" + str(self._incoming)

    def remove_vertex(self, v):
        '''
        @v: a Graph.Vertex object. The vertex to remove from the self graph.
        Remove vertex v from self._incoming and self._outgoing.
        Your code should work for both directed & undirected graph.

        @return: Nothing
        '''
        self._vertices.pop(v.station())
        self._outgoing.pop(v)
        for i in self._outgoing.values():
            if v in i:
                i.pop(v)
        if self.is_directed():
            self._incoming.pop(v)
            for i in self._incoming.values():
                if v in i:
                    i.pop(v)


    def remove_edge(self, u, v):
        '''
        @u: a Graph.Vertex object.
        @v: a Graph.Vertex object.
        If the graph is directed, remove the edge that goes from u to v only.
        If the graph is undirected, remove the edge that connects u and v.

        @return: Nothing
        '''
        self._outgoing[u].pop(v)
        self._incoming[v].pop(u)

"""## Minimum Binary Heap"""

class MinBinaryHeap:
    """Array representation of a minimum binary heap"""

    #-------------------------- nested _PathNode class ------------------------------------

    class Node:
        """Lightweight, nonpublic class for storing a single path."""
        __slots__ = '_path', '_position', '_unique'  #streamline memory usage

        def __init__(self, path, position):
            self._path  = path #Path class instance
            self._position = position
            self._unique = 0

    #------------------------------- PathNode methods --------------------------------------

        def get_path(self):
            """Return Path instance stored in the node"""
            return self._path

        def get_parent(self):
            """Return index of parent node"""
            return self._position//2

        def get_leftchild(self):
            """Return index of leftchild node"""
            return 2*self._position

        def get_rightchild(self):
            """Return index of rightchild node"""
            return 2*self._position+1

        def get_position(self):
            """Return index of node"""
            return 2*self._position+1

        def set_position(self, i):
            """Set index of node"""
            self._position = i

        def get_unique(self):
            return self._unique

        def set_unique(self, value):
            self._unique = value

    #-------------------------- binary heap constructor --------------------------

    def __init__(self, idle, start_time):
        """Create an initially empty binary heap."""
        self._nodes = []
        self._idle = idle
        self._starttime = start_time

    #-------------------------- public accessors --------------------------

    def __len__(self):
        """Return the total number of elements in the tree."""
        return len(self._nodes)

    def get_min(self):
        """Return the shortest path in the heap."""
        if len(self._nodes) != 0:
            return self._nodes[0]
        return None

    def insert(self, path, unique = None):
        """Insert a path in the heap."""
        position = len(self._nodes)
        node = self.Node(path, position)
        if unique != None:
          node.set_unique(unique)
        self._nodes.append(node)
        self.upheap()

    def is_empty(self):
        '''Check status of heap'''
        return len(self._nodes) == 0

    def extract_min(self):
        """Remove and return the shortest path in the heap."""
        if len(self._nodes) == 0:
            return None
        #print(len(self._nodes))
        self._nodes[-1], self._nodes[0] = self._nodes[0], self._nodes[-1]
        min_path = self._nodes.pop().get_path()
        if len(self._nodes) != 0:
          self.downheap()
        return min_path

    def get_starttime(self):
        return self._starttime


    #-------------------------- nonpublic mutators --------------------------
    def is_idle(self):
        """Returns True if the binary heap compare idle time, False if it compares total time"""
        return self._idle

    def get_node(self, i):
        """Return the node at index i"""
        if i >= len(self._nodes):
            return None
        return self._nodes[i]

    def get_value(self, node):
        """Return the value of the node based on the comparison parameter determined by is_idle"""
        if self.is_idle():
            return node.get_path().numoftasks() + node.get_path().get_idleTime()/node.get_path().get_pathTime() + node.get_unique()
        return node.get_path().get_pathTime()

    def swap_nodes(self, i, j):
        """Swap the two nodes at indexes i and j"""
        node1 = self.get_node(i)
        node2 = self.get_node(j)
        if node1 == None or node2 == None:
            return
        node1.set_position(j)
        node2.set_position(i)
        self._nodes[i], self._nodes[j] = node2, node1

    def upheap(self):
        """Update heap after inserting new node in order to maintain min-heap structure"""
        last_node = self.get_node(-1)
        parent_position = last_node.get_parent()
        curr_position = last_node.get_position()
        parent_node = self.get_node(parent_position)
        while self.get_value(parent_node) < self.get_value(last_node):
            if parent_position == curr_position:
                return
            self.swap_nodes(parent_position, curr_position)
            last_node = parent_node
            parent_position = last_node.get_parent()
            curr_position = last_node.get_position()
            parent_node = self.get_node(parent_position)

    def downheap(self):
        """Update heap after removing min node in order to maintain min-heap structure"""
        curr_node = self.get_node(0)
        while True:
            leftchild_position = curr_node.get_leftchild()
            rightchild_position = curr_node.get_rightchild()
            curr_position = curr_node.get_position
            leftchild = self.get_node(leftchild_position)
            rightchild = self.get_node(rightchild_position)
            if leftchild == None and rightchild == None:
                return
            elif leftchild == None:
                if self.get_value(rightchild) > self.get_value(curr_node):
                    return
                swap_nodes(rightchild_position, curr_position)
                curr_node = rightchild
            elif rightchild == None:
                if self.get_value(leftchild) > self.get_value(curr_node):
                    return
                swap_nodes(leftchild_position, curr_position)
                curr_node = leftchild
            else:
                if self.get_value(leftchild) < self.get_value(rightchild):
                    if self.get_value(leftchild) > self.get_value(curr_node):
                        return
                    swap_nodes(leftchild_position, curr_position)
                    curr_node = leftchild
                else:
                    if self.get_value(rightchild) > self.get_value(curr_node):
                        return
                    swap_nodes(rightchild_position, curr_position)
                    curr_node = rightchild

"""## Path"""

class Path:
    class Task:
        __slots__ = '_station', '_sample'
        def __init__(self, station, sample):
          self._station = station
          self._sample = sample

        def get_station(self):
            return self._station

        def get_sample(self):
            return self._sample

    """Representation of a set of consecutive tasks"""
    __slots__ = '_idleTime','_pathTime', '_path', '_timeofday', '_lunchbreak', '_uniqueness', '_starttime', '_assigned' #streamline memory usage

    def __init__(self, path, idleTime, pathTime, time_of_day, lunchbreak = 0, start_time = None):
        self._idleTime = idleTime
        self._pathTime = pathTime
        self._path  = path
        self._timeofday = time_of_day #list [hour, minute]
        self._lunchbreak = lunchbreak #1 scheduled, 0 not scheduled
        self._uniqueness = 0
        self._starttime = start_time
        self._assigned = 0
#------------------------------- Path methods --------------------------------------
    def toggle_assigned(self, e):
        self._assigned = e

    def is_assigned(self):
        return self._assigned

    def get_starttime(self):
        return self._starttime

    def get_uniqueness(self):
        return self._uniqueness

    def set_uniqueness(self, value):
        self._uniqueness = value

    def get_idleTime(self):
        """Return idle time of the path"""
        return self._idleTime

    def get_pathTime(self):
        """Return total time of the path"""
        return self._pathTime

    def get_tasklist(self):
        """Return list of tasks in the path"""
        return self._path

    def __str__(self):
        return self.get_pathlist

    def get_startnode(self):
        """Return first task in the path """
        return self._nodes[0]

    def get_endnode(self):
        """Return last task in the path """
        return self._path[-1].get_station()

    def get_timeofday(self):
        """Return time of day when the last task in the path is completed"""
        #print(type(self._timeofday))
        return self._timeofday[:]

    def updatetime(self, t):
        """Update the time of day when t time has passed, t = [hour, minute]"""
        #curr_time = self._timeofday
        self._timeofday[0] = self._timeofday[0] + t//60 + (self._timeofday[1] + t%60)//60
        self._timeofday[1] = (self._timeofday[1] + t%60)%60
        #print(self._timeofday)

    def updatetotaltime(self, t):
        """Update total time of the path"""
        self._pathTime += t

    def updateidletime(self, t):
        """Update idle time of the path"""
        self._idleTime += t

    def hadlunchbreak(self):
        return self._lunchbreak

    def addlunchbreak(self, next_stop, timeofday):
        self._lunchbreak = 1
        time = "%2d" % timeofday[0] +":" + "%2d" % timeofday[1]
        #route = self.Route("lunchbreak", scheduledtime)
        return self.extend(next_stop, "lunchbreak at " + time)

    def extend(self, next_stop, sample):
        task = self.Task(next_stop, sample)
        new = self._path[:]
        new.append(task)
        path = Path(new, self._idleTime, self._pathTime, self._timeofday[:], self._lunchbreak, self._starttime)
        return path

    def numoftasks(self):
        return len(self._path) - 2

"""## Checker and Checker List"""

class CheckerList:
  #-------------------------- nested Checker class ------------------------------------
  class Checker:
    __slots__ = '_checkerid', '_startshift', '_endshift', '_daysoff', '_validpaths', '_workstatus', '_taskcount', '_uniqueness'
    def __init__(self, checkerid, startshift, endshift, daysoff, workstatus):
      self._checkerid = checkerid
      self._startshift = startshift
      self._endshift = endshift
      self._daysoff = daysoff
      self._workstatus = workstatus
      self._validpaths = {"wkd":{}, "sat":{}, "sun":{}}
      self._taskcount = 0
      self._uniqueness = 0

    def set_uniqueness(self, value):
      self._uniqueness = value

    def get_uniqueness(self):
      return self._uniqueness

    def checkerid(self):
      return self._checkerid

    def startshift(self):
      return self._startshift

    def endshift(self):
      return self._endshift

    def daysoff(self):
      return self._daysoff

    def workstatus(self):
      return self._workstatus

    def validpaths(self):
      return self._validpaths

    def update_validpaths(self, heap, daytype):
      '''Add a heap of valid tasks to the valid tasks dictionary in the form of a queue based on daytype and shift starting time'''
      time = heap.get_starttime()
      paths = Queue()
      taskcount = self.get_taskcount()
      while not heap.is_empty():
        min_path = heap.extract_min()
        taskcount += min_path.numoftasks()-self._workstatus
        paths.add(min_path)
      self._validpaths[daytype][(time[0], time[1])] = paths
      self.set_taskcount(taskcount)

    def set_taskcount(self, value):
      self._taskcount = value

    def get_taskcount(self):
      return self._taskcount

  #-------------------------- CheckerList methods ------------------------------------
  __slots__= '_checkerlist'
  def __init__(self):
    self._checkerlist = []

  def get_checker(self, i):
    try:
      return self._checkerlist[i]
    except:
      return

  def get_checkerlist(self):
    '''Return list of checkers'''
    for i in self._checkerlist:
      yield i

  def shuffle_checkerlist(self):
    '''Reorder checkers, may be used for combinatorics'''
    random.shuffle(self._checkerlist)

  def add_checker(self, checkerid, startshift, endshift, daysoff, workstatus):
    '''Add a checker to the checker list'''
    checker = self.Checker(checkerid, startshift, endshift, daysoff, workstatus)
    self._checkerlist.append(checker)

  def select_checkers(self, num):
    "Randomly select a number of checkers"
    self.shuffle_checkerlist()
    new_checkerlist = CheckerList()
    for i in range(num):
       new_checkerlist._checkerlist.append(self.get_checker(i))
    return new_checkerlist

  def remove_checker(self, checkerid):
    '''TBD'''
    pass

  def get_uniqueness_score(self, filename):
    "Calculate and set uniqueness score"
    onoff = bfehelper.get_onandoff_sample(filename)
    checker_freq = {}
    for checker in self.get_checkerlist():
      checkeronoff = {}
      checker_id = checker.checkerid()
      for daytype in checker.validpaths():
        for time in checker.validpaths()[daytype]:
          for path in checker.validpaths()[daytype][time].get_data():
            for task in path.get_tasklist():
              try:
                sample_id = task.get_sample().sample_id()
              except:
                continue
              checkeronoff[sample_id] = checkeronoff.get(sample_id, 0) + 1
      for key in checkeronoff:
        if checkeronoff[key] != 0:
          onoff[key] += 1
      checker_freq[checker_id] = checkeronoff

    for checker in self.get_checkerlist():
      checker_id = checker.checkerid()
      checkeronoff = checker_freq[checker_id]
      checker_uniqueness = 0
      for daytype in checker.validpaths():
        for time in checker.validpaths()[daytype]:
          for path in checker.validpaths()[daytype][time].get_data():
            uniqueness = 0
            for task in path.get_tasklist():
              try:
                sample_id = task.get_sample().sample_id()
              except:
                continue
              sample_freq = checkeronoff[sample_id]
              list_freq = onoff[sample_id]
              if list_freq != 0:
                uniqueness += sample_freq/sum(checkeronoff.values()) + sum(onoff.values())/list_freq
            checker_uniqueness += uniqueness
            path.set_uniqueness(uniqueness)
      checker.set_uniqueness(checker_uniqueness)

  def restructure(self):
    "Reorder valid tasks of each checker based on uniqueness score"
    for checker in self.get_checkerlist():
      for daytype in checker.validpaths():
        for time in checker.validpaths()[daytype]:
          new_heap = MinBinaryHeap(1, time)
          for path in checker.validpaths()[daytype][time].get_data():
              uniqueness = path.get_uniqueness()
              new_heap.insert(path, uniqueness)
          new_queue = Queue()
          while not new_heap.is_empty():
            path = new_heap.extract_min()
            new_queue.add(path)
          checker.validpaths()[daytype][time] = new_queue

  def reorder_checkers(self):
    "Reorder checkers based on the total number of valid tasks"
    d = {}
    for checker in self.get_checkerlist():
      d[checker.get_taskcount()/450 + checker.get_uniqueness()] = d.get(checker.get_taskcount()/450 + checker.get_uniqueness(), []) + [checker]

    keys = sorted(list(d.keys()))

    new_checkerlist = []

    for key in keys:
      for checker in d[key]:
        new_checkerlist.append(checker)

    self._checkerlist = new_checkerlist

"""## Simple Queue"""

class Queue:
  '''Simple Queue structure for storing and accessing tasks quickly'''
  __slots__ = "_queue", "_data"
  def __init__(self):
    self._queue = []
    self._data = []

  def add(self, e):
    self._data = [e] + self._data
    self._queue = self._data[:]

  def get_first(self):
    if len(self._queue) != 0:
      return self._queue.pop()
    else:
      return -1

  def get_data(self):
    for i in self._data:
      yield i

  def replenish(self):
    self._queue = self._data[:]

  def length(self):
    return len(self._queue)

"""## Schedule"""

class Schedule:
  '''Monthly schedule representing a chromosome'''

  __slots__ = '_schedule', '_checkerlist', '_fitness', '_onoff', '_month', '_year', '_mutationRate'

  def __init__(self, checkerlist, onoff, mutationRate = None, schedule = [], month = None, year = None):
    self._schedule = schedule
    self._checkerlist = checkerlist
    self._fitness = 0
    self._onoff = onoff
    self._month = month  #used to determine days of the week and which days to block off
    self._year = year
    self._mutationRate = mutationRate

  def get_fitness(self):
    '''Return fitness score'''
    return self._fitness

  def set_fitness(self):
    '''Define a scoring function to determine the fitness score and update self._fitness accordingly
    Possible scoring method => Score = 1-idletime/totaltime - numberofoverlaps/totaltasks'''

    schedule = self._schedule
    fitness = 0
    covered = 0
    overlap = 0
    total_idle = 0
    total_paths = 0
    total = 0
    empty = 0
    for checker_list in schedule:
      for week in checker_list:
        for day in week.get_days():
          if day.is_empty():
            empty += 1
            continue
          elif day.is_blocked() or day.is_dayoff():
            continue
          path = day.get_path()
          total_idle += path.get_idleTime()
          total += path.get_pathTime()
          total_paths += path.numoftasks()

    for i in self._onoff:
        if self._onoff[i] == 1:
            covered += 1
        elif self._onoff[i] > 1:
            overlap += 1

    fitness = 1 + (-total_idle + total)/total + (- overlap + covered - empty)/total_paths

    self._fitness = fitness
    return self._fitness

  def mutate(self):
    '''Perform mutation on the schedule, no return value'''
    for checker_schedule in self._schedule:
      for week in checker_schedule:
          population = week.get_population()
          for day in week.get_days():
            if day.is_blocked() or day.is_dayoff():
              continue
            if random.random() <= self._mutationRate:
              if day.is_sat():
                day_population = population["sat"]
              elif day.is_sun():
                day_population = population["sun"]
              else:
                day_population = population["wkd"]
              path = random.choice(day_population)
              #while path.is_assigned():
                #path = random.choice(day_population)
              prev_path = day.get_path()
              prev_path.toggle_assigned(0)
              path.toggle_assigned(1)
              day.set_path(path)

    self.update_onoff()

  def crossover(self, other):
    '''Perform crossover between self and other, return crossover offspring'''
    new_schedule = []
    other_schedule = other._schedule
    for i in range(len(self._schedule)):
      checker = []
      for j in range(len(self._schedule[i])):
        if random.random() < 0.5:
          checker.append(other_schedule[i][j])
        else:
          checker.append(self._schedule[i][j])
      new_schedule.append(checker)

    onoff ={}

    for i in self._onoff:
      onoff[i] = 0

    child = Schedule(self._checkerlist, onoff, self._mutationRate, new_schedule, self._month, self._year)
    child.update_onoff()
    return child

  def update_onoff(self):
    '''Updates the onoff switches'''
    for i in self._onoff:
      self._onoff[i] = 0
    for i in self._schedule:
      for week in i:
        for day in week.get_days():
          path = day.get_path()
          try:
            for task in path.get_tasklist():
              try:
                task.get_sample().sample_id()
              except:
                continue
              self._onoff[task.get_sample().sample_id()] += 1
          except:
            continue

  def initialize(self):
    '''Randomly create a schedule, with population pools assigned accordingly, update in place, no return value
    Note that the schedule initialize will create 6 weeks for each checker and use week.initialize(month, year)'''
    for checker in self._checkerlist.get_checkerlist():
      # for each checker
      checker_month = []
      for i in range(6):
        #for each of the 6 weeks
        new_week = Week(checker, i+1)
        new_week.initialize(self._month,self._year)
        checker_month.append(new_week)
      self._schedule.append(checker_month)
    #self._schedule = select_optimal_v2(self._checkerlist, "sample450.csv", 10)._schedule
    self.update_onoff()

  def export(self, filename):
    workbook = xlwt.Workbook()
    for i in range(len(self._schedule)):
      checker = self._checkerlist.get_checker(i)
      workstatus = checker.workstatus()
      if not workstatus:
        workstatus = "Part-time"
      else:
        workstatus = "Full-time"
      sheet = workbook.add_sheet(checker.checkerid()+ "  "+ workstatus)
      for k in range(len(self._schedule[i])):
        column_counter = 0
        week = self._schedule[i][k]
        for day in week.get_days():
          row_counter = k*10
          if day.is_blocked():
            continue
          dayinfo = day.get_date()
          if dayinfo[3] == 6:
            dayname = "Sunday"
          elif dayinfo[3] == 5:
            dayname = "Saturday"
          elif dayinfo[3] == 4:
            dayname = "Friday"
          elif dayinfo[3] == 3:
            dayname = "Thursday"
          elif dayinfo[3] == 2:
            dayname = "Wednesday"
          elif dayinfo[3] == 1:
            dayname = "Tuesday"
          else:
            dayname = "Monday"
          daydata = str(dayinfo[1]) + "/" + str(dayinfo[0]) + "/" + str(dayinfo[2]) + "\t" + dayname
          sheet.write(row_counter, column_counter, daydata)
          row_counter += 1
          if day.is_empty():
            sheet.write(row_counter, column_counter, 'Empty')
            #row_counter = original_rowcounter + 10
            column_counter = (column_counter + 1) % 7
            continue
          if day.is_dayoff():
            sheet.write(row_counter, column_counter, 'Day Off')
            #row_counter = original_rowcounter + 10
            column_counter = (column_counter + 1) % 7
            continue
          path = day.get_path()
          sheet.write(row_counter, column_counter, 'Shift starts at: ' + bfehelper.displaytime(path.get_starttime()))
          row_counter += 1
          for task in path.get_tasklist():
            sample = task.get_sample()
            station = task.get_station().station()
            try:
              routename = sample.routename()
              sheet.write(row_counter, column_counter, "Route: " + routename + " at " + station + "\n\t\tStarting at: " + bfehelper.displaytime(sample.departuretime()) + "\n\t\tEnding at: " + bfehelper.displaytime(sample.arrivaltime()))
              row_counter += 1
            except:
              sheet.write(row_counter, column_counter, sample.upper() + " at " + station)
              row_counter += 1
          column_counter = (column_counter + 1) % 7
          #row_counter = original_rowcounter + 10
    workbook.save(filename)

  def display(self):
    content = ""
    for i in range(len(self._schedule)):
      checker = self._checkerlist.get_checker(i)
      workstatus = checker.workstatus()
      if not workstatus:
        workstatus = "Part-time"
      else:
        workstatus = "Full-time"
      content += checker.checkerid() + " " +  workstatus + "\n"
      for week in self._schedule[i]:
        #starttime = week.get_starttime()
        for day in week.get_days():
          if day.is_blocked():
            continue
          dayinfo = day.get_date()
          if dayinfo[3] == 6:
            dayname = "Sunday"
          elif dayinfo[3] == 5:
            dayname = "Saturday"
          elif dayinfo[3] == 4:
            dayname = "Friday"
          elif dayinfo[3] == 3:
            dayname = "Thursday"
          elif dayinfo[3] == 2:
            dayname = "Wednesday"
          elif dayinfo[3] == 1:
            dayname = "Tuesday"
          else:
            dayname = "Monday"
          content += str(dayinfo[1]) + "/" + str(dayinfo[0]) + "/" + str(dayinfo[2]) + "\t" + dayname + "\n"
          if day.is_empty():
            content += "\t Impossible\n"
            content += "\n"
            continue
          if day.is_dayoff():
            content += "\t Day Off\n"
            content += "\n"
            continue
          path = day.get_path()
          content += "Shift starts at: " + bfehelper.displaytime(path.get_starttime()) + "\n"
          for task in path.get_tasklist():
            sample = task.get_sample()
            station = task.get_station().station()
            try:
              routename = sample.routename()
              content += "\t Route: " + routename + " at " + station + "\n\t\tStarting at: " + bfehelper.displaytime(sample.departuretime()) + "\n\t\tEnding at: " + bfehelper.displaytime(sample.arrivaltime()) + "\n"
            except:
              content += "\t" + sample.upper() + " at " + station + "\n"
          total_time = path.get_pathTime()
          idle_time = path.get_idleTime()
          content += "Total Time: " + str(total_time//60) + " hours and " + str(total_time % 60) + " minutes\n"
          content += "Total Idle Time: " + str(idle_time//60) + " hours and " + str(idle_time % 60) + " minutes\n"
          content += "\n"
    print(content)
    print()
    overlap = 0
    total = 0
    for i in self._onoff:
      if self._onoff[i] == 1:
        total += 1
      if self._onoff[i] > 1:
        overlap += 1
    print("\tTotal Samples Assigned:", sum(list(self._onoff.values())))
    print("\tTotal Samples Covered:", total)
    print("\tTotal Overlaps:", overlap)


  def evaluate(self, gui = None):
    overlap = 0
    total = 0
    impossible = 0
    assigned = 0
    idle_time = 0
    total_time = 0
    for i in self._onoff:
      if self._onoff[i] == 1:
        total += 1
      if self._onoff[i] > 1:
        overlap += 1
    for checkermonth in self._schedule:
      for i in range(6):
        for day in checkermonth[i].get_days():
          if day.is_empty():
            impossible += 1
          elif day.is_blocked() or day.is_dayoff():
            continue
          else:
            idle_time += day.get_path().get_idleTime()
            total_time += day.get_path().get_pathTime()
            for task in day.get_path().get_tasklist():
              try:
                task.get_sample().sample_id()
                assigned += 1
              except:
                continue
    if gui == None:
      print("\tTotal Samples Assigned:", assigned)
      print("\tTotal Samples Covered:", total)
      print("\tTotal Overlaps:", overlap)
      print("\tTotal Empty Days:", impossible)
      print("\tIdle Time Percentage:", idle_time/total_time)
    else:
      gui.insert(tk.END, "\tTotal Samples Assigned: %d\n\tTotal Samples Covered: %d\n\tTotal Overlaps: %d\n\tTotal Empty Days: %d\n\nSchedule Statistics:\n\nRemaining Samples\n" % (sum(list(self._onoff.values())), total, overlap, impossible))


  def onoff_assignment(self, iterations):
    self._schedule = []
    for checker in self._checkerlist.get_checkerlist():
      # for each checker
      checker_month = []
      for i in range(6):
        #for each of the 6 weeks
        new_week = Week(checker, i+1)
        new_week.create_empty(self._month,self._year)
        checker_month.append(new_week)
      self._schedule.append(checker_month)
    #empty schedule created
    #assign in the following order week 1 - checker 1 - 19, week 2 - checker 1 - 19, ...
    #fill up with 3-sample tasks first, then go through the entire schedule to fill in empty days with 2-sample tasks, then 1-sample tasks
    for n in range(iterations):
      for j in range(len(self._schedule)):
        for i in range(6):
          checkermonth = self._schedule[j]
          week = checkermonth[i]
          checker = self._checkerlist.get_checker(j)
          week.onoff_assignment(self._onoff)

    for j in range(len(self._schedule)):
        for i in range(6):
          checkermonth = self._schedule[j]
          week = checkermonth[i]
          checker = self._checkerlist.get_checker(j)
          week.fillup(self._onoff)

  def refresh(self, missing_samples, week_num):
    "Update schedule based on missing samples"
    for sample_id in missing_samples:
      self._onoff[sample_id] = 0
    for j in range(len(self._schedule)):
        checkermonth = self._schedule[j]
        for i in range(week_num, 6):
          week = checkermonth[i]
          checker = self._checkerlist.get_checker(j)
          week.refresh(self._onoff)

  def evaluate_refresh(self, missing_samples, week_num, gui = None):
    completed_prev = 0
    empty_prev = 0
    missed = 0
    for j in range(len(self._schedule)):
        checkermonth = self._schedule[j]
        for i in range(week_num):
          week = checkermonth[i]
          for day in week.get_days():
            if day.is_dayoff() or day.is_blocked():
              continue
            elif day.is_empty():
              empty_prev += 1
              continue
            else:
              for task in day.get_path().get_tasklist():
                try:
                  if task.get_sample().sample_id() in missing_samples:
                    missed += 1
                  else:
                    completed_prev += 1
                except:
                  #print(task.get_sample())
                  continue

    completed_curr = 0
    empty_curr = 0
    for j in range(len(self._schedule)):
        checkermonth = self._schedule[j]
        for i in range(week_num, 6):
          week = checkermonth[i]
          for day in week.get_days():
            if day.is_dayoff() or day.is_blocked():
              continue
            elif day.is_empty():
              empty_curr += 1
              continue
            else:
              for task in day.get_path().get_tasklist():
                try:
                  task.get_sample().sample_id()
                except:
                  continue
                completed_curr += 1

    still_missed = []
    for i in missing_samples:
      if self._onoff[i] == 0:
        still_missed.append(i)

    if gui == None:
      print()
      print("Before Week %d :" % (week_num+1))
      print("%d samples assigned, %d samples completed, %d samples missed, %d Empty Days" % (completed_prev + missed, completed_prev, missed, empty_prev))
      print()
      print("After Week %d :" % (week_num+1))
      print("%d samples assigned, %d Empty Days" % (completed_curr, empty_curr))
      print()
      print("Refreshed Schedule has :")
      print("%d samples assigned, %d tasks completed, %d tasks to be done, %d total empty days" % (completed_prev + completed_curr, completed_prev, completed_curr, empty_prev + empty_curr))
      print()
      print("%d out of %d missing samples reassigned" % (len(missing_samples)-len(still_missed), len(missing_samples)))
      print()
      print("Unassigned missing samples", still_missed)
    else:
      gui.insert(tk.END, "\nBefore Week %d :\n%d samples assigned, %d samples completed, %d samples missed, %d Empty Days\n\nAfter Week %d :\n%d samples assigned, %d Empty Days\n\nRefreshed Schedule has :\n%d samples assigned, %d tasks completed, %d tasks to be done, %d total empty days\n\n%d out of %d missing samples reassigned\n\n"%(week_num+1,completed_prev + missed, completed_prev, missed, empty_prev, week_num+1,completed_curr, empty_curr,completed_prev + completed_curr, completed_prev, completed_curr, empty_prev + empty_curr,len(missing_samples)-len(still_missed), len(missing_samples)))

"""## Week and Day"""

class Week:
  class Day:
    '''Nested Day Class within each week'''

    __slots__ = '_path', '_date'

    def __init__(self, path, date):
      self._path = path
      self._date = date

    def is_empty(self):
      if self._path == None:
        return True
      return False

    def set_path(self, path):
      '''Set the path (set of tasks) of the day'''
      self._path = path

    def get_path(self):
      '''Get the path (set of tasks) of the day'''
      return self._path

    def get_date(self):
      '''Get the date of the day'''
      return self._date

    def is_sat(self):
      if self._date == "N/A":
        return False
      else:
        #print(self._date)
        if self._date[3] == 5:
          return True
        else:
          return False

    def is_sun(self):
      if self._date == "N/A":
        return False
      else:
        if self._date[3] == 6:
          return True
        else:
          return False

    def is_blocked(self):
      if self._path == "Blocked":
        return True
      else:
        return False

    def is_dayoff(self):
      if self._path == "Day Off":
        return True
      else:
        return False

  '''Weekly schedule representing a part of the chromosome'''

  __slots__ = '_week', '_checker', '_population', '_weeknumber', '_starttime'

  def __init__(self, checker, weeknumber):
    self._week = []
    self._checker = checker
    self._weeknumber = weeknumber
    self._population = None
    self._starttime = None

  def initialize(self, month, year):
    '''Randomly initialize week, block off dayoff and border days not within the month, i.e. a thursday that is in March not April
    randomly selects a starting shift time, thus, setting the population'''
    if year == None or month == None:
      now = datetime.datetime.now()
      year = now.year
      month = now.month
    validpaths = self._checker.validpaths()
    population = {"wkd":[], "sat":[], "sun":[]}
    daysoff = self._checker.daysoff()
    while True:
      if 6 in daysoff and 5 in daysoff:
        if population["wkd"] != []:
          break
      elif 6 in daysoff:
        if population["wkd"] != [] and population["sat"] != []:
          break
      elif 5 in daysoff:
        if population["wkd"] != [] and population["sun"] != []:
          break
      for daytype in validpaths:
        starting_times = validpaths[daytype].keys()
        time = random.choice(list(starting_times))
        self._starttime = time
        paths = []
        try:
          time_queue = validpaths[daytype][time]
        except:
          continue
        for path in time_queue.get_data():
          paths.append(path)
        population[daytype] = paths
      self._population = population

    for i in bfehelper.get_daytypes_week(self._weeknumber, year, month):
      if i[0] == 0:
        day = self.Day("Blocked", "N/A")
      elif i[1] in daysoff:
        #print("checkpoint")
        day = self.Day("Day Off", [i[0], month, year, i[1]])
      else:
        #assigned = 0
       #while not assigned:
         # assigned = 1
          if i[1] == 5:
            paths = self._population["sat"]
          elif i[1] == 6:
            paths = self._population["sun"]
          else:
            paths = self._population["wkd"]
          path = random.choice(paths)
          #if path.is_assigned():
          #  assigned = 0
          #else:
          path.toggle_assigned(1)
          day = self.Day(path, [i[0], month, year, i[1]])
      self._week.append(day)

  def create_empty(self, month, year):
    if year == None or month == None:
      now = datetime.datetime.now()
      year = now.year
      month = now.month
    daysoff = self._checker.daysoff()
    for i in bfehelper.get_daytypes_week(self._weeknumber, year, month):
      if i[0] == 0:
        day = self.Day("Blocked", "N/A")
      elif i[1] in daysoff:
        #print("checkpoint")
        day = self.Day("Day Off", [i[0], month, year, i[1]])
      else:
        day = self.Day(None, [i[0], month, year, i[1]])
      self._week.append(day)

  def onoff_assignment(self, on_off):
    allvalidpaths = self._checker.validpaths()
    week_empty = True
    starting_times1 = allvalidpaths["wkd"]
    starting_times2 = allvalidpaths["sat"]
    starting_times3 = allvalidpaths["sun"]
    #print(starting_times1, starting_times2, starting_times3)
    d = {}
    for time in starting_times1:
      wkd = starting_times1[time].length()
      try:
        sat = starting_times2[time].length()
      except:
        sat = 0
      try:
        sun = starting_times3[time].length()
      except:
        sun = 0
      total = wkd + sat + sun
      d[total] = d.get(total, []) + [time]
    starting_times = []
    for total in sorted(list(d.keys())):
      for time in d[total]:
        starting_times = [time] + starting_times

    while week_empty:
      time = starting_times.pop()
      self._starttime = time
      for day in self.get_days():
        if day.is_empty():
          if day.is_sat():
            validpaths = allvalidpaths["sat"][time]
          elif day.is_sun():
            validpaths = allvalidpaths["sun"][time]
            #print("check")
          else:
            validpaths = allvalidpaths["wkd"][time]
          overlap = 1
          while overlap:
            overlap = 0
            path = validpaths.get_first()
            if path == -1:
              validpaths.replenish()
              break
            path_onoff = {}
            for task in path.get_tasklist():
              try:
                task.get_sample().sample_id()
              except:
                continue
              path_onoff[task.get_sample().sample_id()] = path_onoff.get(task.get_sample().sample_id(), 0) + 1
              if on_off[task.get_sample().sample_id()] == 1 or path_onoff[task.get_sample().sample_id()] > 1:
                overlap = 1
            if not overlap:
              for task in path.get_tasklist():
                try:
                  task.get_sample().sample_id()
                except:
                  continue
                on_off[task.get_sample().sample_id()] = 1
              day.set_path(path)
      week_empty = False
      if starting_times == []:
        break
      for day in self.get_days():
        if day.is_empty():
          week_empty = True
      if week_empty:
        for day in self.get_days():
          if day.is_dayoff() or day.is_blocked() or day.is_empty():
            continue
          else:
            path = day.get_path()
            for task in path.get_tasklist():
                try:
                  task.get_sample().sample_id()
                except:
                  continue
                on_off[task.get_sample().sample_id()] = 0
            day.set_path(None)

  def fillup(self, on_off):
    allvalidpaths = self._checker.validpaths()
    week_empty = True
    starting_times1 = allvalidpaths["wkd"]
    starting_times2 = allvalidpaths["sat"]
    starting_times3 = allvalidpaths["sun"]
    #print(starting_times1, starting_times2, starting_times3)
    d = {}
    for time in starting_times1:
      wkd = starting_times1[time].length()
      try:
        sat = starting_times2[time].length()
      except:
        sat = 0
      try:
        sun = starting_times3[time].length()
      except:
        sun = 0
      total = wkd + sat + sun
      d[total] = d.get(total, []) + [time]
    starting_times = []
    for total in sorted(list(d.keys())):
      for time in d[total]:
        starting_times = [time] + starting_times

    time = starting_times.pop()
    self._starttime = time

    for day in self.get_days():
      if day.is_empty():
        if day.is_sat():
          validpaths = allvalidpaths["sat"][time]
        elif day.is_sun():
          validpaths = allvalidpaths["sun"][time]
        else:
          validpaths = allvalidpaths["wkd"][time]
        overlap = 1
        while overlap:
          overlap = 0
          path = validpaths.get_first()
          if path == -1:
            validpaths.replenish()
            break
          path_onoff = {}
          for task in path.get_tasklist():
            try:
              task.get_sample().sample_id()
            except:
              continue
            path_onoff[task.get_sample().sample_id()] = path_onoff.get(task.get_sample().sample_id(), 0) + 1
            if on_off[task.get_sample().sample_id()] == 1 or path_onoff[task.get_sample().sample_id()] > 1:
              overlap = 1
          if not overlap:
            for task in path.get_tasklist():
              try:
                task.get_sample().sample_id()
              except:
                continue
              on_off[task.get_sample().sample_id()] = 1
            day.set_path(path)

  def refresh(self, onoff):
    for day in self.get_days():
      if day.is_empty() or day.is_blocked() or day.is_dayoff():
        continue
      else:
        path = day.get_path()
        for task in path.get_tasklist():
          try:
            onoff[task.get_sample().sample_id()] = 0
          except:
            continue
        day.set_path(None)
    #print(sum(onoff.values()))
    self.onoff_assignment(onoff)
    #print(sum(onoff.values()))

  def get_starttime(self):
    return self._starttime

  def get_population(self):
    '''Get valid task heap'''
    return self._population

  def get_weeknumber(self):
    '''Get Week Number (1,2,3,4,5,6)'''
    return self._weeknumber

  def get_checker(self):
    '''Get checker associated to this week'''
    return self._checker

  def get_day(self, i):
    '''Return the corresponding day instance'''
    if i >=7 :
      return None
    if self_week == []:
      print("Week not initialized, initializing week...")
      self.initialize()
    return self._week[i]

  def get_days(self):
    '''Iteratable'''
    for day in self._week:
      yield day

"""## Generation"""

class Generation:
  '''Generation of schedules'''

  __slots__ = '_generation','_generationNumber', '_size', '_mutationRate', '_fitnessThreshold', '_month', '_year', '_onoff', '_checkerlist', '_mating_pool', '_elites'

  def __init__(self, generationNumber, size, mutationRate, fitnessThreshold, month, year, onoff, checkerlist, generation = []):
    self._generation = generation #List of schedules in the generation
    self._generationNumber = generationNumber #Gen 0
    self._size = size #number of schedules generated
    self._mutationRate = mutationRate #determines the probability of mutation during reproduction
    self._fitnessThreshold = fitnessThreshold #determines the minimum fitness score an individual must have to participate in reproduction
    self._month = month
    self._year = year
    self._onoff = onoff
    self._checkerlist = checkerlist
    self._mating_pool = []
    self._elites = []

  def initialize(self):
    '''Randomly initialize a generation of schedules --> Gen 0, update in place, no return value'''
    for i in range(self._size):
      new_onoff = copy.deepcopy(self._onoff)
      new_schedule = Schedule(self._checkerlist, new_onoff, self._mutationRate,[], self._month, self._year)
      new_schedule.initialize()
      self._generation.append(new_schedule)

  def natural_selection(self):
    mating_pool = []
    for s in self._generation:
      s.set_fitness()
    pool = sorted(self._generation, key=calculate_fitness, reverse=True)
    max_fitness = pool[0].get_fitness()
    min_fitness = pool[-1].get_fitness()
    self._elites = pool[:10]
    difference = max_fitness - min_fitness
    for i in range(len(self._generation)):
      if difference == 0:
        relative_fitness = int(100 * (self._generation[i].get_fitness() - min_fitness)/ difference)
      else:
        relative_fitness = int(100 * self._generation[i].get_fitness())
      #print(relative_fitness)
      if relative_fitness > 100*self._fitnessThreshold:
        for j in range(relative_fitness):
          mating_pool.append(self._generation[i])
    self._mating_pool = mating_pool

  def reproduce(self):
    '''Perform one reproduction of the generation, return next generation'''
    self.natural_selection()
    new_generation = self._elites[:]
    for i in range(self._size-len(self._elites)):
      p1 = random.choice(self._mating_pool)
      p2 = random.choice(self._mating_pool)
      child = p1.crossover(p2)
      child.mutate()
      new_generation.append(child)
    return Generation(self._generationNumber + 1, self._size, self._mutationRate, self._fitnessThreshold, self._month, self._year, self._onoff, self._checkerlist, new_generation)

  def get_bestIndividual(self):
    '''Find the schedule with the best fitness score and return it'''
    if len(self._generation) == 0:
      print("length error")
    maxfit = self._generation[0].get_fitness()
    best = self._generation[0]
    for schedule in self._generation:
      if schedule.get_fitness() > maxfit:
        maxfit = schedule.get_fitness()
        best = schedule
    return best
