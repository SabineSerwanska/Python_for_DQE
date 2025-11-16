from datetime import date  # Import date class for getting today's date
from datetime import datetime  # Import datetime class for parsing dates
from datetime import timedelta  # Import timedelta for date calculations
from HW_6_text_normalizer import text_normalizer  # Import the text normalization function
import re  # Import regular expressions for text splitting
import os  # Import os module for file operations
import json
import xml.etree.ElementTree as ET
import sqlite3


class News:
    def __init__(self, text, city):
        self.type = "News"  # Set the type as News
        self.text = text_normalizer(text)  # Normalize and store the news text
        self.city = city  # Store the city name
        self.publish_date = date.today()  # Store today's date as publish date

    def add_text(self, db):
        formatted_city = self.city.capitalize().strip()  # Capitalize and clean the city name

        sentences = re.split(r'([.!?])', self.text)  # Split the text into sentences using punctuation
        result = []
        if len(sentences) == 1:  # No punctuation found
            result.append(sentences[0].strip().capitalize())
        else:
            for s in range(0, len(sentences) - 1, 2):  # Loop through sentences in pairs (sentence + punctuation)
                sentence = sentences[s].strip().capitalize() + sentences[
                    s + 1]  # Capitalize first letter and add punctuation
                result.append(sentence)  # Add the formatted sentence to the result list
            if len(sentences) % 2 != 0 and sentences[-1].strip():
                last = sentences[-1].strip().capitalize()
                if not re.search(r'[.!?]$', last):
                    last += '.'
                result.append(last)

        formatted_text = '\n'.join(result)  # Join sentences with new lines

        f_title = f"Title: {self.type}"  # Prepare the title line
        f_publish_date = f"Publish date: {self.publish_date}"  # Prepare the publish date line
        f_city = f"City: {formatted_city}"  # Prepare the city line
        f_text = f"Text: {formatted_text}"  # Prepare the text line

        news = []  # Create an empty list for news lines

        news.extend([f_title, f_publish_date, f_city, f_text])  # Add all lines to the list

        final_news = '\n'.join(news)  # Join all lines into a single string

        with open('feed.txt', 'a', encoding='utf-8') as file:  # Open the file for appending
            file.write(final_news)  # Write the news to the file
            file.write("\n\n")  # Add an empty line after the news


        db.add_news_to_db(self.publish_date, formatted_city, formatted_text)


class Private_ad:
    def __init__(self, text, expiration_date):
        self.type = "Private ad"  # Set the type as Private ad
        self.text = text_normalizer(text)  # Normalize and store the ad text
        self.expiration_date = datetime.strptime(expiration_date,
                                                 "%Y-%m-%d").date()  # Parse and store the expiration date
        self.days_left = (self.expiration_date - date.today()).days  # Calculate and store days left

    def add_text(self, db):
        sentences = re.split(r'([.!?])', self.text)  # Split the text into sentences using punctuation
        result = []
        if len(sentences) == 1:  # No punctuation found
            result.append(sentences[0].strip().capitalize())
        else:
            for s in range(0, len(sentences) - 1, 2):  # Loop through sentences in pairs (sentence + punctuation)
                sentence = sentences[s].strip().capitalize() + sentences[s + 1]  # Capitalize and add punctuation
                result.append(sentence)  # Add to the result list
            if len(sentences) % 2 != 0 and sentences[-1].strip():
                last = sentences[-1].strip().capitalize()
                if not re.search(r'[.!?]$', last):
                    last += '.'
                result.append(last)

        formatted_text = '\n'.join(result)  # Join sentences with new lines

        f_title = f"Title: {self.type}"  # Prepare the title line
        f_days_left = f"Days left: {self.days_left}"  # Prepare the days left line
        f_text = f"Text: {formatted_text}"  # Prepare the text line

        news = []  # Create an empty list

        news.extend([f_title, f_days_left, f_text])  # Add all lines to the list

        final_news = '\n'.join(news)  # Join all lines into a single string

        with open('feed.txt', 'a', encoding='utf-8') as file:  # Open the file for appending
            file.write(final_news)  # Write the ad to the file
            file.write("\n\n")  # Add an empty line after the ad


        db.add_private_ad_to_db(self.days_left, formatted_text)


