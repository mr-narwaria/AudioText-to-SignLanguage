from django.shortcuts import render, HttpResponse, redirect
from AudioText2SignLangApp.models import Contact
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# Create your views here.
# home view
def home(request):
    return render(request, 'home.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/animation')
        else:
            messages.warning(request, 'Invalid username or password.')
            return redirect('/login')
        
    return render(request, 'login.html')

# About View
def about(request):
    return render(request, 'about.html')

# Contact view
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        desc = request.POST.get("desc")
        # print(name, phone, email, desc)
        contact = Contact(name=name, phone=phone, email=email,
                          desc=desc, date=datetime.today())
        contact.save()

        # this is for dismishal message
        messages.success(request, 'submitted successfully!')
        return redirect('/contact')
        # till this
    return render(request, 'contact.html')

# main content animation view
# @login_required(login_url='/login/')
def animation(request):
    if request.method == 'POST':
        text = request.POST.get('sentence')
        # tokenizing the sentence
        text.lower()
        # tokenizing the sentence
        words = word_tokenize(text)

        tagged = nltk.pos_tag(words)
        tense = {}
        tense["future"] = len([word for word in tagged if word[1] == "MD"])
        tense["present"] = len(
            [word for word in tagged if word[1] in ["VBP", "VBZ", "VBG"]])
        tense["past"] = len(
            [word for word in tagged if word[1] in ["VBD", "VBN"]])
        tense["present_continuous"] = len(
            [word for word in tagged if word[1] in ["VBG"]])

        # stopwords that will be removed
        stop_words = set(["mightn't", 're', 'wasn', 'wouldn', 'be', 'has', 'that', 'does', 'shouldn', 'do', "you've", 'off', 'for', "didn't", 'm', 'ain', 'haven', "weren't", 'are', "she's", "wasn't", 'its', "haven't", "wouldn't", 'don', 'weren', 's', "you'd", "don't", 'doesn', "hadn't", 'is', 'was', "that'll", "should've", 'a', 'then', 'the', 'mustn', 'i',
                         'nor', 'as', "it's", "needn't", 'd', 'am', 'have',  'hasn', 'o', "aren't", "you'll", "couldn't", "you're", "mustn't", 'didn', "doesn't", 'll', 'an', 'hadn', 'whom', 'y', "hasn't", 'itself', 'couldn', 'needn', "shan't", 'isn', 'been', 'such', 'shan', "shouldn't", 'aren', 'being', 'were', 'did', 'ma', 't', 'having', 'mightn', 've', "isn't", "won't"])

        # removing stopwords and applying lemmatizing nlp process to words
        lr = WordNetLemmatizer()
        filtered_text = []
        for w, p in zip(words, tagged):
            if w not in stop_words:
                if p[1] == 'VBG' or p[1] == 'VBD' or p[1] == 'VBZ' or p[1] == 'VBN' or p[1] == 'NN':
                    filtered_text.append(lr.lemmatize(w, pos='v'))
                elif p[1] == 'JJ' or p[1] == 'JJR' or p[1] == 'JJS' or p[1] == 'RBR' or p[1] == 'RBS':
                    filtered_text.append(lr.lemmatize(w, pos='a'))
                else:
                    filtered_text.append(lr.lemmatize(w))

        # adding the specific word to specify tense
        words = filtered_text
        temp = []
        for w in words:
            if w == 'I':
                temp.append('Me')
            else:
                temp.append(w)
        words = temp
        probable_tense = max(tense, key=tense.get)

        if probable_tense == "past" and tense["past"] >= 1:
            temp = ["Before"]
            temp = temp + words
            words = temp
        elif probable_tense == "future" and tense["future"] >= 1:
            if "Will" not in words:
                temp = ["Will"]
                temp = temp + words
                words = temp
            else:
                pass
        elif probable_tense == "present":
            if tense["present_continuous"] >= 1:
                temp = ["Now"]
                temp = temp + words
                words = temp

        filtered_text = []
        for w in words:
            path = w + ".mp4"
            f = finders.find(path)
            # splitting the word if its animation is not present in database
            if not f:
                for c in w:
                    filtered_text.append(c)
            # otherwise animation of word
            else:
                filtered_text.append(w)
        words = filtered_text
        return render(request, 'animation.html', {'words': words, 'text': text})
    else:
        if request.user.is_authenticated:
            return render(request, 'animation.html')
        else:
            messages.info(request, 'Login Required')
            return redirect('/login')

# Signup view
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        print(username, email, password)
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already taken.')
            return redirect('/signup')
        
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Use correct email.')
            return redirect('/signup')
        
        # Create the user
        # user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        user.save()

        messages.success(request, 'Successfully Signing Up!.')
        
        # Authenticate and login the user
        authenticated_user = authenticate(request=request, username=username, password=password)
        if authenticated_user is not None:
            login(request, user)
            return redirect('/animation')
        else:
            messages.info(request, 'Invalid username or password.')
            return redirect('/signup')
    return render(request, 'signup.html')


# logout view
def logout_view(request):
    logout(request)
    return redirect('/')
    return redirect(request, 'logout')


def profile_view(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')
    else:
        messages.info(request, 'Login Required')
        return redirect('/login')

