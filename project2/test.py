import functools as ft

class data_analysis:

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
        step1 = list(map(
            lambda series: list(map(
                lambda num, avg: (num - avg) ** 2,
                series,
                average_series
            )),
            list_of_series
        ))

        # Step 2
        std_list = list(map(
            lambda x: 0,
            average_series
        ))

        std_list2 = ft.reduce(
            lambda acc, lst: list(map(
                lambda x, y: x + y,
                acc, lst
            )),
            step1,
            std_list
        )

        # Steps 3 and 4
        for i in range(len(std_list)):
            std_list[i] /= len(list_of_series)
            std_list[i] = std_list[i] ** (1.0/2.0)

        return std_list


dataAnalysis = data_analysis()

print(dataAnalysis.compute_standard_deviation_across_series([[0,10,20],[10,20,30]] , [5.0, 15.0, 25.0]))
