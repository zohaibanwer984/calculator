from .serializers import HistorySerializer
from .models import Histroy

class HistoryViewSet(viewsets.ModelViewSet):
    queryset = Histroy.objects.all()
    serializer_class = HistorySerializer