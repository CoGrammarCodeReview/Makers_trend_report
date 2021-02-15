# Makers trend report generator. Set the date and manually filter students flagged for attention.
import csv
from datetime import datetime
import pandas as pd
import numpy as np

start_date = datetime.strptime("01/02/2021", "%d/%m/%Y")
end_date = datetime.strptime("15/02/2021", "%d/%m/%Y") #excl end date
 
data = pd.read_csv("trends.csv")
data = data.drop(["# workdays since review","Screen Recording URL", "Screen recording", "General feedback",
       "I use an Agile product development process – notes", "I can model anything – notes", "I can TDD anything – notes",
       "I can program fluently – notes", "I can refactor anything – notes","I can debug anything – notes","I write code that is easy to change – notes",
       "I have a methodical problem-solving process – notes","I can justify the way I work – notes","I use an Agile product development process",
       "I can model anything", "I can TDD anything", "I can program fluently","I can debug anything", "I can refactor anything",
       "I have a methodical approach to solving problems","I write code that is easy to change", "I can justify the way I work","Created at"], axis=1)

data = data.rename(columns={"Trends - TDD process": "TDD_trends", "Trends - Requirements-gathering process": "Requirements_trends",
"Trends - General aspects about the review": "General_trends","Trends - Debugging process": "Debugging_trends","Trends - New trend or surprising behaviour":"New_trends"})

#error entries - manually check
errors = data[data["Date"].isnull()] 
data = data[~data["Date"].isnull()] 

print(errors)

#filter to specified date range
data["Date"] = pd.to_datetime(data["Date"],dayfirst=True)
mask = (data["Date"] >= start_date) & (data["Date"] < end_date)
data_inrange = data.loc[mask]

f= open("trends_report.txt","w+")

months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
#DATE
f.write("Trend report for period: {} {} - {} {} {}\n\n".format(start_date.day,months[start_date.month-1],months[end_date.month-1],end_date.day-1,end_date.year))

#NUMBER OF REVIEWS
review_num = len(data_inrange.index)
f.write("Total reviews during this period: {}\n\n".format(review_num))

#COUNT TREND FREQUENCY
f.write("Trends frequency:\n\n")

def count_trend_frequency(data):
    tdd_trends_dict = {"Complex test progression":0,"Structure first approach":0,"Issues with Red-Green-Refactor cycle":0,
    "Not developing code iteratively":0,"Solution remains hard-coded":0,"Removed/modified tests":0}

    general_trends_dict = {"No-show":0,"No UUID provided":0,"UUID error":0,"Little to no improvement between consecutive sessions":0,
    "Little to no vocalisations or justifications for decisions":0,"No git or improper use of git":0,"Notable improvement between sessions":0}

    debugging_trends_dict = {"Not reading error messages":0, "Trying random fixes when debugging":0}

    requirements_trends_dict = {"Didn’t ask about edge cases":0, "Jumped too quickly into coding":0}

    trends_dict = {"TDD_trends":tdd_trends_dict,"General_trends":general_trends_dict,"Debugging_trends":debugging_trends_dict,"Requirements_trends":requirements_trends_dict}
                   
    for col in  data.columns:   
        if "_trends" in col and col != "New_trends":              
            trends_df = data_inrange[col].dropna()
            trends_df= trends_df.str.split(",") 
            flat_list = [item for sublist in trends_df for item in sublist]
            for trend in flat_list:            
                trends_dict[col][trend] += 1
                   
   
    f.write("TDD process:"+"\n")
    for trend in tdd_trends_dict:
        f.write("{}: {}\n".format(trend,tdd_trends_dict[trend]))
    f.write("\nGeneral:"+"\n")
    for trend in general_trends_dict:        
        f.write("{}: {}\n".format(trend,general_trends_dict[trend]))
    f.write("\nRequirements gathering process:"+"\n")
    for trend in requirements_trends_dict:
        f.write("{}: {}\n".format(trend,requirements_trends_dict[trend]))
    f.write("\nDebugging process:"+"\n")
    for trend in debugging_trends_dict:
        f.write("{}: {}\n".format(trend,debugging_trends_dict[trend]))

    f.write("\nOther:"+"\n")
    new_trends = data_inrange['New_trends'].dropna()   
    new_trends_notes = data_inrange['Trends - Notes'].dropna()
    for trend in new_trends:
        f.write("{} \n".format(trend))
    for note in new_trends_notes:
        f.write("{} \n".format(note))

count_trend_frequency(data_inrange)

#FLAG STUDENTS FOR ATTENTION
f.write("\n\nStudents flagged for attention: \n(If more than 4 negative trends and no subsequent review) \n\n")


def flag_students_for_attention(data_inrange):
    data = data_inrange.drop(['ID', 'Identifier if UUID not given', 'Date','Reviewer','Exercise'],axis=1)  
    flagged = []
    
    for index, row in data.iterrows():           
        student = row["Review"]       
        notes = row['Trends - Notes']               
        
        row = row.drop(["Review","Trends - Notes"])
        student_row = row.dropna().values           
        student_trends = [category.split(",") for category in student_row]   
        student_trends = [trend for trendlist in student_trends for trend in trendlist]
   
        pos_trend = student_trends.count("Notable improvement between sessions")
        if(len(student_trends) - pos_trend  >= 4): 
                          
            flagged.append(student) 
            print(student,student_trends)
                
    for student in flagged:
         f.write("{}\n".format(student))

print("NB: Manually check students for improvement")
flag_students_for_attention(data_inrange)

f.close()
