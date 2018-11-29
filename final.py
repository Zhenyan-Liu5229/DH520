from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt
import numpy as np

# the encoding score for job satisfaction
SCORE = {'Strongly Agree':2, 'Agree': 1, 'Undecided': 0,
          'Disagree':-1, 'Strongly Disagree': -2 }

class Alumni:
    
    # the dataset used in the study
    SURVEY_FILE = 'survey.csv'

    def __init__(self):
        self.degree = [] # a list of encoded degree category
        self.entry = []  # a list of encoded entry job category
        self.company = [] # a list of encoded match company scale
        self.position = [] # a list of encoded match job position
        self.satisfaction = [] # a list of calculated job satisfaction score
        self.salary = []   # a list of encoded salary range
        self.alumni = []  # the list of all the information from participants
        self.analysis = []



########## Initialization ################
    def initializing(self):
        self.load_csv_file()
        self.calculate_satisfaction()
        
        age_dict = {"17 – 21 years": 1, "22 – 30 years":2, "31 – 40 years":3}
        gender_dict = {'Prefer not to say':0, 'I am a man.':1, 'I am a woman.':2,
                       'I am non-binary / genderqueer / third gender.':0}
        
        self.age = self.encode(0, age_dict, 4)
        self.gender = self.encode(1, gender_dict, 0)
        
        self.degree_clean()
        self.entry_clean()
        self.salary_clean()
        self.company_match()
        self.position_match()
        self.age_satisfaction()
        self.gender_satisfaction()
        self.degree_satisfaction()
        self.entry_satisfaction()
        self.salary_satisfaction()
        self.company_match_satisfaction()
        self.position_match_satisfaction()



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
            


            
    
    def encode(self, index, enc_dict, default_val):
        ans = []
        for person in self.alumni:
            if person[index] in enc_dict:
                ans.append(enc_dict[person[index]])
            else:
                ans.append(default_val)
        return ans
    
    
    # data encoding for categorical data -degree
    def degree_clean(self):
        for person in self.alumni:
            if person[2][0].lower() == 'a': # Associate's
                person[2] = 1
            elif person[2][0].lower() == 'b': # Bachelor's
                person[2] = 2
            elif person[2][0].lower() == 'm': # Master's
                person[2] = 3
            elif person[2][0].lower() == 'p': # PhD
                person[2] = 4
            elif person[2][0].lower() == 'd': # Diploma
                person[2] = 0
            self.degree.append(person[2])


    # data encoding for categorical data -entry job 
    def entry_clean(self):
        for person in self.alumni:
            if person[3] == 'Yes':
                person[3] = 0
            elif person[3] == 'No':
                person[3] = 1
            self.entry.append(person[3])
    

    # data encoding for categorical data -salary range
    def salary_clean(self):
        for person in self.alumni:
            if person[-4] == 'Under 20000':
                person[-4] = 1
            elif person[-4] == '20000 to 40000':
                person[-4] = 2
            elif person[-4] == '40001 to 60000': 
                person[-4] = 3
            elif person[-4] == '60001 to 80000': 
                person[-4] = 4
            elif person[-4] == '80001 to 100000':
                person[-4] = 5
            elif person[-4] == '100001 to 120000':
                person[-4] = 6
            elif person[-4] == 'Over 120000':
                person[-4] = 7
            else:  # for people did not answer or answer 'prefer not to say'
                person[-4] = 0
            self.salary.append(person[-4])
    

    # data encoding for categorical data -match of company scale/position
    def company_match(self):
        for person in self.alumni:
            if person[4] == 'Other':
                person[4] = 0
            else:
                if person[4] == person[12]:
                    person[4] = 2
                else:
                    person[4] = 1
            self.company.append(person[4])
    

    def position_match(self):
        for person in self.alumni:
            if person[5] == 'Other':
                person[5] = 0
            else:
                if person[5] == person[13]:
                    person[5] = 2
                else:
                    person[5] = 1
            self.position.append(person[5])



