# Generated by Django 5.0.6 on 2024-05-25 12:12

import django.db.models.deletion
import tinymce.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('description', models.CharField(max_length=200)),
                ('content', tinymce.models.HTMLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('published', models.BooleanField(default=False)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
                ('bookmarks', models.ManyToManyField(blank=True, related_name='bookmarked_lessons', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Урок',
                'verbose_name_plural': 'Уроки',
                'ordering': ('published', '-created_at'),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=5000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.profile')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='theory.comment', verbose_name='Parent comment')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='theory.lesson')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='tag')),
                ('slug', models.SlugField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ['id'],
                'unique_together': {('name', 'slug')},
            },
        ),
        migrations.AddField(
            model_name='lesson',
            name='tags',
            field=models.ManyToManyField(blank=True, to='theory.tag'),
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='theme')),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name': 'Тема',
                'verbose_name_plural': 'Темы',
                'unique_together': {('name', 'slug')},
            },
        ),
        migrations.AddField(
            model_name='lesson',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='theory.theme'),
        ),
        migrations.CreateModel(
            name='Textbook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(blank=True, max_length=150, null=True)),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(blank=True, upload_to='textbooks/files/')),
                ('image', models.ImageField(blank=True, default='textbooks/default.png', upload_to='textbooks/img/')),
                ('bookmarks', models.ManyToManyField(blank=True, related_name='bookmarked_textbooks', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, to='theory.tag')),
                ('theme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='theory.theme')),
            ],
            options={
                'verbose_name': 'Учебник',
                'verbose_name_plural': 'Учебники',
                'unique_together': {('name', 'slug')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='lesson',
            unique_together={('name', 'slug', 'theme', 'content')},
        ),
    ]
