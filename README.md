# CMJudge

## Routes 
* `/` : Home Page <br>
* `/users` : Profile Page <br>
* `/assignmentName` : Problem Description <br>
* `/assignmentName/submit` : Submission Page <br>
* `/assignmentName/results` : Results Page <br>

## Prequisites
Autentication required

## Models
### User :
 * `roll` (Integer) (Primary Key)
 * `problems_solved` (Integer)
 * `password` (Hashed CharText)
 
### Assignment :
 * `id` (Primary Key)
 * `name` (CharField)
 
### Question : 
 * `id` (Primary Key)
 * `assignment_id` (Foreign Key)
 * `code` (CharField)
 * `problem_desc` (CharField)
 * `test_cases` (CharField)
 * `difficulty` (Integer)
 
 ### Solved : 
 * `id` (Primary Key)
 * `user_id` (Foreign Key)
 * `question_id` (Foreign Key)

## References : 
* [DRF REACT](https://wsvincent.com/django-rest-framework-react-tutorial/) 
