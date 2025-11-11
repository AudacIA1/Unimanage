
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from faker import Faker
from django.utils import timezone
from datetime import timedelta

from apps.assets.models import AssetCategory, Asset
from apps.loans.models import Loan
from apps.request.models import LoanRequest
from apps.maintenance.models import Maintenance
from apps.events.models import Evento, AttendingEntity # Import AttendingEntity

class Command(BaseCommand):
    help = 'Seeds the database with realistic sample data.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # Setup Faker
        fake = Faker('es_ES')

        # Clean up database
        self.stdout.write('Cleaning up old data...')
        Loan.objects.all().delete()
        LoanRequest.objects.all().delete()
        Maintenance.objects.all().delete()
        Evento.objects.all().delete()
        AttendingEntity.objects.all().delete() # Clean up AttendingEntity
        Asset.objects.all().delete()
        AssetCategory.objects.all().delete()
        get_user_model().objects.filter(is_superuser=False).delete()
        
        # --- Get Groups ---
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        staff_group, _ = Group.objects.get_or_create(name='Staff')
        tech_group, _ = Group.objects.get_or_create(name='Tech')
        user_group, _ = Group.objects.get_or_create(name='User')

        # --- Create Superuser if not exists ---
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            self.stdout.write('Creating superuser...')
            admin_user = User.objects.create_superuser('admin', 'admin@unimanage.com', 'adminpass')
            admin_user.groups.add(admin_group)
        else:
            admin_user = User.objects.get(username='admin')

        # --- Create Users ---
        self.stdout.write('Creating users...')
        staff_user = User.objects.create_user('staff_user', 'staff@unimanage.com', 'password')
        staff_user.first_name = 'Usuario'
        staff_user.last_name = 'Staff'
        staff_user.groups.add(staff_group)
        staff_user.save()

        tech_user = User.objects.create_user('tech_user', 'tech@unimanage.com', 'password')
        tech_user.first_name = 'Usuario'
        tech_user.last_name = 'Técnico'
        tech_user.groups.add(tech_group)
        tech_user.save()

        users = []
        for i in range(10):
            username = fake.user_name()
            while User.objects.filter(username=username).exists():
                username = fake.user_name() + str(i)
            user = User.objects.create_user(username, fake.email(), 'password')
            user.first_name = fake.first_name()
            user.last_name = fake.last_name()
            user.groups.add(user_group)
            user.save()
            users.append(user)

        # --- Create Asset Categories ---
        self.stdout.write('Creating asset categories...')
        categories_names = ['Portátiles', 'Proyectores', 'Cámaras', 'Micrófonos', 'Tablets', 'Pizarras Digitales']
        categories = [AssetCategory.objects.create(name=name) for name in categories_names]

        # --- Create Assets ---
        self.stdout.write('Creating assets...')
        assets = []
        asset_status_choices = [choice[0] for choice in Asset.STATUS_CHOICES]
        for _ in range(30):
            asset = Asset.objects.create(
                name=fake.word().capitalize() + ' ' + random.choice(['Pro', 'Plus', 'X', 'Air']),
                category=random.choice(categories),
                location=f'Sala {random.randint(101, 505)}',
                status=random.choice(asset_status_choices)
            )
            assets.append(asset)

        # --- Create Loan Requests and Loans ---
        self.stdout.write('Creating loan requests and loans...')
        available_assets = [a for a in assets if a.status == 'disponible'] # Use lowercase status
        for i in range(15):
            if not available_assets: break
            asset_to_request = random.choice(available_assets)
            requesting_user = random.choice(users)
            start_date = timezone.now() + timedelta(days=random.randint(1, 30))
            end_date = start_date + timedelta(days=random.randint(1, 10))
            
            req = LoanRequest.objects.create(
                user=requesting_user,
                asset=asset_to_request,
                reason=fake.sentence(),
                start_date=start_date,
                end_date=end_date,
                status=random.choice(['pending', 'approved', 'rejected'])
            )

            if req.status == 'approved':
                loan_status = random.choice(['Activo', 'Devuelto'])
                loan_due_date = end_date # Default due date is end of requested period
                loan_return_date = None # Default return date is None for active loans

                self.stdout.write(f"DEBUG: Attempting to create loan for {asset_to_request.name} with initial status {loan_status}")
                if loan_status == 'Activo' and random.random() < 0.3: # 30% chance to be overdue
                    loan_due_date = timezone.now() - timedelta(days=random.randint(1, 10)) # Set due_date in the past
                    self.stdout.write(f"DEBUG: Overdue condition met for {asset_to_request.name}. New due_date: {loan_due_date}")
                elif loan_status == 'Devuelto':
                    loan_return_date = end_date + timedelta(days=random.randint(0, 5)) # Returned shortly after due date

                loan = Loan.objects.create(
                    asset=asset_to_request,
                    user=requesting_user,
                    loan_date=start_date,
                    due_date=loan_due_date,
                    return_date=loan_return_date,
                    status=loan_status
                )
                self.stdout.write(f"DEBUG: Loan created - Asset: {asset_to_request.name}, User: {requesting_user.username}, Status: {loan_status}, Due Date: {loan_due_date}, Is Overdue: {loan.is_overdue}")

        # --- Create Maintenance Tasks ---
        self.stdout.write('Creating maintenance tasks...')
        assets_for_maintenance = random.sample(assets, 5)
        for asset in assets_for_maintenance:
            start_date = timezone.now() - timedelta(days=random.randint(0, 60))
            Maintenance.objects.create(
                asset=asset,
                performed_by=tech_user.get_full_name() or tech_user.username,
                description=fake.sentence(),
                status=random.choice(['Pendiente', 'En proceso', 'Finalizado'])
            )
            if asset.status == 'disponible':
                asset.status = 'mantenimiento'
                asset.save()
                self.stdout.write(f"DEBUG: Asset {asset.name} status updated to {asset.status} (Maintenance)")

        # --- Create Attending Entities ---
        self.stdout.write('Creating attending entities...')
        entity_names = ['Universidad A', 'Empresa B', 'Organización C', 'Escuela D']
        attending_entities = [AttendingEntity.objects.create(name=name) for name in entity_names]

        # --- Create Events ---
        self.stdout.write('Creating events...')
        for _ in range(5):
            start_date = timezone.now() + timedelta(days=random.randint(1, 60))
            end_date = start_date + timedelta(hours=random.randint(1, 8))
            evento = Evento.objects.create(
                titulo=fake.catch_phrase(),
                descripcion=fake.text(),
                fecha_inicio=start_date,
                fecha_fin=end_date,
                responsable=random.choice([admin_user, staff_user]),
                status='active',
                tipo=random.choice(['evento', 'visita']) # Now includes 'visita'
            )
            if evento.tipo == 'visita' and attending_entities:
                evento.attending_entity = random.choice(attending_entities)
                evento.save()

            if available_assets:
                reserved = random.sample(available_assets, k=min(len(available_assets), 2))
                evento.reserved_assets.set(reserved)


        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))

