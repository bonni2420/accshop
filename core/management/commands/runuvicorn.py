from django.core.management.base import BaseCommand
import uvicorn

class Command(BaseCommand):
    help = "Run the Django Application with Uvicorn"

    def handle(self, *args, **options):
        uvicorn.run(
            "accshop.asgi:application",
            host="127.0.0.1",
            port=8000,
            reload=True
        )
