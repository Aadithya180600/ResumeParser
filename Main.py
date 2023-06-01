from ResumeParser import ResumeParser
from CalAppProbability import CalAppProbability
from Conversions import Conversions

# Calling Pdf to Text Conversion
conversions = Conversions()
conversions.pdftotextconversion('Resume.pdf')

# calling ResumeParser Methods
resumeParser = ResumeParser()
resumeParser.ExtractName()
resumeParser.ExtractPhoneNum()
resumeParser.ExtractingEmailId()
resumeParser.ExtractingURLs()
resumeParser.ExtractingSkills()
resumeParser.ExtractEducation()
resumeParser.ExtractingExperience()
resumeParser.PrintingExtractedData()

print()
print("*********************** SCREENING PROCESS ************************")
print()
# Calling Eligibility checking methods
calAppProbability = CalAppProbability()
calAppProbability.CalEligibilityProbability([])
calAppProbability.PrintingEligibilityProbability()
calAppProbability.counterfactual()