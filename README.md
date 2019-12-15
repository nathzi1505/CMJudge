# CMJudge

## Basic Routes to be made 

* / : the root page : used to login
* /users/:user_id/ : the user page 
  * user/:user_id?=profile : shows the profile page
* /assignments
* /assignments/:assign_id/ : shows the current problems
* /assignments/:assign_id/:problem_id : shows the description of the current problem with the option to submit code.

//No one can access the site without entering:

User model(Preassigned):
 * roll
 * Problems solved ( <int> )
  (List of all Problem (s) ( tb done in frontend , indicate *completed* : the corresponding problems ) )
 * password
 
Assignment model :
 * name
 * id
 
Problem model : 
 * Assignment id( Foreign Key )
 * User id ( Foreign Key )
 * Problem question (CharField )
 * Problem test-cases ( Char Field )
 ( Bonus Feature : Show updated code in textarea for each user )

User clicks on _problem_id _page_ and after submitting the code in the text area , it is sent as a post request to the server.
 
 

## References : 

* [DRF REACT](https://wsvincent.com/django-rest-framework-react-tutorial/) 
