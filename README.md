# University-Management-System

This is a portal where both students and profs can register.
Both Profs and students will have different types of dashboard.
It is deployed on https://unmeshkumar.pythonanywhere.com/

Prof's Dashboard
- Profs can see the courses under them and students enrolled in those courses
- They can change the grades of the students enrolled in those courses
- They can see a bar graph reprsenting the number of students securing a particular grade
- They can add a new course with credits ranging from 1 to 4

Student's dashboard
- Students can see the courses in which they are enrolled and also grades provided in each of them
- They can see their overall CGPA and total credits taken till now
- They can enroll in the courses they haven't enrolled yet
- They can see a bar graph represting the number of courses in which they has got a particular grade
- They can also see the list of students enrolled in the courses they have taken and what is the distribution of grades in the whole course


Steps to run it
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
cd university
python manage.py runserver
```

Now, The django app will be active on localhost:8000

