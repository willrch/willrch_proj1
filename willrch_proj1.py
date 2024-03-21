# Your name: William Richardson
# Your student id: 13075961
# Your email: willrch@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT): Owen Woertink, Emma Vitet
# If you worked with generative AI also add a statement for how you used it.  
# Used Chatgpt to help with debugging 
import csv
import unittest


def csv_loader(filename):
   
    with open(f'{filename}', 'r', newline = '', encoding = 'utf-8-sig') as csvfile:


        csv_reader = csv.reader(csvfile, delimiter = ',')

        columns_names = []
        for row in csv_reader:
            columns_names.append(row[1:])
            break
        header = columns_names[0]

        data_lst = []
        for row in csv_reader:
            data_lst.append(row)

        final_dict = {}
        for i in range(len(data_lst)):
            final_dict[data_lst[i][0]] = {header [0]:data_lst[i][1], header[1]:data_lst[i][2], header[2]:data_lst[i][3]}
        return final_dict


def layoff_risk_level_group(employees, dict_risk_framework):

    risk_dict = {}
    for key1, value1 in dict_risk_framework.items():
        for key2, value2 in employees.items():
            if float(value2['hire_year']) >= value1[0] and float(value2['hire_year']) <= value1[1]:
                if key1 not in risk_dict:
                    risk_dict[key1] = {key2: value2}
                else:
                    risk_dict[key1][key2] = value2
    return risk_dict


def race_or_gender_counter(employees):
    return_dict = {'race' : {}, 'gender' : {}}
    for i in employees:
        race = employees[i]['race']
        gender = employees[i]['gender']
        if race not in return_dict['race']:
            return_dict['race'][race] = 1
        else:
            return_dict['race'][race] += 1
        if gender not in return_dict['gender']:
            return_dict['gender'][gender] = 1
        else:
            return_dict['gender'][gender] += 1
    # print(return_dict)
    return return_dict




def race_and_gender_counter(employees):
    race_gender_dict = {}
    for key, value in employees.items():
        race = value['race']
        gender = value['gender']
        together = f"{race}&{gender}"
        if together in race_gender_dict:
            race_gender_dict[together] += 1
        else:
            race_gender_dict[together] = 1
    return race_gender_dict
    




def csv_writer(data, filename):
   with open(f'{filename}', 'r', newline = '', encoding = 'utf-8-sig') as new_file:
       writer = csv.writer(new_file)

       writer.writerow(['race_and_gender', 'num_employees']) 

       for key, value in data.items():
           writer.writerow(key, value)

#EXTRA CREDIT
def count_employees_by_years_worked(employees):

    final_dict = {}
    year_range = 1976 - 1950
    for i in range(year_range):
        final_dict[year_range - i] = {'White' : {'Male' : 0, 'Female' : 0}, 
                                      'Black' : {'Male' : 0, 'Female' : 0}, 
                                      'Other' : {'Male' : 0, 'Female' : 0}}




class TestEmployeeDataAnalysis(unittest.TestCase):

    def setUp(self):
        
        self.small_file = 'smaller_dataset.csv'
        self.csv_loader = csv_loader(self.small_file)


    def test_csv_loader(self):

        # Your test code for csv_loader goes here
        csv_loader_test = csv_loader(self.small_file)

        # Write a test case that checks for the length of the outer dictionary.
        self.assertEqual(len(csv_loader_test), 10)
        
        # Write a test case that checks for the length of the inner dictionary value of the first (key, value) pair.

        for key, value in csv_loader_test.items():
            self.assertEqual(len(csv_loader_test[key]), 3)
            break



    def test_layoff_risk_level_group(self):
        # Set up the dictionary for the layoff risk level
        layoff_risk_dict = {'Very High': (1970, 1976), 'High': (1964, 1969), 'Medium': (1958, 1963), 'Low': (1954, 1957), 'Very Low': (1950, 1953)}

        # Your test code for layoff_risk_level_group goes here
        sorted_dictionary = layoff_risk_level_group(self.csv_loader, layoff_risk_dict)

        #Test that the function correctly puts employees into different layoff risk level groups based on their hire year.

        self.assertEqual(len(sorted_dictionary['Very Low']), 3)
        self.assertEqual(len(sorted_dictionary['Low']), 3)
        self.assertEqual(len(sorted_dictionary['Very High']), 2)
        self.assertEqual(len(sorted_dictionary['High']),2)
        pass


    def test_race_or_gender_counter(self):

        # Your test code for race_or_gender_counter goes here
        race_or_gender_test = race_or_gender_counter(self.csv_loader)
        
        #Test that there are only two keys in the returned dictionary
        self.assertEqual(len(race_or_gender_test.keys()), 2)


        
        #Test that the function accurately counts the number of employees belonging to each race and gender category.
        self.assertEqual(race_or_gender_test['race'], {'White': 4, 'Black': 4, 'Other': 2})
        self.assertEqual(race_or_gender_test['gender'], {'Male': 5, 'Female': 5})
        pass



    def test_race_and_gender_counter(self):

        # Your test code for race_and_gender_counter goes here
        race_and_gender_test = race_and_gender_counter(self.csv_loader)

        #Test that there are the correct number of keys in the dictionary representing each combination of race and gender in this dataset.
        self.assertEqual(len(race_and_gender_test.keys()), 6)
        
        # Test that the function correctly counts the number of employees within each combination of race and gender.
        self.assertEqual(list(race_and_gender_test.values()), ([2,2,2,2,1,1]))
        pass






