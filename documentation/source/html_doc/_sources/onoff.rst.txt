On/Off Switch Task Assignment
=============================
.. toctree::
   :maxdepth: 1

This section contains documentation on functions used to start on/off switch task assignment, for documentation on how the task assignment process works, please refer to the Schedule, Week and Day classes.

.. function:: select_optimal_v2(checkerlist, filename, iterations, gui = None):

   Starts on/off assignment process, returns generated schedule

   :param checkerlist: CheckerList object
   :type checkerlist: CheckerList
   :param filename: name of sample set file
   :type: string
   :param iterations: number of times on/off assignment is repeated
   :type iterations: int
   :rtype: Schedule object

|

.. function:: generate_schedule(checkerlist, filename, iterations, gui = None):

   Schedule generation with feedback on randomly generated sample set

   :param checkerlist: CheckerList object
   :type checkerlist: CheckerList
   :param filename: name of sample set file
   :type: string
   :param iterations: number of times on/off assignment is repeated
   :type iterations: int
   :param gui: gui object for gui output
   :type gui: tkinter.Text or None
   :rtype: Schedule object
