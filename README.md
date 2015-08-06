# Academic Context

These projects were first written in June and July by Alan Rominger,
as assignments for the Python class in the Iron Yard code school
, Durham NC. The class was taught by [cndreisbach](https://github.com/cndreisbach),
and the [full class curriculum](https://tiyd-python-2015-05.github.io/pages/resources.html)
 can also be found hosted on Github.

 After the program finished, in August 2015, some additional work was done
 to combine all of these into a single Django app, with a shared user system.

# App Descriptions

There are 3 big apps which are contained in this program. In the order in which
they were assigned, they are listed below:

1. MovieLens
  - Clone of: https://movielens.org/
  - A site that allows you to rate and review movies. It operates on the system of 1 to 5 stars for a movie rating, and it allows the entry of a movie review as text as well. It has a substantial amount of demographic data, because these fields are also present for the sample data.
  - This also is set up to pre-load open data from the real MovieLens data set.
2. URLy Bird
  - Clone of: https://bitly.com/
  - A link submission site that produces a short link to redirect a friend to the link in question. In the process it also collects data about the number of times the link has been clicked and tallies user statistics, among other features.
3. QuestionsBox
  - Clone of: http://stackexchange.com/
  - A question and answer site with upvoting and downvoting. In addition to submitting questions and answers on those questions, they can comment on either the question or the answer, and have access to listings based on users, tags, and other things.

# Deployment

This is intended to be deployed to Heroku. The system variables that need to be
set are listed below.

- DATABASE_URL
- DJANGO_SETTINGS_MODULE
- PYTHONPATH
- SECRET_KEY

Some of these, such as the DATABASE_URL, will automatically be set when another
part of the configuration is done, like a migration. Others need to be specially
set according to the related instructions from the course.
