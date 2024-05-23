import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

User = get_user_model()

class School(models.Model):
  name = models.CharField(max_length=70)

  def __str__(self):
    return self.name


class Application(models.Model):
  STATUSES = (
    ('new', 'New'),
    ('submitted', 'Submitted'),
  )

  school = models.ForeignKey(School, on_delete=models.CASCADE)
  status = models.CharField(max_length=15, choices=STATUSES)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return str(self.id)


@receiver(post_save, sender=Application)
def app_submitted(sender, **kwargs):
  from cprompt.darulez.tasks import check_rules_task

  if kwargs['instance'].status == 'submitted':
    check_rules_task(kwargs['instance'])


class DocumentRule(models.Model):
  ACTIONS = (
    ('doc_request', 'Document Request'),
  )

  CONDITIONS = {
    "new": {"date_joined__gt": datetime.datetime(2024, 1, 1)},
    "biz": {"username__startswith": "biz_"},
    "fam2021": {"username__endswith": "_2021"},
  }

  school = models.ForeignKey(School, on_delete=models.CASCADE)
  action = models.CharField(max_length=15, default="doc_request", choices=ACTIONS)
  conditions = models.JSONField()

  def __str__(self):
    return f"{self.school} - {self.id}"


  def conditions_met(self, application):
    qs = self.conditions_queryset(self.conditions)
    user = qs & User.objects.filter(user=application.user).first()
    return user

  @classmethod
  def conditions_queryset(cls, conditions):
    queryset = None

    for cond in conditions:
      if queryset is None:
        queryset = User.objects.filter(**cls.qargs(cond))

      else:
        if cond['operator'] == "AND":
          queryset = queryset & User.objects.filter(**cls.qargs(cond))

        else:
          queryset = queryset | User.objects.filter(**cls.qargs(cond))

    return queryset

  @classmethod
  def qargs(cls, condition):
    #  {"type": "biz", "operator": "AND"},
    return cls.CONDITIONS[condition["type"]]

    # {"field": "biz_owner__year", "comparison": "gte", "value": 2021, "operator": "AND"},
    # return {f"{condition["field"]}__{condition["comparison"]}": condition["value"]}


class DocumentRequest(models.Model):
  application = models.ForeignKey(Application, on_delete=models.CASCADE)
  rule = models.ForeignKey(DocumentRule, on_delete=models.CASCADE)
  created = models.DateTimeField(auto_now_add=True)
  sent = models.DateTimeField(blank=True, null=True)

  def __str__(self):
    return str(self.id)

  def send(self):
    self.sent = timezone.now()
    self.save()
