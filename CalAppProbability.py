from ResumeParser import ResumeParser
from GeneticAlgo import GeneticAlgo

rank_list = {'sql': 3, 'java': 1, 'c#': 6, 'python': 2, 'cpp': 6,
             'spring': 4, 'django': 5, 'flask': 5, 'react': 7, 'angular': 8, 'azure': 9, 'aws': 9, 'html': 11,
             'javascript': 10, 'php': 6, '.net': 4
             }

time_list = {'sql': 30, 'java': 75, 'c#': 30, 'python': 60, 'cpp': 40,
             'spring': 25, 'django': 25, 'flask': 35, 'react': 75, 'angular': 65, 'azure': 80, 'aws': 80, 'html': 10,
             'javascript': 25, 'php': 25, '.net': 25
             }

course_list = {'sql': 'https://www.coursera.org/learn/intro-sql',
               'java': 'https://www.coursera.org/learn/java-introduction',
               'pyhton': 'https://www.coursera.org/specializations/python',
               'c': 'https://www.coursera.org/specializations/coding-for-everyone',
               'c#': 'https://www.coursera.org/learn/introduction-programming-unity',
               '.net': 'https://www.udemy.com/course/parallel-dotnet/'}


class CalAppProbability:

    # Initialization
    def __init__(self) -> None:
        # Declaring Eligibility Probability and initializing to 0
        self.eligibility_probability = 0
        self.threshold = 0.75  # Declared manually for testing
        self.eligible = "This resume did meet the requirements of the job. The applicant is eligible for the role"
        self.noteligible = "This resume did not meet the requirements of the job. The applicant is not eligible for the role"
        self.matchedskills = []
        self.required_skills = []
        self.counterfactual_list = []
        self.resumeParser = ResumeParser()
        self.resumeParser.ExtractingSkills()
        self.resumeSkills = self.resumeParser.skills

    # Method for Constructing Eligibility Probability
    def CalEligibilityProbability(self, applicantSkills):

        if (len(applicantSkills) == 0):
            applicantSkills = self.resumeSkills
        jd_f = open('jd.txt', 'r')
        job_description = jd_f.read()

        required_skills = self.resumeParser.ComparingTextwithSkills(
            job_description)
        self.required_skills = required_skills
        count_skills = 0
        for i in applicantSkills:
            if i in required_skills:
                self.matchedskills.append(i)
                count_skills += 1

        self.eligibility_probability = count_skills/len(required_skills)

    # Method to say is eligible or not
    def isEligible(self):
        if self.threshold <= self.eligibility_probability:
            return self.eligible
        return self.noteligible

    # Method for Printing Data

    def PrintingEligibilityProbability(self):

        # Printing eligibility Probability
        print("\n\nEligibility Probability: " +
              str(self.eligibility_probability))
        print()

        # printing Is Eligible or not
        print(self.isEligible())

    def counterfactual(self):
        neededSkills = []
        for i in self.required_skills:
            if i not in self.matchedskills:
                neededSkills.append(i)

        s = ", ".join(neededSkills)
        counterfactual_list = []
        counterfactual_list = self.generateCounterfactual(neededSkills)
        print("\n\nTry to develop skills like " + str(counterfactual_list) +
              ".\nThis will improve chances of your resume getting screened.")
        for i in counterfactual_list:
            print(f"You can learn {i} from here: " +
                  str(course_list[i.lower()]))

    def generateCounterfactual(self, neededSkills) -> list:

        skills = []
        for i in neededSkills:
            skills.append((i, rank_list[i.lower()], time_list[i.lower()]))
        geneticAlgo = GeneticAlgo(
            skills, self.resumeSkills, self.required_skills)
        return geneticAlgo.geneticAlgo()
