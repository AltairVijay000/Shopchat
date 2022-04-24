from rest_framework.serializers import ModelSerializer
from base.models import Offer


class OfferSerializer(ModelSerializer):
    class Meta:
        model= Offer
        fields='__all__'
