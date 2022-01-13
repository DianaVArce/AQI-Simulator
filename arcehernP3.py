"""
Program: CS115 Project 3
Author: Diana Vanessa Arce-Hernandez

"""


def get_concentration(m):
    """Prompts the user for the reading from monitor m, then returns
    the concentration as an integer or float, rounding it according to the
    following conventions:
        PM-2.5: round to 1 decimal place (ug/m3)
        PM-10: round to integer (ug/m3)
        NO2: round to integer (ppb)
        SO2: round to integer (ppb)
        CO: round to 1 decimal place (ppm)
        O3: round to integer (ppb)

    Args:
        m (str): The type of monitor.

    Returns:
        int or float: The concentration.
    """
    d_list = ['PM-2.5 [ug/m3, 24-hr avg]', 'CO [ppm, 8-hr avg]']
    c = float(input("    -> {}: ".format(m)))
    if c == -1:
        return int(c)
    if m in d_list:
        return round(c, 1)
    else:
        return int(c)


def get_per_pollutant_index(breakpoints, monitors, m, c):
    """Generates the per-pollutant index using the AQI formula for
    the concentration 'c' associated with pollutant monitor 'm'. The
    calculation makes use of the EPA breakpoint table. If the concentration
    is out of range or should be ignored, returns -1; otherwise, returns
    the index that was calculated.

    Each row of 'breakpoints' has the following format:
       [category, [index_low, index_high], p_bounds_list]
    Where p_bounds_list is a 2D list of pollution concentration bounds; each
    row holds the bounds [c_low, c_high] for a particular monitor.

    Args:
        breakpoints (list):  A list of rows comprising the EPA breakpoint table.
        monitors (list): A list of monitors in the same order as p_bounds_list.
        m (str): The monitor originating the concentration.
        c (float or int): The concentration.

    Returns:
        int: The per-pollutant index or -1
    """
    result = -1
    column = monitors.index(m)
    for row in breakpoints:
        i_low = row[1][0]
        i_high = row[1][1]

        c_low = row[2][column][0]
        c_high = row[2][column][1]

        if c_low <= c and c <= c_high:
            result = round(int(i_high - i_low) / (c_high - c_low) * (c - c_low) + i_low)

    return result


def per_pollutant_concentration(location, concentration, index):
    """Prints the per-pollutant concentration for a given location, the
    given concentration, and the index.

    Arg:
        location (str): The city or location inputted by user
        c (int): concetration
        index (int): index
        Returns:
        int or float: The concentration.

    Returns:
       This function does not return anything.
    """

    if concentration != -1 and index > -1:
        print("      ", location, 'concentration', concentration, 'yields', index, 'index')


def Summary_Report(locations, AQI, pm25):
    """Prints a summary report for the location that has:
        the largest AQI, the smallest AQI, and the average PM-2.5
        concentration reading.

    Args:
       Location (str) = location inputted by the user
       AQI (int) = the air quality index

    Returns:
        This function does not return anything.
    """
    max_AQI = max(AQI)
    min_AQI = min(AQI)

    pm_avgerage = 0
    for i in range(len(pm25)):
        pm_avgerage += + float(pm25[i])

    max_city = ""
    for i in range(len(AQI)):
        if AQI[i] == max_AQI:
            max_city = locations[i]

    min_city = ""
    for i in range(len(AQI)):
        if AQI[i] == min_AQI:
            min_city = locations[i]

    print()
    print("Summary Report")
    print("    Location with max AQI is ", max_city, " (", max_AQI, ")", sep="")
    print("    Location with min AQI is ", min_city, " (", min_AQI, ")", sep="")

    if pm_avgerage <= 0:
        print("    Avg PM-2.5 concentration reading: No Data")
    else:
        pm_avgerage = int((pm_avgerage / len(pm25)) * 10)

        # This average is the final average after having been truncated.
        average = pm_avgerage / 10
        print("    Avg PM-2.5 concentration reading:", average)


def main():

    monitors = ['PM-2.5 [ug/m3, 24-hr avg]', 'PM-10 [ug/m3, 24-hr avg]',
                'NO2 [ppb, 1-hr avg]', 'SO2 [ppb, 1-hr avg]', 'CO [ppm, 8-hr avg]',
                'O3 [ppb, 8-hr avg]', 'O3 [ppb, 1-hr avg]']

    ignore = [float('inf'), float('-inf')]

    epa_table = [
        ['Good', [0, 50], [
            [0, 12.0], [0, 54], [0, 53],
            [0, 35], [0, 4.4], [0, 54], ignore
        ]],
        ['Moderate', [51, 100], [
            [12.1, 35.4], [55, 154], [54, 100],
            [36, 75], [4.5, 9.4], [55, 70], ignore
        ]],
        ['Unhealthy for Sensitive Groups', [101, 150], [
            [35.5, 55.4], [155, 254], [101, 360],
            [76, 185], [9.5, 12.4], [71, 85], [125, 164]
        ]],
        ['Unhealthy', [151, 200], [
            [55.5, 150.4], [255, 354], [361, 649],
            [186, 304], [12.5, 15.4], [86, 105], [165, 204]
        ]],
        ['Very Unhealthy', [201, 300], [
            [150.5, 250.4], [355, 424], [650, 1249],
            [305, 604], [15.5, 30.4], [106, 200], [205, 404]
        ]],
        ['Hazardous', [301, 500], [
            [250.5, 500.4], [425, 604], [1250, 2049],
            [605, 1004], [30.5, 50.4], ignore, [405, 604]
        ]]
    ]

    locations = []  # all locations
    aqi_indices = []  # the AQI reading for each location
    pm25_readings = []  # all PM-2.5 readings

    print('=== Air Quality Index (AQI) Calculator ===')
    location = input('\nEnter name of ** Location **: ')

    while location != '':
        if pm25_readings != -1:
            locations.append(location)

        concentrations = []
        ppi = []

        for m in monitors:
            c = get_concentration(m)
            concentrations.append(c)

            index = get_per_pollutant_index(epa_table, monitors, m, c)
            city_name = m.split()
            ppi.append(index)

            #these nested loops are for 8-hr and 1-hr readings that are not equal to -1
            if m == monitors[6]:
                if index > ppi[-2]:
                    per_pollutant_concentration(city_name[0], c, index)
                else:
                    city_name = monitors[-2].split()
                    per_pollutant_concentration(city_name[0], concentrations[-2], ppi[-2])
            elif m != monitors[5]:
                per_pollutant_concentration(city_name[0], c, index)

            if 'PM-2.5' in m and c != -1:
                pm25_readings.append(c)

        AQI = max(ppi)
        aqi_indices.append(AQI)

        print("    AQI for", location, "is", AQI)
        for row in epa_table:
            if row[1][0] <= AQI <= row[1][1]:
                print('    Condition:', row[0])

        location = input('\nEnter name of ** Location **: ')

    #calls the summary report function to print a report at the end of program
    Summary_Report(locations, aqi_indices, pm25_readings)

main()
