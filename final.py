from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt
import numpy as np

# dictionaries to encode data
SCORE = {'Strongly Agree':2, 'Agree': 1, 'Undecided': 0,
          'Disagree':-1, 'Strongly Disagree': -2 }

age_dict = {'17 – 21 years': 1, '22 – 30 years': 2, '31 – 40 years': 3, '41 – 50 years': 4}

gender_dict = {'I am a man.': 1, 'I am a woman.' :2}

entry_dict = {'Yes': 0, 'No': 1} # No > Yes as the question is "is this job an entry level job"

salary_dict = {'Under 20000': 1, '20000 to 40000':2, '40001 to 60000': 3,
              '60001 to 80000': 4, '80001 to 100000': 5, '100001 to 120000': 6,
              'Over 120000': 7}


class Alumni:

    SURVEY_FILE = 'survey.csv'

    def __init__(self):          
        self.degree = [] # a list of encoded degree category
        self.satisfaction = [] # a list of calculated job satisfaction score
        self.analysis = [] # the list of all the satisfaction score for each variable category


########## Processing List ################
    def processing(self): 
        # load the file     
        self.load_csv_file()
        # data encoding
        self.calculate_satisfaction()
        self.age = self.encode(0, age_dict) # a list of encoded age category
        self.gender = self.encode(1, gender_dict) # a list of encoded gender category
        self.degree_clean()
        self.entry = self.encode(3, entry_dict)  # a list of encoded entry job category
        self.salary = self.encode(-4, salary_dict)   # a list of encoded salary range
        self.company = self.match(4) # a list of encoded match company scale
        self.position = self.match(5) # a list of encoded match job position
        # calculate average satisfaction score for each variable category
        self.variable_satisfaction(0, self.age) 
        self.variable_satisfaction(1, self.gender)
        self.variable_satisfaction(2, self.degree)
        self.variable_satisfaction(3, self.entry)
        self.variable_satisfaction(-4, self.salary)
        self.variable_satisfaction(4, self.company)
        self.variable_satisfaction(5, self.position)



########### Data Loading & Data Encoding ########
    def load_csv_file(self, path = SURVEY_FILE):
        # open the dataset and get information for each participant
        with open(path) as file:
            file.readline() # the first line are questions
            self.alumni = [line.strip().split(',') for line in file] # the list of all the information from participants
    

    # calculate the satisfaction score for each person
    def calculate_satisfaction(self):
        for person in self.alumni:
            satisfaction = 0
            for element in person:
                if element in SCORE:
                    satisfaction += SCORE[element]
            # append the average score to the dataset
            person.append(satisfaction / 5)
            self.satisfaction.append(satisfaction / 5)


    # the method to encode age, gender, job level and salary
    def encode(self, index, enc_dict, default_val = 0):
        encoded = []
        for person in self.alumni:
            if person[index] in enc_dict:
                person[index] = enc_dict[person[index]]
            else:
                person[index] = default_val
            encoded.append(person[index])
        return encoded

    
    # data encoding for degree
    def degree_clean(self):
        """Double Encoding: Degree name -> Degree level -> encoded number 
        Eg: Bachelor's Degree in Arts -> Bachelor's -> 2"""
        for person in self.alumni:
            if person[2][0] == 'A': # Associate's
                person[2] = 1
            elif person[2][0] == 'B': # Bachelor's
                person[2] = 2
            elif person[2][0] == 'M': # Master's
                person[2] = 3
            elif person[2][0] == 'P': # PhD
                person[2] = 4
            elif person[2][0] == 'D': # Diploma, Certificate or other 2-year program
                person[2] = 0
            self.degree.append(person[2])


    # the method to encode the match of company scale and position
    def match(self, index):
        encoded = []
        for person in self.alumni:
            # check of this person does not provide answer to this question
            if person[index] == 'other': # 'other' was manually filled in the empty grids
                person[index] = 0
            else:
                if person[index] == person[index + 8]: # 8 because this is the distance in the dataset
                    person[index] = 2 # set match > mismatch as we expect match has higher score
                else:
                    person[index] = 1
            encoded.append(person[index])
        return encoded



