from django.db import models

class ITjob(models.Model):
  job_title = models.CharField(max_length=210)
  job_intro = models.TextField(blank=False, default='')
  job_description = models.TextField(blank=False, default='')
  job_date = models.TextField(blank=False, default='')
  job_link = models.TextField()

  def __str__(self):
    return self.job_title