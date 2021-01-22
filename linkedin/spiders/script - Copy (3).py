import scrapy
import urllib
import requests
from scrapy import Request
from scrapy.http import FormRequest

class DmozItem(scrapy.Item):
	Company = scrapy.Field()
	Location = scrapy.Field()
	Title = scrapy.Field()
	Description = scrapy.Field()
	Logo = scrapy.Field()
	Seniority_level = scrapy.Field()
	Job_Function = scrapy.Field()
	Employment_Type = scrapy.Field()
	Industries = scrapy.Field()
	# Merges = scrapy.Field()
	ApplyLink = scrapy.Field()

class Linked(scrapy.Spider):
    name = "linkedUS"
    page_numbers = 1
    start_urls = (
        'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin',
    )
    handle_httpstatus_list = [303,999]
    BASE_URL = 'https://www.linkedin.com/'
    USER_AGENT='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    headers = {'User-Agent': USER_AGENT}

    def parse(self,response):
    	token = response.css('form input::attr(value)').extract_first()
    	return FormRequest.from_response(response,formdata={
    		'csrf_token':token,
    		'username': 'ajaytest281298@gmail.com',
    		'password' : '@jayTest@113'
    		},callback = self.start_scraping)

    def start_scraping (self,response):
    	
    	lin = [
    	"https://www.linkedin.com/jobs/search?keywords=Java%20Remote&location=United%20States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0"]
  #   	nextpagelink = section.find('a', {'data-tracking-control-name': 'guest_job_search_create-job-alert-bottom-of-results'}
		# nextpageurl = nextpagelink.get('href')
    	for i in lin:
    		return Request(url=i, callback=self.parse_memb)

    def parse_memb(self,response):
    	
    	links = response.css('a.result-card__full-card-link').xpath("@href").extract()
    	for link in links:
    		yield scrapy.Request(link, callback=self.parse_members)
    	next_page = "https://www.linkedin.com/jobs/search?keywords=Java%20Remote&location=United%20States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum="+str(Linked.page_numbers)
    	print("Hello"+str(Linked.page_numbers))
    	if Linked.page_numbers<=5000:
    		Linked.page_numbers +=1
    		yield response.follow(next_page,callback=self.parse_memb)
    	print("Hello"+str(Linked.page_numbers))

    def parse_members(self,response):
    	item = DmozItem()
    	# # links = response.css('div a.job-card-list__title').xpath("@href").extract()
    	# links = response.css('a')
    	# item["ApplyLink"] = links
    	# return item
    	title = response.css('h1.topcard__title::text').extract()
    	logo = response.css('img.artdeco-entity-image').xpath("@data-delayed-url").extract()
    	Company = response.css('a.sub-nav-cta__optional-url::text').extract()
    	City = response.css('span.sub-nav-cta__meta-text::text').extract()
    	ss =response.css('span.job-criteria__text--criteria::text').extract()
    	ar = response.css('a.apply-button').xpath("@href").extract()
    	# sp = response.css('div::text').extract()
    	sp = response.xpath("//div/descendant::text()").extract()
    	text_list = ""
    	for text in sp:
    		text_list=text_list+" "+text
    	text_list = text_list.replace("Sign in",'')
    	text_list = text_list.replace("for the full experience Sign in Join now",'')
    	text_list = text_list.replace("Click the link in the email we",'')
    	text_list = text_list.replace("Boisar Jobs People Learning Join now",'')
    	text_list = text_list.replace("Password Show Forgot password? Sign in Save time",'')
    	text_list = text_list.replace("Sign in",'')
    	# sp = response.css('p::text').extract()
    	# sp += response.css('li::text').extract()
    	if not ar:
    		final_url = response.url
    		item["ApplyLink"] = final_url
    	else:
    		final_url = requests.get(ar[0])
    		item["ApplyLink"] = final_url.url
    	
    	item["Title"] = title
    	item["Logo"] = logo[0]
    	item["Company"] = Company
    	item["Location"] = City
    	item["Description"] = text_list
    	# item["Skill"] = final_url.url
    	if ss[0] =="Not Applicable":
    		item["Seniority_level"] = ""
    	else:
    		item["Seniority_level"] = ss[0]
    	item["Employment_Type"] = ss[1]
    	item["Industries"] = ss[2]
    	item["Job_Function"] = ss[3]
    	return item
    	# print(response.url)