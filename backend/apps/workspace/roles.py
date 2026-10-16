from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

ROLE_PERMISSIONS={
    "Менеджер": {"clients":["view","add","change"],"inquiries":["view","change"],"workspace":["view"]},
    "Руководитель": {"clients":["view","add","change"],"inquiries":["view","change"],"workspace":["view"]},
}
@receiver(post_migrate)
def ensure_workspace_roles(sender,**kwargs):
    if sender.label!="workspace": return
    for name,rules in ROLE_PERMISSIONS.items():
        group,_=Group.objects.get_or_create(name=name); perms=[]
        for app_label,actions in rules.items():
            perms.extend(Permission.objects.filter(content_type__app_label=app_label,codename__regex=rf"^({'|'.join(actions)})_"))
        group.permissions.set(perms)
