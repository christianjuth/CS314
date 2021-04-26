import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import csv
import functools as ft
import numpy as np
from operator import itemgetter
import sys



'''
Compatible with Python3.6
################################ ***************************** ####################################################
# Do not import any additional libraries. Everything that is needed to complete the assignment is already imported.
# Also, please do not use numpy in any of the code you will be filling in.
#   Points will be deducted for using numpy built in functions.
# Functools can only be used to call on the 'reduce' fuction. ie: ft.reduce()
#   All other functions used from functools will result in point deductions
################################ ***************************** ####################################################
'''



'''
################################ Project Overview #################################################################
Data science can be as much an art as .. well, a science. Understanding how different analyses work, what they can do and what their limitations are allows you to use them effectively. Choosing the right types of analysis can be quite tricky. When faced with a sea of data, how are you to condition and measure it in order to wring out some useful observations? Well, that is not the subject of this course. You will however get a taste of how to use Python in order to perform data analysis.

The analyses necessary to generate some interesting observations on GDP, energy use and population mechanics is below, however it needs some critical parts filled in. First you'll fill in some functions that will provide fundamental numerical measurements that will power the statistical analyses that come later. Afterward, you'll use the imported data and some of the functions you've written to generate some the observations. The sourcing and cleaning of the data, the analysis and conditioning and plotting has already been done for you!

Look for the sections below that are marked:
    #### FILL IN CODE HERE ####
    or:
    # FILL IN CODE HERE
    
  to find the places below where your Python expertise is needed.
 
Python is often used in data science and analysis because it is fairly easily to represent data as streams of values that can have actions applied to them. Many types of statistical analysis take this form; apply an operation to a stream of values or to corresponding values in different streams, then use the output of one result as the input to another. Making this linking of operations on streams of data simple to code and graph means Python is fairly well suited for investigating decently-sized sets of data.  

To get started, first download the dataset at:
    https://perso.telecom-paristech.fr/eagan/class/igr204/data/factbook.csv
.. and make sure that the 'factbook.csv' file is in the same directory as this code file.

Then, look for parts labelled:
    #### FILL IN CODE HERE ####
    or:
    # FILL IN CODE HERE
.. in the code and fill in the required functionality.

Then use the functions you coded to complete the analysis/investigation parts entitled:
 question0
 question1
 question2
 question3
Refer to the commented instructions at each specific function for more detailed description of what to code.

Once you fill in the computations to generate the necessary statistics, the following graphs will automatically be generated to demonstrate an observation/answer to each question:
(be sure to submit your completed CS314_Project2.py file, not the images!)
-question0:
'Q0_0_Plots.png'
'Q0_1_Plots.png'

-question1
'Q1_0_Plots.png'
'Q1_1_Plots.png'

-question2
'Q2_0_Plots.png'
'Q2_1_Plots.png'

-question3
'Q3_Linear_Model_Fit_Plots.png'


In order to complete your project, submit your working CS314_Project2.py ,not the images!
'''




