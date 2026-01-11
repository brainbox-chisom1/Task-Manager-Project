from django.core.management.base import BaseCommand
from mytask_app.models import Task, Remainder
from django.utils.email_utils import send_task_mail
from django.utils.time_utils import is_ten_minutes_to_due

class Command(BaseCommand):
    help = "Check tasks and send reminder emails"

    def handle(self, *args, **kwargs):
        tasks = Remainder.objects.all()

        for task in tasks:
            if is_ten_minutes_to_due(task):
                send_task_mail(
                    to_email=task.user.email,  # or task.email
                    task_name=task.task_name
                )
                task.remainder_sent = True
                task.save()

        self.stdout.write("Reminder check completed")
