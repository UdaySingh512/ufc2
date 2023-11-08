"""UFC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from UFC.settings import STATIC_URL, STATICFILES_DIR
from firstapp import views

from django.conf import settings
from django.contrib.staticfiles.urls import static,staticfiles_urlpatterns
from django.urls import re_path as url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mytest',views.test),
    path('userlogin',views.userlogin,name="userlogin"),
    path('allblogs',views.allblogs,name="allblogs"),
    path('Register',views.Register,name="register"),
    path('homepage',views.homepage,name="homepage"),
    path('headercontact',views.headercontact,name="contact"),
    path('video',views.video,name="video"),

  
    path('matches',views.matches,name="matches"),

    
    path('videos',views.videos1,name="videos"),

    url(r'^search_player$',views.search_player,name="search_player"),
    path('athletes',views.athletes1,name="athletes"),

    path('athletes/<str:id>',views.athletesgender,name="athletesgender"),
    path('news',views.news,name='news'),
    path('fullnews/<int:id>',views.fullnews,name='fullnews'),
    path('aboutus',views.aboutus,name="aboutus"),
    path('profile/<int:id>',views.profile,name="profile"),
    path('fullblog/<int:id>',views.fullblog,name='fullblog'),
    path('userprofile',views.userprofile,name="userprofile"),
    path('editprofile',views.editprofile,name='editprofile'),
    path('changepassword',views.changepassword,name='changepassword'),
    path('addreview',views.addreview),
    path('logout',views.logout,name="logout"),
    path('newsapi',views.newsapi,name="newsapi"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('analysis',views.analysis,name="analysis"),
    path('playermatchanalysis',views.playermatchanalysis,name="playermatchanalysis"),
    path('ufcanalysis',views.ufcanalysis,name="ufcanalysis"),
    path('StaticAnalysis',views.StaticAnalysis,name="StaticAnalysis"),
    path('ufctoplocations',views.ufctoplocations,name="ufctoplocations"),
    path('blueageplayers',views.blueageplayers,name="blueageplayers"),
    path('askquestion',views.askquestion,name="askquestion"),
    path('discussion',views.discussion,name="discussion"),
    path('discussionanswer/<int:id>',views.discussionanswer,name="discussionanswer"),
    path('redageplayers',views.redageplayers,name="redageplayers"),
    path('forgotpass',views.forgotpass,name="forgotpass"),
    path('titlebout',views.titlebout,name="titlebout"),
    path('sendmail',views.sendmail,name="sendmail"),
    path('Stanceanalysis',views.Stanceanalysis,name="Stanceanalysis"),
    path('rstanceanalysis',views.rstanceanalysis,name="rstanceanalysis"),
    path('weightclass',views.weightclass,name="weightclass"),
    path('redmatches',views.redmatches,name="redmatches"),
    path('bluematches',views.bluematches,name="bluematches"),
    path('bluekosub',views.bluekosub,name="bluekosub"),
    path('redkosub',views.redkosub,name="redkosub"),
    path('basicinfoanalysis',views.basicinfoanalysis,name="basicinfoanalysis"),
    path('senti',views.senti,name="senti"),
    path('weightcomp',views.weightcomp,name="weightcomp"),
    path('winningcomp',views.winningcomp,name="winningcomp"),
    path('heightcomp',views.heightcomp,name="heightcomp"),
    path('upmatches',views.upmatches,name="upmatches"),

    url(r'^search_players$',views.search_players,name="search_players"),
    path('recordings',views.recordings1,name="recordings"),
    path('changepass',views.changepass,name="changepass"),
    path('Rankings',views.Rankings,name="Rankings"),
    path('countryanalysis',views.countryanalysis,name="countryanalysis"),
    path('wscomp',views.wscomp,name="wscomp"),
    path('editpicture',views.editpicture,name="editpicture"),
]


urlpatterns+=staticfiles_urlpatterns()
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
