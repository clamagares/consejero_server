from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r'applicationConfiguration', views.ApplicationConfigurationView)


urlpatterns = [
    url(r'^applicationConfiguration/(?P<pk>[0-9]+)/$', views.ApplicationConfigurationView.as_view()),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.UsersView.as_view()),
    url(r'^create_user/$', views.CreateUsersView.as_view()),
    url(r'^emergency_contact/$', views.EmergencyContactsView.as_view()),
    url(r'^emergency_contact/(?P<pk>[0-9]+)/$', views.EmergencyContactEdit.as_view()),
    url(r'^user_avatar/$', views.UserAvatarPieces.as_view()),
    url(r'^contact_form/$', views.ContactForm.as_view()),
    url(r'^user_progress/$', views.SaveUserProgress.as_view()),
    url(r'^user_auth/$', views.AuthUser.as_view()),
    url(r'^user_password_recovery/$', views.PostPasswordRecovery.as_view()),
    url(r'^get_library_docs/$', views.GetLibraryDocs.as_view()),
    url(r'^get_corporate_phone_book/$', views.GetCorporatePhoneBook.as_view()),
]