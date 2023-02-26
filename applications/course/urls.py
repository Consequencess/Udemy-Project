from .views import CourseViewSet, CourseItemViewSet, CourseItemFileViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('item', CourseItemViewSet)
router.register('itemfile', CourseItemFileViewSet)
router.register('', CourseViewSet)
urlpatterns = router.urls
