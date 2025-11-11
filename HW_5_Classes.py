from datetime import date  # Import date class for current date
from datetime import datetime  # Import datetime class for date parsing
from datetime import timedelta  # Import timedelta for date calculations
import re  # Import regular expressions for text splitting

class News:
    def __init__(self, text, city):
        self.type = "News"  # Set type as News
        self.text = text  # Store news text
        self.city = city  # Store city name
        self.publish_date = date.today()  # Get today's date

    def add_text(self):
        formatted_city = self.city.capitalize().strip()  # Capitalize and clean city name

        sentences = re.split(r'([.!?])', self.text)  # Split text into sentences
        result = []
        for s in range(0, len(sentences) -1 , 2):  # Loop through sentences
            sentence = sentences[s].strip().capitalize() + sentences[s+1]  # Capitalize first letter and add punctuation
            result.append(sentence)  # Add formatted sentence to result

        formetted_text = '\n'.join(result)  # Join sentences with new lines

        f_title = f"Title: {self.type}"  # Prepare title line
        f_publish_date = f"Publish date: {self.publish_date}"  # Prepare date line
        f_city = f"City: {formatted_city}"  # Prepare city line
        f_text = f"Text: {formetted_text}"  # Prepare text line

        news = []  # Create empty list for news lines

        news.extend([f_title, f_publish_date, f_city, f_text])  # Add all lines to list

        final_news = '\n'.join(news)  # Join all lines into one string

        with open('feed.txt', 'a', encoding='utf-8') as file:  # Open file for appending
            file.write(final_news)  # Write news to file
            file.write("\n\n")  # Add empty line after news


class Private_ad:
    def __init__(self, text, expiration_date):
        self.type = "Private ad"  # Set type as Private ad
        self.text = text  # Store ad text
        self.expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d").date()  # Parse expiration date
        self.days_left = (self.expiration_date - date.today()).days  # Calculate days left

    def add_text(self):
        sentences = re.split(r'([.!?])', self.text)  # Split text into sentences
        result = []
        for s in range(0, len(sentences) - 1, 2):  # Loop through sentences
            sentence = sentences[s].strip().capitalize() + sentences[s + 1]  # Capitalize and add punctuation
            result.append(sentence)  # Add to result

        formetted_text = '\n'.join(result)  # Join sentences with new lines

        f_title = f"Title: {self.type}"  # Prepare title line
        f_days_left = f"Days left: {self.days_left}"  # Prepare days left line
        f_text = f"Text: {formetted_text}"  # Prepare text line

        news = []  # Create empty list

        news.extend([f_title, f_days_left, f_text])  # Add all lines

        final_news = '\n'.join(news)  # Join all lines

        with open('feed.txt', 'a', encoding='utf-8') as file:  # Open file for appending
            file.write(final_news)  # Write ad to file
            file.write("\n\n")  # Add empty line after ad


class Job_ad:
    def __init__(self, job_title, text, salary, initial_valid_days):
        self.type = "Job ad"  # Set type as Job ad
        self.job_title = job_title  # Store job title
        self.text = text  # Store job description
        self.salary = salary  # Store salary
        self.expiration_date = date.today() + timedelta(days=int(initial_valid_days))  # Calculate expiration date
        self.days_left = (self.expiration_date - date.today()).days  # Calculate days left

    def add_text(self):
        sentences = re.split(r'([.!?])', self.text)  # Split text into sentences
        result = []
        for s in range(0, len(sentences) - 1, 2):  # Loop through sentences
            sentence = sentences[s].strip().capitalize() + sentences[s + 1]  # Capitalize and add punctuation
            result.append(sentence)  # Add to result

        formetted_text = '\n'.join(result)  # Join sentences with new lines

        f_title = f"Title: {self.type}"  # Prepare title line
        f_job_title = f"Job title: {self.job_title}"  # Prepare job title line
        f_text = f"Description: {formetted_text}"  # Prepare description line
        f_salary = f"Salary: ${self.salary}"  # Prepare salary line
        f_days_left = f"Valid for: {self.days_left} days"  # Prepare days left line

        news = []  # Create empty list

        news.extend([f_title, f_job_title, f_text, f_salary, f_days_left])  # Add all lines

        final_news = '\n'.join(news)  # Join all lines

        with open('feed.txt', 'a', encoding='utf-8') as file:  # Open file for appending
            file.write(final_news)  # Write job ad to file
            file.write("\n\n")  # Add empty line after job ad



while True:  # Infinite loop for user input
    news_type = input("Hello! Welcome in our tool for adding News or Private Ad or Job Ad to our News Feed. \n"
                      "Chose type of news you want to add:\n "
                      "1 - News\n "
                      "2 - Private_ad\n "
                      "3 - Job_ad \n"
                      "To quit enter - 'q' \n"
                      "Your choose number: ")

    if news_type.lower() == 'q':  # If user wants to quit
        print("Quiting program. See you next time!")  # Print exit message
        break  # Exit loop

    elif news_type == "1":  # If user selects News
        print('You will add your News! You will be asked about providing City and News Text')
        city = input("Provide city name:\n")  # Get city from user
        text = input("Provide text:\n")  # Get news text from user
        ad = News(text, city)  # Create News object
        ad.add_text()  # Save news to file

    elif news_type == "2":  # If user selects Private ad
        print('You will add your Private_ad! You will be asked about Expiration Date and Private ad Text')
        while True:  # Loop for date validation
            expiration_date = input("Provide expiration date in format YYYY-MM-DD: ")  # Get date from user
            try:
                valid_date = datetime.strptime(expiration_date, "%Y-%m-%d").date()  # Try to parse date
                break  # If correct, exit loop
            except ValueError:
                print("Wrong date format! Please use YYYY-MM-DD.")  # If wrong, ask again
        text = input("Provide text: ")  # Get ad text from user
        ad = Private_ad(text, expiration_date)  # Create Private_ad object
        ad.add_text()  # Save ad to file

    elif news_type == "3":  # If user selects Job ad
        print('You will add your Job_ad! You will be asked about Job title and Job description and Salary and Expiration Date')
        job_title = input("Provide Job title: ")  # Get job title
        salary = input("Provide salary brutto in $: ")  # Get salary
        initial_valid_days = input("Provide initial_valid_days: ")  # Get number of valid days
        text = input("Provide Job description: ")  # Get job description
        ad = Job_ad(job_title, text, salary, initial_valid_days)  # Create Job_ad object
        ad.add_text()  # Save job ad to file
