import datetime
import json
import re

import pytest

from cprompt.darulez.models import School, DocumentRule

@pytest.fixture
def school():
  s = School(name="Narf School")
  s.save()
  return s


@pytest.mark.django_db
def test_add_doc_rule(client, school):
  data = {
    "school_id": 1,
    "action": "doc_request",
    "conditions": [
      {"type": "new"},
      {"type": "biz", "operator": "AND"},
      {"type": "fam2021", "operator": "OR"}
    ]
  }
  resp = client.post('/api/v1/darulez/rule/add', json.dumps(data), content_type="application/json")
  assert resp.status_code == 200


def test_querysets(django_user_model):
  c1 = [
    {"type": "new"},
    {"type": "biz", "operator": "AND"},
    {"type": "fam2021", "operator": "OR"}
  ]
  qs = DocumentRule.conditions_queryset(c1)
  print("C1:", qs.query.__str__())
  assert re.search("WHERE.*AND.*OR", qs.query.__str__()) is not None

  c2 = [
    {"type": "new"},
    {"type": "biz", "operator": "OR"},
    {"type": "fam2021", "operator": "OR"}
  ]
  qs = DocumentRule.conditions_queryset(c2)
  print("C2:", qs.query.__str__())
  assert re.search("WHERE.*OR.*OR", qs.query.__str__()) is not None

  qs = DocumentRule.conditions_queryset(c2)
  qs = qs & django_user_model.objects.filter(id=1)
  print("C3:", qs.query.__str__())
  assert re.search("WHERE.*OR.*OR.*AND", qs.query.__str__()) is not None


@pytest.mark.django_db
def test_user_count(client, django_user_model):
  User = django_user_model

  u1 = User(username='biz_me')
  u1.date_joined = datetime.datetime(2024, 5, 1, tzinfo=datetime.timezone.utc)
  u1.save()

  data = {
    "conditions": [
      {"type": "new"},
      {"type": "biz", "operator": "AND"},
      {"type": "fam2021", "operator": "OR"}
    ]
  }
  resp = client.post('/api/v1/darulez/rule/user-count', json.dumps(data), content_type="application/json")
  assert resp.status_code == 200
  assert resp.content == b"1"


@pytest.mark.django_db
def test_queryset_generator(client, django_user_model):
  User = django_user_model

  u1 = User(username='biz_me')
  u1.date_joined = datetime.datetime(2024, 5, 1, tzinfo=datetime.timezone.utc)
  u1.save()

  u2 = User(username='biz_me_2021')
  u2.date_joined = datetime.datetime(2024, 5, 1, tzinfo=datetime.timezone.utc)
  u2.save()

  conditions = [
    {
      "count": 2,
      "values": [
        {"type": "new"},
        {"type": "biz", "operator": "AND"},
        {"type": "fam2021", "operator": "OR"}
      ]
    },
    {
      "count": 1,
      "values": [
        {"type": "new"},
        {"type": "biz", "operator": "AND"},
        {"type": "fam2021", "operator": "AND"}
      ]
    }
  ]

  for cond in conditions:
    qs = DocumentRule.conditions_queryset(cond['values'])
    assert qs.count() == cond['count']
