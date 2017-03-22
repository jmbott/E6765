#### python manage.py runserver 0.0.0.0:8000

a2/models.py

# Create your models here.

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible  # only if you need to support Python 2
class Cities(models.Model):
    city = models.CharField(max_length=200)
    temp_c = models.IntegerField(default=0)
    temp_f = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.city

python manage.py shell

>>> from a2.models import Cities
>>> Cities.objects.all()
<QuerySet []>
>>> from django.utils import timezone
>>> c = Cities(city="New York", temp_c=10, temp_f=50, pub_date=timezone.now())
>>> c.save()
>>> c.id
1
>>> c.pub_date
datetime.datetime(2017, 3, 22, 3, 12, 42, 120761, tzinfo=<UTC>)
>>> Cities.objects.all()
<QuerySet [<Cities: Cities object>]>
>>>

a2/views.py

#from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Cities

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def city(request, city_id):
    city = Cities.objects.filter(id=city_id)
    return HttpResponse(city)

def celsius(request, city_id):
    temp_c = Cities.objects.filter(id=city_id)
    return HttpResponse(temp_c)

def fahrenheit(request, city_id):
    temp_f = Cities.objects.filter(id=city_id)
    return HttpResponse(temp_f)


a2/urls.py

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<city_id>[0-9]+)/$', views.city, name='city'),
    url(r'^(?P<city_id>[0-9]+)/celsius/$', views.celsius, name='celsius'),
    url(r'^(?P<city_id>[0-9]+)/fahrenheit/$', views.fahrenheit, name='fahrenheit'),
]

############

a2/models.py

# Create your models here.

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible  # only if you need to support Python 2
class Cities(models.Model):
    city = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.city

@python_2_unicode_compatible  # only if you need to support Python 2
class Celsius(models.Model):
    city_c = models.ForeignKey(Cities, on_delete=models.CASCADE)
    temp_c = models.IntegerField(default=0)
    def __str__(self):
        return self.temp_c

@python_2_unicode_compatible  # only if you need to support Python 2
class Fahrenheit(models.Model):
    city_f = models.ForeignKey(Cities, on_delete=models.CASCADE)
    temp_f = models.IntegerField(default=0)
    def __str__(self):
        return self.temp_f

UPDATE MODELS:

python manage.py makemigrations a2
python manage.py sqlmigrate a2 0002
python manage.py migrate

FLUSH DATA FROM DATA TABLES:

python manage.py flush

DROP ALL TABLES:

python manage.py sqlflush

python manage.py shell

>>> from a2.models import Cities, Celsius, Fahrenheit
>>> Cities.objects.all()
<QuerySet []>
>>> Celsius.objects.all()
<QuerySet []>
>>> Fahrenheit.objects.all()
<QuerySet []>
>>> from django.utils import timezone
>>> c = Cities(city="New York", pub_date=timezone.now())
>>> c.save()
>>> c.id
2
>>> c.pub_date
datetime.datetime(2017, 3, 22, 11, 42, 42, 539053, tzinfo=<UTC>)
>>> Cities.objects.all()
<QuerySet [<Cities: New York>]>

a2/models.py

# Create your models here.

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible  # only if you need to support Python 2
class Cities(models.Model):
    city = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.city

@python_2_unicode_compatible  # only if you need to support Python 2
class Celsius(models.Model):
    temp_c = models.IntegerField(default=0)
    city = models.ManyToManyField(Cities, blank=True, null=True)
    def __str__(self):
        return self.temp_c

@python_2_unicode_compatible  # only if you need to support Python 2
class Fahrenheit(models.Model):
    temp_f = models.IntegerField(default=0)
    city = models.ManyToManyField(Cities, blank=True, null=True)
    def __str__(self):
        return self.temp_f


a2/models.py

# Create your models here.

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible  # only if you need to support Python 2
class C(models.Model):
    temp_c = models.IntegerField(default=0)
    city = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return str(self.temp_c)

