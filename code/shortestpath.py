"""# Load Packages"""

import time as T
import xlwt
import pandas as pd
import math
import calendar
import datetime
from datetime import timedelta
import random
import pickle
import copy
import csv
import tkinter as tk
from bfehelper import *
import bfehelper
from bfeclasses import *
import bfeclasses
import time as T

"""# Time Constrained K Shortest Path Algorithm"""

def time_constrained_shortest_path(G, valid_paths, start_station, end_station, start_time, fulltime, minimum_task, maximum_task):
    """
    Gathers all valid paths for a given graph by constructing shortest path from one node to the next

    Parameters
    ----------
    G: graph
      graph of all samples for a given borough for a given day type
    valid_paths: binary heap
      valid path heap
    start_station: str
      station where the path starts
    end_station: str
      station where the path ends
    start_time: [hour, minute]
      time at which algorithm starts to traverse the graph
    fulltime: int
      indicates whether or not checker checker is fulltime (0=part time,1=fulltime)
    minimum_task: int
      minimum number of tasks that have to be performed in a day
    maximum_task: int
      maxmimum number of tasks that have to be performed in a day

    Output
    ------
    valid_paths: binary heap
      valid path heap with additional paths added to it




    """
    paths_storage = bfeclasses.MinBinaryHeap(False, start_time[:]) #track total time

    start_node = G.get_vertex(start_station)
    end_node = G.get_vertex(end_station)
    borough = G.get_borough()
    daytype = G.get_daytype()
    if start_node == None:
      print("Start station not found")
      return
    if end_node == None:
      print("End station not found")
      return
    if fulltime:
      path = bfeclasses.Path([], 0, 0, start_time[:], 0, start_time[:])
      init_path = path.extend(start_node, "start")
    else:
      path = bfeclasses.Path([], 0, 0, start_time[:], 1, start_time[:])
      init_path = path.extend(start_node, "start")

    if fulltime:
      hour_limit = 7
    else:
      hour_limit = 6

    paths_storage.insert(init_path)

    while len(paths_storage) != 0:
        shortest_path = paths_storage.extract_min()
        total_time = shortest_path.get_pathTime()
        last_visited = shortest_path.get_endnode()
        curr_time = shortest_path.get_timeofday()
        for edge in G.incident_edges(last_visited, True):
            next_stop = edge.opposite(last_visited)
            travel_time = edge.weight(curr_time) #replace this line
            if next_stop.station() == end_station: #checking if the path that has reached the destination is valid
              final_path = shortest_path.extend(end_node, "end")
              final_path.updatetotaltime(travel_time)
              final_path.updateidletime(travel_time)
              if final_path.get_pathTime() <= hour_limit*60:
                if fulltime:
                  numoftasks = final_path.numoftasks()-final_path.hadlunchbreak()
                else:
                  numoftasks = final_path.numoftasks()
                if numoftasks >= minimum_task and final_path.hadlunchbreak():
                  valid_paths.insert(final_path)
              continue
            for sample in next_stop.samples():
              new_path = shortest_path.extend(next_stop, sample)
              new_path.updatetotaltime(travel_time)
              new_path.updateidletime(travel_time)
              new_path.updatetime(travel_time)
              departure = sample.departuretime()
              roundtrip = sample.roundtriptime()
              arrival = sample.arrivaltime()

              waiting_time = bfehelper.get_difference(departure, new_path.get_timeofday())
              if waiting_time < 0:
                continue
              else:
                pathtime = shortest_path.get_pathTime()
                if not new_path.hadlunchbreak():
                  if waiting_time >= 30 and pathtime >= 180 and pathtime <= 300:
                    new_path = new_path.addlunchbreak(next_stop, new_path.get_timeofday())
                  elif waiting_time >= 0 and pathtime >= 180 and pathtime <= 300:
                    new_path2 = shortest_path.addlunchbreak(last_visited, shortest_path.get_timeofday())
                    new_path2.updatetotaltime(30)
                    new_path2.updateidletime(30)
                    new_path2.updatetime(30)
                    if new_path2.get_pathTime() <= hour_limit*60 and new_path2.numoftasks() <= maximum_task:
                      paths_storage.insert(new_path2)
                new_path.updatetotaltime(waiting_time+roundtrip)
                new_path.updateidletime(waiting_time)
                new_path.updatetime(waiting_time+roundtrip)
                if fulltime:
                  numoftasks = new_path.numoftasks()+1 - new_path.hadlunchbreak()
                else:
                  numoftasks = new_path.numoftasks()+1
                if new_path.get_pathTime() <= hour_limit*60 and numoftasks <= maximum_task:
                  paths_storage.insert(new_path)

    return valid_paths

"""# Valid Path Gathering

## Setup Graphs
"""

