
# Final Project - Medical Device Software: FFR Measurement System
# Vincent Wong
## 1. Project Description
In this 3-day final project (in General Assembly's Software Validation Engineer program), I developed a simple 
medical device software system, focused on fractional flow reserve (FFR) measurements.  

FFR is a ratio of pressure downstream to a narrowed vessel section in the heart, and pressure upstream to that narrowing (aortic pressure). The narrowing is called a stenosis.  
![1_anatomy2.png](images%2F1_anatomy2.png)

![2_FFR.png](images%2F2_FFR.png)

FFR = Pd / Pa, where: 
* Pd = Distal pressure downstream of narrowing
* Pa = Arterial pressure upstream of narrowing

In cardiology, FFR is a 'golden standard' measurement, that is commonly used to determine what treatment to apply to the narrowed vessel. 
![3_ffr2.png](images%2F3_ffr2.png)

Why this project: I've worked on FFR-related products for 3 years throughout my career. As I will work in medical device software after this program, 
it feels natural to create my own basic version of medical device software.  

Notes: 
* I did my best to use as much as I can, of what I learned in the class. In this case, FFR can be calculated just by division. 
As we spent time learning Selenium, I ensured I used Selenium to get FFR from a website, to run my program.
* To keep this representative of what I can accomplish in 3 days, I made no changes to the software after I completed this, on 10Mar2023.  

<hr>

## 2. Technical Requirements

### Use and Functional Requirements:
1. User login and menu
* 1-1 (Login) As a doctor with an account, I log into the system, so that I can perform a procedure or review cases.
* 1-2 (Login Deny) As a doctor or user that entered incorrect credentials (user ID or password), I am denied access, so I do not have access to patient data with incorrect credentials. 
* 1-4 (New Patient) As a doctor, I create a patient account, to attribute cases to a patient not yet on the system. 

2. Begin case
* 2-1 (Select vessel) As a doctor, I can select a vessel on which to perform pressure measurements. 
* 2-2 (Measure FFR) As a doctor, I can perform a measurement, and see the returned FFR.
* 2-3 (Next Action) As a doctor, I can see whether the FFR is clinically good or not good, and any recommended actions.

3. Review case
* 3-1 (Review physician's cases) As a doctor, I can see the cases I performed (or another physician) by date, so I can look back at the cases I've done. 
* 3-2 (Review patient's cases) As a doctor, I can see the case information for a specific patient, so I can see their FFR history.

4. Create user account
* 1-3 (New User Account) As a doctor with an account, I create a user account for another doctor. 

### User interface:
![15.user_interface.png](images%2F15.user_interface.png)

### Administrative requirements:
(not all files are included in my personal Github page)

(Project A)
- At least 6 classes
- Class Diagram
- Use a test-driven development (TDD) approach
- Appropriate naming conventions, docstrings, and OO principles
- Use of test suite
- Version control: use of branches, at least 60 commits
<hr>

## 3. Technologies Used:
* Pycharm: IDE used to program in Python language
* Google Chrome: web browser usage, for use of FFR calculator website
* Python libraries: Pandas for dataframes, Selenium for web automation testing, unit testing, PyTest for test result logging
* Github, Git: version control, user story logging

## 4. Screenshots:
1. User login and menu:

![5.login.png](images%2F5.login.png)
2. Begin case:
* 2a. Select existing patient
* 2b. Create new patient
* 
![4.flow_1.png](images%2F4.flow_1.png)

3. Review case:
* 3a. List cases by patient
* 3b. List cases by user

![9.review.png](images%2F9.review.png)

Database relationship diagram:

![10.data_relationship.png](images%2F10.data_relationship.png) 

4. Create new user account 

![7.createuser.png](images%2F7.createuser.png)

Architecture: 
* Each method of each class is listed below. Methods call and may pass arguments to one another (downstream, right to left), and may return outputs upstream (left to right). 
* There are three classes (System, User, Main) that include methods specific to the System, User, or the user without access (Main).
* There are 4 separate databases that relate to one another via foreign and primary keys, which are called by read and write methods in the System class. 

![17.architecture.png](images%2F17.architecture.png)

Class diagram: 

![16.classdiagram.png](images%2F16.classdiagram.png)
<hr>

## 5. Project Hurdles and Wins:
* Wins
  * Software resembles medical device software, which my career focuses on. I'm happy about that, especially with the FFR theme.
  * For unit testing without user input, I'm proud of the verifications I've done for the System class.
* Hurdles
  * Ran out of time. Couldn't complete all requirements. 
    * Application was ambitious for me, for 2.5 days. Was relatively large to code, test, and document. 
  * Had issues with simulating user input for unit testing.
  * Couldn't get to applying error handling for all workflows in the program. 
  * Database files have to be manually reset in src folder, to run unit tests. 
<hr>

## 6. Icebox:
* Could not meet these requirements in time: 
  * I only have 3 out of 6 classes. 
  * Unit testing for all classes. 
  * Cleanup of files

* Could not do these in time:
  * system.py: 
    * Set up encapsulation for the data reading, for cybersecurity. 
      * Unit testing could not access the data read method, so any higher-level methods can access the databases.
  * user.py: 
    * Adjust ranges for Pd and Pa, so that FFR does not measure above 1.0.
  * test_system.py: write a method to automatically reset files for unit testing.
    * Unit test for System requires manual resetting of files, to work. 
    * System counter is set higher, without change to default unit test value of 100. 

* User story: 1-5 (Confirmation) As a doctor, I can see my username and the patient I'm working on, before I work on a case. So I can confirm the case record will be attributed to the correct doctor and patient. 
  * Lower priority to other user stories. 
<hr>

## 7. Credits:
- People:
  - GA Instructors: Suresh, Iris, Winston
  - My program classmates, for collaboration. Raymond, for helping troubleshoot my mock issue. 
  - My wife and extended family, for taking care of my kid while I've been in class, these 9 weeks. 
  - My management at Abbott that gave me this opportunity, and my teammates there that supported my work while I'm in this class. 
- Technical:
  - Project 1: Bank. I leveraged my code and architecture from this project for this one. 
  - See src files for citations for any sources I used.
<hr>

## 8. Code

### (1) main.py

![i_main.png](images%2Fi_main.png)
<hr>

### (2) user.py

![i_u1.png](images%2Fi_u1.png)

![i_u2.png](images%2Fi_u2.png)

![i_u3.png](images%2Fi_u3.png)

![i_u4.png](images%2Fi_u4.png)

![i_u5.png](images%2Fi_u5.png)

![i_u6.png](images%2Fi_u6.png)
<hr>

### (3) system.py

![i_s1.png](images%2Fi_s1.png)

![i_s2.png](images%2Fi_s2.png)

![i_s3.png](images%2Fi_s3.png)

![i_s4.png](images%2Fi_s4.png)

![i_s5.png](images%2Fi_s5.png)

![i_s6.png](images%2Fi_s6.png)

![i_s7.png](images%2Fi_s7.png)
<hr>

### Files - databases: 
### data_user.csv

![i_f1.png](images%2Fi_f1.png)

### data_patient.csv 

![i_f2.png](images%2Fi_f2.png)

### data_measurement.csv

![i_f3.png](images%2Fi_f3.png)

### data_case.csv

![i_f4.png](images%2Fi_f4.png)

### system_count

![i_f5.png](images%2Fi_f5.png)

### Unit test: test_system.py

![i_ts1.png](images%2Fi_ts1.png)

![i_ts2.png](images%2Fi_ts2.png)

![i_ts3.png](images%2Fi_ts3.png)

![i_ts4.png](images%2Fi_ts4.png)

![i_ts5.png](images%2Fi_ts5.png)
<hr>