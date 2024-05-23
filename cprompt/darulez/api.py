from ninja import Router, ModelSchema

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
