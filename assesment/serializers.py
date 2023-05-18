from rest_framework import serializers
from .models import (
    Assesment,
    AssessmentScores,
    AssesmentCriteria
)

from user_accounts.serializers import (
    CustomUserSerializer
)

def get_assessed_data(instance):
    data = AssessmentScores.objects.filter(assessment=instance)
    assessment_data = []
    for item in data:
            assessment_data.append(AssessmentScoresSerializer(item).data)
    return assessment_data

def get_overall_ratings(instance):
    overall_ratings = {}
    all_criterias = AssesmentCriteria.objects.all()
    for criteria in all_criterias:
        overall_ratings[criteria.criteria_name] = 0
        overall_ratings[criteria.criteria_name+"_count"] = 0
        overall_ratings[criteria.criteria_name+"_avg_rating"] = 0

    
    for data in instance:
        new_data_set = data["scores"]["score_data"]
        for item in new_data_set:
            print(item)
            for k,v in item.items():
                overall_ratings[k] += v
                overall_ratings[k+"_count"] += 1
                overall_ratings[k+"_avg_rating"] = round(overall_ratings[k] / overall_ratings[k+"_count"],2)

    print(overall_ratings)
    overall_data = {}
    for k,v in overall_ratings.items():
        if('avg_rating' in str(k)):
            overall_data[k] = v
    
    print(overall_data)
    return(overall_data)

        

class AssessmentScoresSerializer(serializers.ModelSerializer):
    assessed_by = CustomUserSerializer(many=False,read_only=True)
    class Meta:
        model = AssessmentScores
        exclude = ("id",)




class AssessmentSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = CustomUserSerializer(instance.user).data
        assessed_data = get_assessed_data(instance)
        response['assessed_data'] =  assessed_data
        assessed = AssessmentScores.objects.filter(assessment__id=instance.id).filter(assessed_by=self.context.get('request').user).exists()
        response['is_assessed'] =  assessed
        response['assessed_data_avg'] = get_overall_ratings(assessed_data)
        return response 

    class Meta:
        model = Assesment
        fields = "__all__"
        read_only_fields = ('id',)

class AssessmentCriteriaSerializer(serializers.ModelSerializer):
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)

    #     data = []
    #     for k,v  in response:
    #         print(k,v)
    #         # data.append(AssessmentCriteriaSerializer(item).data)

    #     response["criterias"] = data

    #     return response


    class Meta:
        model = AssesmentCriteria
        fields = "__all__"