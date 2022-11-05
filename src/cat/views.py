from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch


from . import models
from . import serializers
from .permissions import IsInventoryCatUser
from ..base.classes import MixedSerializer


class ProductView(ListAPIView):
    queryset = models.Product.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ShopProductSerializer


class InventoryView(MixedSerializer, ModelViewSet):
    lookup_field = 'id'
    queryset = models.Inventory.objects.all()
    permission_classes = [IsInventoryCatUser]
    serializer_classes_by_action = {
        'create': serializers.CreateItemSerializer,
        'list': serializers.CatInventorySerializer,
        'update': serializers.UpdateInventoryItemSerializer
    }

    def get_queryset(self):
        item_qt = models.Item.objects.select_related('product', 'product__category')
        queryset = models.Inventory.objects.prefetch_related(
            Prefetch('item', queryset=item_qt)
        ).filter(id=self.kwargs['id'])
        return queryset


class HintView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.HintSerializer


class PhraseView(ListAPIView):
    queryset = models.Phrase.objects.all()
    serializer_class = serializers.PhraseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ["name", ]


class CatView(ModelViewSet):
    queryset = models.Cat.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.GetCatSerializer
