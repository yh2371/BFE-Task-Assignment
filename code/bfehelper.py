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
from bfeclasses import *

"""# Utility Functions

## Date and Time Formatting

### Format time
"""

def format_time(time):
  """
Formats time data into a list as [hour, minute]

Parameters
----------
time: str
      Time read from file

Return
---------
[hour, minute]: list of int
      List of hours and minutes
  """

  '''Format time data into a list represented as [hour, minute]'''
  time = str(int(time))
  if len(time) <= 2:
      hour = 0
  else:
      hour = int(time[:-2])
  minute = int(time[-2:])
  return [hour, minute]

"""### Get days in a month"""

def get_daystypes(year = None, month = None):
  """
  Yield iteration of day type of each day

  Parameters
  ----------
  year: null
      The year

  month: null
      The month
  """

  '''Yield iteration of day type of each day in given month/year, if no month/year is given, the current month/year will be chosen'''
  cal = calendar.Calendar()
  if year == None or month == None:
    now = datetime.datetime.now()
    year = now.year
    month = now.month

  for i in cal.itermonthdays2(year, month):
    #if i[0] != 0:
    yield i

def get_daysinmonth(year = None, month = None):
  """
  Returns total number of days in given month/year

  Parameters
  ----------
  year: null
      The year

  month: null
      The month

  Returns
  -------
  ret_day: int
      Total number of days

  """

  '''Return total number of days in given month/year, if no month/year is given, the current month/year will be chosen'''
  if year == None or month == None:
    now = datetime.datetime.now()
    year = now.year
    month = now.month
  ret_day = calendar.monthrange(now.year, now.month)[1]

  return ret_day

def get_daytype(s):
  """
  Get the type of the day

  Parameters
  ----------
  s: str
      Type of day

  Return
  ------
  int from 0 to 6 inclusive
      int representation of day type
  """

  if s == "SAT":
    return 5
  elif s == "SUN":
    return 6
  elif s == "MON":
    return 0
  elif s == "TUE":
    return 1
  elif s == "WED":
    return 2
  elif s == "THU":
    return 3
  elif s == "FRI":
    return 4

def get_daytypes_week(weeknumber, year=None, month=None):
  """
  Get the day type given the week

  Parameters
  ----------
  weeknumber: int
      int representation of week

  year: null
      The year

  month: null
      The month

  Returns
  -------
  i: int
      integer representation of daytype

  """
  cal = calendar.Calendar()
  if year == None or month == None:
    now = datetime.datetime.now()
    year = now.year
    month = now.month

  counter = 0
  for i in cal.itermonthdays2(year, month):
    if (weeknumber-1)*7 <= counter and weeknumber*7 > counter:
      yield i
    counter += 1

"""### Get difference between two time points"""

def get_difference(t1, t2):
    """
    Compute time difference between t1 and t2

    Parameters
    ----------
    t1: int
        int representation of time 1

    t2: int
        int representation of time 2

    Returns
    -------
    minute_diff: int
        Time difference in minutes

    -1: int
        Unable to calculate

    """

    """Compute time differenct between time t1 = [h1, m1] and t2 = [h2, m2]"""
    hour_diff = (t1[0]-t2[0])*60
    minute_diff = t1[1] - t2[1]
    if hour_diff > 0:
      return hour_diff + minute_diff
    elif hour_diff == 0 and minute_diff >= 0:
      return minute_diff
    if hour_diff < 0 and t1[0] == 0:
      return (24 - t2[0])*60 + minute_diff
    else:
      return -1

"""### Update time of day"""

def update(t2, t):
    """
    Update the time of day when t time has passed

    Parameters
    ----------
    t: int
        Time passed in minutes

    t2: [hour, minute]
        Time of the day

    Output
    ------
    t2: [hour, minute]
        Time of the day
    """
    """Update the time of day when t time has passed, t = [hour, minute]"""
    #curr_time = self._timeofday
    t2[0] = t2[0] + t//60 + (t2[1] + t%60)//60
    t2[1] = (t2[1] + t%60)%60
    print(t2)

"""## Data Processing

### Clean Sample Data
"""

