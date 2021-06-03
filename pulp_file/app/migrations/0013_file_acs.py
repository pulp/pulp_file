# Generated by Django 2.2.24 on 2021-07-13 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0069_acs'),
        ('file', '0012_delete_filefilesystemexporter'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileAlternateContentSource',
            fields=[
                ('alternatecontentsource_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='file_filealternatecontentsource', serialize=False, to='core.AlternateContentSource')),
            ],
            options={
                'default_related_name': '%(app_label)s_%(model_name)s',
            },
            bases=('core.alternatecontentsource',),
        ),
        migrations.CreateModel(
            name='FileAlternateContentSourcePath',
            fields=[
                ('alternatecontentsourcepath_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='file_filealternatecontentsourcepath', serialize=False, to='core.AlternateContentSourcePath')),
            ],
            options={
                'default_related_name': '%(app_label)s_%(model_name)s',
            },
            bases=('core.alternatecontentsourcepath',),
        ),
    ]
