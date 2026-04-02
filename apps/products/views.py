from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.products.filters import ProductFilter
from apps.products.pagination import ProductPagination

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

class CategoryDetailView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdmin()]

    def get_object(self, pk):
        try:
            return Category.objects.select_related('parent_category').prefetch_related('subcategories').get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response({'message': 'success', 'data': serializer.data})

    def put(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'success', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return Response({'message': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response({'message': 'success'}, status=status.HTTP_204_NO_CONTENT)

class ProductListView(APIView):
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminOrSeller()]
        return [AllowAny()]

    # Database → [Stage 1: Filter] → [Stage 2: Paginate] → [Stage 3: Serialize] → Response
    def get(self, request):
        queryset = Product.objects.select_related('category', 'seller').all()

        # loop filter cate -> product -> price
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(request, queryset, self)

        # pagination
        paginator = ProductPagination()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = ProductSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)


        # fallback if pagination is disable
        serializer = ProductSerializer(queryset, many=True)
        return Response({'message': 'success', 'data': serializer.data})

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response({
                'message': 'success',
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_object(self, pk):
        try:
            return Product.objects.select_related('category', 'seller').get(pk=pk)
        except Product.DoesNotExist:
            return None

    def check_ownership(self, request, product):
        return request.user.is_admin or product.seller == request.user

    def get(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response({'message': 'success', 'data': serializer.data})

    def put(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        if not self.check_ownership(request, product):
            return Response({'message': 'You do not have permission to edit this product.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'success', 'data': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if not product:
            return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        if not self.check_ownership(request, product):
            return Response({'message': 'You do not have permission to delete this product.'}, status=status.HTTP_403_FORBIDDEN)
        product.delete()
        return Response({'message': 'success'}, status=status.HTTP_204_NO_CONTENT)