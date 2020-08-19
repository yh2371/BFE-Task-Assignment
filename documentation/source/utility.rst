Utility Functions
=================

.. toctree::
   :maxdepth: 1

This section contains documentation on all the utility functions used in this project.

Date and Time Formatting
------------------------

.. function:: format_time(time):

   Formats a time string into a list of the form [hour, time]

   :param time: read from file, e.g. "14:20"
   :type time: string
   :rtype: list of integers in the form [hour, minute] where hour is between 0 and 23 and minute is between 0 and 59

|

.. function:: get_daystypes(year=None, month=None):

   Yield iteration of day type of each day in given month/year, if no month/year is specified, the current month/year will be chosen

   :param year: year number
   :type year: int or None
   :param month: month number
   :type month: int or None
   :rtype: Iteration of [date, daytype] objects. The date corresponds to the date in the month, if date == 0 then the object is from the previous/next month. The daytype is an int with the following correspondence 0-Monday, ..., 6-Sunday

|

.. function:: get_daysinmonth(year=None, month=None):

   Returns number of days in given month/year, if no month/year is specified, the current month/year will be chosen

   :param year: year number
   :type year: int or None
   :param month: month number
   :type month: int or None
   :rtype: Number of days (int)

|

.. function:: get_daytype(s):

   Changes a daytype string to its corresponding daytype index

   :param s: daytype string e.g. "MON"
   :type year: string
   :rtype: Daytype index (int) e.g. 0 for "MON"

|

.. function:: get_daytypes_week(weeknumber, year=None, month=None):

   Yield iteration of day type of each day in the selected week of the given month/year, if no month/year is specified, the current month/year will be chosen

   :param weeknumber: index corresponding to the week in the month, value ranges between 0 and 5
   :type weeknumber: int
   :param year: year number
   :type year: int or None
   :param month: month number
   :type month: int or None
   :rtype: Iteration of [date, daytype] objects. The date corresponds to the date in the month, if date == 0 then the object is from the previous/next month. The daytype is an int with the following correspondence 0-Monday, ..., 6-Sunday

|

.. function:: get_difference(t1, t2):

   Compute time in minutes needed to get from time t2 to time t1

   :param t1: end time
   :type t1: time list of the form [hour, minute]
   :param t2: start time
   :type t2: time list of the form [hour, minute]
   :rtype: Time difference in minutes (int) or -1 if t1 < t2

|

.. function:: update(t2, t):

   Update the time of day after t minutes have passed

   :param t2: previous time of day
   :type t2: time list of the form [hour, minute]
   :param t: the number of minutes that have passed by since t2
   :type t: int
   :rtype: Current time of day in the form of [hour, minute]

|

Data Processing
---------------

.. function:: clean_data(filename):

   Reads the base sample data file, calculates round trip durations, and exports to a new data file cleaned_data.csv

   :param filename: filename of base sample data file
   :type filename: string
   :rtype: None

|

.. function:: select_cleaned_data(filename, numofsamples):

   Randomly selects a set of samples for schedule generation and exports to a new data file sample450.csv

   :param filename: filename of cleaned sample data file
   :type filename: string
   :param numofsamples: list containing number of samples corresponding to weekday, saturday, sunday
   :type numofsamples: list of int
   :rtype: None

|

.. function:: get_clean_data(filename, borough, daytype):

   Retrieve clean data from the cleaned data file corresponding to the given borough and daytype

   :param filename: filename of cleaned sample data file
   :type filename: string
   :param borough: borough ID
   :type borough: string
   :param day_type: day type, weekday, saturday or sunday
   :type daytype: string
   :rtype: Returns the following lists of sample information: origins (strings), origin coordintaes ([long, lat]), destinations (strings), destination coordinates ([long, lat]), departure times ([hour,minute]), arrival times ([hour,minute]), route ids (strings), sample ids (strings)

|

.. function:: get_checker_data(filename):

   Retrieve information about the checkers

   :param filename: filename of the checker data file
   :type filename: string
   :rtype: Returns two list corresponding to Full-time checker and Part-time checker info, each element in the list is a tuple of the form (checker id, shift: (start, end):, shift duration, list of index of days off):

|

.. function:: get_onandoff_sample(filename):

   Retrieves on/off switch initial information to create an on/off switch dictionary

   :param(filename): filename of sample file
   :type filename: string
   :rtype: Returns a dictionary with sample ids as keys and 0 as values

|

