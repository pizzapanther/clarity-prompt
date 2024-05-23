from django.db import models

class School(models.Model):
  name = models.CharField(max_length=70)

  def __str__(self):
    return self.name


class Application(models.Model):
  school = models.ForeignKey(School, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.id)


class DocumentRule(models.Model):
  ACTIONS = (
    ('doc_request', 'Document Request')
  )

  school = models.ForeignKey(School, on_delete=models.CASCADE)
  action = models.CharField(max_length=15, default="doc_request")
  conditions = models.JSONField()

  def __str__(self):
    return f"{self.school} - {self.id}"


class DocumentRequest(models.Model):
  application = models.ForeignKey(Application, on_delete=models.CASCADE)
  created = models.DateTimeField(auto_now_add=True)
  sent = models.DateTimeField(blank=True, null=True)

  def __str__(self):
    return str(self.id)
