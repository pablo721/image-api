from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.core import signing
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import api_view
from .serializers import ImageSerializer
from .models import Image



class LoginView(TemplateView):
    template_name = 'uploadapi/login.html'
    form = AuthenticationForm

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            request.session.set_expiry(87600)
            login(request, user)
            return redirect('uploadapi:images-list')
        return render(request, 'uploadapi/login_failed.html')


    def get_context_data(self, **kwargs):
        return {'form': self.form}



def generate_temp_url(duration, data=None):
    url = reverse('uploadapi:temp', args=[signing.dumps(data)])
    return settings.BASE_URL + url + f'?duration={duration}'


@api_view(['GET'])
def links(request, pk):
    if not request.user.user_account.account_tier.has_expiring_links:
        raise Http404
    duration = int(request.GET['duration']) if 'duration' in str(request.GET) else 300  # default duration set to 300 seconds, can be changed by adding ?duration=new_value to the url 
    
    if duration < 300 or duration > 30000:
        return Response("Invalid expiration time. Please select a number between 300 and 30000.")
    
    obj = Image.objects.get(pk=pk)
    if obj.account != request.user.user_account:
        raise Http404
    obj_url = settings.BASE_URL + obj.binary.url

    return Response({f'link (expires after {duration} seconds)': generate_temp_url(duration, obj_url)})



def temp(request, signed_data):
    duration = int(request.GET['duration'])
    try:
        data = signing.loads(signed_data, max_age=duration)
    except signing.BadSignature:
        raise Http404
    return HttpResponse(f'<img src="{data}">')



class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        return Image.objects.filter(account=self.request.user.user_account)


