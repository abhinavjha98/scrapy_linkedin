import scrapy
import urllib
import requests
from scrapy import Request
from scrapy.http import FormRequest


class LinkedinSpider(scrapy.Spider):

	name = "linkedin"
	allowed_domains = ["linkedin.com"]
	user_name = 'ajaytest281298@gmail.com'
	passwd = '@jayTest@113'

# Uncomment the following lines for full spidering
# start_urls = ["http://www.linkedin.com/directory/people-%s-%d-%d-%d"
#               % (alphanum, num_one, num_two, num_three)
#                 for alphanum in "abcdefghijklmnopqrstuvwxyz"
#                 for num_one in xrange(1,11)
#                 for num_two in xrange(1,11)
#                 for num_three in xrange(1,11)
#               ]

# Temporary start_urls for testing; remove and use the above start_urls in production
# start_urls = ["http://www.linkedin.com/directory/people-a-23-23-2"]
	start_urls = ["https://www.linkedin.com/in/rebecca-liu-93a12a28/"]
	login_page = 'https://www.linkedin.com/uas/login'
# TODO: allow /in/name urls too?
# rules = (
#     Rule(SgmlLinkExtractor(allow=('\/pub\/.+')),
#          callback='parse_item'),
# )

	def init_request(self):
		return Request(url=self.login_page,callback=self.login)

	def login(self,response):
		return FormRequest.from_response(response,formdata={
	    'session_key':user_name,'session_password':passwd
	},
	                                 callback = self.check_login_response)

	def check_login_response(self,response):
		return self.initialized()