.. function:: display(schedule):

   Takes a Schedule object and prints out the formatted schedule in the terminal

   :param schedule: generated schedule to be displayed
   :type schedule: Schedule
   :rtype: None

|

.. function:: displaytime(time):

   Converts a [hour, time] list into a time string

   :param time: [hour, time] representation of time
   :type time: list of int
   :rtype: String format of time, e.g. "17:45"

|

.. function:: weight_function(curr_time, borough, day_type):

   Calculates the weight of edges (traveling time) in minutes. The data is retrieved based on 8:00 AM OTP data if current time of day is before noon, otherwise data is retrieved based on 2:00 PM OTP data. A time buffer of 15 minutes is added, for traveling times exceeding 2 hours, the traveling time is set to 2 hours.

   :param curr_time: current time period of day indicator, 0-morning, 1-evening
   :type curr_time: int
   :param borough: borough ID
   :type borough: string
   :param day_type: day type, weekday, saturday or sunday
   :type day_type: string
   :rtype: Dictionary of dictionaries with stations names as ids and traveling time in minutes as values. Access a value using dict[destination][origin].

|

.. function:: construct_checkerlist(filename):

   Retrieves info from checker info file and turns in into a CheckerList object

   :param filename: filename of checker data file
   :type filename: string
   :rtype: An CheckerList object containing information about all checkers

|

.. function:: create_graph(filename, borough, daytype):

   Creates a graph corresponding to a given borough and day type

   :param filename: filename of sample data
   :type filename: string
   :param borough: borough ID
   :type borough: string
   :param day_type: day type, weekday, saturday or sunday
   :type daytype: string
   :rtype: A Graph object corresponding to a given borough and day type

|

.. function:: get_ratio(checkerlist, numofsamples, month=None, year=None):

   Calculates the number of samples needed in the random sample set for weekdays saturdays, sundays based on month info and checker availability

   :param checkerlist: checker info
   :type checkerlist: CheckerList
   :param numofsamples: number of samples to be in the random sample set
   :type numofsamples: int
   :param month: month of schedule
   :type month: int or None
   :param year: year of schedule
   :type year: int or None
   :rtype: list of the number of samples to be selected for the random sample set for each daytype in the order [weekday, saturday, sunday]

|

Evaluation
----------

.. function:: evaluate_tasks(checkerlist, filename):

   Checks how many samples from the sample set are included in the valid tasks gathered

   :param checkerlist: object containing checker info and valid task info
   :type checkerlist: CheckerList
   :param filename: filename of sample file
   :type filename: string
   :rtype: Number of unique samples covered by the valid tasks and a list of sample ids representing samples not covered by the valid tasks gathered

   |

.. function:: matrixScore(schedule):

   Calculates the total number of samples completed, total idle time, total percentage of basis completed, total time, and number of empty days

   :param schedule: the schedule to be evaluated
   :type schedule: Schedule
   :rtype: Total number of samples completed (int), total idle time in minutes (int), total percentage of basis completed (float), total time in minutes (int), and number of empty days (int)

   |

.. function:: calculate_fitness(schedule):

   Calculates the fitness score of the schedule

   :param schedule: the schedule to be evaluated
   :type schedule: Schedule
   :rtype: Fitness score of the schedule (float)

   |

.. function:: get_invalid(checkerlist, filename):

   Calculate the number of samples not covered by valid tasks for each day type

   :param checkerlist: checker info
   :type checkerlist: CheckerList
   :rtype: The number of samples not covered by valid tasks in the order weekday, saturday, sunday

|

.. function:: evaluate_empty_days(checkerlist, filename, schedule2, daycounts, gui=None):

   Calculate and display the number of valid tasks remaining, the number of empty days for each day type for each checker and the total number of samples covered for each daytype

   :param checkerlist: checker info
   :type checkerlist: CheckerList
   :param filename: filename of sample data file
   :type filename: string
   :param schedule2: generated schedule
   :type schedule2: Schedule
   :param daycounts: list of number of samples for each day type in the sample set
   :type daycounts: list of int
   :param gui: a tkinter text object to display info in gui, if None, then info is printed in the terminal
   :type gui: Tkints.Text or None
   :rtype: None

|

.. function:: get_random_missing(schedule, num):

   Randomly select a number of samples assigned in the schedule to fail. Updates schedule on/off to reflect the failure.

   :param schedule: generated schedule
   :type schedule: Schedule
   :param num: number of failed samples
   :type num: int
   :rtype: Schedule object with failed samples information included
