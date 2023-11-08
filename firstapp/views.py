import matplotlib
from io import BytesIO
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from django.conf import settings
from django.core.mail import send_mail

from PIL import Image, ImageDraw
import PIL, PIL.Image
from io import StringIO
import pandas as pd
import matplotlib
from io import BytesIO
import io
import base64
#################################

import email
from django.shortcuts import render,redirect
from firstapp import models
import datetime
from firstapp.models import athletes,match, registeredUsers, videosnew
# Create your views here.
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
 
class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'NHPoQ69bsSnZS6n1IDRzeleI3'
        consumer_secret = 'RSIvkf2nffkWdF0pSC0fGJNBawZ6WU0JlwkiutLDZpZ2Kl1fXC'
        access_token = '1512351554128723973-hpIdZfttgXhmZ1S7ek8b0cA0t0yDyU'
        access_token_secret = 'cDIWs0EaCyd8XWbRbg9mlY8yfBPkeebkQPLkFfV7i5MK6'
 
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
            print("authenticated")
        except:
            print("Error: Authentication Failed")
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query, count ):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
 
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search_tweets(q = query, count = count)
 
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
 
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
 
                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            # return parsed tweets
            return tweets
 
        except Exception as e:
            # print error (if any)
            print("Error : " + str(e))
def test(request):
    return render(request,'test1.html')




def changepass(request):

    if request.method=='POST':
        reg=registeredUsers.objects.get(id=request.session['userid'])
        password=request.POST.get('oldpass')
        newpass=request.POST.get('newpass')
        confpass=request.POST.get('confpass')
        if(newpass==confpass):
            p=reg.password

            if(password==p):
                reg.password=newpass
                reg.confpass=confpass
                reg.save()
                rest="Password Changed"
                return render(request,'changepass.html',{'rest':rest})
            else:
                res="Invalid Current Password"
                return render(request,'changepass.html',{'res': res})    
        else:
            res="confirm Password and new Password Do Not Match"
            return render(request,"changepass.html",{'res':res})
    else:
        return render(request,'changepass.html')

def contact(request):
    return render(request,'contactus.html')

def userlogin(request):
    if request.method=='POST':
        email=request.POST.get('useremail')
        password=request.POST.get('password')
        print(email,password)

        if models.registeredUsers.objects.filter(emailid=email,password=password).exists():
            print('logged in')
            users=models.registeredUsers.objects.get(emailid=email)
            request.session['userid']=users.id

            return redirect('/userprofile')

        else:
            return render(request,'userlogin.html',{'res':1})


    return render(request,'userlogin.html')  

def allblogs(request):
    blogs=models.blogs.objects.all()
     #print(blogs)
    return render(request,'allblogs.html',{'data': blogs}) 




def headercontact(request):
    if request.method=='POST':
      

        username=request.POST.get('user_name')
        email=request.POST.get('user_email')
        usermessage=request.POST.get('message')

        hc=models.enquiry() #create an object

        hc.username=username
        hc.emailid=email
        hc.message=usermessage

        hc.save()
        return render(request,'headercontact.html',{'res':1}) 


    return render(request,'headercontact.html',) 


def Register(request):
    if request.method=='POST':
      username=request.POST.get('username')
      email=request.POST.get('useremail')
      password=request.POST.get('userpass') 
      confpass=request.POST.get('confpass')  
      
      if password==confpass:
          if models.registeredUsers.objects.filter(emailid=email).exists():
              return render(request,'Register.html',{'res':2})
          else:
              print('Registered')

              user=models.registeredUsers()    

              user.username=username
              user.emailid=email
              user.password=password

              user.save()
              return redirect('userlogin')

            

      else :
          return render(request,'Register.html',{'res':1})
    return render(request,'Register.html') 

def homepage(request):

    import datetime
    from datetime import date
    from newsapi.newsapi_client import NewsApiClient
    import pandas as pd

    newsapi= NewsApiClient(api_key='2638dc220b4d48428b930de9a8ed5d2e')
    json_data= newsapi.get_everything(q='ufc',
                            language='en',
                            from_param=str(date.today() - datetime.timedelta(days=29)),
                            to= str(date.today()),
                            page_size=3,
                            page=1,
                            sort_by='relevancy'
                            )
    k=json_data['articles']    


    upcoming=models.match.objects.filter(matchDate__gte=datetime.date.today())[:4]
    print(upcoming)

    return render(request,'homepage.html',{'upcoming':upcoming,'k':k}) 


def upmatches(request):
    return render(request,'upmatches.html')     

def video(request):
    return render(request,'video.html')  


    

def matches(request):
    content={}
    match=models.match.objects.all()[:8]
    print(match)

    upcoming=models.match.objects.filter(matchDate__gte=datetime.date.today())
    print(upcoming)

    content={
        'match':match,
        'upcoming':upcoming
    }
    return render(request,'matches.html',content)

def search_match(request):
    x=True
    matches=request.POST.get("match")
    print(matches)

    m=match.objects.filter(athlete1__contains=matches)
    print("p is", m)
    print(type(m))


    return render(request,'matches.html',{'match':m}) 


def videos1(request):
    videos=models.videosnew.objects.all()[:6]
    print(videos)

    return render(request,'videos.html',{'videos':videos}) 

def recordings1(request):
    videos=models.videosnew.objects.all()[:8]

    print(videos)

    return render(request,'recordings.html',{'videos':videos}) 
def search_players(request):
    x=True
    players=request.POST.get("player_name")
    print(players)

    p=videosnew.objects.filter(title__contains=players)
    print("p is", p)
    print(len(p))
    if len(p)>0:
        return render(request,'recordings.html',{'videos':p}) 
    else:
        msg='Please enter a valid name '
        return render(request,'recordings.html',{'videos':'','msg':msg}) 



def athletes1(request):
      allathletes=models.athletes.objects.all()

      return render(request,'athletes.html',{'data': allathletes,'key':1}) 
def search_player(request):
    x=True
    player=request.POST.get("player_name")
    print(player)

    p=athletes.objects.filter(name__contains=player)
    print("p is", p)
    print(type(p))
    if len(p)>0:
        return render(request,'athletes.html',{'data':p}) 
    else:
        msg='Please enter a valid name '
        return render(request,'athletes.html',{'data':'','msg':msg}) 




def athletesgender(request,id):
    content={}
    allathletes=models.athletes.objects.filter(gender=id)
    #print(blogs)
    if id=='Men':
        content={'data':allathletes,
        'key':2}
    elif id=='Women':
        content={'data':allathletes,
        'key':3}
    return render(request,'athletes.html',content) 
     

def news(request):
    news=models.news.objects.all()
     #print(blogs)
    return render(request,'news.html',{'data': news})  
      

