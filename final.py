from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt
import numpy as np

# dictionaries to encode data
SCORE = {'Strongly Agree':2, 'Agree': 1, 'Undecided': 0,
          'Disagree':-1, 'Strongly Disagree': -2 }

age_dict = {'17 – 21 years': 1, '22 – 30 years': 2, '31 – 40 years': 3, '41 – 50 years': 4}

gender_dict = {'Prefer not to say':0, 'I am a man.': 1, 'I am a woman.' :2,
              'I am non-binary / genderqueer / third gender.': 0}

entry_dict = {'Yes': 0, 'No': 1}

salary_dict = {'Under 20000': 1, '20000 to 40000':2, '40001 to 60000': 3,
              '60001 to 80000': 4, '80001 to 100000': 5, '100001 to 120000': 6,
              'Over 120000': 7}


class Alumni:
    # the dataset used in the study
    SURVEY_FILE = 'survey.csv'

    def __init__(self):          
        self.degree = [] # a list of encoded degree category
        self.satisfaction = [] # a list of calculated job satisfaction score
        self.alumni = []  # the list of all the information from participants
        self.analysis = [] # the list of all the satisfaction score for each variable category


########## Processing List ################
    def processing(self):       
        self.load_csv_file()
        self.calculate_satisfaction()
        self.age = self.encode(0, age_dict) # a list of encoded age category
        self.gender = self.encode(1, gender_dict) # a list of encoded gender category
        self.degree_clean()
        self.entry = self.encode(3, entry_dict)  # a list of encoded entry job category
        self.salary = self.encode(-4, salary_dict)   # a list of encoded salary range
        self.company = self.match(4) # a list of encoded match company scale
        self.position = self.match(5) # a list of encoded match job position
        self.variable_satisfaction(0, self.age)
        self.variable_satisfaction(1, self.gender)
        self.variable_satisfaction(2, self.degree)
        self.variable_satisfaction(3, self.entry)
        self.variable_satisfaction(-4, self.salary)
        self.variable_satisfaction(4, self.company)
        self.variable_satisfaction(5, self.position)



########### Data Loading & Data Encoding ########
    def load_csv_file(self, path = SURVEY_FILE):
        # open the dataset and get information for each person
        with open(path) as file:
            file.readline()
            for line in file:
                line = line.strip().split(',')
                self.alumni.append(line)
    

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

    
    # data encoding for categorical data -degree
    def degree_clean(self):
        for person in self.alumni:
            if person[2][0] == 'A': # Associate's
                person[2] = 1
            elif person[2][0] == 'B': # Bachelor's
                person[2] = 2
            elif person[2][0] == 'M': # Master's
                person[2] = 3
            elif person[2][0] == 'P': # PhD
                person[2] = 4
            elif person[2][0] == 'D': # Diploma
                person[2] = 0
            self.degree.append(person[2])


    # the method to encode the match of company scale and position
    def match(self, index):
        encoded = []
        for person in self.alumni:
            if person[index] == 'other':
                person[index] = 0
            else:
                if person[index] == person[index + 8]:
                    person[index] = 2
                else:
                    person[index] = 1
            encoded.append(person[index])
        return encoded



########### Calculate average score for each encoded category ########
    def variable_satisfaction(self, index, variable):
        total_score = {}
        for person in self.alumni:
            if person[index] in total_score:
                total_score[person[index]] += person[-1]
            else:
                total_score[person[index]] = person[-1]

        number_of_people = {}
        for category in variable:
            if category in number_of_people:
                number_of_people[category] += 1
            else:
                number_of_people[category] = 1
        
        variable_satisfaction = {}
        for key in total_score:
            variable_satisfaction[key] = format(float(total_score[key])/float(number_of_people[key]),'.2f')
        self.analysis.append(variable_satisfaction)


a = Alumni()
a.processing() 


########### Calculate Pearson/Spear-man Correlation ########
for n, relations in enumerate(a.analysis):
    factors = []
    score = []
    for key, value in relations.items():
        factors.append(key)
        score.append(float(value))
    print(pearsonr(factors, score))
    print(spearmanr(factors, score))

    if n == 0:
        plt.title('Figure 1: Age and Job Satisfaction')
        plt.xlabel('Age')
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

# ########### Visualization (Scatter plot & line of linear regression) ########
    for i, y in enumerate(score):
        plt.annotate(y, (factors[i], score[i]))
    

    plt.ylabel('Satisfaction Score')
    plt.ylim([0, 2.5])
    plt.yticks(np.arange(0, 2.5, 0.5))
    plt.scatter(factors, score, color='black')
    
    fit = np.polyfit(factors, score, 1)
    # fit_fn is now a function which takes in x and returns an estimate for y
    fit_fn = np.poly1d(fit) 
    plt.plot(factors, score, 'yo', factors, fit_fn(factors), '--k')

    plt.show()
