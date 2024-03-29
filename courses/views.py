from .serializers import *
from courses.models import Sector, Course, Cart

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers


class CoursesHomeView(APIView):
    def get(self, request, *args, **kwargs):
        sectors = Sector.objects.order_by("?")[:6]

        sector_response = []

        for sector in sectors:
            sector_courses = sector.related_course.order_by("?")[:4]
            courses_serializer = CourseDisplaySerializer(sector_courses, many=True)

            sector_obj = {
                "sector_name": sector.name,
                "sector_uuid": sector.sector_uuid,
                "featured_course": courses_serializer.data,
                "sector_image": sector.sector_image_url,
            }

            sector_response.append(sector_obj)

        return Response(data=sector_response, status=status.HTTP_200_OK)


class CourseDetail(APIView):
    def get(self, request, course_uuid, *args, **kwargs):
        course = Course.objects.filter(course_uuid=course_uuid)

        if not course:
            return HttpResponseBadRequest("course does not exist")

        serializer = CourseSerializer(course[0])

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SectorCourse(APIView):
    def get(self, request, sector_uuid, *args, **kwargs):
        sector = Sector.objects.filter(sector_uuid=sector_uuid)

        if not sector:
            return HttpResponseBadRequest("Sector does not exist")

        sector_courses = sector[0].related_course.all()
        serializer = CourseListSerailizer(sector_courses, many=True)

        return Response(
            {
                "sector_name": sector[0].name,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class SearchCourse(APIView):

    def get(self, request, search_term):
        matches = Course.objects.filter(Q(title__icontains=search_term))
        serializer = CourseListSerailizer(matches, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AddComment(APIView):
    def post(self, request, course_uuid):
        try:
            course = Course.objects.get(course_uuid=course_uuid)
        except Course.DoesNotExist:
            return HttpResponseBadRequest("Course does not exist")

        content = request.data

        if not content.get("message"):
            return Response(
                "Message field is required", status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CommentSerializer(data=content)

        if serializer.is_valid():
            # user = User.username
            comment = serializer.save()
            course.comments.add(comment)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseStudy(APIView):
    def get(self, request, course_uuid):
        try:
            course = Course.objects.get(course_uuid=course_uuid)
        except Course.DoesNotExist:
            return HttpResponseBadRequest("course Does not exist")

        request.user = User.objects.get(id=1)
        user_course = request.user.paid_courses.filter(course_uuid=course_uuid)
        if not user_course:
            return HttpResponseNotAllowed("User does not own this course")

        serializer = CourseSerializer(course)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CartAPI(APIView):
    # serializer_class = ProductSerializer

    def get(self, request):
        # user_cart = Cart.objects.filter(user=request.user)
        
        user_cart = Cart.objects.all()
        serializer = ProductSerializer(user_cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # serializer = self.serializer_class(data=request.data)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                    {"message": "Course Added successfully"},
                    status=status.HTTP_201_CREATED,
                )
        # return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors)
        
class CartRemoveAPI(APIView):
    def get(self, request, pk):
        try:
            user_cart = Cart.objects.get(pk=pk)
            serializer = ProductSerializer(user_cart)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            raise Http404("Cart not found")

    def delete(self, request, pk):
        try:
            qus = Cart.objects.get(pk=pk)
            qus.delete()
            return Response({"Course removed successfully!"})
        except Cart.DoesNotExist:
            raise Http404("Cart not found")
