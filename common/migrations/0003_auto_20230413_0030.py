# Generated by Django 3.2.18 on 2023-04-12 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0001_initial'),
        ('common', '0002_auto_20230412_1501'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='postings_like',
        ),
        migrations.AddField(
            model_name='user',
            name='comments_agree',
            field=models.ManyToManyField(related_name='users_agree', to='discussion.Comment'),
        ),
        migrations.AddField(
            model_name='user',
            name='comments_disagree',
            field=models.ManyToManyField(related_name='users_disagree', to='discussion.Comment'),
        ),
        migrations.AddField(
            model_name='user',
            name='postings_best',
            field=models.ManyToManyField(related_name='users_best', to='discussion.Posting'),
        ),
        migrations.AddField(
            model_name='user',
            name='postings_worst',
            field=models.ManyToManyField(related_name='users_worst', to='discussion.Posting'),
        ),
    ]