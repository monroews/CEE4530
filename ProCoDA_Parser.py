from aide_design.play import *

def read_state(dates, state, column, units="", path=""):
    """Reads a ProCoDA file and outputs the data column and time vector for
    each iteration of the given state.

    Parameters
    ----------
    dates : string list
        A list of dates for which data was recorded, in the form "M-D-Y"

    state : string
        The name of the state for which data should be extracted

    column : string
        Index of the column that you want to extract. Column 0 is time.
        The first data column is column 1.

    units : string
        The units you want to apply to the data, e.g. 'mg/L'.
        Defaults to "" which indicates no units

    path : strings
        Optional argument of the path to the folder containing your ProCoDA
        files. Defaults to the current directory if no argument is passed in

    Returns
    -------
    time : float list
        List of times corresponding to the data (with units)

    data : float list
        List data in the given column during the given state with units

    Example
    -------
    time, data = read_state(["6-19-2013", "6-20-2013"], "1. Backwash entire system", 28, "mL/s")

    """
    data_agg = []
    day = 0
    first_day = True
    overnight = False

    for d in dates:
        state_file = path + "statelog " + d + ".xls"
        data_file = path + "datalog " + d + ".xls"

        states = pd.read_csv(state_file, delimiter='\t')
        data = pd.read_csv(data_file, delimiter='\t')

        states = np.array(states)
        data = np.array(data)

        # get the start and end times for the state
        state_start_idx = states[:, 2] == state
        state_start = states[state_start_idx, 0]
        state_end_idx = np.append([False], state_start_idx[0:(np.size(state_start_idx)-1)])
        state_end = states[state_end_idx, 0]

        if overnight:
            state_start = np.insert(state_start, 0, 0)
            state_end = np.insert(state_end, 0, states[0, 0])

        if state_start_idx[-1]:
            state_end.append(data[0, -1])

        # get the corresponding indices in the data array
        data_start = []
        data_end = []
        for i in range(np.size(state_start)):
            add_start = True
            for j in range(np.size(data[:, 0])):
                if (data[j, 0] > state_start[i]) and add_start:
                    data_start.append(j)
                    add_start = False
                if (data[j, 0] > state_end[i]):
                    data_end.append(j-1)
                    break

        if first_day:
            start_time = data[1, 0]

        # extract data at those times
        for i in range(np.size(data_start)):
            t = data[data_start[i]:data_end[i], 0] + day - start_time
            c = data[data_start[i]:data_end[i], column]
            if overnight and i == 0:
                data_agg = np.insert(data_agg[-1], np.size(data_agg[-1][:, 0]),
                                     np.vstack((t, c)).T)
            else:
                data_agg.append(np.vstack((t, c)).T)

        day += 1
        if first_day:
            first_day = False
        if state_start_idx[-1]:
            overnight = True

    data_agg = np.vstack(data_agg)
    if units == !":
        return data_agg[:, 0]*u.day, data_agg[:, 1]*u(units)
    else:
        return data_agg[:, 0]*u.day, data_agg[:, 1]

def average_state(dates, state, column, units="", path=""):
    """Outputs the average value of the data for each instance of a state in
    the given ProCoDA files

    Parameters
    ----------
    dates : string list
        A list of dates for which data was recorded, in the form "M-D-Y"

    state : string
        The name of the state for which data should be extracted

    column : string
        Index of the column that you want to extract. Column 0 is time.
        The first data column is column 1.

    units : string
        The units you want to apply to the data, e.g. 'mg/L'.
        Defaults to "" which indicates no units

    path : strings
        Optional argument of the path to the folder containing your ProCoDA
        files. Defaults to the current directory if no argument is passed in

    Returns
    -------
    float list
        A list of averages for each instance of the given state

    Example
    -------
    data_avgs = average_state(["6-19-2013", "6-20-2013"], "1. Backwash entire system", 28, "mL/s")

    """
    data_agg = []
    day = 0
    first_day = True
    overnight = False

    for d in dates:
        state_file = path + "statelog " + d + ".xls"
        data_file = path + "datalog " + d + ".xls"

        states = pd.read_csv(state_file, delimiter='\t')
        data = pd.read_csv(data_file, delimiter='\t')

        states = np.array(states)
        data = np.array(data)

        # get the start and end times for the state
        state_start_idx = states[:, 2] == state
        state_start = states[state_start_idx, 0]
        state_end_idx = np.append([False], state_start_idx[0:(np.size(state_start_idx)-1)])
        state_end = states[state_end_idx, 0]

        if overnight:
            state_start = np.insert(state_start, 0, 0)
            state_end = np.insert(state_end, 0, states[0, 0])

        if state_start_idx[-1]:
            state_end.append(data[0, -1])

        # get the corresponding indices in the data array
        data_start = []
        data_end = []
        for i in range(np.size(state_start)):
            add_start = True
            for j in range(np.size(data[:, 0])):
                if (data[j, 0] > state_start[i]) and add_start:
                    data_start.append(j)
                    add_start = False
                if (data[j, 0] > state_end[i]):
                    data_end.append(j-1)
                    break

        if first_day:
            start_time = data[1, 0]

        # extract data at those times
        for i in range(np.size(data_start)):
            c = data[data_start[i]:data_end[i], column]
            if overnight and i == 0:
                data_agg = np.insert(data_agg[-1], np.size(data_agg[-1][:]), c)
            else:
                data_agg.append(c)

        day += 1
        if first_day:
            first_day = False
        if state_start_idx[-1]:
            overnight = True

    averages = np.zeros(np.size(data_agg))
    for i in range(np.size(data_agg)):
        averages[i] = np.average(data_agg[i])

    if units != "":
        return averages*u(units)
    else:
        return averages

