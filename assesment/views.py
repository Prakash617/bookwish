from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
import json

from rest_framework.permissions import IsAdminUser

# from .models import (
#     Assesment
# )
from .models import *
from .serializers import (
    AssessmentScoresSerializer,
    AssessmentSerializer,
    AssessmentCriteriaSerializer
)

# Create your views here.
class AssessmentList(ListCreateAPIView):
    queryset = Assesment.objects.all()
    serializer_class = AssessmentSerializer


class AssessmentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Assesment.objects.all()
    serializer_class = AssessmentSerializer
    lookup_field = "id"
    
    
def valid_score_json(obj):
    print({"score_data":[obj]})
    return {"score_data":[obj]}


class AssessmentCriteriaView(ListCreateAPIView):
    queryset = AssesmentCriteria.objects.all()
    serializer_class = AssessmentCriteriaSerializer
    permission_classes = [IsAdminUser]

    


class AssessmentScoresViewSet(ModelViewSet):
    queryset = AssessmentScores.objects.all()
    serializer_class = AssessmentScoresSerializer
    
    def list(self, request, *args, **kwargs):
        print("Listing assessment scores")
        return super().list(request, *args, **kwargs)
    
    # post request sample
    # {
    #     "assessment": 2,
    #     "scores": {
    #             "score_data": [
    #                 {
    #                     "vocabulary": 1
    #                 }
    #             ]
    #         }
    # }
    
    def create(self, request, *args, **kwargs):
        print("Creating assessment scores")
        response = {}
        try:
            assessment_score  = request.data
            if type(assessment_score['scores']) == str:
                score = json.loads(assessment_score['scores'])
            else:
                score = assessment_score['scores']
            
            score_data = score['score_data'][0]
            valid_assesments = {}
            assessment = Assesment.objects.get(id = assessment_score['assessment'])
            print(assessment)
            for k in score_data:
                print(k)
                if AssesmentCriteria.objects.filter(criteria_name = k).exists():
                    valid_assesments[k] = score_data[k]
                    
            alread_exists = AssessmentScores.objects.filter(assessed_by=request.user,assessment=assessment).exists()
            if alread_exists:
                qs = AssessmentScores.objects.update(assessed_by=request.user,assessment=assessment,scores=valid_score_json(valid_assesments))
                print("update assessment",qs)
            else:
                qs = AssessmentScores.objects.create(assessed_by=request.user,assessment=assessment,scores=valid_score_json(valid_assesments))
                response['data'] = AssessmentScoresSerializer(qs).data
            response['status'] = 'success'
            print('Success')
            
            return Response(response,status=status.HTTP_201_CREATED)
        except:
            print('Failed')
            response['status'] = '404 Not Found'
            return Response(response,status=status.HTTP_404_NOT_FOUND)
        
        
    def destroy(self, request, pk=None, *args, **kwargs ):
        
        if pk:
            assesment_obj = Assesment.objects.get(id = pk)
            print("assesment",assesment_obj)
            assessmentScores = AssessmentScores.objects.get(assessed_by = request.user, assessment = assesment_obj)
            print('perform_destroy')
            self.perform_destroy(assessmentScores)
            return Response({'message':'deleted',"status":status.HTTP_204_NO_CONTENT})
        
        return Response({'message':"Unsuccessfull-not provided assesment_id "},status=status.HTTP_500_INTERNAL_SERVER_ERROR)