import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from accounts.models import GameAccount, Category


class Command(BaseCommand):
    help = "Seed 50 fake game accounts"

    def handle(self, *args, **options):
        categories = list(Category.objects.filter(id__gte=1, id__lte=20))

        if not categories:
            self.stdout.write(self.style.ERROR("❌ Không có category từ 1–20"))
            return

        names = [
            "Liên Quân Rank Cao",
            "Free Fire Full Skin",
            "Liên Minh Rank Kim Cương",
            "Genshin AR Cao",
            "Valorant Full Agent",
            "PUBG Acc VIP",
            "CSGO Prime",
            "FIFA Online Team Ngon",
            "Tốc Chiến Rank Cao",
            "Steam Account VIP",
        ]

        accounts = []

        for i in range(50):
            category = random.choice(categories)
            name = random.choice(names)

            is_sold = random.choice([True, False])

            account = GameAccount(
                name=f"{name} #{i+1}",
                category=category,
                description="Tài khoản chơi ổn định, thông tin đầy đủ, đổi pass được.",
                price=random.randint(50_000, 5_000_000),
                stock=0 if is_sold else random.randint(1, 5),
                username=f"user_{slugify(name)}_{i}",
                password="password123",
                email=f"user{i}@gmail.com",
                phone_number=f"09{random.randint(10000000, 99999999)}",
                is_sold=is_sold,
            )

            accounts.append(account)

        GameAccount.objects.bulk_create(accounts)

        self.stdout.write(
            self.style.SUCCESS("✅ Đã tạo thành công 50 game accounts")
        )