class Job_ad:
    def __init__(self, job_title, text, salary, initial_valid_days):
        self.type = "Job ad"  # Set the type as Job ad
        self.job_title = job_title  # Store the job title
        self.text = text_normalizer(text)  # Normalize and store the job description
        self.salary = salary  # Store the salary
        self.expiration_date = date.today() + timedelta(
            days=int(initial_valid_days))  # Calculate and store expiration date
        self.days_left = (self.expiration_date - date.today()).days  # Calculate and store days left

    def add_text(self, db):
        sentences = re.split(r'([.!?])', self.text)  # Split the text into sentences using punctuation
        result = []
        if len(sentences) == 1:  # No punctuation found
            result.append(sentences[0].strip().capitalize())
        else:
            for s in range(0, len(sentences) - 1, 2):  # Loop through sentences in pairs (sentence + punctuation)
                sentence = sentences[s].strip().capitalize() + sentences[s + 1]  # Capitalize and add punctuation
                result.append(sentence)  # Add to the result list
            if len(sentences) % 2 != 0 and sentences[-1].strip():
                last = sentences[-1].strip().capitalize()
                if not re.search(r'[.!?]$', last):
                    last += '.'
                result.append(last)

        formatted_text = '\n'.join(result)  # Join sentences with new lines

        f_title = f"Title: {self.type}"  # Prepare the title line
        f_job_title = f"Job title: {self.job_title}"  # Prepare the job title line
        f_text = f"Description: {formatted_text}"  # Prepare the description line
        f_salary = f"Salary: ${self.salary}"  # Prepare the salary line
        f_days_left = f"Valid for: {self.days_left} days"  # Prepare the days left line

        news = []  # Create an empty list

        news.extend([f_title, f_job_title, f_text, f_salary, f_days_left])  # Add all lines to the list

        final_news = '\n'.join(news)  # Join all lines into a single string

        with open('feed.txt', 'a', encoding='utf-8') as file:  # Open the file for appending
            file.write(final_news)  # Write the job ad to the file
            file.write("\n\n")  # Add an empty line after the job ad

        db.add_job_ad_to_db(self.job_title, formatted_text, self.salary, self.days_left)


class Add_from_txt:
    def __init__(self, path):
        if path.lower() == 'default':  # If user enters 'default', use 'input.txt'
            self.path = 'input.txt'
        else:
            self.path = path  # Otherwise, use the provided path

    def read_file(self):
        dicts = []  # Create an empty list to store dictionaries
        blok = {}  # Create an empty dictionary for each record
        with open(self.path, 'r', encoding='utf-8') as file:  # Open the input file for reading
            for line in file:  # Loop through each line in the file
                line = line.strip()  # Remove leading/trailing whitespace
                if not line:  # If the line is empty
                    if blok:  # If the current block is not empty
                        dicts.append(blok)  # Add the block to the list
                        blok = {}  # Start a new block
                else:
                    if '=' in line:  # If the line contains '='
                        key, value = line.split('=', 1)  # Split into key and value
                        blok[key.strip().lower()] = value.strip()  # Add to the current block
            if blok:  # After the loop, if there is a block left
                dicts.append(blok)  # Add it to the list
        return dicts  # Return the list of dictionaries

    def remove_file(self):
        if os.path.exists(self.path):  # If the file exists
            os.remove(self.path)  # Remove the file


class Add_from_json:
    def __init__(self, path):
        if path.lower() == 'default':  # If user enters 'default', use 'input.json'
            self.path = 'input.json'
        else:
            self.path = path  # Otherwise, use the provided path

    def read_file(self):
        # dicts = []  # Create an empty list to store dictionaries
        # blok = {}  # Create an empty dictionary for each record
        with open(self.path, 'r', encoding='utf-8') as file:  # Open the input file for reading
            data = json.load(file)

        return data  # Return the list of dictionaries

    def remove_file(self):
        if os.path.exists(self.path):  # If the file exists
            os.remove(self.path)  # Remove the file


