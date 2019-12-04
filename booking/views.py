from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import datetime
from .models import User, Flight, Review, Train


@csrf_exempt
def index(request):
    if request.method == 'POST':
        source = request.POST['source']
        sourceArr = source.split(',')
        sourceCity = sourceArr[0]
        destination = request.POST['destination']
        destinationArr = destination.split(',')
        destinationCity = destinationArr[0]
        startdate = request.POST['startdate']
        startdate = startdate.split('-')
        year = int(startdate[0])
        month = int(startdate[1])
        day = int(startdate[2])
        flightClass = request.POST['class']
        if (flightClass == 'economy'):
            flights = Flight.objects.filter(sourceLocation=sourceCity).filter(destinationLocation=destinationCity).filter(
                departureDate=datetime.date(year, month, day)).filter(numSeatsRemainingEconomy__gt=0)
            flights = list(flights)
            return render(request, 'index.html', {"results": "yes", "some_list": flights, "class": flightClass})
        elif (flightClass == 'business'):
            flights = Flight.objects.filter(sourceLocation=sourceCity).filter(destinationLocation=destinationCity).filter(
                departureDate=datetime.date(year, month, day)).filter(numSeatsRemainingBusiness__gt=0)
            flights = list(flights)
            return render(request, 'index.html', {"results": "yes", "some_list": flights, "class": flightClass})
        else:
            flights = Flight.objects.filter(sourceLocation=sourceCity).filter(destinationLocation=destinationCity).filter(
                departureDate=datetime.date(year, month, day)).filter(numSeatsRemainingFirst__gt=0)
            flights = list(flights)
            return render(request, 'index.html', {"results": "yes", "some_list": flights, "class": flightClass})
    else:
        return render(request, 'index.html')
    # figure out how booking will work (send to booking page?)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        check_user = User.objects.filter(email=email)
        valid_user = (len(list(check_user)) == 1)

        if (valid_user):
            current_user = email
            user_name = check_user.first().username
            request.session['current_user'] = current_user
            request.session['user_name'] = user_name
            return render(request, 'index.html', {'msg': 'Login successful'})
        else:
            return render(request, 'login.html', {'msg': 'Failed. Please try again'})
    else:
        return render(request, 'login.html')


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        existing_email = User.objects.filter(email=email)
        is_new_user = (len(list(existing_email)) == 0)
        if (is_new_user):
            new_user = User.objects.create(username=username, email=email, password=password)
            new_user.save()
            return render(request, 'login.html', {'msg': 'Sign up successful'})
        else:
            return render(request, 'signup.html', {'msg': 'Error. Email already exists'})
    else:
        return render(request, 'signup.html')


@csrf_exempt
def reviews(request):
    if request.method == 'POST':
        review = request.POST['review']
        author = request.session['user_name']
        current_date = datetime.datetime.today().strftime('%Y-%m-%d')
        user_exists = Review.objects.filter(author=author)
        if (len(list(user_exists)) == 0):
            new_review = Review.objects.create(
                review=review, submissionDate=current_date, author=author)
            new_review.save()
            return render(request, 'reviews.html', {'msg': 'Review recorded!'})
    else:
        reviews = Review.objects.all()
        return render(request, 'reviews.html', {'results': 'yes', 'some_list': reviews})


@csrf_exempt
def trains(request):
    if request.method == 'POST':
        source = request.POST['source']
        sourceArr = source.split(',')
        sourceCity = sourceArr[0]
        destination = request.POST['destination']
        destinationArr = destination.split(',')
        destinationCity = destinationArr[0]
        startdate = request.POST['startdate']
        startdate = startdate.split('-')
        year = int(startdate[0])
        month = int(startdate[1])
        day = int(startdate[2])
        trainClass = request.POST['class']
        trains = Train.objects.filter(sourceLocation=sourceCity).filter(
            destinationLocation=destinationCity).filter(departureDate=datetime.date(year, month, day))
        trains = list(trains)
        if (trainClass == 'economy'):
            trains = Train.objects.filter(sourceLocation=sourceCity).filter(destinationLocation=destinationCity).filter(
                departureDate=datetime.date(year, month, day)).filter(numSeatsRemainingEconomy__gt=0)
            trains = list(trains)
            return render(request, 'trains.html', {"results": "yes", "some_list": trains, "class": trainClass})
        elif (trainClass == 'business'):
            trains = Train.objects.filter(sourceLocation=sourceCity).filter(destinationLocation=destinationCity).filter(
                departureDate=datetime.date(year, month, day)).filter(numSeatsRemainingBusiness__gt=0)
            trains = list(trains)
            return render(request, 'trains.html', {"results": "yes", "some_list": trains, "class": trainClass})
        else:
            trains = Train.objects.filter(sourceLocation=sourceCity).filter(destinationLocation=destinationCity).filter(
                departureDate=datetime.date(year, month, day)).filter(numSeatsRemainingFirst__gt=0)
            trains = list(trains)
            return render(request, 'trains.html', {"results": "yes", "some_list": trains, "class": trainClass})
    else:
        return render(request, 'trains.html')


def book(request):
    if request.method == 'POST':
        objId = request.GET.get('id')
        bookType = request.GET.get('type')
        card_number = request.POST['card_number']
        card_type = request.POST['card_type']
        try:
            current_user = request.session['current_user']
        except:
            return render(request, 'book.html', {'msg': "You're not signed in, please sign in before trying to book!"})
        current_date = datetime.datetime.today().strftime('%Y-%m-%d')
        if (bookType == 'flight'):
            travelClass = request.GET.get('class')
            obj = Flight.objects.filter(id=objId).first()
            if (travelClass == 'economy'):
                Flight.objects.filter(id=objId).update(
                    numSeatsRemainingEconomy=obj.numSeatsRemainingEconomy-1)
            elif (travelClass == 'business'):
                Flight.objects.filter(id=objId).update(
                    numSeatsRemainingBusiness=obj.numSeatsRemainingBusiness-1)
            elif (travelClass == 'first'):
                Flight.objects.filter(id=objId).update(
                    numSeatsRemainingFirst=obj.numSeatsRemainingFirst-1)
        return render(request, 'book.html', {'msg': 'Booking successful'})
    else:
        objId = request.GET.get('id')
        bookType = request.GET.get('type')
        if (bookType == 'flight'):
            travelClass = request.GET.get('class')
            obj = Flight.objects.filter(id=objId)
            return render(request, 'book.html', {'booking': 'yes', 'some_list': obj, 'type': bookType, 'class': travelClass})
        elif (bookType == 'train'):
            travelClass = request.GET.get('class')
            obj = Train.objects.filter(id=objId)
            return render(request, 'book.html', {'booking': 'yes', 'some_list': obj, 'type': bookType, 'class': travelClass})
        else:
            return render(request, 'book.html')


def logout(request):
    # clear session
    del request.session['current_user']
    del request.session['user_name']
    return render(request, 'index.html', {'msg': 'Logout successful'})
