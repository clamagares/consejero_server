from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render, redirect
from Users.models import *
from user_interaction.models import *
from django.db import connection
import json
from django.utils.safestring import mark_safe

class DashBoard(View):

    def get(self, request):
        validate_session(request)
        locations = Location.objects.all()
        advances = UserTopicProgress.objects.all().order_by('-date_completed')
        locates, progress = [], []
        for location in locations:
            for advance in advances:
                if advance.user.id == location.user.id:
                    locates.append(location)
                    progress.append(advance)
        location_advances = [{"locates": l, "advances": a} for l, a in zip(locates, progress)]

        profiles = Profile.objects.filter(user__is_staff = False, user__is_superuser = False)
        genders = Gender.objects.all()
        
        genders_percentage = {}
        for profile in profiles:
           for gender in genders:
                if gender.id == profile.gender.id:
                    if gender.name in genders_percentage:
                        genders_percentage[gender.name] += 1
                    else:
                        genders_percentage[gender.name] = 1

        return render (request, 'dashboard.html', {'locations':location_advances, 'genders_percentage':mark_safe(json.dumps(genders_percentage))})
        

def validate_session(request):

    if not request.user.is_authenticated() == "False":
        pass
        #return redirect('login')
