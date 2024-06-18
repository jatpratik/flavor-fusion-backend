import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from .models import Recipe
from .serializers import RecipeSerializer

# Create your views here.
class RecipeViewSet(APIView):

        def get(self, request, format=None):
            print("hello", request)
            data =  Recipe.objects.all()
            print("data",data)
            recipe = RecipeSerializer(data, many=True)
            # json_data = json.dumps(list(data))
            return JsonResponse(recipe.data, safe=False)

        def post(self, request, format=None):
            data = RecipeSerializer(data=request.data)
            if data.is_valid():
                print("hello", request.data)
                valid_data = data.validated_data
                recipe = Recipe.objects.create(**valid_data)
                recipe.save()
                return JsonResponse(status=status.HTTP_201_CREATED , data={'message': 'Recipe created successfully'})
            else:
                return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
