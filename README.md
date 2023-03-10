
# Final Project - Medical Device Software: FFR Measurement System
# Vincent Wong
## 1. Project Description
In this final project (in General Assembly's Software Test Engineer program), I developed a simple 
medical device software system, focused on fractional flow reserve (FFR) measurements.  

FFR is a ratio of the pressure downstream of a narrowed vessel section in the heart, and pressure upstream to that narrowing (aortic pressure). The narrowing is called a stenosis.  

![1_anatomy.png](..%2Fimages%2F1_anatomy.png)

![2_FFR.png](..%2Fimages%2F2_FFR.png)
FFR = Pd / Pa, where: 
* Pd = Distal pressure downstream of narrowing
* Pa = Arterial pressure upstream of narrowing

In cardiology, FFR is a 'golden standard' measurement, that is commonly used to determine what treatment to apply to the narrowed vessel. 
![3_ffr2.png](..%2Fimages%2F3_ffr2.png)

Why I picked this: I've worked on FFR-related products for 3 years throughout my career. As I will work in medical device software after this program, 
it feels natural to create my own basic version of medical device software.  

Note: I did my best to use as much as I can, of what I learned in the class. In this case, FFR can be calculated just by division. 
As we spent time learning Selenium, I ensured I used Selenium to get FFR from a website, to run my program.

Test functions in "Functional Requirements" below.


## 2. Technical Requirements

### Functional requirements
![11.userstories.png](..%2Fimages%2F11.userstories.png)

User interface:
![15.user_interface.png](..%2Fimages%2F15.user_interface.png)

### Administrative requirements

(Project A)
- At least 6 classes
- Class Diagram
- Use a test-driven development (TDD) approach
- Appropriate naming conventions, docstrings, and OO principles
- Use of test suite
- Version control: use of branches, at least 60 commits
<hr>

## 3. Technologies Ued
* Pycharm: IDE used to program in Python language
* Google Chrome: web browser usage, for use of FFR calculator website
* Python libraries: Pandas for dataframes, Selenium for web automation testing, unit testing, PyTest for test result logging
* Github, Git: version control, user story logging

## 4. Screenshots
1. User login and menu:

![5.login.png](..%2Fimages%2F5.login.png)
2. Begin case:
* 2a. Select existing patient
* 2b. Create new patient
![4.flow_1.png](..%2Fimages%2F4.flow_1.png)

3. Review case:
* 3a. List cases by patient
* 3b. List cases by user

![9.review.png](..%2Fimages%2F9.review.png)

Database relationship diagram:
![10.data_relationship.png](..%2Fimages%2F10.data_relationship.png)

4. Create new user account
![7.createuser.png](..%2Fimages%2F7.createuser.png)

Class diagram:
![16.classdiagram.png](..%2Fimages%2F16.classdiagram.png)

Pytest report:
* Only for System class. 
* See separate document. 

## 5. Project Hurdles and Wins
* Wins
  * Software resembles medical device software, which my career focuses on. I'm happy about that, especially with the FFR theme.
  * For unit testing without user input, I'm proud of the verifications I've done for the System class.
* Hurdles
  * Ran out of time. Couldn't complete all requirements. 
    * Application was ambitious for me, for 2.5 days. Was relatively large to code, test, and document. 
  * Had issues with simulating user input for unit testing.
  * Couldn't get to applying error handling for all workflows in the program. 
  * Database files have to be manually reset in src folder, to run unit tests. 

## 6. Planning Charts / Project Workflow
* User stories
  * See above
Completed status of user stories: 
![12.userstoriescompleted.png](..%2Fimages%2F12.userstoriescompleted.png)

## 7. Icebox
* Could not meet these requirements in time: 
  * Have 6 classes. I only have 3. 
  * Unit testing for all classes. 

* User story: 1-5 (Confirmation) As a doctor, I can see my username and the patient I'm working on, before I work on a case. So I can confirm the case record will be attributed to the correct doctor and patient. 
  * Lower priority to other user stories. 

## 8. Credits
- People:
  - GA Instructors: Suresh, Iris, Winston
  - My program classmates, for collaboration. Raymond, for helping troubleshoot my mock issue. 
  - My wife and extended family, for taking care of my kid while I've been in class, these 9 weeks. 
- Technical:
  - Project 1: Bank. I leveraged my code and architecture from this project for this one. 
  - See src files for citations for any sources I used.