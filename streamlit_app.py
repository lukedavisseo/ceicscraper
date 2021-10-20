import requests
from requests.exceptions import Timeout, SSLError, MissingSchema
import streamlit as st
from scraper_api import ScraperAPIClient
import pandas as pd
import json
import tldextract

api_key = st.text_input("Enter ScraperAPI key")

# ScraperAPI auth

client = ScraperAPIClient(api_key)

# SERP data to put into a DataFrame

serp = {
	'urls': [],
	'titles': [],
	'meta_desc': [],
	'competitor': []
}

# List of competitors

competitor_urls = ["tradingeconomics.com", "theglobaleconomy.com", "countryeconomy.com", "focus-economics.com", "worldbank.org", "knoema.com"]

# Area to enter data

st.title("CEIC Scraper")

multi_kw = st.text_area('Enter keywords, 1 per line').lower()

lines = multi_kw.split("\n")
keywords = [line for line in lines]

submit = st.button('Submit')

# Code to execute when submit button is pressed

if submit:

	msg = st.markdown('Processing, please wait...')

	for k in keywords:
		
		st.header(f'{k}')

		google_search_url = 'http://www.google.com/search?q=' + k.replace(' ', '+')

		st.write(google_search_url)

		payload = {'api_key': api_key, 'url': google_search_url, 'autoparse': 'true'}
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
		proxy_url = requests.get('http://api.scraperapi.com/?', payload, headers=headers)

		try:
			response = proxy_url.json()
			org = response.get("organic_results")

		except (ValueError):
			st.error(f"Error found! Continuing...")
			continue

		for results in range(0,len(org)):
			link = (org[results]['link'])
			ext = tldextract.extract(link)
			if ext.registered_domain in competitor_urls:
				serp['urls'].append(link)
				serp['titles'].append(org[results]['title'])
				serp['meta_desc'].append(org[results]['snippet'])
				serp['competitor'].append("Competitor match found")
				st.write(f'Competitor match found: {ext.registered_domain}')
			else:
				st.write("No competitors found")

	msg = st.markdown('Completed!')
