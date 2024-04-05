# Text-Audio-Speech To Sign Language Converter

A Web Application that takes in live audio speech recording as input, converts it into text and displays the relevant Indian Sign Language animations.

# Technology Requirement 
> - Django Framework is used for website building and backend control.
> - Frontend using HTML,CSS,JavaScript.
> - Text Preprocessing using Natural Language Toolkit(NLTK).

## Prerequisites

> - Python >= 3.7
> - Browser supports Web Speech API
> - Download all required packages for Python script A2SL/views.py


Project Demo Video:


Create Virtual environment by using virtualenv 
command
pip install virtualenv
python -m venv venv
activate virtual environment command: 
venv\Scripts\activate

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py runserver 8000