class Add_from_xml:  # Defines a class for handling XML file input
    def __init__(self, path):  # Constructor that takes the file path as an argument
        if path.lower() == 'default':  # If the user enters 'default'
            self.path = 'input.xml'  # Set the default file path to 'input.xml'
        else:
            self.path = path  # Otherwise, use the provided file path

    def read_file(self):  # Method to read and process the XML file
        tree = ET.parse(self.path)  # Parse the XML file and create an element tree
        root = tree.getroot()  # Get the root element of the XML tree
        dicts = []  # Initialize an empty list to store records as dictionaries
        for child in root:  # Iterate over each direct child of the root
            blok = {"type": child.tag.lower()}  # Create a dictionary with the type (child tag name)
            for subchild in child:  # Iterate over each sub-element (field) of the child
                blok[subchild.tag.lower()] = subchild.text.strip() if subchild.text else ""  # Add the field to the dictionary, stripping whitespace or using an empty string if no text
            dicts.append(blok)  # Add the dictionary (record) to the list
        return dicts  # Return the list of dictionaries containing the XML data

    def remove_file(self):
        if os.path.exists(self.path):  # If the file exists
            os.remove(self.path)  # Remove the file


class Save_to_db:
    def __init__(self, db_path='feed.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS NEWS (
                NEWS_ID integer PRIMARY KEY AUTOINCREMENT,
                PUBLISH_DATE text,
                CITY text,
                TEXT text);
            ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS PRIVATE_AD (
                PRIVATE_AD_ID integer PRIMARY KEY AUTOINCREMENT,
                DAYS_LEFT integer,
                TEXT text);
            ''')

        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS JOB_AD (
                        JOB_AD_ID integer PRIMARY KEY AUTOINCREMENT,
                        JOB_TITLE text,
                        DESCRIPTION text,
                        SALARY text,
                        DAYS_LEFT integer);
                ''')

        self.conn.commit()


    def add_news_to_db(self, publish_date, city, text):
        self.cursor.execute('''
                SELECT * FROM NEWS WHERE LOWER(text)=LOWER(?) AND LOWER(city)=LOWER(?) AND LOWER(publish_date)=LOWER(?)
                ''', (text, city, str(publish_date)))
        result = self.cursor.fetchone()
        if result:
            print("Duplicate found, not adding.")
        else:
            self.cursor.execute('''
            INSERT INTO NEWS (publish_date, city, text)
            VALUES (?, ?, ?)
            ''', (str(publish_date), city, text))
            self.conn.commit()

    def add_private_ad_to_db(self, days_left, text):
        self.cursor.execute('''
                        SELECT * FROM PRIVATE_AD WHERE days_left= ? AND LOWER(text)=LOWER(?)
                        ''', (days_left, text))
        result = self.cursor.fetchone()
        if result:
            print("Duplicate found, not adding.")
        else:
            self.cursor.execute('''
            INSERT INTO PRIVATE_AD (days_left, text)
            VALUES (?, ?)
            ''', (days_left, text))
            self.conn.commit()

    def add_job_ad_to_db(self, job_title, description, salary, days_left):
        self.cursor.execute('''
                        SELECT * FROM JOB_AD WHERE LOWER(job_title)=LOWER(?) AND LOWER(description)=LOWER(?)
                         AND LOWER(salary) = LOWER(?) AND days_left = ?
                        ''', (job_title, description, salary, days_left))
        result = self.cursor.fetchone()
        if result:
            print("Duplicate found, not adding.")
        else:
            self.cursor.execute('''
            INSERT INTO JOB_AD (job_title, description, salary, days_left)
            VALUES (?, ?, ?, ?)
            ''', (job_title, description, salary, days_left))
            self.conn.commit()

    def close(self):
        self.conn.close()



