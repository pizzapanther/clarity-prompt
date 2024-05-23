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
def test_user_count(client):
  data = {
    "conditions": [
      {"type": "new"},
      {"type": "biz", "operator": "AND"},
      {"type": "fam2021", "operator": "OR"}
    ]
  }
  resp = client.post('/api/v1/darulez/rule/user-count', json.dumps(data), content_type="application/json")
  assert resp.status_code == 200
  assert resp.content == b"0"
