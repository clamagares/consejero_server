import json
import datetime


from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import render, redirect
from Users.models import *
from user_interaction.models import *
from django.db import connection
from django.utils.safestring import mark_safe
from dateutil.relativedelta import relativedelta




class DashBoard(View):
    def get(self, request):
        locations = Location.objects.all().order_by('-date_created')
        today = datetime.datetime.now()
        advances = UserTopicProgress.objects.all().order_by('-date_completed')
        profiles = Profile.objects.filter(user__is_staff = False, user__is_superuser = False)
        genders = Gender.objects.all()



        locates, progress = [], []
        names, doc_type, doc_num, birthdate, age_general, gender_general, ethnic, location_general, conditions_general, advance_general  = [], [], [], [], [], [], [], [], [], []

        for location in locations:
            for advance in advances:
                if advance.user.id == location.user.id:
                    locates.append(location)
                    progress.append(advance)

        location_advances = [{"locates": l, "advances": a} for l, a in zip(locates, progress)]
        
        genders_percentage = {}
        genders_names_by_age = {}
        gender_names_by_advance = {}
        advance_by_ethnic_group = {}
        advance_by_condition = {}

        for profile in profiles:
            for gender in genders:
                if gender.id == profile.gender.id:
                    
                    if gender.name in genders_percentage:
                        genders_percentage[gender.name] += 1
                    else:
                        genders_percentage[gender.name] = 1
                    
                    age, gender_name = save_gender_by_age(today,profile)
                    
                    if gender_name in genders_names_by_age:
                        if age in genders_names_by_age[gender_name]:
                            genders_names_by_age[gender_name][age] +=1
                        else:
                            genders_names_by_age[gender_name][age] = 1
                    else:
                        genders_names_by_age[gender_name] = {age:1}


                    for advance in advances:
                        if advance.user.id == profile.user.id:
                            if gender_name in gender_names_by_advance:

                                if advance.topic_activity.topic.description in gender_names_by_advance[profile.gender.name]:
                                    gender_names_by_advance[profile.gender.name][advance.topic_activity.topic.description] += 1
                                else:
                                    gender_names_by_advance[profile.gender.name][advance.topic_activity.topic.description] = 1

                            else:
                                gender_names_by_advance[profile.gender.name] = {advance.topic_activity.topic.description:1}
                            
                            if profile.ethnic_group.name in advance_by_ethnic_group:
                                if advance.topic_activity.topic.description in advance_by_ethnic_group[profile.ethnic_group.name]:
                                    advance_by_ethnic_group[profile.ethnic_group.name][advance.topic_activity.topic.description] += 1
                                else:
                                    advance_by_ethnic_group[profile.ethnic_group.name][advance.topic_activity.topic.description] = 1
                            else:
                                advance_by_ethnic_group[profile.ethnic_group.name] = {advance.topic_activity.topic.description:1}


                            if profile.condition.name in advance_by_condition:
                                if advance.topic_activity.topic.description in advance_by_condition[profile.condition.name]:
                                    advance_by_condition[profile.condition.name][advance.topic_activity.topic.description] += 1
                                else:
                                    advance_by_condition[profile.condition.name][advance.topic_activity.topic.description] = 1
                            else:
                                advance_by_condition[profile.condition.name] = {advance.topic_activity.topic.description:1}
            for location in locations:
                if location.user.id == profile.user.id:
                    for advance in advances:
                        if advance.user.id == location.user.id:
                            if profile.document_number not in doc_num:
                                names.append(profile.user.first_name + ' ' + profile.user.last_name)
                                doc_type.append(profile.document_type.name)
                                doc_num.append(profile.document_number)
                                birthdate.append(profile.birthdate.strftime("%Y-%m-%d"))
                                age_general.append(relativedelta(today, profile.birthdate).years)
                                gender_general.append(profile.gender.name)
                                ethnic.append(profile.ethnic_group.name)
                                location_general.append(location.city.name)
                                conditions_general.append(profile.condition.name)
                                advance_general.append(advance.topic_activity.topic.description)




        general_information = [{"names": names, "doc_type": doc_type, "doc_num": doc_num, "birthdate": birthdate, "age_general": age_general, "gender_general": gender_general, "ethnic": ethnic, "location_general": location_general, "conditions_general": conditions_general, "advance_general": advance_general} for names,  doc_type,  doc_num, birthdate, age_general, gender_general, ethnic, location_general, conditions_general, advance_general in zip( names,  doc_type,  doc_num, birthdate, age_general, gender_general, ethnic, location_general, conditions_general, advance_general)]

        return render (request, 'dashboard.html', {'locations':location_advances, 'genders_percentage':mark_safe(json.dumps(genders_percentage)), 'genders_names_by_age':mark_safe(json.dumps(genders_names_by_age)), 'gender_names_by_advance':mark_safe(json.dumps(gender_names_by_advance)), 'advance_by_ethnic_group':mark_safe(json.dumps(advance_by_ethnic_group)), 'advance_by_condition':mark_safe(json.dumps(advance_by_condition)), 'general_information':general_information })
  





def save_gender_by_age(today,profile):
    difference_in_years = relativedelta(today, profile.birthdate).years
    
    if difference_in_years >= 0 and difference_in_years <=4:
        return "0-4", profile.gender.name

    if difference_in_years >= 5 and difference_in_years <=9:
        return "5-9", profile.gender.name

    if difference_in_years >= 10 and difference_in_years <=14:
        return "10-14", profile.gender.name

    if difference_in_years >= 15 and difference_in_years <=19:
        return "15-19", profile.gender.name

    if difference_in_years >= 20 and difference_in_years <=24:
        return "20-24", profile.gender.name

    if difference_in_years >= 25 and difference_in_years <=29:
        return "25-29", profile.gender.name

    if difference_in_years >= 30 and difference_in_years <=34:
        return "30-34", profile.gender.name

    if difference_in_years >= 35 and difference_in_years <=39:
        return "35-39", profile.gender.name

    if difference_in_years >= 40 and difference_in_years <=44:
        return "40-44", profile.gender.name

    if difference_in_years >= 45 and difference_in_years <=49:
        return "45-49", profile.gender.name

    if difference_in_years >= 50 and difference_in_years <=54:
        return "50-54", profile.gender.name

    if difference_in_years >= 55 and difference_in_years <=59:
        return "55-59", profile.gender.name

    if difference_in_years >= 60 and difference_in_years <=64:
        return "60-64", profile.gender.name

    if difference_in_years >= 65 and difference_in_years <=69:
        return "65-69", profile.gender.name

    if difference_in_years >= 70 and difference_in_years <=74:
        return "70-74", profile.gender.name

    if difference_in_years >= 75 and difference_in_years <=79:
        return "75-79", profile.gender.name

    if difference_in_years >= 80 and difference_in_years <=84:
        return "80-84", profile.gender.name

    if difference_in_years >= 85 :
        return "85-+", profile.gender.name



def validate_session(request):
    print("Session validation")




