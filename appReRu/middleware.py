from django.contrib.gis.geoip2 import GeoIP2
from django.conf import settings  # Import Django settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Visitor, VisitorMetadata
from django.utils.deprecation import MiddlewareMixin
from geoip2.errors import AddressNotFoundError
from user_agents import parse

class VisitorMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent_string = request.META.get('HTTP_USER_AGENT')
        
        # Parse user agent string
        user_agent = parse(user_agent_string)

        # Create a GeoIP object
        geoip = GeoIP2(path=settings.GEOIP_PATH)

        try:
            # Get geolocation information based on the IP address
            geolocation_data = geoip.city(ip_address)
        except AddressNotFoundError:
            # Handle the case where the IP address is not found in the database
            geolocation_data = {'country_code': 'NA', 'city': 'Unknown'}

        # Filter Visitor objects by IP address
        visitors = Visitor.objects.filter(ip_address=ip_address)

        if visitors.exists():
            # If Visitor objects with the same IP address exist, use the first one
            visitor = visitors.first()
        else:
            # Create a new Visitor object with IP address
            visitor = Visitor.objects.create(ip_address=ip_address)

        # Create VisitorMetadata object with extracted metadata
        visitor_metadata = VisitorMetadata.objects.create(
            visitor=visitor,
            user_agent=user_agent_string,
            referer=request.META.get('HTTP_REFERER'),
            language=request.META.get('HTTP_ACCEPT_LANGUAGE'),
            screen_resolution=request.META.get('HTTP_SCREEN_RESOLUTION'),
            browser=user_agent.browser.family,
            operating_system=user_agent.os.family,
            device_type=user_agent.device.family,
            timezone=request.META.get('HTTP_TIMEZONE'),
            country=geolocation_data.get('country_code'),
            city=geolocation_data.get('city'),
            latitude=geolocation_data.get('latitude'),
            longitude=geolocation_data.get('longitude')
        )

        # Attach the visitor and metadata objects to the request for later use
        request.visitor = visitor
        request.visitor_metadata = visitor_metadata




class HandleExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response


    #def process_exception(self, request, exception):
        # If any exception occurs, redirect to the error view
        #return HttpResponseRedirect(reverse('error'))

