# CMJudge

## Routes 
* `/` : Root Page <br>
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
 * `name` (Char Field)
 * `id` (Integer) (Primary Key)
 
### Problem : 
 * `assignment_id` (CharField) (Primary Key) 
 * `user_id` (Foreign Key)
 * `problem_desc` (CharField)
 * `test_cases` (Char Field)
 * `difficulty` (Integer)
 
 ### Solved : 
 * `user_id` (Foreign Key)
 * `assignment_id` (Foreign Key)

## References : 
* [DRF REACT](https://wsvincent.com/django-rest-framework-react-tutorial/) 
