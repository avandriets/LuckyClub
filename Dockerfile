FROM python:3
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code
 ADD requirements.txt /code/
 RUN pip install psycopg2
 RUN pip install -r requirements.txt
 ADD . /code/
 ENV FLASK_APP=/code/lucky_club/lucky_club.py
 RUN flask initdb

 EXPOSE 8000
# one user service
# CMD ["python", "application.py"]
CMD ["gunicorn", "wsgi:application", "-b", "0.0.0.0:8000", "--log-file", "-", "--access-logfile", "-", "--workers", "4", "--keep-alive", "0"]