def setup_graphs(filename, boroughs, gui = None):
  """
  Builds graphs for each day type using the graph of each borough and stores the elements as a dictionary with the day type as the key
  and the graph of all boroughs as the value.

  Parameters
  ----------
  filename: str
    name of file that stores all samples
  boroughs: list
    contains all five boroughs

  Outputs
  -------
  graphs: dict
    dictionary with day type as key and graph of all boroughs for that day type as the value

  """
  graphs ={"wkd":{}, "sat":{}, "sun":{}}
  for borough in boroughs:
    graphs["wkd"][borough] = bfehelper.create_graph(filename, borough, 'weekday')
    graphs["sat"][borough] = bfehelper.create_graph(filename, borough, 'saturday')
    graphs["sun"][borough] = bfehelper.create_graph(filename, borough, 'sunday')
  if gui == None:
    print("Graph Construction Complete...\n")
  else:
    gui.insert(tk.END, "Graph Construction Complete...\n\n")
  return graphs

"""## Get Checker Valid Tasks"""

def get_checker_tasks(graphs, start_station, end_station, minimum_task, maximum_task, checker, daytype, time_increment, time_range):
    """
    Retrieves valid tasks for a given checker from the graph

    Parameters
    ----------
    graphs: dict
      graphs of the given day type for all boroughs
    start_station: str
      station checker starts at
    end_station: str
      station checker end at
    minimum_task: int
      minimum number of tasks that a checker must complete in a day
    maximum_task: int
      maximum number of tasks a checker is allowed to complete in a day, constrains path lengths to make runtime shorter
    checker: str
      checker ID
    daytype: str
      day of the week that is being evaluated
    time_increment: int
      increments of the checker starting time in hours
    time_range: int
      allowed starting time window duration in hours

    Outputs
    -------
    adds valid paths to checker heap

    """
    shift_start = checker.startshift()
    shift_end = checker.endshift()
    workstatus = checker.workstatus()
    if workstatus:
      hours = 7
    else:
      hours = 6
    start_hour = shift_start[0]
    end_hour = (shift_end[0]-hours-time_range)%24
    while start_hour < end_hour:
      valid_paths = bfeclasses.MinBinaryHeap(True, [(start_hour*60)//60, (start_hour*60)%60]) #track idle time
      for i in range(int(time_range/time_increment)):
        for borough in graphs[daytype]:
          G = graphs[daytype][borough]
          valid_paths = time_constrained_shortest_path(G, valid_paths, start_station, end_station, [(start_hour*60)//60, (start_hour*60)%60], workstatus, minimum_task, maximum_task)
        start_hour = (start_hour + time_increment)%24
      checker.update_validpaths(valid_paths, daytype)

"""## Get All Checker Valid Tasks"""

def get_allchecker_tasks(checkerlist, filename, start_station, end_station, minimum_task, maximum_task, boroughs, time_increment, time_range, gui=None):
  """
  Retrieves tasks for all checkers

  Parameters
  ----------
  checkerlist: list
    list of all available checkers
  filename: str
    graph file
  start_station: str
    station checkers start at
  end_station: str
    station checkers end at
  minimum_task: int
    minimum number of tasks that a checker must complete in a day
  maximum_task: int
    maximum number of tasks a checker is allowed to complete in a day, constrains path lengths to make runtime shorter
  boroughs: list
    list of all boroughs
  time_incriment: int
    increments the checker starting time for which a path is created in multiples of this value
  time_range: int
    number of checker working hours for the day type


  Outputs
  -------
  checkerlist: list
    all paths all checkers can take
  """
  initial_t = T.time()
  graphs = setup_graphs(filename, boroughs, gui)
  for checker in checkerlist.get_checkerlist():
      sat = 1
      sun = 1
      daysoff = checker.daysoff()
      for i in daysoff:
        if i == 5:
          sat = 0
        if i == 6:
          sun = 0
      get_checker_tasks(graphs, start_station, end_station, minimum_task, maximum_task, checker, "wkd", time_increment, time_range)
      if sat:
        get_checker_tasks(graphs, start_station, end_station, minimum_task, maximum_task, checker, "sat", time_increment, time_range)
      if sun:
        get_checker_tasks(graphs, start_station, end_station, minimum_task, maximum_task, checker, "sun", time_increment, time_range)
      if gui == None:
        print(checker.checkerid(), "Valid Tasks Gathering Complete...\n")
      else:
        gui.insert(tk.END, checker.checkerid() + " Valid Tasks Gathering Complete...\n\n")

  elapsed_time = T.time() - initial_t
  if gui == None:
    print("Total Time: " + str(elapsed_time) + "\n")
    print("All Valid Tasks Gathered!")
  else:
    gui.insert(tk.END, "Total Time: " + str(elapsed_time) + "\n\n" + "All Valid Tasks Gathered!\n")
  return checkerlist
