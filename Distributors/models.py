from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from process.models import Products
from process.models import Market
from orgin.ent.tool import Entity
# Create your models here.

User = get_user_model()

class Distributors(Entity):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='Distributors')
    image = models.ImageField(upload_to='media/Dis', null = True, blank= True)
    @property
    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
    

class TypeOfDistribution(Entity):
        manufacturer2Consumer = 'Manufacturer to Consumer'
        indirect_distribution = 'Indirect Distribution'
        intensive_distribution = 'Intensive Distribution'
        selective_distribution = 'Selective Distribution'
        exclusive_distribution = 'Exclusive Distribution'
        dual_distribution = 'Dual Distribution'
        franchising = 'Franchising'
        dropshipping = 'Dropshipping'
        multichannel_distribution = 'Multichannel Distribution'


        DistributorsType = models.CharField('type', max_length=260, choices=[
            (manufacturer2Consumer, manufacturer2Consumer),
            (indirect_distribution, indirect_distribution),
            (intensive_distribution, intensive_distribution),
            (selective_distribution, selective_distribution),
            (exclusive_distribution, exclusive_distribution),
            (dual_distribution, dual_distribution),
            (franchising, franchising),
            (dropshipping, dropshipping),
            (multichannel_distribution, multichannel_distribution),
        ])
        is_default = models.BooleanField('is_default')

        def __str__(self):
             return self.DistributorsType
        