def clean_data(filename):
  """
  Read then clean data of cvs files

  Parameter
  --------
  filename: str
        Name of the file to be read and cleaned

  """
  df = pd.read_csv(filename)
  duration_list = []
  df = df.drop(['BEF_ORIGIN','BEF_DESTINATION','RET_ORIGIN','RET_DESTINATION','BEF_LAT_D','BEF_LONG_O','RET_LAT_O','RET_LAT_D','RET_LONG_D','RET_LONG_O'],axis = 1)

  for index,row in df.iterrows():
    if math.isnan(row['RET_SRT_TIME']) != True and math.isnan(row['RET_SRT_DEST_TIME']) != True:
      hour_start_time = row['RET_SRT_TIME'] // 100
      minute_start_time = row['RET_SRT_TIME'] % 100
      hour_destination = row['RET_SRT_DEST_TIME'] //100
      minute_destination = row['RET_SRT_DEST_TIME'] %100

      time1 = timedelta(hours = hour_start_time, minutes = minute_start_time)
      time2 = timedelta(hours = hour_destination,minutes = minute_destination)
      zeros = timedelta(hours = 0, minutes = 0)
      midnight = timedelta(hours = 24)


      if hour_destination == 0:
        duration = (time2 - zeros + midnight - time1)
        duration_list.append(duration.seconds/60)
      else:
        duration = (time2 - time1)
        duration_list.append(duration.seconds/60)
    else:
      duration = timedelta(hours = 0, minutes = 0)
      duration_list.append(duration.seconds/60)

  switch = [0]*df.shape[0]
  df['DURATION'] = duration_list
  df['SWITCH'] = switch
  df.to_csv('/content/drive/My Drive/cleaned_data.csv')

"""### Select Samples"""

def select_cleaned_data(filename, numofsamples):
  """
  Select number of samples from cleaned files

  Parameter
  --------
  filename: str
        Name of the file to be read

  numofsamples: int
        Number of samples to be selected

  """
  df_initial = pd.read_csv(filename)
  #data = df_initial.loc[df_initial['SWITCH'] == 0]
  daytypes = ["WKD", "SATURDAY", "SUNDAY"]
  selected = []
  for i in range(3):
    data = df_initial.loc[df_initial['BFE_DAY'] == daytypes[i]]
    Origins = data['ORIGIN'].to_list()
    Destinations = data['DESTINATION'].to_list()
    Duration = data['DURATION'].to_list()
    Route_ID = data['ROUTE'].to_list()
    Sample_ID = data['SAMPLE_ID'].tolist()
    Switch = data["SWITCH"].tolist()

    Departure_time = data["LVTIME"].to_list()
    Arrival_time = data["ARRTIME"].to_list()
    Before_Dep = data["BEF_SRT_TIME"].to_list()
    Before_Arr = data["BEF_SRT_DEST_TIME"].to_list()
    Return_Dep = data["RET_SRT_TIME"].to_list()
    Return_Arr = data["RET_SRT_DEST_TIME"].to_list()

    Origin_long = data['LONG_O'].to_list()
    Origin_lat = data['LAT_O'].to_list()

    Dest_long = data['LONG_D'].to_list()
    Dest_lat = data['LAT_D'].to_list()

    BFE_day = data["BFE_DAY"].to_list()
    Borough = data["BORO"].to_list()

    indexes = list(range(len(Origins)))
    random.shuffle(indexes)
    for i in range(numofsamples[i]):
      selected.append([Origins[i], Destinations[i], Duration[i], Route_ID[i], Sample_ID[i],Departure_time[i], Arrival_time[i],Before_Dep[i], Before_Arr[i],Return_Dep[i], Return_Arr[i],Origin_long[i], Origin_lat[i], Dest_long[i], Dest_lat[i],Switch[i], BFE_day[i], Borough[i]])

  df = pd.DataFrame(selected, columns =['ORIGIN', 'DESTINATION','DURATION','ROUTE','SAMPLE_ID', 'LVTIME', 'ARRTIME', 'BEF_SRT_TIME','BEF_SRT_DEST_TIME','RET_SRT_TIME', 'RET_SRT_DEST_TIME', 'LONG_O', 'LAT_O', 'LONG_D', 'LAT_D', 'SWITCH', 'BFE_DAY','BORO'])
  df.to_csv('sample450.csv')

"""### Get Clean Data"""

