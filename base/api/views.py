from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Offer
from .serializers import OfferSerializer
from base.api import serializers

@api_view(['GET','PUT', 'POST'])
def getRoutes(request):
    routes=[
        'GET/api',
        'GET/api/offers',
        'GET/api/offers/:id'
    ]
    return Response(routes)
@api_view(['GET'])
def getOffers(request):
    offers= Offer.objects.all()
    serializer=OfferSerializer(offers, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getOffer(request,pk):
    offer= Offer.objects.get(id=pk)
    serializer=OfferSerializer(offer, many=False)
    return Response(serializer.data)