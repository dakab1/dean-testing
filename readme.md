
## dean test

### Requirements:
* Use git for version control
* Publish on GitHub or send us a compressed repo 
* If making publicly available, please avoid using '----' or ‘----’ in repo name or description

#### Functionality
* Create locally running RESTful web API django-rest-framework recommended, though not necessary
* that accepts a request with 'city' and 'period' args 
* fetches weather data for that location and period of time from some public API e.g. Yahoo! Weather 
* computes min, max, average and median temperature and humidity for that location and period and returns that to the user
*Should be done in one day

#### Extra goals:
* Provide a view which renders a bar chart for the requested data 
* Deploy it somewhere

### Solution
* Used free options available on openweathermap.org
* Used django-test-framework

### Installation
I suggest you do the below in virtualenv

```pip install -r requirements.txt```

### Start dev server
```./manage.py runserver 0.0.0.0:8000```

#### Example Call
Here is an example call if you are running on localhost in debug: 
http://localhost:8000/v1/forecast/centurion/?period=1

The period parameter is numeric and each increment of 1 is a multiplier to the next 3 hour slot for a weather forecast. The cycles are as follows:

If it we call the api just before midnight, the following subsiquent values would result in the following periods:

1) midnight
2) 3am
3) 6am
4) 9am
5) 12am
6) 3pm
7) 6pm
8) 9pm

These numbers keep going up until 5 days for the free version of the API.