########### Calculate average score for each encoded category ########
    def variable_satisfaction(self, index, variable):
        # calculate the total_score for each category
        total_score = {}
        for person in self.alumni:
            if person[index] in total_score:
                total_score[person[index]] += person[-1]
            else:
                total_score[person[index]] = person[-1]
        
        # calculate the total number of people within each category
        number_of_people = {}
        for category in variable:
            if category in number_of_people:
                number_of_people[category] += 1
            else:
                number_of_people[category] = 1
        
        # the average score of each category
        variable_satisfaction = {}
        for key in total_score:
            # restrict the average score into 2 decimals
            variable_satisfaction[key] = format(float(total_score[key])/float(number_of_people[key]),'.2f')
        self.analysis.append(variable_satisfaction)


data = Alumni()
data.processing() 


########### Calculate Pearson/Spear-man Correlation ########
for n, relations in enumerate(data.analysis):
    factors = [key for key in relations]
    score = [float(relations[key]) for key in relations]

    # print the Pearson/Spearman correlations retuls
    print('The Pearson\'s r is %s, p-value is %s.' 
           % (pearsonr(factors, score)[0], pearsonr(factors, score)[-1]))
    print('The Spearman coefficient is %s, p-value is %s.\n' 
           % (spearmanr(factors, score)[0], spearmanr(factors, score)[-1]))


# ########### Visualization (Scatter plot & line of linear regression) ########
    # set title, xlabel and xticks for each visualization
    if n == 0:
        plt.title('Figure 1: Age and Job Satisfaction')
        plt.xlabel('Age')
        # convert encoded numbers into original categories
        plt.xticks([1, 2, 3, 4], ['17 – 21 years','22 – 30 years','31 – 40 years','41 – 50 years'])

    elif n == 1:
        plt.title('Figure 2: Gender and Job Satisfaction')
        plt.xlabel('Gender')
        plt.xticks([0, 1, 2], ['Other','Male','Female'])

    elif n == 2:
        plt.title('Figure 3: Degree and Job Satisfaction')
        plt.xlabel('Degree')
        plt.xticks([0, 1, 2, 3, 4], ['Diploma','Associate','Bachelor', 'Master', 'PhD'])

    elif n == 3:
        plt.title('Figure 4: Job Level and Satisfaction')
        plt.xlabel('Job Level')
        plt.xticks([0, 1], ['Entry Level', 'Not Entry Level'])

    elif n == 4:
        plt.title('Figure 5: Annual Salary and Satisfaction')
        plt.xlabel('Salary')
        plt.xticks([0, 1, 2, 3, 4, 5, 6, 7], ['N/A', 'Under 20k','20k to 40k',
                                              '40k to 60k', '60k to 80k',
                                              '80k to 100k', '100k to 120k',
                                              'Over 120k'])
    elif n == 5:
        plt.title('Figure 6: Match of Company Scale and Satisfaction')
        plt.xlabel('Match of Company Scale')
        plt.xticks([0, 1, 2], ['Other', 'Mismatch', 'Match'])

    else:
        plt.title('Figure 7: Match of Position and Satisfaction')
        plt.xlabel('Match of Job Position')
        plt.xticks([0, 1, 2], ['Other', 'Mismatch', 'Match'])

    # annotate each plot with the score
    for i, y in enumerate(score):
        plt.annotate(y, (factors[i], score[i]))
    
    plt.ylabel('Satisfaction Score')
    # limit the y axis as the score range in (0, 2); 2.5 because I want 2 to appear in the graph
    plt.ylim([0, 2.5])
    plt.yticks(np.arange(0, 2.5, 0.5))
    plt.scatter(factors, score, color='black')
    
    # show the regression line; code from web
    fit = np.polyfit(factors, score, 1)
    # fit_fn is now a function which takes in x and returns an estimate for y
    fit_fn = np.poly1d(fit) 
    plt.plot(factors, score, 'yo', factors, fit_fn(factors), '--k')

    plt.show()
