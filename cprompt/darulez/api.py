from ninja import Router, ModelSchema, Schema
from ninja.orm.fields import AnyObject
from cprompt.darulez.models import DocumentRule, School


router = Router()

class DocRuleScheam(ModelSchema):
  class Meta:
    model = DocumentRule
    fields = ['id', 'school', 'action', 'conditions']

class AddDocRuleScheam(ModelSchema):
  class Meta:
    model = DocumentRule
    fields = ['school', 'action', 'conditions']

@router.post("/rule/add", response=DocRuleScheam)
def add_rule(request, data: AddDocRuleScheam):
  kwargs = data.dict()
  kwargs['school'] = School.objects.get(id=kwargs['school'])

  rule = DocumentRule(**kwargs)
  rule.save()

  return rule


class CountSchema(Schema):
  conditions: AnyObject


@router.post("/rule/user-count", response=int)
def users_matching_conditions(request, data: CountSchema):
  qs = DocumentRule.conditions_queryset(data.conditions)
  return qs.count()
