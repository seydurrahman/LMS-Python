from django.shortcuts import render
from . import models
from . import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
# Create your views here.

@api_view(['GET', 'POST'])
def category_list_create(request):
    if request.method == 'GET':
        categories = models.Category.objects.all()
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        if not request.user.is_authenticated or request.user.role != 'admin':
            return Response({'detail': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'categories': categories, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def course_list_create(request):
    if request.method == 'GET':
        category = request.query_params.get('category')
        search = request.query_params.get('search')
        queryset = models.Course.objects.all()
        if category:
            queryset = queryset.filter(category__title__icontains=category)
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if request.user.is_authenticated and request.user.role == 'instructor':
            queryset = queryset.filter(instructor=request.user)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = serializers.CourseSerializer(paginated_queryset, many=True,context={'request': request})
        return paginator.get_paginated_response(serializer.data)
    elif request.method == 'POST':
        if not request.user.is_authenticated or request.user.role != 'teacher':
            return Response({'detail': 'Only Teacher can create courses.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Course Details page
@api_view(['GET', 'POST'])
def lesson_list_create(request):
    if request.method == 'GET':
        course = request.query_params.get('courseId')
        if not course:
            return Response({'detail': 'Course parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            course = models.Course.objects.get(pk=course)
        except models.Course.DoesNotExist:
            return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
        is_teacher = request.user.is_authenticated and request.user.role == 'teacher' and course.instructor == request.user
        is_admin = request.user.is_authenticated and request.user.role == 'admin'
        is_enrollment = models.Enrollment.objects.filter(course=course, student=request.user,status="active").exists() if request.user.is_authenticated and request.user.role == "student" else False

        if not (is_teacher or is_admin or is_enrollment):
            return Response({'detail': 'You do not have permission to view lessons for this course.'}, status=status.HTTP_403_FORBIDDEN)
        lessons = models.Lesson.objects.filter(course=course)
        serializer = serializers.LessonSerializer(lessons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        course = request.query_params.get('courseId')
        if not course:
            return Response({'detail': 'Course parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            course = models.Course.objects.get(pk=course)
        except models.Course.DoesNotExist:
            return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)
        if request.user != course.instructor: 
            return Response({'detail': 'Only the instructor of this course can add lessons.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = serializers.LessonSerializer(data=request.data,status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save(course=course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# Lesson details home work

