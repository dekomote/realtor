from django.contrib.gis.admin import OSMGeoAdmin, site, StackedInline
from django.contrib.gis.geos import Point
from models import RealEstate, Region, RealEstateOwner

from django.conf.urls.defaults import patterns, include, url
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from views import region_map, export_shapefile, export_shapefile_regions

pnt = Point(22, 41.6, srid=4326)
pnt.transform(900913)


class RegionAdmin(OSMGeoAdmin):
    max_resolution = 21664300.0339
    default_zoom = 7
    default_lon, default_lat = pnt.coords
    search_fields = ('name', 'ascii_name',)
    list_editable = ('population',)
    list_display = ('name', 'population',
                    'region_map_link', 'add_realestate_link')
    list_display_links = ('name', )
    
    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.module_name
        urls = super(RegionAdmin, self).get_urls()
        
        new_urls = patterns('', 
            url(r'^region_map/(?P<region_slug>.+)/$', region_map,
                name = '%s_%s_region_map' % info),
        )
        return new_urls + urls
        
    def region_map_link(self, obj):
        info = obj._meta.app_label, obj._meta.module_name
        return '<a href="%s">%s</a>' % (
            reverse('admin:%s_%s_region_map' % info,
                    kwargs = {"region_slug": obj.slug}),
            _("Open Region Map")
            )

    region_map_link.allow_tags = True
    
    def add_realestate_link(self, obj):
        return obj.add_realestate_link

    add_realestate_link.allow_tags = True
    
    export_shapefile.short_description = _("Export a zipped ESRI files (Region Data)")    
    export_shapefile_regions.short_description = _("Export a zipped ESRI files (Realestate Data)")
    actions = [export_shapefile, export_shapefile_regions]
    
    
class RealEstateAdmin(OSMGeoAdmin):
    list_display = ('__unicode__', 'region', 'type', 'area', 'price',
                    'estimated_price', 'owner')
    list_editable = ('type', 'area', 'price')    
    list_filter = ('type', 'region', 'owner')    
    search_fields = ('id', 'region', 'type', 'area', 'price', 'estimated_price',
                    'owner',  'address', 'notes')    
    exclude = ('region',)
    
        
        
    map_width = 800
    map_height = 600
    default_zoom = 8
    default_lon, default_lat = pnt.coords
    max_resolution = 21664300.0339
    
    def add_view(self, request, form_url = '', extra_context = None):        
        self.default_lat = request.GET.get("lat", pnt.coords[1]);
        self.default_lon = request.GET.get("lon", pnt.coords[0]);
        self.default_zoom = 14
        return super(RealEstateAdmin, self).add_view(request,
                                                 form_url = form_url,
                                                 extra_context = extra_context)    
    
    export_shapefile.short_description = _("Export a zipped ESRI file")
    
    actions = [export_shapefile,]

class RealEstateOwnerAdmin(OSMGeoAdmin):    
    list_display = ('first_name', 'last_name', 'person_id', 'phone', 'email')
    list_editable = ('phone', 'email')
    list_display_links = ('person_id',)
    search_fields = ('first_name', 'last_name', 'person_id')
    ordering = ('first_name', 'last_name')
    


site.register(Region, RegionAdmin)
site.register(RealEstateOwner, RealEstateOwnerAdmin)
site.register(RealEstate, RealEstateAdmin)