class data_analysis:
    def __init__(self):
        self.data_file = 'factbook.csv'

        self.fields_list_IN = [
            'Country',
            'Area(sq km)',
            'Birth rate(births/1000 population)',
            'Current account balance',
            'Death rate(deaths/1000 population)',
            'Debt - external',

            'Electricity - consumption(kWh)',
            'Electricity - production(kWh)',
            'Exports',
            'GDP',
            'GDP - per capita',

            'GDP - real growth rate(%)',
            'HIV/AIDS - adult prevalence rate(%)',
            'HIV/AIDS - deaths',
            'HIV/AIDS - people living with HIV/AIDS',
            'Highways(km)',

            'Imports',
            'Industrial production growth rate(%)',
            'Infant mortality rate(deaths/1000 live births)',
            'Inflation rate (consumer prices)(%)',
            'Internet hosts',

            'Internet users',
            'Investment (gross fixed)(% of GDP)',
            'Labor force',
            'Life expectancy at birth(years)',
            'Military expenditures - dollar figure',

            'Military expenditures - percent of GDP(%)',
            'Natural gas - consumption(cu m)',
            'Natural gas - exports(cu m)',
            'Natural gas - imports(cu m)',
            'Natural gas - production(cu m)',

            'Natural gas - proved reserves(cu m)',
            'Oil - consumption(bbl/day)',
            'Oil - exports(bbl/day)',
            'Oil - imports(bbl/day)',
            'Oil - production(bbl/day)',

            'Oil - proved reserves(bbl)',
            'Population',
            'Public debt(% of GDP)',
            'Railways(km)',
            'Reserves of foreign exchange & gold',

            'Telephones - main lines in use',
            'Telephones - mobile cellular',
            'Total fertility rate(children born/woman)',
            'Unemployment rate(%)'
        ]

        self.fields_type_list_IN = ['string']
        self.fields_type_list_IN.extend(['float' for i in range(0,len(self.fields_list_IN)-1)])

        # Reads the csv dataset into global variable self.data_l
        self.data_l = self.read_data_file(fields_list=self.fields_list_IN, types_list=self.fields_type_list_IN)


    ##################################### DO NOT CHANGE THESE FUNCTIONS #################################### START

    ########## Read data file function #############
    def read_data_file(self, fields_list, types_list):

        '''
        # File reading function accepting two arguments

        :param fields_list: fields of the dataset
        :param types_list: the type to convert the field data into
        :return: 
        '''

        csv_file = self.data_file
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file, delimiter=';')
            line_count = 0

            search_field_idx_l = []
            data_list = []
            for j in range(0, len(fields_list)):
                data_list.append([])

            for row in csv_reader:

                if line_count == 0:
                    for search_field in fields_list:
                        for field_idx, field in enumerate(row):
                            if search_field == field:
                                search_field_idx_l.append(field_idx)
                    line_count += 1

                    # print(row)
                elif line_count == 1:
                    line_count += 1

                else:
                    disqualify = False
                    for k in range(0, len(search_field_idx_l)):
                        if row[search_field_idx_l[k]] == '':
                            disqualify = True
                    if disqualify == True:
                        continue
                    else:
                        line_count += 1
                    for k in range(0, len(search_field_idx_l)):
                        if types_list[k] == 'string':
                            data_list[k].append(str(row[search_field_idx_l[k]]))
                        elif types_list[k] == 'float':
                            data_list[k].append(float(row[search_field_idx_l[k]]))

                            # if line_count==5:
                            #     break

        return data_list

    ########## Basic operations functions #############
    def find_largest_value(self,data_list):
        max_value = data_list[0]
        for i in range(1,len(data_list)):
            if data_list[i]>max_value:
                max_value=data_list[i]
        return max_value

    def apply_power(self,a,p):
        return a**p

    def subtract_numbers(self,a,b):
        return a-b

    def add_numbers(self,a,b):
        return a+b

    def multiply_numbers(self,a,b):
        return a*b

    def divide_numbers(self,a,b):
        return a/b

    def greater_than(self,value,threshold):
        return value>threshold

    def less_than(self,value,threshold):
        return value<threshold

    ##################################### DO NOT CHANGE THESE FUNCTIONS #################################### END

    ################################## FILL IN THESE FUNCTIONS ################################# START
    def normalize_series(self,data_series):

        '''
        This function takes a list of values called 'data_series' and needs to normalize this list.
        To normalize the data_series list, each value in the data_series needs to be divided by the sum of all values in the list.
        Output is the normalized list named 'normalized_series', in the same order as the input list.
        
        Example: 
            Input: [1,2,3,4,5] 
                ->
            Output: [0.06666666666666667, 0.13333333333333333, 0.2, 0.26666666666666666, 0.3333333333333333]
            
        '''

        arrSum = 0
        for num in data_series:
            arrSum += num

        normalized_series = []

        for i in range(len(data_series)):
            normalized_series.append(data_series[i] / arrSum)

        return normalized_series



    def compute_average_across_series(self,list_of_series):

        '''
        This function takes as input a list of arbitrarily many sub-lists, with each sub-list being the same length.
        This function needs to output a list that holds the average of all corresponding values over all sub-lists.
        For example, the first value in the output list will be the average of all the first values of all the sub-lists and
                the second falue in the output list will be the average of all the second values of all the sub-lists, etc.
                
        To compute average implement following steps:
            1. Add up all the lists in list_of_series, resulting in a sum list.
            2. Divide each element in sum list from step 1 by the number of lists in list_of_series.
        
        Example:
            Input: [[0,10,20],[10,20,30]] 
                -> 
            Output: [5.0, 15.0, 25.0]
            
        '''

        average_list = []

        if len(list_of_series) == 0:
            return []
        
        length = len(list_of_series[0])
        for _ in range(length):
            average_list.append(0)
        
        for arr in list_of_series:
            i = 0
            for num in arr:
                average_list[i] = average_list[i] + num
                i += 1

        for i in range(length):
            average_list[i] = average_list[i] / len(list_of_series)

        return average_list



    def compute_standard_deviation_across_series(self,list_of_series,average_series):

        '''
        This function takes as input 
            1. a list of arbitrarily many sub-lists, with each sub-list being the same length.
            2. a list representing the average of all the lists
        This function needs to output a list that is the standard deviation of all the sub-lists.
        So each element in output list is the standard deviation of all corresponding elements in all sub-lists.
        To compute the standard deviation:
            1. Subtract the average_of_series list from each list list_of_data_series list and take the resulting difference lists to the power of 2
            2. Add up all the lists from step 1, resulting in a sum list.
            3. Divide each element of the sum list form step 2 by the number of lists in list_of_series
            4. Take the square root of each element in the list from step 3
        
        Example:
            Inputs: [[0,10,20],[10,20,30]] , [5.0, 15.0, 25.0]
                ->
            Output: [5.0, 5.0, 5.0]
        
        '''

        # Step 1
        step1 = []

        i = 0
        for lst in list_of_series:
            step1.append([])
            j = 0
            for num in lst:
                val = num - average_series[j]
                val = val ** 2
                step1[i].append(val)
                j += 1
            i += 1

        # Step 2
        std_list = []

        for _ in average_series:
            std_list.append(0)

        for arr in step1:
            i = 0
            for num in arr:
                std_list[i] = std_list[i] + num
                i += 1

        # Steps 3 and 4
        for i in range(len(std_list)):
            std_list[i] /= len(list_of_series)
            std_list[i] = std_list[i] ** (1.0/2.0)

        return std_list



    def compute_correlations(self,data_series_1,data_series_2):

        '''
        This function takes as input two lists of same length.
        It outputs a list of element by element correlation of these two lists. To compute correlation between two lists:
            1. Compute average of each list
            2. Subtract list average from every element in the list (repeat for both lists)
            3. Multiply the corresponding differences for each each list. (first by first, second by second, etc.)
            
        Example:
            [-10,0,10,20],[20,10,10,20]
                ->
            [-75.0, 25.0, -25.0, 75.0]
        
        '''

        # Step 1
        series1_sum = 0
        for num in data_series_1:
            series1_sum += num
        series1_avg = series1_sum / len(data_series_1)

        series2_sum = 0
        for num in data_series_2:
            series2_sum += num
        series2_avg = series2_sum / len(data_series_2)

        # Step 2
        series1 = []
        series2 = []
        for i in range(len(data_series_1)):
            series1.append(data_series_1[i] - series1_avg)

        for i in range(len(data_series_2)):
            series2.append(data_series_2[i] - series2_avg)

        # Step 3
        net_correlation = []
        for i in range(len(series1)):
            net_correlation.append(series1[i] * series2[i])

        return net_correlation



    def compute_net_correlation(self,data_series_1,data_series_2):

        '''
        This function takes as input two lists of same length.
        It outputs net correlation value between these two lists. To compute correlation between two lists:
            1. Compute the average of each list
            2. Subtract a list's average from every element in the list (repeat for both lists)
            3. Multiply corresponding differences from each list to compute the element-wise correlation
            4. Sum all the values from step 3 to compute the net correlation value
        
        Example:
            [-10,0,10,20],[20,10,10,20]
                ->
            0
        
        '''
        
        net_correlation = self.compute_correlations(data_series_1, data_series_2)

        net_correlation_sum = 0
        for num in net_correlation:
            net_correlation_sum += num

        return net_correlation_sum



    def compute_ratio(self,data_series_1,data_series_2):

        '''
        This function takes as input two lists of same length.
        It outputs a list that holds the ratio of corresponding elements from the two input lists, data_series_1/data_series_2 
        Make sure function will gracefully fail if a 0 is encountered in data_series_2 (ie. return problem, not error)
        
        Example:
            [2, 3, 6],[2, 1.5, 2]
                ->
            [1, 2, 3]
        
        '''

        ratio_list = []
        for i in range(len(data_series_1)):
            if data_series_2[i] == 0:
                sys.exit("Divide by zero error")
            
            ratio_list.append(data_series_1[i] / data_series_2[i])

        return ratio_list



    def compute_average_of_series(self,data_series):

        '''
        This function takes as input a list.
        It outputs the average (arithmetic mean) of the input list. To compute average implement following steps:
            1. Sum all the elements of the data_series
            2. Divide the above computed sum by the length of the data_series
        
        Example:
            [1,2,3]
                ->
            2

        '''

        arrSum = 0
        for num in data_series:
            arrSum += num

        return arrSum / len(data_series)



    def compute_standard_deviation_of_series(self,data_series,average_of_series):

        '''
        This function takes as input a list.
        It outputs the standard deviation of the input list. To compute the standard deviation:
            1. Subtract the average_of_series value from each element in data_series and take this difference to the power of 2
            2. Sum all values computed in step 1
            3. Divide value from step 2 by the length of data_series list
            4. Take the square root of value form step 3
            
            
        Example:
            [1,2,3],2
                ->
            0.816496580927726

        '''
        
        # Steps 1 and 2
        arrSum = 0
        for num in data_series:
            tmp = num - average_of_series
            arrSum += tmp ** 2

        # Step 3
        step3 = arrSum / len(data_series)

        # Step 4
        series_standard_deviation = step3 ** (1.0/2.0)

        return series_standard_deviation



    ################################## FILL IN THESE FUNCTIONS ################################# END

    ################################## Question Functions with build in plotting ################################# START

    def question0(self):

        '''
        In this question, you will explore the relationship between different energy sources and gdp per capita.
        First, you will compute and look at:
            1. Oil consumption per capita
            2. Electricity consumption per capita
            3. Natural Gas consumption per capita
            4. Oil production per capita
            5. Electricity production per capita
            6. Natural Gas production per capita
            vs
            GDP - per capita
        You should observe that consumption of all 3 energy sources is positively related to gdp per capita
        
        Second, you will make the 3 energy sources consumption measures comparable and compute:
            Average +/- standard deviation energy consumption
        
        '''

        # Extracts data series - don't change
        oc_raw = self.data_l[self.fields_list_IN.index('Oil - consumption(bbl/day)')]
        ec_raw = self.data_l[self.fields_list_IN.index('Electricity - consumption(kWh)')]
        gc_raw = self.data_l[self.fields_list_IN.index('Natural gas - consumption(cu m)')]
        op_raw = self.data_l[self.fields_list_IN.index('Oil - production(bbl/day)')]
        ep_raw = self.data_l[self.fields_list_IN.index('Electricity - production(kWh)')]
        gp_raw = self.data_l[self.fields_list_IN.index('Natural gas - production(cu m)')]
        gdppc_raw = self.data_l[self.fields_list_IN.index('GDP - per capita')]
        pop_raw = self.data_l[self.fields_list_IN.index('Population')]


        '''
        # Compute energy consumption/production per capita
        Use function compute_ratio to divide each of series:
            1.oc_raw
            2.ec_raw
            3.gc_raw
            4.op_raw
            5.ep_raw
            6.gp_raw
            by series pop_raw
        '''
        #### FILL IN CODE #### START
        oil_consumption_pc = self.compute_ratio(oc_raw, pop_raw)
        electricity_consumption_pc = self.compute_ratio(ec_raw, pop_raw)
        gas_consumption_pc = self.compute_ratio(gc_raw, pop_raw)
        oil_production_pc = self.compute_ratio(op_raw, pop_raw)
        electricity_production_pc = self.compute_ratio(ep_raw, pop_raw)
        gas_production_pc = self.compute_ratio(gp_raw, pop_raw)
        #### FILL IN CODE #### END

        # Visualize per capita energy consumption and production vs gdp per capita - don't change
        fig0 = plt.figure(figsize=(19,10))
        ax0_1 = fig0.add_subplot(231)
        ax0_2 = fig0.add_subplot(232)
        ax0_3 = fig0.add_subplot(233)
        ax0_4 = fig0.add_subplot(234)
        ax0_5 = fig0.add_subplot(235)
        ax0_6 = fig0.add_subplot(236)

        dot_size=15
        ax0_1.scatter(gdppc_raw,oil_consumption_pc, c='k', s = dot_size)
        ax0_2.scatter(gdppc_raw,electricity_consumption_pc, c = 'k', s = dot_size)
        ax0_3.scatter(gdppc_raw,gas_consumption_pc, c = 'k', s = dot_size)
        ax0_4.scatter(gdppc_raw,oil_production_pc, c = 'k', s = dot_size)
        ax0_5.scatter(gdppc_raw,electricity_production_pc, c = 'k', s = dot_size)
        ax0_6.scatter(gdppc_raw,gas_production_pc, c = 'k', s = dot_size)
        ax0_1.set_xlabel('GDP - per capita')
        ax0_2.set_xlabel('GDP - per capita')
        ax0_3.set_xlabel('GDP - per capita')
        ax0_4.set_xlabel('GDP - per capita')
        ax0_5.set_xlabel('GDP - per capita')
        ax0_6.set_xlabel('GDP - per capita')
        ax0_1.set_ylabel('Oil - consumption(bbl/day) - per capita')
        ax0_2.set_ylabel('Electricity - consumption(kWh) - per capita')
        ax0_3.set_ylabel('Natural gas - consumption(cu m) - per capita')
        ax0_4.set_ylabel('Oil - production(bbl/day) - per capita')
        ax0_5.set_ylabel('Electricity - production(kWh) - per capita')
        ax0_6.set_ylabel('Natural gas - production(cu m) - per capita')
        ax0_1.grid()
        ax0_2.grid()
        ax0_3.grid()
        ax0_4.grid()
        ax0_5.grid()
        ax0_6.grid()

        '''
        Normalize the per capital consumption data of each energy source to make them comparable
        Specifically normalize sereis: 1. oil_consumption_pc, electricity_consumption_pc, gas_consumption_pc 
        '''
        #### FILL IN CODE #### START
        oil_consumption_per_capita_norm = self.normalize_series(oil_consumption_pc)
        electricity_consumption_per_capita_norm = self.normalize_series(electricity_consumption_pc)
        gas_consumption_per_capita_norm = self.normalize_series(gas_production_pc)
        #### FILL IN CODE #### END

        '''
        Compute average and standard deviation series of the 3 energy sources
        So use compute_average_across_series,compute_standard_deviation_across_series functions on:
          [oil_consumption_per_capita_norm, electricity_consumption_per_capita_norm, gas_consumption_per_capita_norm] 
        '''
        #### FILL IN CODE #### START
        energy_consumption_average = self.compute_average_across_series([oil_consumption_per_capita_norm, electricity_consumption_per_capita_norm, gas_consumption_per_capita_norm])
        energy_consumption_std = self.compute_standard_deviation_across_series([oil_consumption_per_capita_norm, electricity_consumption_per_capita_norm, gas_consumption_per_capita_norm], energy_consumption_average)
        #### FILL IN CODE #### END

        # Sort series by gdp per capita - don't change
        data_to_sort0 = zip(gdppc_raw, oil_consumption_per_capita_norm, electricity_consumption_per_capita_norm, gas_consumption_per_capita_norm,energy_consumption_average,energy_consumption_std)
        sorted_data0 = sorted(data_to_sort0, key=itemgetter(0))
        gdppc_raw_sorted, oil_consumption_per_capita_norm_sorted, electricity_consumption_per_capita_norm_sorted, gas_consumption_per_capita_norm_sorted,energy_consumption_ave_sorted,energy_consumption_std_sorted = zip(*sorted_data0)

        # Visualization code - don't change
        fig1 = plt.figure(figsize=(19,10))
        ax1_1 = fig1.add_subplot(121)
        ax1_2 = fig1.add_subplot(122)
        ax1_1.plot(list(gdppc_raw_sorted), list(oil_consumption_per_capita_norm_sorted), c='b', label='Oil')
        ax1_1.plot(list(gdppc_raw_sorted), list(electricity_consumption_per_capita_norm_sorted), c='r', label='Electricity')
        ax1_1.plot(list(gdppc_raw_sorted), list(gas_consumption_per_capita_norm_sorted), c='g', label='Natural Gas')
        ax1_1.scatter(list(gdppc_raw_sorted), list(oil_consumption_per_capita_norm_sorted), c='b', s = dot_size)
        ax1_1.scatter(list(gdppc_raw_sorted), list(electricity_consumption_per_capita_norm_sorted), c='r', s = dot_size)
        ax1_1.scatter(list(gdppc_raw_sorted), list(gas_consumption_per_capita_norm_sorted), c='g', s = dot_size)
        ax1_1.set_xlabel('GDP - per capita')
        ax1_1.set_ylabel('Energy Consumption %')
        ax1_1.legend()

        ax1_2.errorbar(list(gdppc_raw_sorted), energy_consumption_ave_sorted,energy_consumption_std_sorted, c='k',capsize=5)
        ax1_2.scatter(list(gdppc_raw_sorted), energy_consumption_ave_sorted, c='k', s = dot_size)
        ax1_2.set_xlabel('GDP - per capita')
        ax1_2.set_ylabel('Energy Consumption % Averaged')
        ax1_1.grid()
        ax1_2.grid()

        fig0_fn = 'Q0_0_Plots.png'
        fig0.savefig(fig0_fn)

        fig1_fn = 'Q0_1_Plots.png'
        fig1.savefig(fig1_fn)

        return energy_consumption_average


    def question1(self):

        '''
        In this question, you will explore the relationship between infant mortality and fertility rate vs gdp per capita.
        First, you will compute and look at:
            1. Net correlation between infant mortality rate and total fertility rate. 
                You should observe that these two factors are correlated together.
            2. Kid fatality per woman (the opposite of fertility rate)
                You should observe that this metric is non-linearly negatively correlated with GDP-per capita
            3. Net fertility rate
                You should observe that this metric is non-linearly negatively correlated with GDP-per capita
            4. Ratio of net fertility rate and fatality rate
                You should observe that this metric is highly correlated with GDP - per capita
            vs
            GDP - per capita
        
        Second, you will make the 3 energy sources consumption measures comparable and compute:
            Average +/- standard deviation energy consumption

        '''

        # Extracts data series - don't change
        infant_mortality_rate = self.data_l[self.fields_list_IN.index('Infant mortality rate(deaths/1000 live births)')]
        fertility_rate = self.data_l[self.fields_list_IN.index('Total fertility rate(children born/woman)')]
        gdppc_raw = self.data_l[self.fields_list_IN.index('GDP - per capita')]

        # Visualization code - don't change
        fig2 = plt.figure(figsize=(19,10))
        ax2_1 = fig2.add_subplot(131)
        ax2_2 = fig2.add_subplot(132)
        ax2_3 = fig2.add_subplot(133)
        dot_size = 15
        ax2_1.scatter(gdppc_raw, infant_mortality_rate, c='k', s=dot_size)
        ax2_2.scatter(gdppc_raw, fertility_rate, c='k', s=dot_size)
        ax2_3.scatter(infant_mortality_rate, fertility_rate, c='k', s=dot_size)
        ax2_1.set_xlabel('GDP - per capita')
        ax2_2.set_xlabel('GDP - per capita')
        ax2_3.set_xlabel('Infant mortality rate(deaths/1000 live births)')
        ax2_1.set_ylabel('Infant mortality rate(deaths/1000 live births)')
        ax2_2.set_ylabel('Total fertility rate(children born/woman)')
        ax2_3.set_ylabel('Total fertility rate(children born/woman)')
        ax2_1.grid()
        ax2_2.grid()
        ax2_3.grid()

        '''
        Compute net correlation between infant mortality rate and total fertitlity rate
        So apply function compute_net_correlation to data series: infant_mortality_rate,fertility_rate
        '''
        #### FILL IN CODE #### START
        net_correlation_infant_fatality_rate_and_fertility_rate = self.compute_net_correlation(infant_mortality_rate, fertility_rate)
        #### FILL IN CODE #### END


        '''
        Compute net fertility rate (number of kids that survive/woman)
        To get fertility rate compute following:
            kid_fatality_per_woman: fertility_rate*infant_mortality_rate/1000
            net_fertility_rate: fertility_rate-kid_fatality_per_woman
            ratio_survival_over_fatality_per_woman: net_fertility_rate/kid_fatality_per_woman
        '''
        #### FILL IN CODE #### START
        kid_fatality_per_woman = list(map(
            self.divide_numbers,
            list(map(self.multiply_numbers, fertility_rate, infant_mortality_rate)),
            list(map(lambda x: 1000, fertility_rate))
        ))
        net_fertility_rate = list(map(self.subtract_numbers, fertility_rate, kid_fatality_per_woman))
        ratio_survival_over_fatality_per_woman = list(map(self.divide_numbers, net_fertility_rate, kid_fatality_per_woman))
        #### FILL IN CODE #### END

        '''
        Compute net correlation between ratio_survival_over_fatality_per_woman vs GDP-per capita
        To do so apply function compute_net_correlation to ratio_survival_over_fatality_per_woman,gdppc_raw
        '''
        #### FILL IN CODE #### START
        net_correlation_ratio_survival_over_fatality_per_woman_vs_gdppc = self.compute_net_correlation(ratio_survival_over_fatality_per_woman,gdppc_raw)
        #### FILL IN CODE #### END


        # Visualization code - don't change
        ax2_3.set_title('Net_Correlation: ' + str(net_correlation_infant_fatality_rate_and_fertility_rate))
        fig3 = plt.figure(figsize=(19,10))
        ax3_1 = fig3.add_subplot(131)
        ax3_2 = fig3.add_subplot(132)
        ax3_3 = fig3.add_subplot(133)
        ax3_1.scatter(gdppc_raw,kid_fatality_per_woman, c='k', s=dot_size)
        ax3_2.scatter(gdppc_raw, net_fertility_rate, c='k', s=dot_size)
        ax3_3.scatter(gdppc_raw, ratio_survival_over_fatality_per_woman, c='k', s=dot_size)
        ax3_3.set_title('Net_Correlation: '+str(net_correlation_ratio_survival_over_fatality_per_woman_vs_gdppc))
        ax3_1.set_xlabel('GDP - per capita')
        ax3_2.set_xlabel('GDP - per capita')
        ax3_3.set_xlabel('GDP - per capita')
        ax3_1.set_ylabel('Kid fatality rate per woman')
        ax3_2.set_ylabel('Net fertility rate(children born+survived/woman)')
        ax3_3.set_ylabel('Net fertility rate/Fatality rate')
        ax3_1.grid()
        ax3_2.grid()
        ax3_3.grid()

        fig2_fn = 'Q1_0_Plots.png'
        fig2.savefig(fig2_fn)

        fig3_fn = 'Q1_1_Plots.png'
        fig3.savefig(fig3_fn)

        return ratio_survival_over_fatality_per_woman


    def question2(self):

        '''
        In this question, you will explore the relationship between country's birth rate and death rate vs GDP-per capita.
        First, you will compute and look at:
            1. Birth rate and death rate vs GDP- per capita. 
                You should observe that death rate is positively correlated with GDP- per capita.
                You should observe that birth rate is negatively correlated with GDP- per capita.
            2. Element-wise correlation between birth rate and death rate.
                You should observe that birth rate and death rate are anti correlated for low GDP-per capita countries 
                and uncorrelated for higher GDP-per capita countries
            3. Net birth rate vs GDP-per capita
                You should observe that there is a threshold in GDP-per capita that splits countries into two groups:
                    1. High net birth rate -> low GDP-per capita
                    2. Low net birth rate -> high GDP-per capita
            4. Generate the list of countries in 3.1, and 3.2 above
                
        '''


        # Extracts data series - don't change
        birth_rate = self.data_l[self.fields_list_IN.index('Birth rate(births/1000 population)')]
        death_rate = self.data_l[self.fields_list_IN.index('Death rate(deaths/1000 population)')]
        gdppc_raw = self.data_l[self.fields_list_IN.index('GDP - per capita')]
        countries_raw = self.data_l[self.fields_list_IN.index('Country')]

        '''
        Compute element wise correlation between birth_rate and death_rate by applying using compute_correlations
        '''
        #### FILL IN CODE #### START
        correlation_series = self.compute_correlations(birth_rate, death_rate)
        #### FILL IN CODE #### END

        '''
        Compute the net birth rate by taking difference: birth_rate-death_rate
        '''
        #### FILL IN CODE #### START
        net_birth_rate = list(map(self.subtract_numbers, birth_rate, death_rate))
        #### FILL IN CODE #### END


        # Visualization code - don't change
        dot_size = 15
        fig4 = plt.figure(figsize=(19,10))
        ax4_1 = fig4.add_subplot(211)
        ax4_2 = fig4.add_subplot(212)
        fig5 = plt.figure(figsize=(19,10))
        ax5_1 = fig5.add_subplot(111)
        ax4_1.scatter(gdppc_raw, birth_rate, label='birth_rate', c = 'g', s = dot_size)
        ax4_1.scatter(gdppc_raw, death_rate, label='death_rate',c = 'r', s = dot_size)
        ax4_2.scatter(gdppc_raw, correlation_series, c='k', s=dot_size)
        ax4_1.set_xlabel('GDP - per capita')
        ax4_2.set_xlabel('GDP - per capita')
        ax4_1.set_ylabel('Rate per 1000')
        ax4_2.set_ylabel('Correlation')
        ax4_1.legend()
        ax4_1.grid()
        ax4_2.grid()
        ax5_1.scatter(gdppc_raw, net_birth_rate, c='k', s=dot_size)
        ax5_1.set_xlabel('GDP - per capita')
        ax5_1.set_ylabel('Net Rate per 1000')


        # GDP-per capita threshold, don't change
        gdp_per_capita_threshold = 11000 # round to nearest thousand

        '''
        Fill the initialized lists:
            1. high_net_birth_rate_countries: list of countries with GDP-per capita smaller than gdp_per_capita_threshold
            2. low_net_birth_rate_countries: list of countries with GDP-per capita larger than gdp_per_capita_threshold  
        So you need to filter for countries with GDP-per capita above/below the threshold
        '''
        high_net_birth_rate_countries = [] # don't change
        low_net_birth_rate_countries = [] # don't change
        #### FILL IN CODE #### START
        high_net_birth_rate_countries = list(map(
            lambda x: x[0],
            list(filter(lambda x: x[1] < gdp_per_capita_threshold, 
                list(map(lambda x, y: [x, y], countries_raw, gdppc_raw))
            ))
        ))
        low_net_birth_rate_countries = list(map(
            lambda x: x[0],
            list(filter(lambda x: x[1] > gdp_per_capita_threshold, 
                list(map(lambda x, y: [x, y], countries_raw, gdppc_raw))
            ))
        ))
        #### FILL IN CODE #### END

        '''
        Compute the average and standard deviation GDP-per capita of each group of countries from above:
            1. high_net_birth_rate_countries
            2. low_net_birth_rate_countries
        Use functions compute_average_of_series,compute_standard_deviation_of_series
        '''
        #### FILL IN CODE #### START
        high_net_birthrate_gdppc_average = self.compute_average_of_series(
            # Im so sorry for this, but since we only stored countries previously,
            # we need to retrieve the values assosiated with those countries
            list(map(
                lambda x: x[1],
                list(filter(
                    lambda x: x[0] in high_net_birth_rate_countries,
                    list(map(lambda x, y: [x, y], countries_raw, gdppc_raw))
                ))
            ))
        )
        high_net_birthrate_gdppc_std = self.compute_standard_deviation_of_series(
            list(map(
                lambda x: x[1],
                list(filter(
                    lambda x: x[0] in high_net_birth_rate_countries,
                    list(map(lambda x, y: [x, y], countries_raw, gdppc_raw))
                ))
            )),
            high_net_birthrate_gdppc_average
        )
        low_net_birthrate_gdppc_average = self.compute_average_of_series(
            list(map(
                lambda x: x[1],
                list(filter(
                    lambda x: x[0] in low_net_birth_rate_countries,
                    list(map(lambda x, y: [x, y], countries_raw, gdppc_raw))
                ))
            ))
        )
        low_net_birthrate_gdppc_std = self.compute_standard_deviation_of_series(
            list(map(
                lambda x: x[1],
                list(filter(
                    lambda x: x[0] in low_net_birth_rate_countries,
                    list(map(lambda x, y: [x, y], countries_raw, gdppc_raw))
                ))
            )),
            low_net_birthrate_gdppc_average
        )
        #### FILL IN CODE #### END

        # Print lists of countries, don't change
        print('Countries with high net birth     rate:')
        print('Average GDP - per capita: '+str(low_net_birthrate_gdppc_average)+' +/- '+str(low_net_birthrate_gdppc_std))
        for c_idx ,c in enumerate(low_net_birth_rate_countries):
            print(str(c_idx)+'. ' + str(c))
        print('Countries with low net birth rate:')
        print('Average GDP - per capita: ' + str(high_net_birthrate_gdppc_average) + ' +/- ' + str(
            high_net_birthrate_gdppc_std))
        for c_idx, c in enumerate(high_net_birth_rate_countries):
            print(str(c_idx) + '. ' + str(c))
        ax5_1.axvline(x=gdp_per_capita_threshold,linestyle='--',label='GDP - per capita threshold')
        ax5_1.legend()
        ax5_1.grid()

        fig4_fn = 'Q2_0_Plots.png'
        fig4.savefig(fig4_fn)

        fig5_fn = 'Q2_1_Plots.png'
        fig5.savefig(fig5_fn)

        return net_birth_rate


    def question3(self,energy_consumption_average_IN,ratio_kids_survive_over_kids_fatality_IN):

        '''
        In this question, use 2 metrics from previous questions to predict GDP-per capita using a linear model.
        The hard part of constructing a model is done for you. 
        Plus, you have already generated all the needed metrics in previous questions.
        Here, all you have to do is generate the test data in the appropriate ranges.
        '''

        # Extraction of data, don't change
        gdppc_raw = self.data_l[self.fields_list_IN.index('GDP - per capita')]

        '''
        Test data for energy consumption average data
        Generate a list of length 10 with equally spaced values starting from 0.01 and ending with 0.12
        '''
        #### FILL IN CODE #### START
        t1 = [0.01 + x * ((0.12 - 0.01) / 9) for x in range(0, 10)]
        #### FILL IN CODE #### END

        '''
        Test data for energy consumption average data
        Generate a list of length 10 with equally spaced values starting from 30 and ending with 270
        '''
        #### FILL IN CODE #### START
        t2 = [30 + x * ((270 - 30) / 9) for x in range(0, 10)]
        #### FILL IN CODE #### END

        # Model Fitting, don't change
        A1 = np.vstack([np.asarray(energy_consumption_average_IN), np.ones(len(energy_consumption_average_IN))]).T
        print(np.asarray(gdppc_raw))
        m1, c1 = np.linalg.lstsq(A1, np.asarray(gdppc_raw), rcond=None)[0]
        A2 = np.vstack([np.asarray(ratio_kids_survive_over_kids_fatality_IN), np.ones(len(ratio_kids_survive_over_kids_fatality_IN))]).T
        m2, c2 = np.linalg.lstsq(A2, np.asarray(gdppc_raw), rcond=None)[0]
        predicted_gdppc1 = m1*np.asarray(t1) + c1
        predicted_gdppc2 = m2*np.asarray(t2) + c2

        # Visualization Code, don't change
        dot_size = 15
        fig6 = plt.figure(figsize=(19,10))
        ax6_1 = fig6.add_subplot(121)
        ax6_2 = fig6.add_subplot(122)
        ax6_1.scatter(energy_consumption_average_IN, gdppc_raw, c='k', s=dot_size,label='data')
        ax6_2.scatter(ratio_kids_survive_over_kids_fatality_IN, gdppc_raw, c='k', s=dot_size,label='data')
        ax6_1.plot(t1, predicted_gdppc1, c='r', label='model', linewidth=2.0)
        ax6_2.plot(t2, predicted_gdppc2, c='r', label='model', linewidth=2.0)
        ax6_1.set_xlabel('Energy Consumption Average')
        ax6_2.set_xlabel('Net Child Survivability at Birth')
        ax6_1.set_ylabel('GDP - per capita')
        ax6_2.set_ylabel('GDP - per capita')
        ax6_1.legend()
        ax6_2.legend()
        ax6_1.grid()
        ax6_2.grid()

        fig6_fn = 'Q3_Linear_Model_Fit_Plots.png'
        fig6.savefig(fig6_fn)

    ################################## Question Functions with build in plotting ################################# END



# Question functions, don't change for final submission
if __name__=='__main__':
    ca = data_analysis()
    energy_data_series = ca.question0()
    survival_rate_data_series = ca.question1()
    ca.question2()
    ca.question3(energy_consumption_average_IN=energy_data_series,ratio_kids_survive_over_kids_fatality_IN=survival_rate_data_series)
# plt.show()

