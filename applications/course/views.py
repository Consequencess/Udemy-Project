import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from applications.course.models import Course, CourseItem, CourseItemFile, Theme, Category
from applications.course.permissions import IsMentorOfCourseOrReadOnly
from applications.course.serializers import CoursesSerializer, CourseItemSerializer, CourseItemFileSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100000


class CourseFilter(django_filters.FilterSet):
    theme = django_filters.ModelChoiceFilter(queryset=Theme.objects.all(), field_name='theme')

    class Meta:
        model = Course
        fields = ['theme', 'category', 'sub_category']


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CoursesSerializer
    permission_classes = [IsMentorOfCourseOrReadOnly]
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    filterset_class = CourseFilter
    search_fields = ['title', 'user__first_name', 'category__title']
    ordering_fields = ['id', 'ratings']
    pagination_class = LargeResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CourseItemViewSet(viewsets.ModelViewSet):
    queryset = CourseItem.objects.all()
    serializer_class = CourseItemSerializer
    permission_classes = [IsMentorOfCourseOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CourseItemFileViewSet(viewsets.ModelViewSet):
    queryset = CourseItemFile.objects.all()
    serializer_class = CourseItemFileSerializer
    permission_classes = [IsMentorOfCourseOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)









