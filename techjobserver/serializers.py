from rest_framework import serializers 
from techjobserver.models import ITjob
 
 
class JobscraperSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = ITjob
        fields = ('id',
                  'job_title',
                  'job_intro',
                  'job_description',
                  'job_date',
                  'job_link')