# myapp/views.py
from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from langchain import OpenAI
from langchain.prompts import PromptTemplate
import time
from .models import EntitiesMaster
from WAIB3_project.settings import *


"""API for save entity"""
def save_entity(request):
    url = request.GET.get('url')
    if not url:
        return JsonResponse({'error': 'URL parameter is required'}, status=400)

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
  
    driver = None

    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(3)

        artist_name = driver.find_element(By.CSS_SELECTOR, '.cell .subhead4').text
        program_name = driver.find_element(By.CSS_SELECTOR, '.text-left .subhead4').text
        artist_role = driver.find_element(By.CSS_SELECTOR, '.subhead6').text
        date = driver.find_element(By.CSS_SELECTOR, '.body-text3').text
        time_ = driver.find_element(By.CSS_SELECTOR, '.body-text3').text
        auditorium = driver.find_element(By.CSS_SELECTOR, '.content .location').text

        entity = EntitiesMaster(
            artist_name=artist_name,
            program_name=program_name,
            artist_role=artist_role,
            date=date,
            time=time_,
            auditorium=auditorium,
            url=url
        )
        entity.save()

        template = PromptTemplate(
            input_variables=["artist_name", "program_name", "artist_role", "date", "time", "auditorium"],
            template="""
            Artist Name: {artist_name}
            Program Name: {program_name}
            Artist Role: {artist_role}
            Date: {date}
            Time: {time}
            Auditorium: {auditorium}
            """,
        )

        llm = OpenAI(api_key=OPENAI_KEY)  

        processed_data = llm(template.format(
            artist_name=artist_name,
            program_name=program_name,
            artist_role=artist_role,
            date=date,
            time=time_,
            auditorium=auditorium,
            url=url
        ))

        return JsonResponse({'data': processed_data}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    finally:
        if driver:
            driver.quit()


"""API for """
def get_entity(request):
    url = request.GET.get('url')
    if not url:
        return JsonResponse({'error': 'URL parameter is required'}, status=400)

    try:
        entities = EntitiesMaster.objects.filter(url=url).values(
            'artist_name', 'program_name', 'artist_role', 'date', 'time', 'auditorium'
        )
        if not entities:
            return JsonResponse({'error': 'No entities found for the provided URL'}, status=404)

        return JsonResponse({'entities': list(entities)}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)