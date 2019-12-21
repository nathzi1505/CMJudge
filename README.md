# CMJudge

## Routes 
`/` : Root Page <br>
`/users` : Profile Page <br>
`/assignmentName` : Problem Description <br>
`/assignmentName/submit` : Submission Page <br>
`/assignmentName/results` : Results Page <br>

## Prequisites
Autentication required

## Models
### User :
 * `roll`
 * `problems_solved`
  (List of all Problem (s) (to be done in frontend, indicate *completed* : the corresponding problems))
 * `password`
 
### Assignment : 
 * `name`
 * `id`
 
### Problem : 
 * `assignment_id` (Foreign Key)
 * `user_id` (Foreign Key)
 * `problem_question` (CharField)
 * `test-cases` (Char Field)

## References : 
* [DRF REACT](https://wsvincent.com/django-rest-framework-react-tutorial/) 