def fullnews(request,id):
        news=models.news.objects.get(id=id)
        print(news)
        return render(request,'fullnews.html',{'data':news}) 

def aboutus(request):

    return render(request,'aboutus.html') 
    
def profile(request,id):

    content={}
    umatches=set()

    a=models.athletes.objects.get(id=id)
    print(a)

    match1=models.match.objects.filter(athlete1=a, matchDate__gte=datetime.date.today())
    print(match1)

    match2=models.match.objects.filter(athlete2=a, matchDate__gte=datetime.date.today())
    print(match2)

    umatches=umatches.union(match1,match2)
    print(umatches)

    
    Rmatches=set()

    b=models.athletes.objects.get(id=id)
    print(b)

    match1=models.match.objects.filter(athlete1=b, matchDate__lte=datetime.date.today())
    print(match1)

    match2=models.match.objects.filter(athlete2=b, matchDate__lte=datetime.date.today())
    print(match2)

    Rmatches=Rmatches.union(match1,match2)
    print(Rmatches)


    content={'data':a,
            'umatches':umatches,
            'data':b,
            'Rmatches':Rmatches}
    return render(request,'profile.html',content)  

def fullblog(request,id):
    blogs=models.blogs.objects.get(id=id)
    print(blogs)
    return render(request,'fullblog.html',{'data':blogs})       

def userprofile(request):
    if not request.session.has_key('userid'):
        return redirect('userlogin/')
    uid=request.session['userid']
    user=models.registeredUsers.objects.get(id=uid)
    
    return render(request,'userprofile.html',{'user':user})

def editprofile(request):

    if not request.session.has_key('userid'):

        return redirect('userlogin/')
    uid=request.session['userid']
    user=models.registeredUsers.objects.get(id=uid)
    if request.method=='POST' :
        detail=registeredUsers.objects.get(id=request.session['userid'])
        detail.username=request.POST.get('un')
        detail.phoneNumber=request.POST.get('pn')
        detail.gender=request.POST.get('gen')
        detail.dob=request.POST.get('dob')
        detail.city=request.POST.get('city')
        detail.state=request.POST.get('state')
        detail.save()
        data=registeredUsers.objects.get(id=request.session['userid'])
        return render(request,'userprofile.html',{'user':data})
    else:

        return render(request,'editprofile.html',{'user':user})

def editpicture(request):
    if not request.session.has_key('userid'):

        return redirect('userlogin/')
    
    if request.method=='POST':
        uid=request.session['userid']
        user=models.registeredUsers.objects.get(id=uid)
        detail=registeredUsers.objects.get(id=request.session['userid'])
        detail.profilePicture=request.FILES['pp']
        detail.save()
        data=registeredUsers.objects.get(id=request.session['userid'])
        return render(request,'userprofile.html',{'user':data})


    else:

        return render(request,'editpicture.html')  

def changepassword(request):
    return render(request,'changepassword.html')

def addreview(request):
    uid=request.session['userid']
    user=models.registeredUsers.objects.get(id=uid)
    if request.method=='POST':
        r=models.reviews()
        r.subject= request.POST.get('subject')
        r.message= request.POST.get('review')
        r.user=user
        
        r.save()
        return render(request,'addreview.html',{'res':1})

    return render(request,'addreview.html')

def logout(request)    :
    del request.session['userid']
    return redirect('/userlogin')

def newsapi(request)  :
        import datetime
        from datetime import date
        from newsapi.newsapi_client import NewsApiClient
        import pandas as pd

        newsapi= NewsApiClient(api_key='2638dc220b4d48428b930de9a8ed5d2e')
        json_data= newsapi.get_everything(q='ufc',
                                  language='en',
                                  from_param=str(date.today() - datetime.timedelta(days=29)),
                                  to= str(date.today()),
                                  page_size=18,
                                  page=1,
                                  sort_by='relevancy'
                                  )
        k=json_data['articles']                          
        return render(request,'newsapi.html',{'k' : k }) 

def dashboard(request):
    return render(request,'dashboard.html')

def forgotpass(request):
    if(request.method=='POST'):
        em=request.POST.get('em')
        user=registeredUsers.objects.filter(emailid=em)

        if(len(user)>0) :
            pw=user[0].password
            subject="Password"
            message="your Password is " + pw
            email_from=settings.EMAIL_HOST_USER
            recipient_list=[em,]
            send_mail(subject,message,email_from,recipient_list)
            rest="your password is sent to your recipient email account. Please check"
            print("mailsent")
            return render(request,'forgotpass.html',{'rest':rest}) 
        else:
            res="This email id is not registered"
            return render(request,'forgotpass.html',{'res':res})    
    else:
        res=''
        return render(request,'forgotpass.html')


            

def analysis(request):
    return render(request,'analysis.html') 
