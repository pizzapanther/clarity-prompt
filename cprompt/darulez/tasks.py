from cprompt.darulez.models import Application, DocumentRule, DocumentRequest

def check_rules_task(app_id):
  application = Application.objects.get(id=app_id)
  for rule in DocumentRule.objects.filter(school=application.school):
    if rule.conditions_met(application):
      if rule.action == "doc_request":
        request = DocumentRequest(application=application, rule=rule)
        request.save()
        request.send()
