from rest_framework import routers
from .views import *


router = routers.DefaultRouter()

router.register(r'category', QuestionnaireCategoryViewSet)
router.register(r'parameter', QuestionnaireParameterViewSet)
router.register(r'', QuestionnaireEvaluateViewSet)

urlpatterns = router.urls