#You do not need to change anything in the main() function

def main():

    # Load employee data from the CSV file

    employee_data = csv_loader('GM_employee_data.csv')
    
    # Task 1: Put employees into different layoff risk level groups based on their hire year
    layoff_risk_level = {'Very High': (1970, 1976), 'High': (1964, 1969), 'Medium': (1958, 1963), 'Low': (1954, 1957), 'Very Low': (1950, 1953)}
    dict_layoff_risk_level = layoff_risk_level_group(employee_data, layoff_risk_level)
    


    # Task 2: Count employees by race or gender for all employees and for employees whose layoff risk level is "Medium", "Low" or "Very Low"
    employees_not_high_risk = {**dict_layoff_risk_level["Medium"], **dict_layoff_risk_level["Low"], **dict_layoff_risk_level["Very Low"]} 
    race_gender_counts_total = race_or_gender_counter(employee_data)

    
    race_gender_counts_not_high_risk = race_or_gender_counter(employees_not_high_risk)



    # Task 3: Count employees by race and gender combinations for all employees and for employees whose layoff risk level is "Medium", "Low" or "Very Low"

    gendered_race_counts_total = race_and_gender_counter(employee_data)

    gendered_race_counts_not_high_risk = race_and_gender_counter(employees_not_high_risk)



    # Print and interpret the results

    print("Analysis Results:")

    print("--------------------------------------------------------")



    # Task 1: Putting employees into different layoff risk level groups based on their hire year

    print("Task 1: Group Employees by Hire Year")

    print(f"Number of employees hired total: {len(employee_data)}")

    print(f"Number of employees with medium, low or very low risk: {len(employees_not_high_risk)}")

    print("--------------------------------------------------------")



    # Task 2: Comparing race or gender of all employees and employees with medium, low or very low risk

    print("Task 2: Comparing Race and Gender of All Employees and Employees with Medium, Low or Very Low Risk")

    print("Category: All Employees ---> Employees with Medium, Low or Very Low Risk")

    print("Race:")

    for category, count_all in race_gender_counts_total['race'].items():

        count_not_high_risk = race_gender_counts_not_high_risk['race'].get(category, 0)

        print(f"\t{category}: {count_all} ---> {count_not_high_risk}")



    print("Gender:")

    for category, count_all in race_gender_counts_total['gender'].items():

        count_not_high_risk = race_gender_counts_not_high_risk['gender'].get(category, 0)

        print(f"\t{category}: {count_all} ---> {count_not_high_risk}")



    print("--------------------------------------------------------")



    # Task 3: Comparing race and gender combinations for all employees and employees with medium, low or very low risk

    print("Task 3: Comparing Gendered Race Combinations for All Employees and Employees with Medium, Low or Very Low Risk")

    print("Category: All Employees ---> Employees with Medium, Low or Very Low Risk")

    print("Gendered races:")

    for category, count_all in gendered_race_counts_total.items():

        count_not_high_risk = gendered_race_counts_not_high_risk.get(category, 0)

        print(f"\t{category}: {count_all} ---> {count_not_high_risk}")



    print("--------------------------------------------------------")



    csv_writer(gendered_race_counts_total, "GM_employee_data_all_before_layoffs.csv")

    csv_writer(gendered_race_counts_not_high_risk, "GM_employee_data_not_high_risk.csv")






if __name__ == "__main__":
    
    # Comment this main() if you want clear view of tests
    main()
   
    unittest.main(verbosity=2)

    main()