########### Calculate average score for each encoded category ########
    # age - satisfaction
    def age_satisfaction(self):
        total_score = {}
        for person in self.alumni:
            if person[0] in total_score:
                total_score[person[0]] += person[-1]
            else:
                total_score[person[0]] = person[-1]

        number_of_people = {}
        for age in self.age:
            if age in number_of_people:
                number_of_people[age] += 1
            else:
                number_of_people[age] = 1
        
        age_satisfaction = {}
        for key in total_score:
            age_satisfaction[key] = format(float(total_score[key])/float(number_of_people[key]),'.2f')
        self.analysis.append(age_satisfaction)


    # gender - satisfaction
    def gender_satisfaction(self):
        total_score = {}
        for person in self.alumni:
            if person[1] in total_score:
                total_score[person[1]] += person[-1]
            else:
                total_score[person[1]] = person[-1]

        number_of_people = {}
        for gender in self.gender:
            if gender in number_of_people:
                number_of_people[gender] += 1
            else:
                number_of_people[gender] = 1
        
        gender_satisfaction = {}
        for key in total_score:
            gender_satisfaction[key] = format(float(total_score[key])/float(number_of_people[key]),'.2f')
        self.analysis.append(gender_satisfaction)


    # degree - satisfaction
    def degree_satisfaction(self):
        total_score = {}
        for person in self.alumni:
            if person[2] in total_score:
                total_score[person[2]] += person[-1]
            else:
                total_score[person[2]] = person[-1]

        number_of_people = {}
        for degree in self.degree:
            if degree in number_of_people:
                number_of_people[degree] += 1
            else:
                number_of_people[degree] = 1
        
        degree_satisfaction = {}
        for key in total_score:
            degree_satisfaction[key] = format(float(total_score[key])/float(number_of_people[key]),'.2f')
        self.analysis.append(degree_satisfaction)


    # job level - satisfaction
    def entry_satisfaction(self):
        total_score = {}
        for person in self.alumni:
            if person[3] in total_score:
                total_score[person[3]] += person[-1]
            else:
                total_score[person[3]] = person[-1]

        number_of_people = {}
        for entry in self.entry:
            if entry in number_of_people:
                number_of_people[entry] += 1
            else:
                number_of_people[entry] = 1
        
        entry_satisfaction = {}
        for key in total_score:
            entry_satisfaction[key] = format(float(total_score[key])/float(number_of_people[key]),'.2f')
        self.analysis.append(entry_satisfaction)


    # salary - satisfaction
    def salary_satisfaction(self):
        total_score = {}
        for person in self.alumni:
            if person[-4] in total_score:
                total_score[person[-4]] += person[-1]
            else:
                total_score[person[-4]] = person[-1]

        number_of_people = {}
        for salary in self.salary:
            if salary in number_of_people:
                number_of_people[salary] += 1
            else:
                number_of_people[salary] = 1
        
        salary_satisfaction = {}
        for key in total_score:
            salary_satisfaction[key] = format(float(total_score[key])/float(number_of_people[key]),'.2f')
        self.analysis.append(salary_satisfaction)


    # match of company_scale - satisfaction
    def company_match_satisfaction(self):
        total_score = {}
        for person in self.alumni:
            if person[4] in total_score:
                total_score[person[4]] += person[-1]
            else:
                total_score[person[4]] = person[-1]

        number_of_people = {}
        for match in self.company:
            if match in number_of_people:
                number_of_people[match] += 1
            else:
                number_of_people[match] = 1
        
        company_match_satisfaction = {}
        for key in total_score:
            company_match_satisfaction[key] = format(float(total_score[key])/float(number_of_people[key]),'.2f')
        self.analysis.append(company_match_satisfaction)
        
    
    # match of job position - satisfaction
    def position_match_satisfaction(self):
        total_score = {}
        for person in self.alumni:
            if person[5] in total_score:
                total_score[person[5]] += person[-1]
            else:
                total_score[person[5]] = person[-1]

        number_of_people = {}
        for match in self.position:
            if match in number_of_people:
                number_of_people[match] += 1
            else:
                number_of_people[match] = 1
        
        position_match_satisfaction = {}
        for key in total_score:
            position_match_satisfaction[key] = format(float(total_score[key])/float(number_of_people[key]),'.2f')
        self.analysis.append(position_match_satisfaction)


a = Alumni()
a.initializing() 


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
        plt.xticks([0, 1, 2], ['Other', 'Match', 'Mismatch'])

    else:
        plt.title('Figure 7: Match of Position and Satisfaction')
        plt.xlabel('Match of Job Position')
        plt.xticks([0, 1, 2], ['Other', 'Match', 'Mismatch'])

# ########### Visualization (Scatter plot & line of linear regression) ########
    # age - satisfaction

    plt.ylabel('Satisfaction Score')
    plt.ylim([0, 2.5])
    plt.yticks(np.arange(0, 2.5, 0.5))
    plt.scatter(factors, score, color='black')
    
    fit = np.polyfit(factors, score, 1)
    # fit_fn is now a function which takes in x and returns an estimate for y
    fit_fn = np.poly1d(fit) 
    plt.plot(factors, score, 'bo', factors, fit_fn(factors), '--k')

    plt.show()
