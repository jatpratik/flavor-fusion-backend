from django.db import models

class Recipe(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    recipe_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image_url = models.URLField(max_length=255)

    class Meta:
        db_table = 'recipe'

    def __str__(self):
        return self.recipe_name
