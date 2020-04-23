from django.shortcuts import render
from django.http import JsonResponse
from .models import CustomUser
from rest_framework import viewsets
from .serializers import UserSerializer, ConvSerializer
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json
from django.core import serializers
from django.http import HttpResponse
from django.views.generic import ListView
from django.views import View
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.conf import settings
import requests
from django.core.cache import cache
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
import threading
from django.contrib.staticfiles.templatetags.staticfiles import static
# @csrf_exempt
# class UserViewSet(DetailView):
#     # queryset = CustomUser.objects.all()
#     # serializer_class = UserSerializer

#     def post(self, request,*args, **kwargs):
#         data = request.POST
#         print(data)
list_countrydetl = []
flag = True
@method_decorator(csrf_exempt, name='dispatch')
class Webhook(View):

    global list_countrydetl
    def post(self, request):
        
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if body:
            print(body)
            #saveConv(body)
            getCoviddetails(request)             
            try:
                if body['queryResult']['action'] == "userdetl":
                    if body['queryResult']['parameters']['email'] and \
                    body['queryResult']['parameters']['phone_num'] and \
                    body['queryResult']['parameters']['zip_code']:
                        emailAddress = body['queryResult']['parameters']['email']
                        phone_num = body['queryResult']['parameters']['phone_num']
                        pincode = body['queryResult']['parameters']['zip_code']
                        user_data = UserSerializer(data={'emailAddress' : emailAddress,\
                        'phone_num' : phone_num,\
                        'pincode' : pincode})
                        if user_data.is_valid():
                           user_data.save()
                           print("Userdata Saved")  
                        mail_send(emailAddress)
                        # print("--- %s seconds ---" % (time.time() - start_time))
                        # time.sleep(5)
                        # response = {
                  
                        # "fulfillmentMessages": [
                          
                        #   {
                        #     "text": {
                        #     "text": [         
                        #       """Thank you For the Information. we have sent you a mail.
                        #       Do you have any further queries?"""
                        #     ]
                        #     }
                        #   }
                        #   ]}
                        
                        # return JsonResponse(response, content_type='application/json')
            except:
                  pass  
    
@csrf_exempt
def getCoviddetails(request):

    import pandas as pd
    global list_countrydetl
    coviddata = getCovidData()
    countrywise_count = cache.get('countrywise_count')
    if not countrywise_count:
        list_countrydetl = []
        countrywise_count = {}
        confirmed = 0
        deaths = 0
        recovered = 0
          
        for i in coviddata['data']['covid19Stats']:
            if i['country'] is not None and i['country'] in countrywise_count:
                if i['confirmed'] is not None:
                    countrywise_count[i['country']]['confirmed'] = countrywise_count[i['country']]['confirmed'] + i['confirmed']
                if i['deaths'] is not None:
                    countrywise_count[i['country']]['deaths'] = countrywise_count[i['country']]['deaths'] + i['deaths']
                if i['recovered'] is not None:
                    countrywise_count[i['country']]['recovered'] = countrywise_count[i['country']]['recovered'] + i['recovered']
            else:
                if i['country'] is not None:
                    if i['confirmed'] is None:
                        i['confirmed'] = 0
                    if i['deaths'] is None:
                        i['deaths'] = 0
                    if  i["recovered"] is None:
                        i["recovered"] = 0
                    countrywise_count[i['country']] = {
                        "confirmed": i['confirmed'],
                        "deaths": i['deaths'],
                        "recovered": i["recovered"]
                        }
        cache.set('countrywise_count', countrywise_count, 4 * 60 * 60)
    for i,j in countrywise_count.items():
        list_countrydetl.append([i,j['confirmed'], j['deaths'], j['recovered']])

    response = list_countrydetl

    

    if request.method == "GET":
        return JsonResponse(response, content_type='application/json', safe = False)
    else:    
        return response


 



def getCovidData():
  #https://stackoverflow.com/questions/9990347/django-json-strategy
    coviddata = cache.get('covidcachedata')
    if not coviddata:
        coviddata = requests.get(settings.COVID19API, \
                            headers={"x-rapidapi-host": settings.COVIDAPIHOST,\
                                    "x-rapidapi-key": settings.COVID19APIKEY}).json()

        cache.set('covidcachedata', coviddata, 4 * 60 * 60)
    return coviddata


def saveConv(data):
  
  if data is not None:
    json_data = {"session": data['session'],
                "userconv": data['queryResult']['queryText'],
                "botconv": data['queryResult']['fulfillmentText']}
    serializer = ConvSerializer(data=json_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    

def mail_send(to):
    global list_countrydetl
    subject = 'Test Mail'
    text_content = "Test Message"
    html_message = html_generator(list_countrydetl)
    #print(html_message)
    from_whom = settings.EMAIL_HOST_USER
    message = EmailMultiAlternatives(subject, text_content, from_whom, [to])
    message.attach_alternative(html_message, "text/html")
    message.send()
    print("i am done")


def html_generator(listdata):

  msg_body = cache.get('msg_body') 
  if not msg_body:
    with open('E:\\MEAN_STACK\\Django-Workspace\\backend\\covid19dashboard\\covid19dashboardapi\\templates\\covid19details.html', 'r') as myfile:
      covidrecom = myfile.read()
    # with open(static('covid19details.html'), 'r') as myfile:
    #   covidrecom = myfile.read()

    tbl_cntent = ""
    for i in listdata:
        tbl_cntent += """<tr>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        </tr>""".format(str(i[0]),str(i[1]),str(i[2]),str(i[3]))
    
    msg_body = """<!DOCTYPE html>
      <html>
      <head>
      <style>
      table {{
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
      }}

      td, th {{
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
      }}

      tr:nth-child(even) {{
        background-color: #dddddd;
      }}
      h2{{
        background-color: #223279;
        color: white;
        text-align: center;
      }}
      
      </style>
      </head>
      
      <body style="width: 800px;">
    
    Hi,<br>
        Hope you are doing well. Please find the detailed report below.<br> 
        <b>STAY HOME, STAY SAFE<b><br>   
      
    <div style="height: 600px; width: 800px; overflow: auto">
    <h2>COVID19 WORLD REPORT</h2>
      <table>
      <thead>
        <tr>
          <th>Country</th>
          <th>Confirmed</th>
          <th>Deaths</th>
          <th>Recovered</th>
        </tr></thead><tbody>{}</tbody></table></div><br>
        <br>
        <br/>
        <br/>
        {}
        </body>
      </html>""".format(tbl_cntent, str(covidrecom))
    cache.set('msg_body', msg_body, 4 * 60 * 60)
  #print(msg_body)
  return msg_body

