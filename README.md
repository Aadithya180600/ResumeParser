# ResumeParser
Parsing a resume, predicting whether it will get screened for a given job description or not and generating counterfactual suggestions.


This application will do the following things
1. Parse the resume, extract all the details from the resume
2. Predict whether a resume can get screened for a given job description
3. If it prrdicted No then develop counterfactual suggestions to make the resume getting screened.

## Tech used:
NER technique of NLP for extracting data.
Created a model which can predict the probability of getting screened based on skill set.
Generating counterfactuals suggestion on which skills need to be updated/developed to get the resume screened for the given job description
Counterfactuals are generated using the genetic algorthm

## How to run:
Download or clone the files to your space.
Keep all the files in same folder.
Make sure all the packages that needed are downloaded -  NLTK, Spacy, PyPDF2, docx2txt.
For resume, Keep the resume that need to be parsed in the same folder with name ```resume.pdf``` or give the appropraite path and extension in the Main.py file.
Update the ```jd.txt``` file with the required job description for which the resume is used to apply.
run the ```Main.py``` file. 
Results will be displayed on the console.

## Detailed Explanation of All things:
A Resume can be in any format and written in any style. Our resume parser will accept some of the basic formats of the resume everyone uses, like "pdf," "docx," "doc," "odt," "rtf," Etc., and convert it into text format. The text-formatted data will be processed using Natural Language Processing techniques, and tags will be assigned accordingly. The tagged data will be used to autofill an application.

The main things we need to extract from a resume to fill an application are name, education details, experience details, phone number, email address, URLs like LinkedIn and GitHub, and technical skills of the applicant. We used simple rule-based implementation to approach the solution. The following will explain the approach used for every field. 

### Extracting Name: 

To extract the name of the applicant, we tried two different approaches; one was to use the “PER” tagged words from spacy NER, and the other was a direct approach where we started with the assumption that the first line of the resume will always be the name of the applicant. 

### Extracting Phone Number: 

To extract the phone number, we used the regular expression that matches a phone number and searched the text for a match. The founded match was considered as the applicant’s phone number. 

### Extracting Email Address: 

To extract the email address, we used a similar approach to extracting the phone number. We wrote a regular expression that matched the email addresses and searched all the text for the match. The match was extracted and tagged as an email address. 

### Extracting URLs: 

Here also used regular expressions to match URL formats and extracted all the URLs as a list. After extracting them, we tried to match the most common URLs, like LinkedIn and GitHub, and separately tagged them. The rest are classified as other URLs. 

### Extracting Skills: 

There are numerous different skills one can find in a resume. We particularly tried to parse software-related resumes with skills related to the software side. The extraction of skills cannot be done using simple regular expressions. So, to extract the skills, we initially constructed the list of skills or skills database with different skills commonly found in a resume. We hardcoded this list and saved it. Now, using NLTK, we tokenized all the words of the resume and tried to match those words with the skills list. The matched terms are separately stored in a list. Then using the NLTK bigrams and trigrams method, we created bigrams and trigrams of the previously tokenized text. These newly formed bigrams and trigrams are also searched against the skills database and matched skills appended to applicants' skills list. Finally, we applied a set to remove all the duplicate skills, sorted the skills in alphabetical order, and returned them. 

### Extracting Education and Experience: 

These were the trickiest part. We thought of different approaches, but no approach gave good accuracy. So, we finally settled on the following approach, which performed relatively better. We initially constructed a list of fields we can find in the resume. We approached this solution assuming that the field heading would be the first or second words of the line. For education, we searched every line’s starting word to see if there was any match with “education.” For Experience, we again created a small list of words that an applicant typically used to mark the Experience field in a resume. We mapped these words with the starting words of every line, and the matched line is considered the starting line of Experience Details. The end of the fields was also determined using a similar way where we searched for another field match. If there is another field match, we consider the current field ended. We stored all the data of the current field separately and returned it. 

### Calculating Eligibility Probability: 

Every job application has specific requirements that need to be met by an applicant. We tried to decide whether the applicant was eligible for a particular job role by parsing an applicant's resume. For this, we depended on the required skills for a job and the applicant's skills. We extracted the skills mentioned in the job description using the same technique we used for extracting an applicant's skills. Then, we compared both lists to find that the number of skills of the applicant matched the skills of the job description. This count was then divided by the total number of skills required for the job to get the Probability. The idea is to determine a threshold value so that the applicant will be considered eligible for the job if the Probability is above the threshold; else, he is not eligible.

To generate the counterfactuals, we first need a good feature or features to generate the suggestions. We cannot use features like experience because we cannot suggest getting a year or two of experience to get the resume screened. That would be unnatural and irrational to suggest. Hence, we focused on an important feature which is skill set. We can suggest which skill can be developed so the resume can get screened. 

### How to suggest which skill to learn? 

The naïve approach is to get the unmatched job description skills in the resume and suggest them directly to the applicants. But if we do it that way, there may be unnecessary suggestions, and sometimes the model will suggest so many skills that it will take longer to develop. A suggestion like that will be irrational. Hence, our model needs to be smart enough to generate a skill set that will be better to suggest. 

To suggest better skills, we need to consider different things. The skills we suggest should be: 

Easy to learn in less time. 

Time it will take to complete the course should be less. 

Important skills which will get the resume screened. 

Suggest a smaller number of skills so that applicants can learn everything before it’s too late. 

 

As we formed the rules of which skills should be suggested, the next thing to focus on is how we will know which will fill our requirements. Two better weights to assign are ranking a skill based on its demand and ranking it based on the time it will take to learn it. 

 

### Ranking skills based on demand 

We used online job search websites and applications to rank the skills based on demand and got the data from different sources like LinkedIn, indeed.com, and others. We searched for which skill had the highest demand and ranked the skills accordingly. 

### Ranking skills based on the time it takes to develop them 

We assigned rankings to skills based on the time needed to develop a specific skill. We used skill development platforms and websites like Coursera, LinkedIn, Udemy, and other related websites. We searched for the fundamental courses on every skill and used the time it would take to learn that course. 

Based on the weights assigned, we need to suggest a skill set with a better ranking and less time to develop those skills. One way to solve this is to consider it a 0-1 knapsack problem, and we can solve it to get a good set of skills. We intend to solve this using a genetic algorithm instead of greedy or other approaches for better results. 

### Generating Counterfactuals: 

If a particular resume got a pessimistic prediction of getting screened, then we will suggest counterfactual examples to make it get screened. To generate counterfactuals, we focused mainly on the skills. We assigned ranks and time taken to learn a course. Rankings and weights are assigned to the skills in the skill database. Skills that are unmatched from the skills in the resume to skills needed by the job description are separated and given as input to a genetic algorithm to calculate the best skill set. 

### Fitness function of Genetic algorithm: 

The fitness function will take a set of skills, add those to the already existing skill set of the applicant and calculate the probability of getting the resume screened with this new skill set. It will also calculate the time needed to develop those skills. If the skill set gets screened, the total time will be returned so that we can select the skills with the least time to develop. 

 

After generating the counterfactuals, we suggest links to different course vendors to develop this skill. One can generate revenue by displaying a course of specific sponsored vendors. 