def get_clean_data(filename, borough, daytype):
  '''Retrieve cleaned data'''

  df_initial = pd.read_csv(filename)

  df = df_initial.loc[df_initial['SWITCH'] == 0]
  current_borough = df.loc[df['BORO'] == borough]

  '''Initiate data storage'''
  origins = []
  destinations = []
  departures = []
  arrivals = []
  route_ids = []
  origin_coord = []
  destination_coord = []
  sample_ids = []

  '''Determine day type '''
  if daytype == "weekday":
    data = current_borough.loc[current_borough['BFE_DAY'] == "WKD"]
  elif daytype == "saturday":
    data = current_borough.loc[current_borough['BFE_DAY'] == 'SATURDAY']
  else:
    data = current_borough.loc[current_borough['BFE_DAY']== 'SUNDAY']

  '''Retrieve corresponding data'''
  Origins = data['ORIGIN'].to_list()
  Destinations = data['DESTINATION'].to_list()
  Duration = data['DURATION'].to_list()
  Route_ID = data['ROUTE'].to_list()
  Sample_ID = data['SAMPLE_ID'].tolist()

  Departure_time = data["LVTIME"].to_list()
  Arrival_time = data["ARRTIME"].to_list()
  Before_Dep = data["BEF_SRT_TIME"].to_list()
  Before_Arr = data["BEF_SRT_DEST_TIME"].to_list()
  Return_Dep = data["RET_SRT_TIME"].to_list()
  Return_Arr = data["RET_SRT_DEST_TIME"].to_list()

  Origin_long = data['LONG_O'].to_list()
  Origin_lat = data['LAT_O'].to_list()
  Origin_coord = []

  Dest_long = data['LONG_D'].to_list()
  Dest_lat = data['LAT_D'].to_list()
  Dest_coord = []

  '''Format and arrange data into lists'''
  for i in range(len(Origin_long)):
    temp_tuple = (Origin_lat[i],Origin_long[i])
    Origin_coord.append(temp_tuple)

  for i in range(len(Dest_long)):
      temp_tuple = (Dest_lat[i],Dest_long[i])
      Dest_coord.append(temp_tuple)

  for i in range(len(Before_Arr)):
    if not math.isnan(Before_Arr[i]):
        sample_ids.append(Sample_ID[i])
        origins.append(Destinations[i])
        destinations.append(Origins[i])
        route_ids.append(Route_ID[i])
        departures.append(format_time(Before_Dep[i]))
        arrivals.append(format_time(Arrival_time[i]))
        origin_coord.append(Dest_coord[i])
        destination_coord.append(Origin_coord[i])

  for i in range(len(Return_Arr)):
    if not math.isnan(Return_Arr[i]):
        sample_ids.append(Sample_ID[i])
        origins.append(Origins[i])
        destinations.append(Destinations[i])
        route_ids.append(Route_ID[i])
        departures.append(format_time(Departure_time[i]))
        arrivals.append(format_time(Return_Arr[i]))
        origin_coord.append(Origin_coord[i])
        destination_coord.append(Dest_coord[i])

  return origins, origin_coord, destinations, destination_coord, departures, arrivals, route_ids, sample_ids

"""### Get Checker Data"""

