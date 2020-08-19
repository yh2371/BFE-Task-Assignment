"""# Load Packages"""

from bfehelper import *
import bfehelper
import bfeclasses

"""# On/Off Task Assignment

## Generate Schedule With Schedule Object"""

def select_optimal_v2(checkerlist, filename, iterations,gui = None):
  """
  Generates schedule using on/off switch

  Parameters
  ----------
  checkerlist: CheckerList object
  filename: str
    sample set file filename
  iterations: int
    number of times assignment is executed

  Outputs
  -------
  schedule: Schedule object

  """
  checkerlist.reorder_checkers()
  #checkerlist.shuffle_checkerlist()
  on_off = bfehelper.get_onandoff_sample(filename)
  schedule = bfeclasses.Schedule(checkerlist, on_off)
  schedule.onoff_assignment(iterations)
  schedule.evaluate(gui)
  return schedule

def generate_schedule(checkerlist, filename, iterations, gui = None):
  daycounts = bfehelper.get_ratio(checkerlist, 450)
  if gui == None:
    print("Random Sample Set: ", daycounts)
    print()
    print("Valid Heap Missed Samples:")
    wkd, sat, sun = bfehelper.get_invalid(checkerlist, "sample450.csv")
    print()
    print("Missing: %d weekdays, %d saturdays, %d sundays\n" %(wkd, sat, sun))
    print("Valid Tasks cover: %d weekday samples, %d saturday samples, %d sunday samples\n" %(daycounts[0]-wkd, daycounts[1]-sat, daycounts[2]-sun))
    print("Schedule Results:")
  else:
    wkd, sat, sun = bfehelper.get_invalid(checkerlist, "sample450.csv")
    gui.insert(tk.END, "Random Sample Set: " + "[%d, %d, %d]"%(daycounts[0],daycounts[1],daycounts[2]) + "\n\n" + "Valid Tasks cover: %d weekday samples, %d saturday samples, %d sunday samples\n\n" %(daycounts[0]-wkd, daycounts[1]-sat, daycounts[2]-sun) + "\nSample Results:\n")
  return select_optimal_v2(checkerlist, "sample450.csv", iterations, gui)
