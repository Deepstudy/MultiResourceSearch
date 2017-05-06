import json
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.resources import Resource
from tastypie.http import HttpCreated

class My_Resources(Resource):
	class Meta:
		resource_name = 'search'
		allowed_methods = ['get']
		
		#Method of the Resource Class. .. method:: Resource.obj_get_list(self, bundle, **kwargs)

	def obj_get_list(self, bundle, **kwargs):
		query = bundle.request.GET.get('q')
		if not query:
			response = {'status': 0, 'message': 'Empty query'}
		else:
			#from my_task.tasks import google, duck_duck_go, twitter
			from my_task.tasks import google, duck_duck_go, twitter

			# Async process    
			from celery.result import ResultSet

			#A collection of results.
			rs = ResultSet([])

			# Add AsyncResult as a new member of the set.

			rs.add(google.delay(query))
			rs.add(duck_duck_go.delay(query))
			rs.add(twitter.delay(query))
			response = rs.get()  # waiting for the results
			url = "http://127.0.0.1:8000/my_resources/v1/search/?q={query}".format(query=query)
			try:
				response = {'query': query, 'results': {'google': {'text': response[0], 'url': url},
					    'duckduckgo': {'text': response[1], 'url': url},'twitter': {'text': response[2], 'url': url}}}
			except AttributeError:
				response = {'status': 0, 'message': 'Result Timeout'}            


		# For immediate response
		raise ImmediateHttpResponse(response=HttpCreated(content=json.dumps(response), content_type='application/json; charset=UTF-8'))
