from django.core.management.base import BaseCommand
from prices.models import Package

class Command(BaseCommand):
    help = "Insert or update packages in the database"

    def handle(self, *args, **kwargs):
        packages_data = [
            {"package_type": "Premium", "price": 999, "platforms": "up to 4", "posts_per_month": 90, "credits": 300, "content_text": True, "content_photos": True, "content_video": True, "editing": "Before and after approval", "history": "last year"},
            {"package_type": "Advanced", "price": 649, "platforms": "up to 3", "posts_per_month": 60, "credits": 200, "content_text": True, "content_photos": True, "content_video": True, "editing": "Before and after approval", "history": "month 6"},
            {"package_type": "Standard", "price": 449, "platforms": "up to 2", "posts_per_month": 30, "credits": 100, "content_text": True, "content_photos": True, "content_video": False, "editing": "Before approval", "history": "month 3"},
            {"package_type": "Beginners", "price": 229, "platforms": "1", "posts_per_month": 15, "credits": 40, "content_text": True, "content_photos": True, "content_video": False, "editing": "Before approval", "history": "last month"},
        ]

        for package_data in packages_data:
            package, created = Package.objects.update_or_create(
                package_type=package_data["package_type"],
                defaults={
                    "price": package_data["price"],
                    "platforms": package_data["platforms"],
                    "posts_per_month": package_data["posts_per_month"],
                    "credits": package_data["credits"],
                    "content_text": package_data["content_text"],
                    "content_photos": package_data["content_photos"],
                    "content_video": package_data["content_video"],
                    "editing": package_data["editing"],
                    "history": package_data["history"],
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Inserted new package: {package.package_type}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Updated existing package: {package.package_type}"))

        self.stdout.write(self.style.SUCCESS("Packages updated successfully!"))