@python_2_unicode_compatible  # only if you need to support Python 2
class F(models.Model):
    temp_f = models.IntegerField(default=0)
    city = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return str(self.temp_f)

>>> from a2.models import C, F
>>> C.objects.all()
<QuerySet []>
>>> F.objects.all()
<QuerySet []>
>>> from django.utils import timezone
>>> c = C(temp_c="12", city="New York", pub_date=timezone.now())
>>> c
<C: 12>
>>> c.save()
>>> c.city
'New York'
>>> C.objects.all()
<QuerySet [<C: 12>]>
>>>
>>> cb = C(temp_c="14", city="Big Sky", pub_date=timezone.now())
>>> cb.save()
>>> C.objects.all()
<QuerySet [<C: 12>, <C: 14>]>
>>>


a2/views.py

#from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import C, F

def index(request):
    return HttpResponse("Hello, world.")

#def city(request, city_id):
#    city = Cities.objects.filter(id=city_id)
#    return HttpResponse(city)

def celsius(request, city_id):
    temp_c = C.objects.filter(city=str(city_id))
    return HttpResponse(temp_c)

def fahrenheit(request, city_id):
    temp_f = F.objects.filter(city=str(city_id))
    return HttpResponse(temp_f)

a2/urls.py

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^(?P<city_id>[0-9]+)/$', views.city, name='city'),
    url(r'^(?P<city_id>)/celsius/$', views.celsius, name='celsius'),
    url(r'^(?P<city_id>[0-9]+)/fahrenheit/$', views.fahrenheit, name='fahrenheit'),
]

>>> from a2.models import C, F
>>> C.objects.all()
<QuerySet []>
>>> from django.utils import timezone
>>> c = C(temp_c="12", city="ny", pub_date=timezone.now())
>>> c.save()
>>> c = C(temp_c="14", city="bs", pub_date=timezone.now())
>>> c.save()
>>> C.objects.all()
<QuerySet [<C: 12>, <C: 14>]>

a2/urls.py

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^(?P<city_id>[0-9]+)/$', views.city, name='city'),
    url(r'^(?P<city_id>)[1-4]+/celsius/$', views.celsius, name='celsius'),
    url(r'^(?P<city_id>[1-4]+)/fahrenheit/$', views.fahrenheit, name='fahrenheit'),
]

# city 1 = ny
# city 2 = no
# city 3 = bs
# city 4 = sf

>>> from a2.models import C, F
>>> C.objects.all()
<QuerySet []>
>>> from django.utils import timezone
>>> c = C(temp_c="12", city="1", pub_date=timezone.now())
>>> c.save()
>>> c = C(temp_c="14", city="2", pub_date=timezone.now())
>>> c.save()
>>> c = C(temp_c="16", city="3", pub_date=timezone.now())
>>> c.save()
>>> c = C(temp_c="18", city="4", pub_date=timezone.now())
>>> c.save()
>>> C.objects.all()
<QuerySet [<C: 12>, <C: 14>, <C: 16>, <C: 18>]>
>>>

a2/views.py

#from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import C, F

def index(request):
    return HttpResponse("Hello, world.")

#def city(request, city_id):
#    city = Cities.objects.filter(id=city_id)
#    return HttpResponse(city)

def celsius(request, city_id):
    temp_c = C.objects.filter(city=city_id)
    return HttpResponse(temp_c)

def fahrenheit(request, city_id):
    temp_f = F.objects.filter(city=city_id)
    return HttpResponse(temp_f)

a2/models.py

# Create your models here.

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible  # only if you need to support Python 2
class C(models.Model):
    temp_c = models.IntegerField(default=0)
    city = models.IntegerField(default=1)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return str(self.temp_c)

@python_2_unicode_compatible  # only if you need to support Python 2
class F(models.Model):
    temp_f = models.IntegerField(default=0)
    city = models.IntegerField(default=1)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return str(self.temp_f)
