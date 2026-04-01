from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Category, Product
from apps.products.serializers import CategorySerializer, ProductSerializer
from apps.users.permissions import IsAdmin, IsAdminOrSeller

class CategoryListView(APIView):

    def get_permissions(self): 
        if self.request.method == 'POST':
            return [IsAdmin()]
        return [AllowAny()]

    def get(self, request): # display categories
        categories = Category.objects.select_related('parent_category').prefetch_related('subcategories').all()
        serializer = CategorySerializer(categories, many=True)
        return Response({
            'message': 'success',
            'data': serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'success',
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
