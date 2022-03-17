# first-django-rest-framework

This project is developed as an exercise during TM R&D Internship.



### Running the project locally

First, clone the repository to the local machine: <br /> <br />
`git clone https://github.com/fasa79/first-django-rest-framework.git`
<br /> <br />
Then install the requirements <br /> <br />
`pip install -r requirements.txt`
<br /> <br />
Create mysql database as per details in `thd/settings.py`, insert existing data from excel file and run the database
<br /> <br />
Apply the migrations: <br /> <br />
`python manage.py migrate`
<br /> <br />
Then, run the development server: <br /> <br />
`python manage.py migrate`
<br /> <br />
Finally, run the test script: <br /> <br />
`python testThdAPI.py `
<br /> <br />
Check `testThdAPI.py` for the unit test result
<br /> <br />
**Have Fun!**