def perform_function_on_state(func, dates, state, column, units="", path=""):
    """Performs the function given on each state of the data for the given state
    in the given column and outputs the result for each instance of the state

    Parameters
    ----------
    func : function
        A function which will be applied to data from each instance of the state

    dates : string list
        A list of dates for which data was recorded, in the form "M-D-Y"

    state : string
        The name of the state for which data should be extracted

    column : string
        Index of the column that you want to extract. Column 0 is time.
        The first data column is column 1.

    units : string
        The units you want to apply to the data, e.g. 'mg/L'.
        Defaults to "" which indicates no units

    path : strings
        Optional argument of the path to the folder containing your ProCoDA
        files. Defaults to the current directory if no argument is passed in

    Returns
    -------
    float list
        A list of averages for each instance of the given state

    Requires
    --------
    func takes in a list of data with units and outputs the correct units

    Example
    -------
    def avg_with_units(lst):
        num = np.size(lst)
        acc = 0
        for i in lst:
            acc = i + acc

        return acc / num

    data_avgs = perform_function_on_state(avg_with_units,["6-19-2013", "6-20-2013"], "1. Backwash entire system", 28, "mL/s")

    """
    data_agg = []
    day = 0
    first_day = True
    overnight = False

    for d in dates:
        state_file = path + "statelog " + d + ".xls"
        data_file = path + "datalog " + d + ".xls"

        states = pd.read_csv(state_file, delimiter='\t')
        data = pd.read_csv(data_file, delimiter='\t')

        states = np.array(states)
        data = np.array(data)

        # get the start and end times for the state
        state_start_idx = states[:, 2] == state
        state_start = states[state_start_idx, 0]
        state_end_idx = np.append([False], state_start_idx[0:(np.size(state_start_idx)-1)])
        state_end = states[state_end_idx, 0]

        if overnight:
            state_start = np.insert(state_start, 0, 0)
            state_end = np.insert(state_end, 0, states[0, 0])

        if state_start_idx[-1]:
            state_end.append(data[0, -1])

        # get the corresponding indices in the data array
        data_start = []
        data_end = []
        for i in range(np.size(state_start)):
            add_start = True
            for j in range(np.size(data[:, 0])):
                if (data[j, 0] > state_start[i]) and add_start:
                    data_start.append(j)
                    add_start = False
                if (data[j, 0] > state_end[i]):
                    data_end.append(j-1)
                    break

        if first_day:
            start_time = data[1, 0]

        # extract data at those times
        for i in range(np.size(data_start)):
            c = data[data_start[i]:data_end[i], column]
            if overnight and i == 0:
                data_agg = np.insert(data_agg[-1], np.size(data_agg[-1][:]), c)
            else:
                data_agg.append(c)

        day += 1
        if first_day:
            first_day = False
        if state_start_idx[-1]:
            overnight = True

    output = np.zeros(np.size(data_agg))
    for i in range(np.size(data_agg)):
        if units != "":
            output[i] = func(data_agg[i]*u(units))
        else:
            output[i] = func(data_agg[i])

    return output

def plot_state(dates, state, column, units="", path=""):
    """Reads a ProCoDA file and plots the data column for each iteration of
    the given state.

    Parameters
    ----------
    dates : string list
        A list of dates for which data was recorded, in the form "M-D-Y"

    state : string
        The name of the state which should be plotted

    column : string
        Index of the column that you want to extract. Column 0 is time.
        The first data column is column 1.

    units : string
        The units you want to apply to the data, e.g. 'mg/L'.
        Defaults to "" which indicates no units

    path : strings
        Optional argument of the path to the folder containing your ProCoDA
        files. Defaults to the current directory if no argument is passed in

    Returns
    -------
    None

    Example
    -------
    plot_state(["6-19-2013", "6-20-2013"], "1. Backwash entire system", 28, "mL/s")

    """
    data_agg = []
    day = 0
    first_day = True
    overnight = False

    for d in dates:
        state_file = path + "statelog " + d + ".xls"
        data_file = path + "datalog " + d + ".xls"

        states = pd.read_csv(state_file, delimiter='\t')
        data = pd.read_csv(data_file, delimiter='\t')

        states = np.array(states)
        data = np.array(data)

        # get the start and end times for the state
        state_start_idx = states[:, 2] == state
        state_start = states[state_start_idx, 0]
        state_end_idx = np.append([False], state_start_idx[0:(np.size(state_start_idx)-1)])
        state_end = states[state_end_idx, 0]

        if overnight:
            state_start = np.insert(state_start, 0, 0)
            state_end = np.insert(state_end, 0, states[0, 0])

        if state_start_idx[-1]:
            state_end.append(data[0, -1])

        # get the corresponding indices in the data array
        data_start = []
        data_end = []
        for i in range(np.size(state_start)):
            add_start = True
            for j in range(np.size(data[:, 0])):
                if (data[j, 0] > state_start[i]) and add_start:
                    data_start.append(j)
                    add_start = False
                if (data[j, 0] > state_end[i]):
                    data_end.append(j-1)
                    break

        if first_day:
            start_time = data[1, 0]

        # extract data at those times
        for i in range(np.size(data_start)):
            t = data[data_start[i]:data_end[i], 0] + day - start_time
            c = data[data_start[i]:data_end[i], column]
            if overnight and i == 0:
                data_agg = np.insert(data_agg[-1], np.size(data_agg[-1][:, 0]),
                                     np.vstack((t, c)).T)
            else:
                data_agg.append(np.vstack((t, c)).T)

        day += 1
        if first_day:
            first_day = False
        if state_start_idx[-1]:
            overnight = True

    plt.figure()
    for i in data_agg:
        t = i[:,0] - i[0,0]
        plt.plot(t,i[:,1])

    plt.show()