db = Save_to_db()

while True:  # Infinite loop for user input
    news_type = input("Hello! Welcome in our tool for adding News or Private Ad or Job Ad to our News Feed. \n"
                      "Chose type of news you want to add:\n "
                      "1 - News\n "
                      "2 - Private_ad\n "
                      "3 - Job_ad \n"
                      "F - Add from txt file\n"
                      "JSON - Add from json file\n"
                      "XML - Add from XML file\n"
                      "To quit enter - 'q' \n"
                      "Your choose option: ")  # Prompt user for input

    if news_type.lower() == 'q':  # If user wants to quit
        print("Quiting program. See you next time!")  # Print exit message
        break  # Exit the loop


    elif news_type.lower() == "f":  # If user selects file input
        print('You will add your feed from txt file!')  # Inform user about file input
        path = input(
            "Provide the path to input file or type 'default' if file is in current folder as 'input.txt': ")  # Get file path
        configs = Add_from_txt(path)  # Create Add_from_files object
        try:
            dicts = configs.read_file()  # Try to read records from file
        except FileNotFoundError:
            print("File not found!")  # Print error if file does not exist
            continue  # Go back to menu
        for my_dict in dicts:  # Loop through each record
            keys = set(my_dict.keys())  # Get set of keys in the record
            if {'city', 'text'} <= keys:  # If it's a News record
                ad = News(text=my_dict['text'], city=my_dict['city'])  # Create News object
                ad.add_text(db)  # Save news to file

            elif {'expiration_date', 'text'} <= keys:  # If it's a Private ad
                ad = Private_ad(text=my_dict['text'],
                                expiration_date=my_dict['expiration_date'])  # Create Private_ad object
                ad.add_text(db)  # Save ad to file
            elif {'job_title', 'description', 'salary_brutto_in_us', 'initial_valid_days'} <= keys:  # If it's a Job ad
                ad = Job_ad(job_title=my_dict['job_title'], text=my_dict['description'],
                            salary=my_dict['salary_brutto_in_us'],
                            initial_valid_days=my_dict['initial_valid_days'])  # Create Job_ad object
                ad.add_text(db)  # Save job ad to file
        configs.remove_file()  # Remove the file after processing


    elif news_type.lower() == "json":  # Check if user selected JSON file input
        print('You will add your feed from JSON!')  # Inform the user about JSON input
        path = input(
            "Provide the path to input file or type 'default' if file is in current folder as 'input.json': ")  # Ask for file path
        configs = Add_from_json(path)  # Create an Add_from_json object with the given path
        try:
            dicts = configs.read_file()  # Try to read records from the JSON file
        except FileNotFoundError:
            print("File not found!")  # Print error if file does not exist
            continue  # Return to menu
        except json.JSONDecodeError:
            print("JSON format error! Please check your file.")  # Print error if JSON is invalid
            continue  # Return to menu
        for idx, my_dict in enumerate(dicts, 1):  # Loop through each record, with index for error reporting
            try:
                keys = set(my_dict.keys())  # Get all keys from the current record
                job_keys = {k.lower() for k in keys}  # Normalize all keys to lowercase for comparison
                if {'city', 'text'} <= job_keys:  # Check if it's a News record
                    ad = News(text=my_dict['text'], city=my_dict['city'])  # Create News object
                    ad.add_text(db)  # Save news to file
                elif {'expiration_date', 'text'} <= job_keys:  # Check if it's a Private ad
                    ad = Private_ad(text=my_dict['text'],
                                    expiration_date=my_dict['expiration_date'])  # Create Private_ad object
                    ad.add_text(db)  # Save ad to file

                elif {'job_title', 'description', 'salary_brutto_in_us',
                      'initial_valid_days'} <= job_keys:  # Check if it's a Job ad
                    salary_key = next((k for k in my_dict if k.lower() == 'salary_brutto_in_us'),
                                      None)  # Find salary key regardless of case
                    ad = Job_ad(
                        job_title=my_dict['job_title'],
                        text=my_dict['description'],
                        salary=my_dict[salary_key],
                        initial_valid_days=my_dict['initial_valid_days']
                    )  # Create Job_ad object

                    ad.add_text(db)  # Save job ad to file
                else:
                    raise KeyError(
                        "Missing required fields for any record type.")  # Raise error if record type is unknown
            except KeyError as e:
                print(f"Record {idx}: Missing required field(s) or wrong format: {e}")  # Print error for this record
                continue  # Continue to next record

        configs.remove_file()  # Remove the JSON file after processing


    elif news_type.lower() == "xml":  # Check if user selected JSON file input
        print('You will add your feed from XML!')  # Inform the user about JSON input
        path = input(
            "Provide the path to input file or type 'default' if file is in current folder as 'input.xml': ")  # Ask for file path
        configs = Add_from_xml(path)  # Create an Add_from_json object with the given path
        try:
            dicts = configs.read_file()  # Try to read records from the XML file
        except FileNotFoundError:
            print("File not found!")  # Print error if file does not exist
            continue  # Return to menu
        except ET.ParseError:
            print("XML format error! Please check your file.")
            continue

        for idx, my_dict in enumerate(dicts, 1):
            job_keys = set(my_dict.keys())
            if my_dict.get('type') == 'news' and {'city', 'text'} <= job_keys:
                ad = News(text=my_dict['text'], city=my_dict['city'])
                ad.add_text(db)
            elif my_dict.get('type') == 'private_ad' and {'expiration_date', 'text'} <= job_keys:
                ad = Private_ad(text=my_dict['text'], expiration_date=my_dict['expiration_date'])
                ad.add_text(db)
            elif my_dict.get('type') == 'job_ad' and {'job_title', 'description', 'salary_brutto_in_us',
                                                      'initial_valid_days'} <= job_keys:
                ad = Job_ad(
                    job_title=my_dict['job_title'],
                    text=my_dict['description'],
                    salary=my_dict['salary_brutto_in_us'],
                    initial_valid_days=my_dict['initial_valid_days']
                )
                ad.add_text(db)
            else:
                print(f"Record {idx}: Missing required field(s) or wrong format.")

        configs.remove_file()  # Remove the XML file after processing


    elif news_type == "1":  # If user selects News
        print('You will add your News! You will be asked about providing City and News Text')  # Inform user
        city = input("Provide city name:\n")  # Get city from user
        text = input("Provide text:\n")  # Get news text from user
        ad = News(text, city)  # Create News object
        ad.add_text(db)  # Save news to file


    elif news_type == "2":  # If user selects Private ad
        print(
            'You will add your Private_ad! You will be asked about Expiration Date and Private ad Text')  # Inform user
        while True:  # Loop for date validation
            expiration_date = input("Provide expiration date in format YYYY-MM-DD: ")  # Get expiration date from user
            try:
                valid_date = datetime.strptime(expiration_date, "%Y-%m-%d").date()  # Try to parse the date
                break  # If correct, exit the loop
            except ValueError:
                print("Wrong date format! Please use YYYY-MM-DD.")  # Print error if format is wrong
        text = input("Provide text: ")  # Get ad text from user
        ad = Private_ad(text, expiration_date)  # Create Private_ad object
        ad.add_text(db)  # Save ad to file


    elif news_type == "3":  # If user selects Job ad
        print(
            'You will add your Job_ad! You will be asked about Job title and Job description and Salary and Expiration Date')  # Inform user
        job_title = input("Provide Job title: ")  # Get job title from user
        salary = input("Provide salary brutto in $: ")  # Get salary from user
        initial_valid_days = input("Provide initial_valid_days: ")  # Get number of valid days from user
        text = input("Provide Job description: ")  # Get job description from user
        ad = Job_ad(job_title, text, salary, initial_valid_days)  # Create Job_ad object
        ad.add_text(db)  # Save job ad to file

db.close()
