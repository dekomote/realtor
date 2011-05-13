from django.contrib.gis.db import models
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

REALESTATE_TYPE_CHOICES = (
    ("H", _("House"),),
    ("B", _("Building"),),
    ("L", _("Land"),),
    ("O", _("Other"),),
    )


class Region(models.Model):
    name = models.CharField(max_length = 150)
    ascii_name = models.CharField(max_length = 150)
    slug = models.SlugField(max_length = 50, unique = True, db_index = True)
    map_center = models.PointField()
    poly =  models.PolygonField()
    population = models.PositiveIntegerField(default = 0)
    
    objects = models.GeoManager()
    
    class Meta:
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')
        ordering = ('-population', 'name',)
    
    def __unicode__(self):
        return self.name

    def __str__(self):
        return unicode(self).encode('utf-8')
    
    @property
    def add_realestate_link(self):        
        info = RealEstate._meta.app_label, RealEstate._meta.module_name
        pnt = self.map_center
        pnt.transform(900913)
        return '<a href="%s?%s">%s</a>' % (
            reverse('admin:%s_%s_add' % info,),
            "lon=%s&amp;lat=%s" % pnt.coords,
            _("Add a Real Estate")
            )


class RealEstateOwner(models.Model):
    
    first_name = models.CharField(_("first name"), max_length = 255)
    last_name = models.CharField(_("last name"), max_length = 255)
    email = models.EmailField(_("email"), blank = True)
    phone = models.CharField(_("phone number"), max_length = 50)
    person_id = models.CharField(_("identification number"), max_length = 50)
    
    class Meta:
        verbose_name = _('real estate owner')
        verbose_name_plural = _('real estate owners')        

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name,)

    def __str__(self):
        return unicode(self).encode('utf-8')


class RealEstate(models.Model):
        
    
    type = models.CharField(_("type"), max_length = 1,
                            choices = REALESTATE_TYPE_CHOICES)
    price = models.DecimalField(_("price"), max_digits = 8, decimal_places = 2,
                                help_text = _("price per square meter"))
    area = models.DecimalField(_("area"), max_digits = 8, decimal_places = 2,
                                help_text = _("area in sqare meters"))
    address = models.CharField(_("address"), max_length = 500,
                               blank = True)
    notes = models.TextField(_("notes"), blank = True)
    
    region = models.ForeignKey(Region)    
    owner = models.ForeignKey(RealEstateOwner)
    
    poly = models.PolygonField(_("polygon"))
    objects = models.GeoManager()
    
    
    def clean(self):
        
        region = Region.objects.filter(poly__bbcontains = self.poly)
        if not region:
            raise ValidationError(
                "The realestate is placed in an undefined region")
        else:
            self.region = region[0]        
    
    class Meta:
        verbose_name = _('real estate')
        verbose_name_plural = _('real estates')        

    def __unicode__(self):
        return "%s%s %s" % (self.type, self.id, self.region.name,)

    def __str__(self):
        return unicode(self).encode('utf-8')
    
    @property
    def estimated_price(self):
        return self.area * self.price