def playermatchanalysis(request):
    if request.method=="POST":
        #imports - same
        x=str(request.POST.get('Player_name'))
        import pandas as pd
        import matplotlib.pyplot as plt
       
        #std=StandardScaler()
        fig=plt.figure(figsize=(6, 7), dpi=80,facecolor='#f9f9f9', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        #visualization
        import pandas as pd
        df = pd.read_csv('ufc.csv')
        #x=input('select any player:') 
        df1=df[df['B_fighter'].str.contains(x)]
        if(len(df1)==0):
            msg="Select correct Player"
            return render(request,'playermatchanalysis.html',{'msg':msg}) 
        df1=df1.loc[:,['R_fighter','B_fighter','date','country','Winner']]
        k=['R player','B player','date','country','winner']
        print(df1)
        df2=df[df['R_fighter'].str.contains(x)]
        if(len(df2)==0):
            msg="Select correct Player"
            return render(request,'playermatchanalysis.html',{'msg':msg}) 
        df2=df2.loc[:,['R_fighter','B_fighter','date','country','Winner']]
        k=['R player','B player','date','country','winner']
        print(df2)

       
        #save the image - same
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        return render(request, 'graphic.html', {'graphic': graphic.decode('utf8'),'k':k})


        #return render(request,'playermatchanalysis.html')
    else:

        return render(request,'playermatchanalysis.html')


def ufcanalysis(request):
    return render(request,'ufcanalysis.html')

def StaticAnalysis(request):
    return render(request,'StaticAnalysis.html') 

def ufctoplocations(request):
    if request.method=="POST":
        #imports - same
        x=int(request.POST.get('no'))
        import pandas as pd
        import matplotlib.pyplot as plt
        #std=StandardScaler()
        fig=plt.figure(figsize=(6, 7), dpi=80,facecolor='#f9f9f9', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        #visualization
        df = pd.read_csv('ufc.csv')
        img=plt.imread('imgufc.jpg')
        df2=df.groupby('location')['location'].count().sort_values(ascending=False)
        df2=pd.DataFrame(df2)
        #x=int(input('select top locations where matches played  ') )
        df2=df2.iloc[0:x,:]
        ax=df2.plot.bar(alpha=0.7,color='skyblue')
        t='UFC \n Top'+str(x)+' locations'
        ax.set_title(t ,fontsize=17,fontweight='bold' , color='red')
        ax.set_xlabel('Name of location' ,fontsize=15,fontweight='bold')
        ax.set_ylabel('No. of location' ,fontsize=15,fontweight='bold')
        
        ax.imshow(img,extent=[-1,len(df2.index),0,df2['location'].max()+200],aspect='auto')
        #save the image - same
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        return render(request, 'graphic.html', {'graphic': graphic.decode('utf8')})


        #return render(request,'playermatchanalysis.html')
    else:

        return render(request,'ufctoplocations.html')

def askquestion(request):
    if not request.session.has_key('userid'):
        return redirect('userlogin/')
    uid=request.session['userid']
    user=models.registeredUsers.objects.get(id=uid)
    if request.method=='POST':
        r=models.question()
     
        r.question= request.POST.get('question')
        r.user=user
        
        r.save()
        return render(request,'askquestion.html',{'res':1})

    return render(request,'askquestion.html')

def discussion(request):
    questions=models.question.objectall().order_by('-id')
    return render(request,'discussion.html',{'data':questions}) 

def discussionanswer(request,id):
    return render(request,'discussionanswer.html')           

def blueageplayers(request):
    if request.method=="POST":
        #imports - same
        x=int(request.POST.get('start_age'))
        y=int(request.POST.get('last_age'))
        if y>x:

            import pandas as pd
            import matplotlib.pyplot as plt
            #std=StandardScaler()
            fig=plt.figure(figsize=(6, 7), dpi=80,facecolor='#f9f9f9', edgecolor='w')
            matplotlib.rcParams['axes.labelsize'] = 14
            matplotlib.rcParams['xtick.labelsize'] = 8
            matplotlib.rcParams['ytick.labelsize'] = 12
            matplotlib.rcParams['text.color'] = 'k'
            #visualization

            import pandas as pd 
            import matplotlib.pyplot as plt

            df = pd.read_csv('ufc.csv')
            df.columns

            df1=df[df['Winner']=='Blue']

            df1=df1[(df1['B_age']>x) &( df1['B_age']<y)]
            c=['blueviolet','indigo','mediumorchid','darkorchid','darkviolet','purple',
   'darkmagenta','mediumvioletred','palevioletred','hotpink','deeppink','crimson','red']
            ax=df1.groupby('B_age')['Winner'].count().plot.barh(figsize=(8,8),fontsize=15,color=c)
            ax.set_title('UFC\n\n Age analysis of Blue fighters who have won the fights' ,fontsize=17,fontweight='bold' , color='red')
            ax.set_xlabel('Fight Won' ,fontsize=15,fontweight='bold')
            ax.set_ylabel('Blue Fighters age' ,fontsize=15,fontweight='bold')
            for index, value in enumerate(df1.groupby('B_age')['Winner'].count()):
                plt.text(value, index-0.2, int(value),fontsize=15)
                
            #save the image - same
            buf = io.BytesIO()
            plt.margins(0.8)
            # Tweak spacing to prevent clipping of tick-labels
            plt.subplots_adjust(bottom=0.35)
            plt.savefig(buf, format='png')
        
            fig.savefig('abc.png')
            
            plt.close(fig)
            image = Image.open("abc.png")
            draw = ImageDraw.Draw(image)
            
            image.save(buf, 'PNG')
            content_type="Image/png"
            buffercontent=buf.getvalue()


            graphic = base64.b64encode(buffercontent) 
            return render(request, 'graphic.html', {'graphic': graphic.decode('utf8')})
        else:
            msg='Please Enter correct ranges'
            return render(request,'blueageplayers.html',{'msg':msg})


        #return render(request,'playermatchanalysis.html')
    else:

        return render(request,'blueageplayers.html')

def redageplayers(request):
    if request.method=="POST":
        #imports - same
        x=int(request.POST.get('start_age'))
        y=int(request.POST.get('last_age'))
        if y>x:

            import pandas as pd
            import matplotlib.pyplot as plt
            #std=StandardScaler()
            fig=plt.figure(figsize=(6, 7), dpi=80,facecolor='#f9f9f9', edgecolor='w')
            matplotlib.rcParams['axes.labelsize'] = 14
            matplotlib.rcParams['xtick.labelsize'] = 8
            matplotlib.rcParams['ytick.labelsize'] = 12
            matplotlib.rcParams['text.color'] = 'k'
            #visualization

            import pandas as pd 
            import matplotlib.pyplot as plt

            df = pd.read_csv('ufc.csv')
            df.columns
            df1=df[df['Winner']=='Red']

            df1=df1[(df1['R_age']>x) &( df1['R_age']<y)]
            c=['palevioletred','hotpink','deeppink','crimson','red','darkred','firebrick','maroon','brown']
            ax=df1.groupby('R_age')['Winner'].count().plot.barh(figsize=(10,12),fontsize=15,color=c)
            ax.set_title('UFC\n\n Age analysis of R fighters who have won the fights' ,fontsize=17,fontweight='bold' , color='red')
            ax.set_xlabel('Fight Won' ,fontsize=15,fontweight='bold')
            ax.set_ylabel('Red Fighters age' ,fontsize=15,fontweight='bold')
            for index, value in enumerate(df1.groupby('R_age')['Winner'].count()): 
                plt.text(value, index-0.2, int(value),fontsize=15)    
    
                
            #save the image - same
            buf = io.BytesIO()
            plt.margins(0.8)
            # Tweak spacing to prevent clipping of tick-labels
            plt.subplots_adjust(bottom=0.35)
            plt.savefig(buf, format='png')
        
            fig.savefig('abc.png')
            
            plt.close(fig)
            image = Image.open("abc.png")
            draw = ImageDraw.Draw(image)
            
            image.save(buf, 'PNG')
            content_type="Image/png"
            buffercontent=buf.getvalue()


            graphic = base64.b64encode(buffercontent) 
            return render(request, 'graphic.html', {'graphic': graphic.decode('utf8')})
        else:
            msg='Please Enter correct ranges'
            return render(request,'redageplayers.html',{'msg':msg})

        #return render(request,'playermatchanalysis.html')
    else:

        return render(request,'redageplayers.html')


def titlebout(request):
    if request.method=="POST":
        #imports - same
        x=int(request.POST.get('title'))
        import pandas as pd
        import matplotlib.pyplot as plt
        #std=StandardScaler()
        fig=plt.figure(figsize=(6, 7), dpi=80,facecolor='#f9f9f9', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        #visualization
        df = pd.read_csv('ufc.csv')
        df['year']=pd.DatetimeIndex(df['date']).year
        df=df[df['year']==x]
        ax=df.groupby('title_bout')['title_bout'].count().plot.barh(rot=360,color=('deepskyblue','dodgerblue'),figsize=(10,6))
        ax.set_title('UFC\n\n title bouts fought in '+ str(x),color='red',fontweight='bold',fontsize=15)
        right_side = ax.spines[["right","top"]]
        right_side.set_visible(False)
        for index, value in enumerate(df.groupby('title_bout')['title_bout'].count()): 
            plt.text(value, index-0.2, int(value),fontsize=12) 
        #save the image - same
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        return render(request, 'graphic.html', {'graphic': graphic.decode('utf8')})


        #return render(request,'playermatchanalysis.html')
    else:

        return render(request,'titlebout.html')   

def sendmail(request):
    return render(request,'sendmail.html')

def Stanceanalysis(request):
    if request.method=="POST":
        #imports - same
        x=str(request.POST.get('stance'))
        import pandas as pd
        import matplotlib.pyplot as plt
        #std=StandardScaler()
        fig=plt.figure(figsize=(6, 7), dpi=80,facecolor='#f9f9f9', edgecolor='#f9f9f9')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        #visualization
        df = pd.read_csv('ufc.csv')
       
        df['year']=pd.DatetimeIndex(df['date']).year
        df1=df[df['B_Stance']==x]
        if(len(df1)==0):
            msg="Select correct stance"
            return render(request,'Stanceanalysis.html',{'msg':msg}) 
        df1=df1.groupby('year')['B_Stance'].count()
        ax=df1.plot.line(color='aqua',linewidth=4)
        plt.title('UFC\n\n Stance Analysis- ' +x ,color='red',fontsize=15,fontweight='bold')
        plt.ylabel('no. of fighters')
        plt.xlim(2010,2022)
        #save the image - same
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        return render(request, 'graphic.html', {'graphic': graphic.decode('utf8')})


        #return render(request,'playermatchanalysis.html')
    else:

        return render(request,'Stanceanalysis.html') 

def rstanceanalysis(request):
    if request.method=="POST":
        #imports - same
        x=str(request.POST.get('stance'))
        import pandas as pd
        import matplotlib.pyplot as plt
        #std=StandardScaler()
        fig=plt.figure(figsize=(6, 7), dpi=80,facecolor='#f9f9f9', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        #visualization
        df = pd.read_csv('ufc.csv')
       
        df['year']=pd.DatetimeIndex(df['date']).year
        df1=df[df['R_Stance']==x]
        if(len(df1)==0):
            msg="Select correct stance"
            return render(request,'rstanceanalysis.html',{'msg':msg}) 
        df1=df1.groupby('year')['R_Stance'].count()
        ax=df1.plot.line(color='aqua',linewidth=4)
        plt.title('UFC\n\n Stance Analysis- ' +x ,color='red',fontsize=15,fontweight='bold')
        plt.ylabel('no. of fighters')
        plt.xlim(2010,2022)
        #save the image - same
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        return render(request, 'graphic.html', {'graphic': graphic.decode('utf8')})


        #return render(request,'playermatchanalysis.html')
    else:

        return render(request,'rstanceanalysis.html')           

def weightclass(request):
    if request.method=="POST":
        #imports - same
        x=str(request.POST.get('Division'))
        import pandas as pd
        import matplotlib.pyplot as plt
        #std=StandardScaler()
        fig=plt.figure(figsize=(6, 7), dpi=80,facecolor='#f9f9f9', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        #visualization
        df = pd.read_csv('ufc.csv')
        df['year']=pd.DatetimeIndex(df['date']).year
        
        df1=df[df['weight_class']==x]
        if(len(df1)==0):
            msg="Select correct Player"
            return render(request,'weightclass.html',{'msg':msg}) 
        df1=df1.groupby('year')['weight_class'].count()
        ax=df1.plot.line(color='aqua',linewidth=4)
        ax.margins(x=0)

        plt.title('UFC\n\n weightdivsion Analysis-' +x ,color='red',fontsize=15,fontweight='bold')

        #save the image - same
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        return render(request, 'graphic.html', {'graphic': graphic.decode('utf8')})


        #return render(request,'playermatchanalysis.html')
    else:

        return render(request,'weightclass.html')  

def redmatches(request):
    if request.method=="POST":
        #imports - same
        x=str(request.POST.get('Player'))
        import pandas as pd
        import matplotlib.pyplot as plt
        #std=StandardScaler()
        fig=plt.figure(figsize=(7, 8), dpi=80,facecolor='#f9f9f9', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        #visualization
        df = pd.read_csv('ufc.csv')
        img=plt.imread('imgufc2.jpg')
        df=df[df['R_fighter']==x]
        if(len(df)==0):
            msg="Select correct Player"
            return render(request,'redmatches.html',{'msg':msg}) 

        df1=df[df['Winner']=='Red']
        df1=df1.groupby('Winner')['Winner'].count()
        df1=pd.DataFrame(df1)
        df1.index=['Winning fights']


        df2=df.groupby('R_fighter')['R_fighter'].count()
        df2=pd.DataFrame(df2)
        df2.index=['Total fights']

        plt.title('UFC \n '+x,color='red',fontweight='bold')
        plt.ylabel('No. of Fights')
        plt.bar(df1.index,df1.Winner,label='Winning Fights',alpha=0.7)
        for index, value in enumerate(df1['Winner']): 
            plt.text(index, value, int(value),fontsize=15,color='w') 
        plt.bar(df2.index,df2.R_fighter,label='Total Fights',alpha=0.7)
        for index, value in enumerate(df2['R_fighter']): 
            plt.text(index+1, value, int(value),fontsize=15,color='w')  
        plt.legend()
        plt.imshow(img,extent=[-1,len(df1.index)+1,0,df2['R_fighter'].max()+5],aspect='auto')

        #save the image - same
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        return render(request, 'graphic.html', {'graphic': graphic.decode('utf8')})


        #return render(request,'playermatchanalysis.html')
    else:

        return render(request,'redmatches.html') 


def bluematches(request):
    if request.method=="POST":
        #imports - same
        x=str(request.POST.get('Player'))
        import pandas as pd
        import matplotlib.pyplot as plt
        #std=StandardScaler()
        fig=plt.figure(figsize=(7, 8), dpi=80,facecolor='#f9f9f9', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        #visualization
        df = pd.read_csv('ufc.csv')
        img=plt.imread('imgufc2.jpg')
        df=df[df['B_fighter']==x]
        if(len(df)==0):
            msg="Select correct Player"
            return render(request,'bluematches.html',{'msg':msg}) 

        df1=df[df['Winner']=='Blue']
        df1=df1.groupby('Winner')['Winner'].count()
        df1=pd.DataFrame(df1)
        df1.index=['Winning fights']


        df2=df.groupby('B_fighter')['B_fighter'].count()
        df2=pd.DataFrame(df2)
        df2.index=['Total fights']

        plt.title('UFC \n '+x,color='red',fontweight='bold')
        plt.ylabel('No. of Fights')
        plt.bar(df1.index,df1.Winner,label='Winning Fights',alpha=0.7)
        for index, value in enumerate(df1['Winner']): 
            plt.text(index, value, int(value),fontsize=15,color='w') 
        plt.bar(df2.index,df2.B_fighter,label='Total Fights',alpha=0.7)
        for index, value in enumerate(df2['B_fighter']): 
            plt.text(index+1, value, int(value),fontsize=15,color='w') 
        plt.legend()
        plt.imshow(img,extent=[-1,len(df1.index)+1,0,df2['B_fighter'].max()+5],aspect='auto')
        #save the image - same
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        return render(request, 'graphic.html', {'graphic': graphic.decode('utf8')})


        #return render(request,'playermatchanalysis.html')
    else:

        return render(request,'bluematches.html')


def bluekosub(request):
    if request.method=="POST":
        #imports - same
        x=int(request.POST.get('win'))
        import pandas as pd
        import matplotlib.pyplot as plt
        #std=StandardScaler()
        fig=plt.figure(figsize=(6, 7), dpi=80,facecolor='#f9f9f9', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        #visualization
        df = pd.read_csv('ufc.csv')
        img=plt.imread('imgufc.jpg')
        df['year']=pd.DatetimeIndex(df['date']).year
        df1=df.groupby('year')['B_win_by_KO-TKO','B_win_by_Submission'].sum()
        df1=df1.loc[x,:]
        ax=df1.plot.bar(rot=360,alpha=0.7,figsize=(10,8))
        plt.title('UFC\n\n KO and Submissions-'+str(x),color='red',fontweight='bold',fontsize=15)
        plt.ylabel('no. of macthes', fontsize=10)
        ax.imshow(img,extent=[-1,len(df1.index),0,df1['B_win_by_KO-TKO'].max()+200],aspect='auto')
        for index, value in enumerate(df1.iloc[0:]): 
            plt.text(index, value, int(value),fontsize=15,color='white') 
        #save the image - same
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        return render(request, 'graphic.html', {'graphic': graphic.decode('utf8')})


        #return render(request,'playermatchanalysis.html')
    else:

        return render(request,'bluekosub.html')  


def redkosub(request):
    if request.method=="POST":
        #imports - same
        x=int(request.POST.get('win'))
        import pandas as pd
        import matplotlib.pyplot as plt
        #std=StandardScaler()
        fig=plt.figure(figsize=(6, 7), dpi=80,facecolor='#f9f9f9', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        #visualization
        df = pd.read_csv('ufc.csv')
        img=plt.imread('imgufc.jpg')
        df['year']=pd.DatetimeIndex(df['date']).year
        df1=df.groupby('year')['R_win_by_KO-TKO','R_win_by_Submission'].sum()
        df1=df1.loc[x,:]
        ax=df1.plot.bar(rot=360,color='red',alpha=0.6,figsize=(10,8))
        plt.title('UFC\n\n KO and Submissions-'+str(x),color='red',fontweight='bold',fontsize=15)
        plt.ylabel('no. of macthes', fontsize=10)
        ax.imshow(img,extent=[-1,len(df1.index),0,df1['R_win_by_KO-TKO'].max()+200],aspect='auto')
        for index, value in enumerate(df1.iloc[0:]): 
            plt.text(index, value, int(value),fontsize=15,color='white')         
        #save the image - same
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        return render(request, 'graphic.html', {'graphic': graphic.decode('utf8')})


        #return render(request,'playermatchanalysis.html')
    else:

        return render(request,'redkosub.html')  

def basicinfoanalysis(request):
    if request.method=="POST":
        #imports - same
        x=str(request.POST.get('basicinfo'))
        import pandas as pd
        import matplotlib.pyplot as plt
        #std=StandardScaler()
        fig=plt.figure(figsize=(6, 7), dpi=80,facecolor='#f9f9f9', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        #visualization
        df = pd.read_csv('ufc.csv')
        df['year']=pd.DatetimeIndex(df['date']).year
        df1=df.groupby('year')[x].mean() 
        if(len(df1)==0):
            msg="Select correct name"
            return render(request,'basicinfoanalysis.html',{'msg':msg}) 

        ax=df1.plot.line(color='aqua',linewidth=4,figsize=(6,8))
        plt.title('UFC\n\n ' +x+ ' Analysis\n 2010-2021 ',color='red',fontsize=15,fontweight='bold')
        plt.ylabel(x+ '-mean',fontsize=12) 
        plt.xlim(2010,2022)

        #save the image - same
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
    
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        return render(request, 'graphic.html', {'graphic': graphic.decode('utf8')})


        #return render(request,'playermatchanalysis.html')
    else:

        return render(request,'basicinfoanalysis.html')        

def senti(request):
    if request.method=='POST':
        x=str(request.POST.get('player'))
        api = TwitterClient()
        tweets = api.get_tweets(query = x, count = 1000)
        
        # picking positive tweets from tweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        # percentage of positive tweets
        ppt=100*(len(ptweets)/len(tweets))
        print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
        # picking negative tweets from tweets
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        print(ntweets)
        # percentage of negative tweets
        pnt=100*(len(ntweets)/len(tweets))
        print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))

        neutraltweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
        # percentage of neutral tweets
        print(neutraltweets)
        #pnnt=100*(len(tweets - ntweets - ptweets)/len(tweets))
        pnnt=((len(tweets)-len(ntweets)-len(ptweets))/len(tweets))*100

        #print("Neutral tweets percentage: {} %".format(100*len(tweets - ntweets - ptweets)/len(tweets)))
        print(((len(tweets)-len(ntweets)-len(ptweets))/len(tweets))*100)
     
        
        # printing first 5 positive tweets
        print("\n\nPositive tweets:")
        
        # printing first 5 negative tweets
        print("\n\nNegative tweets:")

        print("\n\nNeutral Tweets:")

        nt=[]
        for tweet in ntweets[:5]:
            nt.append(tweet['text'])
            print(tweet['text'])
        pt=[]
        
        for tweet in ptweets[:5]:
            print(tweet['text'])
            pt.append(tweet['text'])

        nnt=[]
        for tweet in neutraltweets[:5]:
            print(tweet['text'])
            nnt.append(tweet['text'])            
        return render(request,'sentiresult.html',{'ptweets':pt,'ntweets':nt,'neutraltweets':nnt,'ppt':ppt,'pnt':pnt,'pnnt':pnnt})  
    else:
        return render(request,'senti.html')  

def weightcomp(request):
    if request.method=="POST":
        #imports - same
        x=str(request.POST.get('first_player'))
        y=str(request.POST.get('second_player'))
        import pandas as pd
        import matplotlib.pyplot as plt
        #std=StandardScaler()
        fig=plt.figure(figsize=(6, 7), dpi=80,facecolor='#f9f9f9', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        #visualization

        df= pd.read_csv('ufc.csv')
        img=plt.imread('imgufc.jpg')
        df1=df[df['B_fighter']==x]
        df2=df[df['R_fighter']==y]
        df1=df1.iloc[0,:]
        df2=df2.iloc[0,:]
        df1=pd.DataFrame(df1)
        df1=df1.transpose()
        df2=pd.DataFrame(df2)
        df2=df2.transpose()

        plt.bar(df1['B_fighter'],df1['B_Weight_lbs'],alpha=0.7)
        for index, value in enumerate(df1['B_Weight_lbs']):
            plt.text(index, value, int(value),fontsize=12,color='white',fontweight='bold')         
        plt.bar(df2['R_fighter'],df2['R_Weight_lbs'],alpha=0.7)
        for index, value in enumerate(df2['R_Weight_lbs']):
            plt.text(index+1, value, int(value),fontsize=12,color='white',fontweight='bold')          
        plt.title('UFC\n weight comparison of ' +x+ ' and ' +y,color='red',fontweight='bold',fontsize=14)
        plt.ylabel('Weight in lbs')
        plt.xlabel('name of fighters')
        plt.imshow(img,extent=[-1,len(df2.index)+1,0,df2['R_Weight_lbs'].max()+80],aspect='auto') 

 
            
        #save the image - same
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
        plt.tight_layout()
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        return render(request, 'graphic.html', {'graphic': graphic.decode('utf8')})


        #return render(request,'playermatchanalysis.html')
    else:

        return render(request,'weightcomp.html') 

def heightcomp(request):
    if request.method=="POST":
        #imports - same
        x=str(request.POST.get('first_player'))
        y=str(request.POST.get('second_player'))
        import pandas as pd
        import matplotlib.pyplot as plt
        #std=StandardScaler()
        fig=plt.figure(figsize=(6, 7), dpi=80,facecolor='#f9f9f9', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        #visualization

        df = pd.read_csv('ufc.csv')
        img=plt.imread('imgufc.jpg')
        df1=df[df['B_fighter']==x]
        if(len(df1)==0):
            msg="Select correct Player"
            return render(request,'winningcomp.html',{'msg':msg})  
        df2=df[df['R_fighter']==y]
        if(len(df2)==0):
            msg="Select correct Player"
            return render(request,'winningcomp.html',{'msg':msg})  
        df1=df1.iloc[0,:]
        df2=df2.iloc[0,:]
        df1=pd.DataFrame(df1)
        df1=df1.transpose()
        df2=pd.DataFrame(df2)
        df2=df2.transpose()

        plt.bar(df1['B_fighter'],df1['B_Height_cms'],alpha=0.7)
        for index, value in enumerate(df1['B_Height_cms']):
            plt.text(index, value, int(value),fontsize=12,color='white',fontweight='bold') 
        plt.bar(df2['R_fighter'],df2['R_Height_cms'],alpha=0.7)
        for index, value in enumerate(df2['R_Height_cms']): 
            plt.text(index+1, value, int(value),fontsize=12,color='white',fontweight='bold') 
        plt.title('UFC\n Height comparison of '+x+ ' and ' +y,color='red',fontweight='bold',fontsize=15)
        plt.ylabel('Height in cms')
        plt.xlabel('name of fighters')
        plt.imshow(img,extent=[-1,len(df2.index)+1,0,df2['R_Height_cms'].max()+80],aspect='auto') 


            
        #save the image - same
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
        
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        return render(request, 'graphic.html', {'graphic': graphic.decode('utf8')})


        #return render(request,'playermatchanalysis.html')
    else:

        return render(request,'heightcomp.html')            

def winningcomp(request):
    if request.method=="POST":
        #imports - same
        x=str(request.POST.get('first_player'))
        y=str(request.POST.get('second_player'))
        import pandas as pd
        import matplotlib.pyplot as plt
        #std=StandardScaler()
        fig=plt.figure(figsize=(6, 7), dpi=80,facecolor='#f9f9f9', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        #visualization

        df = pd.read_csv('ufc.csv')
        img=plt.imread('imgufc.jpg')
        dff=df
        df=df[df['R_fighter']==x]
        if(len(df)==0):
            msg="Select correct Player"
            return render(request,'winningcomp.html',{'msg':msg})  


        fig=plt.figure(figsize=(12,5) ,facecolor='whitesmoke')
        fig.suptitle('UFC\n\n' , color='red' , fontweight='bold',fontsize=17)

        ax=plt.subplot(1,2,1)
        df1=df[df['Winner']=='Red']
        df1=df1.groupby('Winner')['Winner'].count()
        df1=pd.DataFrame(df1)
        df1.index=['Winning fights']


        df2=df.groupby('R_fighter')['R_fighter'].count()
        df2=pd.DataFrame(df2)
        df2.index=['Total fights']

        plt.title(x,color='red',fontweight='bold')
        
        plt.bar(df1.index,df1.Winner,label='Winning Fights')
        for index, value in enumerate(df1['Winner']):

            plt.text(index, value, int(value),fontsize=15,color='red') 
        plt.bar(df2.index,df2.R_fighter,label='Total Fights')
        for index, value in enumerate(df2['R_fighter']): 
            plt.text(index+1, value, int(value),fontsize=15,color='red')  
       
        plt.legend()
        plt.imshow(img,extent=[-1,len(df2.index)+1,0,df2['R_fighter'].max()+5],aspect='auto')
        ax=plt.subplot(1,2,2)

        # started second 
        df=dff
        df3=df[df['R_fighter']==y]
        if(len(df3)==0):
            msg="Select correct Player"
            return render(request,'winningcomp.html',{'msg':msg})  
        df4=df3[df3['Winner']=='Red']
        df4=df4.groupby('Winner')['Winner'].count()
        df4=pd.DataFrame(df4)
        df4.index=['Winning fights']

        df5=df3.groupby('R_fighter')['R_fighter'].count()
        df5=pd.DataFrame(df5)
        df5.index=['Total fights']

        plt.title(y,color='red',fontweight='bold')
        plt.bar(df4.index,df4.Winner,label='Winning Fights')
        for index, value in enumerate(df4['Winner']):

            plt.text(index, value, int(value),fontsize=15,color='red') 
        plt.bar(df5.index,df5.R_fighter,label='Total Fights')
        for index, value in enumerate(df5['R_fighter']): 
            plt.text(index+1, value, int(value),fontsize=15,color='red')         
        plt.legend()
        plt.imshow(img,extent=[-1,len(df5.index)+1,0,df5['R_fighter'].max()+6],aspect='auto')
            
        #save the image - same
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
        plt.tight_layout()
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        return render(request, 'graphic.html', {'graphic': graphic.decode('utf8')})


        #return render(request,'playermatchanalysis.html')
    else:

        return render(request,'winningcomp.html')  

def Rankings(request):
    import requests

    url = "https://current-ufc-rankings.p.rapidapi.com/"

    headers = {
        "X-RapidAPI-Host": "current-ufc-rankings.p.rapidapi.com",
        "X-RapidAPI-Key": "14bdd6d9e5mshb58dd6abe40afc7p1c89bfjsnd35e996177c5"
    }

    response = requests.request("GET", url, headers=headers)
    import json
    json_data = json.loads(response.text)
    print(response.text)
    k=response.text

    for x in json_data:
        print(x['weightClass'])
        print(x['fighters'])
        print(" ")
        print("----------------------------")
        print("")

    for x in json_data:
    
        print(type(x['fighters']))
        for z in x['fighters']:
            print(z['fighter_ranking'])
            print(z['fullName'])



    lp=[]
    for x in json_data:
        
        print(x['weightClass'])
        l1=x['weightClass']
        if x['weightClass']=="Pound for Pound":
            l2=[]
            
            for z in x['fighters']:
                print(z['fighter_ranking'])
                print(z['fullName'])
                print("************")
            
                l2.append([l1,z['fullName'],z['fighter_ranking']])
                lp.append([z['fullName'],z['fighter_ranking']])
    print(" ")
    print("----------------------------")
    print("")
    print("Flyweight")  
    lf=[]
    for x in json_data:
        
        #print(x['weightClass'])
        l1=x['weightClass']
        if x['weightClass']=="Flyweight":
            print(x['weightClass'])
            l2=[]
            
            for z in x['fighters']:
                print(z['fighter_ranking'])
                print(z['fullName'])
                print("************")
            
                l2.append([l1,z['fullName'],z['fighter_ranking']])
                lf.append([z['fullName'],z['fighter_ranking']])
    print(" ")
    print("----------------------------")
        
    lb=[]
    for x in json_data:
        
        
        l1=x['weightClass']
        if x['weightClass']=="Bantamweight":
            print(x['weightClass'])
            l2=[]
            
            for z in x['fighters']:
                print(z['fighter_ranking'])
                print(z['fullName'])
                print("************")
            
                l2.append([l1,z['fullName'],z['fighter_ranking']])
                lb.append([z['fullName'],z['fighter_ranking']])
    print(" ")
    print("----------------------------------")   

    lfe=[]
    for x in json_data:
        
        
        l1=x['weightClass']
        if x['weightClass']=="Featherweight":
            print(x['weightClass'])
            l2=[]
            
            for z in x['fighters']:
                print(z['fighter_ranking'])
                print(z['fullName'])
                print("************")
            
                l2.append([l1,z['fullName'],z['fighter_ranking']])
                lfe.append([z['fullName'],z['fighter_ranking']])
    print(" ")
    print("----------------------------------")

    ll=[]
    for x in json_data:
        
    
        l1=x['weightClass']
        if x['weightClass']=="Lightweight":
            print(x['weightClass'])
            l2=[]
            
            for z in x['fighters']:
                print(z['fighter_ranking'])
                print(z['fullName'])
                print("************")
            
                l2.append([l1,z['fullName'],z['fighter_ranking']])
                ll.append([z['fullName'],z['fighter_ranking']])
    print(" ")
    print("----------------------------")
            


    lw=[]
    for x in json_data:
        
        
        l1=x['weightClass']
        if x['weightClass']=="Welterweight":
            print(x['weightClass'])
            l2=[]
            
            for z in x['fighters']:
                print(z['fighter_ranking'])
                print(z['fullName'])
                print("************")
            
                l2.append([l1,z['fullName'],z['fighter_ranking']])
                lw.append([z['fullName'],z['fighter_ranking']])
    print(" ")
    print("----------------------------------")  
    
    lm=[]
    for x in json_data:
        
        
        l1=x['weightClass']
        if x['weightClass']=="Middleweight":
            print(x['weightClass'])
            l2=[]
            
            for z in x['fighters']:
                print(z['fighter_ranking'])
                print(z['fullName'])
                print("************")
            
                l2.append([l1,z['fullName'],z['fighter_ranking']])
                lm.append([z['fullName'],z['fighter_ranking']])
    print(" ")
    print("----------------------------------") 

    llh=[]
    for x in json_data:
        
        
        l1=x['weightClass']
        if x['weightClass']=="Light Heavyweight":
            print(x['weightClass'])
            l2=[]
            
            for z in x['fighters']:
                print(z['fighter_ranking'])
                print(z['fullName'])
                print("************")
            
                l2.append([l1,z['fullName'],z['fighter_ranking']])
                llh.append([z['fullName'],z['fighter_ranking']])
    print(" ")
    print("----------------------------------")          
    
    lh=[]
    for x in json_data:
        
        
        l1=x['weightClass']
        if x['weightClass']=="Heavyweight":
            print(x['weightClass'])
            l2=[]
            
            for z in x['fighters']:
                print(z['fighter_ranking'])
                print(z['fullName'])
                print("************")
            
                l2.append([l1,z['fullName'],z['fighter_ranking']])
                lh.append([z['fullName'],z['fighter_ranking']])
    print(" ")
    print("----------------------------")
    
    lwp=[]
    for x in json_data:
        
        
        l1=x['weightClass']
        if x['weightClass']=="Women's Pound for Pound":
            print(x['weightClass'])
            l2=[]
            
            for z in x['fighters']:
                print(z['fighter_ranking'])
                print(z['fullName'])
                print("************")
            
                l2.append([l1,z['fullName'],z['fighter_ranking']])
                lwp.append([z['fullName'],z['fighter_ranking']])
    print(" ")
    print("----------------------------")

    lws=[]
    for x in json_data:
        
        
        l1=x['weightClass']
        if x['weightClass']=="Women's Strawweight":
            print(x['weightClass'])
            l2=[]
            
            for z in x['fighters']:
                print(z['fighter_ranking'])
                print(z['fullName'])
                print("************")
            
                l2.append([l1,z['fullName'],z['fighter_ranking']])
                lws.append([z['fullName'],z['fighter_ranking']])
    print(" ")
    print("----------------------------")

    lwf=[]
    for x in json_data:
        
        
        l1=x['weightClass']
        if x['weightClass']=="Women's Flyweight":
            print(x['weightClass'])
            l2=[]
            
            for z in x['fighters']:
                print(z['fighter_ranking'])
                print(z['fullName'])
                print("************")
            
                l2.append([l1,z['fullName'],z['fighter_ranking']])
                lwf.append([z['fullName'],z['fighter_ranking']])
    print(" ")
    print("----------------------------")

    lwb=[]
    for x in json_data:
        
        
        l1=x['weightClass']
        if x['weightClass']=="Women's Bantamweight":
            print(x['weightClass'])
            l2=[]
            
            for z in x['fighters']:
                print(z['fighter_ranking'])
                print(z['fullName'])
                print("************")
            
                l2.append([l1,z['fullName'],z['fighter_ranking']])
                lwb.append([z['fullName'],z['fighter_ranking']])
    print(" ")
    print("----------------------------")

    return render(request,'Rankings.html',{'lp':lp,'lf':lf,'lb':lb,'lfe':lfe,'ll':ll,'lw':lw,'lm':lm,'llh':llh,
    'lh':lh,'lwp':lwp,'lws':lws,'lwf':lws,'lfb':lwb})  


def countryanalysis(request):
    if request.method=="POST":
        #imports - same
        x=str(request.POST.get('country'))
        
        import pandas as pd
        import matplotlib.pyplot as plt
        #std=StandardScaler()
        fig=plt.figure(figsize=(6, 7), dpi=80,facecolor='#f9f9f9', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        #visualization

        df = pd.read_csv('ufc.csv',parse_dates=['date'])
        img=plt.imread('imgufc2.jpg')
        
        df['year']=pd.DatetimeIndex(df['date']).year
        #df22=df[df["year"]==2019]
        df1=df[df['country']==x]
        df1=df1.groupby('year')['country'].count()
        df1=pd.DataFrame(df1)
      
        ax=df1.plot.bar(rot=360,alpha=0.7,figsize=(9,7),color='royalblue')
        ax.set_title('UFC\n No. of fights in "'+x+ '" over the year',fontsize=15,color='red',fontweight='bold')
        ax.set_ylabel('No. of fights',fontsize=10)
        ax.set_xlabel('Years',fontsize=10)
        for index, value in enumerate(df1['country']):
        #print(index)
        #print(value)
            plt.text(index-0.2, value, int(value),color='white',fontsize=10) 
        ax.imshow(img,extent=[-1,len(df1.index),0,df1['country'].max()+50],aspect='auto')   

 
            
        #save the image - same
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
        plt.tight_layout()
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        return render(request, 'graphic.html', {'graphic': graphic.decode('utf8')})


        #return render(request,'playermatchanalysis.html')
    else:

        return render(request,'countryanalysis.html')
 
def wscomp(request):
    if request.method=="POST":
        #imports - same
        x=str(request.POST.get('first_player'))
        y=str(request.POST.get('second_player'))
        import pandas as pd
        import matplotlib.pyplot as plt
        #std=StandardScaler()
        fig=plt.figure(figsize=(6, 7), dpi=80,facecolor='#f9f9f9', edgecolor='w')
        matplotlib.rcParams['axes.labelsize'] = 14
        matplotlib.rcParams['xtick.labelsize'] = 8
        matplotlib.rcParams['ytick.labelsize'] = 12
        matplotlib.rcParams['text.color'] = 'k'
        #visualization

        import pandas as pd 
        import matplotlib.pyplot as plt
        df = pd.read_csv('ufc.csv')
        #Thiago Santos
        #Karol Rosa


        df1=df[df['R_fighter']==x]
        if(len(df1)==0):
            msg="Select correct Player"
            return render(request,'wscomp.html',{'msg':msg}) 
        df1=df1.iloc[0,:]
        df1=pd.DataFrame(df1)
        df1=df1.transpose()
        df1=df1.set_index('R_fighter')

        df3=df[df['B_fighter']==y]
        if(len(df3)==0):
            msg="Select correct Player"
            return render(request,'wscomp.html',{'msg':msg}) 
        df3=df3.iloc[0,:]
        df3=pd.DataFrame(df3)
        df3=df3.transpose()
        df3=df3.set_index('B_fighter')

        ##ew
        fig=plt.figure(figsize=(9,5),facecolor='#f9f9f9')

        #make two rows and three columns for subplots
        plt.subplot(3,3,1)
        az=df1.loc[:,'R_current_lose_streak'].plot.bar(rot=360,color='red')
        az.set_title('R_current_lose_streak',fontweight='bold')
        az.set_facecolor('bisque')

        plt.subplot(3,3,2)
        az=df1.loc[:,'R_current_win_streak'].plot.bar(rot=360,color='red')
        az.set_title('R_current_win_streak',fontweight='bold')
        az.set_facecolor('bisque')

        plt.subplot(3,3,3)
        az=df1.loc[:,'R_longest_win_streak'].plot.bar(rot=360,color='red')
        az.set_title('R_longest_win_streak',fontweight='bold')
        az.set_facecolor('bisque')
        

        plt.subplot(3,3,7)
        az=df3.loc[:,'B_current_lose_streak'].plot.bar(rot=360,color='blue')
        az.set_title('B_current_lose_streak',fontweight='bold')
        az.set_facecolor('bisque')

        plt.subplot(3,3,8)
        az=df3.loc[:,'B_current_win_streak'].plot.bar(rot=360,color='blue')
        az.set_title('B_current_win_streak',fontweight='bold')
        az.set_facecolor('bisque')

        plt.subplot(3,3,9)
        az=df3.loc[:,'B_longest_win_streak'].plot.bar(rot=360,color='blue')
        az.set_title('B_longest_win_streak',fontweight='bold')
        az.set_facecolor('bisque')
        

 
            
        #save the image - same
        buf = io.BytesIO()
        plt.margins(0.8)
        # Tweak spacing to prevent clipping of tick-labels
        plt.subplots_adjust(bottom=0.35)
        plt.savefig(buf, format='png')
        plt.tight_layout()
        fig.savefig('abc.png')
        
        plt.close(fig)
        image = Image.open("abc.png")
        draw = ImageDraw.Draw(image)
        
        image.save(buf, 'PNG')
        content_type="Image/png"
        buffercontent=buf.getvalue()


        graphic = base64.b64encode(buffercontent) 
        return render(request, 'graphic.html', {'graphic': graphic.decode('utf8')})


        #return render(request,'playermatchanalysis.html')
    else:

        return render(request,'wscomp.html') 
      