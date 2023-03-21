from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import TemplateView
from django.conf import settings
from .models import *

from django.views.generic import ListView
from rest_framework import generics

from .serializers import ItemByuSerializer

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class ItemBuyAPIView(generics.ListAPIView):
    serializer_class = ItemByuSerializer

    def get_queryset(self):
        return Item.objects.filter(pk=self.kwargs['pr_k'])

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        item = Item.objects.get(pk=self.kwargs['pr_k'])
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(item.price),
                        'product_data': {
                            'name': item.name
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


class SuccessView(TemplateView):
    template_name = "stripeapp/success.html"


class CancelView(TemplateView):
    template_name = "stripeapp/cancel.html"


class MainPage(ListView):
    model = Item
    template_name = 'stripeapp/index.html'
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Main page'
        return context


class ShowItem(ListView):
    model = Item
    template_name = 'stripeapp/item.html'
    context_object_name = 'item'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Item description'
        context['STRIPE_PUBLIC_KEY'] = settings.STRIPE_PUBLIC_KEY
        return context

    def get_queryset(self):
        return Item.objects.get(pk=self.kwargs['item_id'])
