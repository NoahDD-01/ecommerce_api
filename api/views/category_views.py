import uuid
from django.db.models import Q
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from ..models import Category
from ..serializers import CategorySerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def category_create(request):
    serializer = CategorySerializer(data =request.data,context = {"request":request})
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message":"Category created","data":serializer.data},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def category_list(request):
    qs = Category.objects.filter(parent=None)

    q = request.query_params.get("search")
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
    
    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")
    if start_date:
        qs = qs.filter(created_at_date_gte=start_date)
    if end_date:
        qs = qs.filter(created_at_date_lte = end_date)

    ordering = request.query_params.get("ordering")
    if ordering:
        qs = qs.order_by(ordering)

    else:
        qs = qs.order_by("name")
    
    paginator = PageNumberPagination()
    paginator.page_size = 3
    page = paginator.paginate_queryset(qs,request)
    ser = CategorySerializer(page,many=True,context={"request":request})

    return paginator.get_paginated_response({
        "message":"Category list fetched successfully.",
        "categories":ser.data
    })

@api_view(["GET"])
@permission_classes([AllowAny])
def category_detail(request,pk:uuid.UUID):
    try:
        obj = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response ({"detail": "Not found"},status=404)
    
    ser = CategorySerializer(obj)
    return Response({"message":"Category detail","data":ser.data})

@api_view(["PUT","PATCH"])
@permission_classes([IsAuthenticated])
def category_update(request,pk:uuid.UUID):
    try:
        obj = Category.objects.get(pk=pk)
    except:
        return Response({"detail":"Not found"},status=404)
    
    ser = CategorySerializer(
        obj,data = request.data,partial = True,
        context = {"request":request}
    )
    if ser.is_valid():
        ser.save()
        return Response({"message":"Category updated","data":ser.data})
    return Response(ser.errors,status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def category_delete (request,pk:uuid.UUID):
    try:
      obj = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({"detail":"Not found."},status=404)
    
    obj.delete()
    return Response({"message":"Category deleted."},status=status.HTTP_204_NO_CONTENT)