def get_checker_data(filename):
  df = pd.read_csv(filename)
  duration_list = []

  df.loc[df['shift_end'] == 0, 'shift_end'] = 2400

  for index,row in df.iterrows():
    if math.isnan(row['shift_start']) != True and math.isnan(row['shift_end']) != True:
      hour_start_time = row['shift_start'] // 100
      hour_end = row['shift_end'] //100

      time1 = timedelta(hours = hour_start_time)
      time2 = timedelta(hours = hour_end)

      zeros = timedelta(hours = 0, minutes = 0)
      midnight = timedelta(hours = 24)

      if hour_end == 0:
        duration = (midnight - time1)
        duration_list.append(duration.seconds/3600)
      else:
        duration = (time2 - time1)
        duration_list.append(duration.seconds/3600)
    else:
      duration = timedelta(hours = 0, minutes = 0)
      duration_list.append(duration.seconds/3600)

  df['duration'] = duration_list

  df = df.dropna(how='all', axis='columns')

  Full_time = df.loc[df['work_status'] == 'Full Time']
  Part_time = df.loc[df['work_status'] == 'Part Time']

  # create two lists that store each checker's shift and duration

  Full_time_list = []
  Part_time_list = []

  for index,row in Full_time.iterrows():
    checker_name = row['checker']
    shift = ((row['shift_start'])//100,(row['shift_end'])//100)
    checker_duration = row['duration']
    checker_assign = row["Assignment"]
    checker_daysoff = row["rdo"].split("-")
    if checker_assign == "B":
      for i in range(len(checker_daysoff)):
        checker_daysoff[i] = get_daytype(checker_daysoff[i].strip())
      Full_time_shift = (checker_name,shift,checker_duration, checker_daysoff)
      Full_time_list.append(Full_time_shift)

  for index,row in Part_time.iterrows():
    checker_name = row['checker']
    shift = ((row['shift_start'])//100,(row['shift_end'])//100)
    checker_duration = row['duration']
    checker_assign = row["Assignment"]
    checker_daysoff = row["rdo"].split("-")
    if checker_assign == "B":
      for i in range(len(checker_daysoff)):
        checker_daysoff[i] = get_daytype(checker_daysoff[i].strip())
      Part_time_shift = (checker_name,shift,checker_duration, checker_daysoff)
      Part_time_list.append(Part_time_shift)

  return Full_time_list, Part_time_list

"""### Initialize On and Off switch data"""

def get_onandoff_sample(filename):
  '''Retrieve on and off switch corresponding to each sample'''
  df = pd.read_csv(filename)
  switches = df['SWITCH'].tolist()
  sample_ids = df['SAMPLE_ID'].tolist()
  on_off = {}
  for i in range(len(switches)):
    on_off[sample_ids[i]] = switches[i]
  return on_off

"""## Display"""

def display(schedule):
    for i in schedule:
      try:
        checker = i[0][0]
      except:
        return
      workstatus = checker.workstatus()
      if not workstatus:
        workstatus = "Part-time"
      else:
        workstatus = "Full-time"
      counter = 1
      print(checker.checkerid(), workstatus)
      for j in i:
        task = j[1]
        content = "DAY " + str(counter) + ":\n"
        if task == "Blocked":
          continue
        if task == "Day Off" or task =="Impossible":
          content += task + "\n"
          counter += 1
          print(content)
          print()
          continue
        content += "Shift starts at: " + displaytime([j[2][0], j[2][1]]) + "\n"
        counter += 1
        for k in task.get_pathlist():
          route = k.get_route()
          station = k.get_station().station()
          try:
            routename = route.routename()
            content += "\t" + routename + " at " + station + "\n\t\tStarting at: " + displaytime(route.departuretime()) + "\n\t\tEnding at: " + displaytime(route.arrivaltime()) + "\n"
          except:
            content += "\t" + route.upper() + " at " + station + "\n"
          #except:
        print(content)
        total_time = task.get_pathTime()
        idle_time = task.get_idleTime()
        print("Total Time: " + str(total_time//60) + " hours and " + str(total_time % 60) + " minutes")
        print("Total Idle Time: " + str(idle_time//60) + " hours and " + str(idle_time % 60) + " minutes")
        print()

def displaytime(time):
  hour = time[0]
  minute = time[1]
  return "%02d" % hour + ":" + "%02d" % minute

"""## Weight Function"""

def weight_function(curr_time, borough, day_type):
  """Reads csv files and returns weight value of an edge

  Parameters
  ------------
  curr_time: str
      The current time of the day

  borough: str
      The borough of the edge

  day_type: str
      The current type of the day

  Return
  --------
  weights: dictionary
      Stores the weight values of the edge
  """

  #origin_actual = edge.endpoints()[0].station()
  #dest_actual = edge.endpoints()[1].station()

  if curr_time == 0:
    curr_time = "8_00am"
  else:
    curr_time = "2_00pm"

  if day_type == "weekday":
    day_type = "WKD"
  elif day_type == "saturday":
    day_type = "SATURDAY"
  else:
    day_type = "SUNDAY"

  filename = curr_time + '/result_'+ borough + "_" + day_type + "_" + curr_time

  path = './time_charts_new/' + filename + ".csv"
  #print(path)

  #reads
  header_list = ["Start", "Destination", "Time"]
  #read the csv file based on the path
  #collect column data
  df = pd.read_csv(path, header = None, usecols=[1, 3, 4], names=header_list)

  origin = df["Start"]
  destination = df["Destination"]

  #transition each column into list
  list_of_start = df['Start'].to_list()
  list_of_dest = df['Destination'].to_list()
  list_of_time = df['Time'].to_list()

  #should check to make sure each list has the same length
  list_len = len(list_of_start)

  weights = {}
  for i in range(0, list_len):
    weights[list_of_start[i]] = weights.get(list_of_start[i], {})
    if list_of_time[i]//60 >= 120:
      weights[list_of_start[i]][list_of_dest[i]] = 120
    elif list_of_time[i]//60 <= 10:
      weights[list_of_start[i]][list_of_dest[i]] = 10
    else:
      weights[list_of_start[i]][list_of_dest[i]] = list_of_time[i]//60 + 15

  return weights

"""## Checker List Construction"""

def construct_checkerlist(filename):
  """
  Function to construct a list of checker availability for a given month


  Parameters
  ----------
  filename: str
    a file containing checkers and their associated availability for a month

  Output
  ------
  checkerlist: list
    a list of checker availability with checker ID, shift start and end time, RDOs and work status


  """
  full_timers, part_timers = get_checker_data(filename)
  checkerlist = CheckerList()

  for checker_data in full_timers:
    duration = checker_data[2]
    if duration < 7:
      continue
    checkerid = checker_data[0]
    shift = checker_data[1]
    startshift = [int(shift[0]), 0]
    endshift = [int(shift[1]), 0]
    daysoff = checker_data[3]
    workstatus = 1
    checkerlist.add_checker(checkerid, startshift, endshift, daysoff, workstatus)

  for checker_data in part_timers:
    duration = checker_data[2]
    if duration < 6:
      continue
    checkerid = checker_data[0]
    shift = checker_data[1]
    startshift = [int(shift[0]), 0]
    endshift = [int(shift[1]), 0]
    daysoff = checker_data[3]
    workstatus = 0
    checkerlist.add_checker(checkerid, startshift, endshift, daysoff, workstatus)

  return checkerlist

"""## Graph Construction"""

def create_graph(filename, borough, daytype):
  '''
  Function for constructing graph using cleaned dataset

  Parameters
  ----------
  filename: str
    base sample set for a given borough
  borough: str
    name of the borough in the given csv file (Q,B,BX,M,S)
  daytype: str
    type of day of given csv file (WKD,SATURDAY,SUNDAY)

  Outputs
  -------
  G: graph
    a graph of the given daytype and borough

  '''
  origins, origin_coord, destinations, dest_coord, departures, arrivals, routes, sample_ids = get_clean_data(filename, borough, daytype)
  if not(len(origins) == len(destinations) and len(origins) == len(routes) and len(origins) == len(departures)):
    print("Data Length Error")
    print("Origins: " + str(len(origins)) + "\n", "Destinations: " + str(len(destinations)) + "\n", "Routes: " + str(len(routes)) + "\n", "Times: " + str(len(times)) + "\n")
    return

  morning_weights = weight_function(0, borough, daytype) #preload edge weight data for faster access
  evening_weights = weight_function(1, borough, daytype)

  G = Graph(True, borough, daytype)

  for i in range(len(origins)):
    origin = origins[i]
    destination = destinations[i]
    route = routes[i]
    sample_id = sample_ids[i]
    departure = departures[i]
    arrival = arrivals[i]
    u = G.insert_vertex(origin, origin_coord[i])
    v = G.insert_vertex(destination, dest_coord[i])
    G.insert_edge(u, v, route, arrival, departure, sample_id)
    edge = G.get_edge(u, v)
    try:
      morning = morning_weights[origin][destination]
    except:
      try:
        morning = morning_weights[destination][origin]
      except:
        morning = 60 #edges missing OTP data are set to a 60 minute travel time by default
    try:
      evening = evening_weights[origin][destination]
    except:
      try:
        evening = evening_weights[destination][origin]
      except:
        evening = 60
    edge.set_weight(morning, evening)

  G.insert_vertex("LIC", [0,0]) #assuming the long island city node is denoted as "LIC"

  for i in G.vertices():
    for j in G.vertices():
      G.insert_edge(i, j)
      G.insert_edge(j, i)
      edge = G.get_edge(i, j)
      try:
        morning = morning_weights[origin][destination]
      except:
        try:
          morning = morning_weights[destination][origin]
        except:
          morning = 60
      try:
        evening = evening_weights[origin][destination]
      except:
        try:
          evening = evening_weights[destination][origin]
        except:
          evening = 60
      edge.set_weight(morning, evening)
      edge2 = G.get_edge(j, i)
      try:
        morning = morning_weights[origin][destination]
      except:
        try:
          morning = morning_weights[destination][origin]
        except:
          morning = 60
      try:
        evening = evening_weights[origin][destination]
      except:
        try:
          evening = evening_weights[destination][origin]
        except:
          evening = 60
      edge2.set_weight(morning, evening)

  return G

"""## Score Function"""

def matrixScore(schedule):
  total_tasks_complete = 0
  total_idle_time = 0
  total_time = 0
  impossible_days = 0
  percentage_of_basis_completed = 0.0
  TOTAL_BASE_TASK = 450.0
  for checker_schedule in schedule:  # a list of path
    checker = checker_schedule[0][0]
    workstatus = checker.workstatus()
    for path in checker_schedule:
      path = path[1]
      if path == "Impossible":
        impossible_days += 1
        continue
      elif path == "Day Off" or path == 'Blocked':
        continue
      total_tasks_complete += path.numoftasks() - workstatus
      total_idle_time += path.get_idleTime()
      total_time += path.get_pathTime()
  percentage_of_basis_completed = total_tasks_complete/TOTAL_BASE_TASK
  return total_tasks_complete, total_idle_time, percentage_of_basis_completed, total_time, impossible_days

"""## Evaluate Task Coverage"""

def evaluate_tasks(checkerlist, filename):
  '''Check how many samples are included in the valid tasks gathered'''
  onoff = get_onandoff_sample(filename)
  for checker in checkerlist.get_checkerlist():
    validpaths = checker.validpaths()
    for daytype in validpaths:
      for time in validpaths[daytype]:
        for path in validpaths[daytype][time].get_data():
          for task in path.get_tasklist():
            try:
              task.get_sample().sample_id()
            except:
              continue
            onoff[task.get_sample().sample_id()] = 1
  counter = 0
  l = []
  for i in onoff:
    if onoff[i] == 0:
      #print(i)
      counter += 1
      l.append(i)
  #print(l)
  #print(counter)
  return sum(list(onoff.values())), len(onoff), l



"""## Calculate Fitness"""

def calculate_fitness(s): # to use as a key in the following min/max function, althought I'm not sure if it works
    """
    Calculate fitness score

    Parameter
    ---------
    s: Schedule Class
        A schedule class object

    Return
    ------
    s.get_fitness(): int
        A schedule's fitness score
    """
    return s.get_fitness()

"""## Calculate Sample Ratio"""

def get_ratio(checkerlist, numofsamples, month=None, year=None):
  """
  Calculates the ratio of checkers available for a given day type to the total number of days for a month

  Parameters
  ----------
  checkerlist: list
    a list of checkers and their availability
  numofsamples: int
    number of samples in the sample set
  month: str
    month being evaluated
  year: str
    year being evaluated

  Outputs
  -------
  [wkd_portion, sat_portion, sun_portion]: list
    contains ratio of each weekday type to the total number of days for that month

  """
  daycounts = {}
  for daytype in get_daystypes(year, month):
    if daytype[0] != 0:
      daycounts[daytype[1]] = daycounts.get(daytype[1], 0) + 1
  wkd = 0
  sat = 0
  sun = 0
  for checker in checkerlist.get_checkerlist():
    daysoff = checker.daysoff()
    for daytype in daycounts:
      if daytype in daysoff:
        continue
      elif daytype == 6:
        sun += daycounts[daytype]
      elif daytype == 5:
        sat += daycounts[daytype]
      else:
        wkd += daycounts[daytype]
  total = wkd + sat + sun
  wkd_portion = int(numofsamples*wkd/total)
  sat_portion = int(numofsamples*sat/total)
  sun_portion = numofsamples - wkd_portion - sat_portion
  return [wkd_portion, sat_portion, sun_portion]

"""More util functions for evaluation"""
def get_invalid(checkerlist, filename):
  a, b, l = evaluate_tasks(checkerlist, filename)
  df = pd.read_csv(filename)
  sample_id = df["SAMPLE_ID"].tolist()
  duration = df["DURATION"].tolist()
  route = df["ROUTE"].tolist()
  daytypes = df["BFE_DAY"].tolist()

  wkd = 0
  sat = 0
  sun = 0

  for i in range(len(sample_id)):
    if sample_id[i] in l:
      print(sample_id[i], duration[i], route[i], daytypes[i])
      if daytypes[i] == "WKD":
        wkd += 1
      elif daytypes[i] == "SATURDAY":
        sat += 1
      else:
        sun += 1

  return wkd, sat, sun

def evaluate_empty_days(checkerlist, filename, schedule2, daycounts, gui=None):
  scheduleonoff = schedule2._onoff
  checkeronoff={}
  totalonoff_wkd = get_onandoff_sample("sample450.csv")
  totalonoff_sat = get_onandoff_sample("sample450.csv")
  totalonoff_sun = get_onandoff_sample("sample450.csv")
  daycounts = get_ratio(checkerlist, 450)
  for checker in checkerlist.get_checkerlist():
    counter = 0
    onoff = get_onandoff_sample("sample450.csv")
    oneonoff = get_onandoff_sample("sample450.csv")
    content = checker.checkerid() + ": "
    for daytype in checker.validpaths():
      timeonoff = get_onandoff_sample("sample450.csv")
      for time in checker.validpaths()[daytype]:
          for data in checker.validpaths()[daytype][time].get_data():
            counter += 1
            for task in data.get_tasklist():
              try:
                if daytype == "wkd":
                  oneonoff[task.get_sample().sample_id()] = 1
                  if scheduleonoff[task.get_sample().sample_id()] == 1:
                    totalonoff_wkd[task.get_sample().sample_id()] = 1
                if daytype == "sat":
                  if scheduleonoff[task.get_sample().sample_id()] == 1:
                    totalonoff_sat[task.get_sample().sample_id()] = 1
                if daytype == "sun":
                  if scheduleonoff[task.get_sample().sample_id()] == 1:
                    totalonoff_sun[task.get_sample().sample_id()] = 1
                if scheduleonoff[task.get_sample().sample_id()] == 0:
                  timeonoff[task.get_sample().sample_id()] = 1
              except:
                continue
      content += str(sum(list(timeonoff.values()))) + " " + daytype + ", "
    content += "remaining\n"
    if gui == None:
      print(content)
    else:
      gui.insert(tk.END, content)
    checkeronoff[checker.checkerid()] = onoff

  if gui == None:
    print()
    print("Samples Covered:")
    print(sum(totalonoff_wkd.values()), "out of", str(daycounts[0]), "weekday samples")
    print(sum(totalonoff_sat.values()), "out of", str(daycounts[1]), "saturday samples")
    print(sum(totalonoff_sun.values()), "out of", str(daycounts[2]), "sunday samples")
    print()
  else:
    gui.insert(tk.END, "\nSamples Covered:\n%d out of %s weekday samples\n%d out of %s saturday samples\n%d out of %s sunday samples\n\nEmpty Days:\n" % (sum(totalonoff_wkd.values()), str(daycounts[0]),sum(totalonoff_sat.values()),str(daycounts[1]), sum(totalonoff_sun.values()),str(daycounts[2])))

  for i in range(len(schedule2._schedule)):
    checkermonth = schedule2._schedule[i]
    checker = checkerlist.get_checker(i)
    wkd = 0
    sat = 0
    sun = 0
    for week in checkermonth:
      for day in week.get_days():
        if day.is_empty():
          if day.is_sat():
            sat += 1
          elif day.is_sun():
            sun += 1
          else:
            wkd += 1
    if gui == None:
      print(checker.checkerid(), "Empty Days: %d wkd, %d sat, %d sun" % (wkd, sat, sun))
    else:
      gui.insert(tk.END, checker.checkerid() + " Empty Days: %d wkd, %d sat, %d sun\n" % (wkd, sat, sun))

def get_random_missing(schedule, num):
  assigned = []
  for key in schedule._onoff:
    if schedule._onoff[key] == 1:
      assigned.append(key)
  random.shuffle(assigned)
  return assigned[:num]
