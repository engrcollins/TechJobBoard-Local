import requests
import time
import re
import os
import json
import html
import datefinder
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from .models import ITjob
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from techjobserver.serializers import JobscraperSerializer
from rest_framework.decorators import api_view

def scrape(request):
#def scrape():
  p_start = 309518
  p_end = 309532
  session = requests.Session()
  session.max_redirects = 3
  session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
  base_url = "https://www.hotnigerianjobs.com/hotjobs/"

  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  sample_url= os.path.join(BASE_DIR, 'techjobserver/sample')

  for page in range(0, 2):
        """
        present_url = base_url + str(page)
        print('\n scraping ' + present_url +'\n')
        time.sleep(20)
        page_req = session.get(present_url, verify=False)
        job_status = page_req.status_code
        print(job_status)
        content = page_req.content
        soup = BSoup(content, "html.parser")
        """
        i = 1
        soup = BSoup(open(sample_url + str(page) +'.html'))
        Jobs = soup.find('div', {"class":"middlecol"})
        job_case = Jobs.find_all('div', {'class':'mycase'})[0]
        job_title = job_case.find('span', {'class':'jobheader'})
        desc = job_case.find('div', {'class':'mycase4'})
        desc = desc.find_all('div')[1]
        job_description = desc.find_all('div')
        job_intro = desc.find_all('p')[0]
        job_link = job_title.find('a')
        job_link = job_link['href']
        post_date = job_case.find('span', {'class':'semibio'})
        matches = datefinder.find_dates(post_date.text)
        for match in matches:
            post_date = match.strftime("%A %b %d, %Y")
            print(post_date)
        try:
            raw_title = job_title.text.lower()
        except AttributeError:
            continue
        print(raw_title)

        title_list = ("Backend Developer", "Backend Engineer", "Business Analyst", "Business Intelligence Analyst", 
        "Chief Information Officer", "CIO", "Cloud Architect", "Cloud Engineer", "Computer Analyst", "Computer Engineer", 
        "Cyber Security Analyst", "Data Analyst", "Data Architect", "Data Entry", "Data Scientist", "Data Engineer", "Network Administrator", 
        "Database Administrator", "DevOps", "DevOps Engineer", "Engineer", "Frontend Developer", "Frontend Engineer", 
        "Fullstack Developer", "Fullstack Engineer", "Graphics Designer", "Hardware", "Information Security Analyst", 
        "Information Security Consultant", "IT Director", "IT Manager", "IT Technician", "Mobile Developer", 
        "Mobile App Developer", "Network Engineer", "Network Manager", "Network Technician", "Product Manager", "Programmer", "Project Manager",
        "Quality Assurance Tester", "QA Analyst", " Quality Assurance Engineer", "React Developer", "Sales Engineer", 
        "Salesforce Administrator", "Site Reliability Engineer", "Software Quality Assurance Analyst", "Software Developers", 
        "Software Engineer", "Software Support", "Software Tester", "System Administrator", "Systems Analyst", 
        "Systems Engineer", "Technical Designer", "Technical Engineer", "Technical Lead", "Technical Product Manager", 
        "Technical Project Manager", "Technical Sales", "Technical Support", "UI/UX", 
        "UI/UX Designer")
        raw_list = (x.lower() for x in title_list)
        
        if any(word in raw_title for word in raw_list):
            print('\n scraping ' + job_link +'\n')
            #for child in soup.recursiveChildGenerator():
            job_description = str(job_description)
            job_description = html.escape(job_description)
            job_load = {"job_title": job_title.text, 
                    "job_description": job_description,
                    "job_intro": job_intro.text, 
                    "job_date": post_date, 
                    "job_link": job_link }
            jobscraper_serializer = JobscraperSerializer(data=job_load)
            if jobscraper_serializer.is_valid():
                jobscraper_serializer.save()
                i += 1
                if i == 2:
                    jobscraper = ITjob.objects.all()
                    job_title = request.GET.get('job_title', None)
                    if job_title is not None:
                        jobscraper = jobscraper.filter(job_title__icontains=job_title)
                    jobscraper_serializer = JobscraperSerializer(jobscraper, many=True)
                    return JsonResponse(jobscraper_serializer.data, safe=False, status=status.HTTP_201_CREATED) 
            else:
                print(jobscraper_serializer.errors)
                #return JsonResponse(jobscraper_serializer.errors, status=status.HTTP_400_BAD_REQUEST))

    # find all jobs
@api_view(['GET'])
def job_list(request):
    if request.method == 'GET':
        jobscraper = ITjob.objects.all()
        job_title = request.GET.get('job_title', None)
        if job_title is not None:
            jobscraper = jobscraper.filter(job_title__icontains=job_title)
        jobscraper_serializer = JobscraperSerializer(jobscraper, many=True)
        #print(jobscraper_serializer.data)
        return JsonResponse(jobscraper_serializer.data, safe=False, status=status.HTTP_201_CREATED)

    # find job by pk (id)
def job_detail(request, pk):
    print(pk)
    try: 
        jobscraper = ITjob.objects.get(pk=pk)
        #print(newData)
        job_load = {"job_title": jobscraper.job_title, 
                    "job_description": html.unescape(jobscraper.job_description),
                    "job_intro": jobscraper.job_intro, 
                    "job_date": jobscraper.job_date, 
                    "job_link": jobscraper.job_link
                    }
    except ITjob.DoesNotExist: 
        return JsonResponse({'message': 'The page does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    # GET / PUT / DELETE jobscraper

    #Retrieve a single object
    if request.method == 'GET': 
        jobscraper_serializer = JobscraperSerializer(job_load)

        return JsonResponse(jobscraper_serializer.data)
    """    
    if request.method == 'GET':
        tutorials = Tutorial.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
    
             for child in job_description:
                child = str(child)
                child = html.escape(child)
                print("\n" +child +"\n") 
                dict_load = {"job_title": job_title.text, 
                    "job_description": child, 
                    "job_date": post_date.text, 
                    "job_link": job_link }
                print(dict_load)
                jobscraper_serializer = JobscraperSerializer(data=dict_load)
                if jobscraper_serializer.is_valid():
                    jobscraper_serializer.save()
                    pass
                    #return JsonResponse(jobscraper_serializer.data, status=status.HTTP_201_CREATED) 
                else:
                    print(jobscraper_serializer.errors)
                    #return JsonResponse(jobscraper_serializer.errors, status=status.HTTP_400_BAD_REQUEST))
        else:
            print('This is not an IT job')
    """