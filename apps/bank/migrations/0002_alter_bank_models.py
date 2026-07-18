import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bankaccount',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='banktransaction',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='user',
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='bank_account',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='card_number',
            field=models.CharField(
                max_length=16,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message='شماره کارت باید دقیقاً ۱۶ رقم باشد.',
                        regex='^\\d{16}$',
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name='banktransaction',
            name='source_card',
            field=models.CharField(
                max_length=16,
                validators=[
                    django.core.validators.RegexValidator(
                        message='شماره کارت باید دقیقاً ۱۶ رقم باشد.',
                        regex='^\\d{16}$',
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name='banktransaction',
            name='destination_card',
            field=models.CharField(
                max_length=16,
                validators=[
                    django.core.validators.RegexValidator(
                        message='شماره کارت باید دقیقاً ۱۶ رقم باشد.',
                        regex='^\\d{16}$',
                    )
                ],
            ),
        ),
    ]
