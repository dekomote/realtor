from django.contrib.gis.admin import OSMGeoAdmin, site, StackedInline
from django.contrib.gis.geos import Point
from models import RealEstate, Region, RealEstateOwner

pnt = Point(22, 41.6, srid=4326)
pnt.transform(900913)


class RegionAdmin(OSMGeoAdmin):
    max_resolution = 21664300.0339
    default_zoom = 7
    default_lon, default_lat = pnt.coords
    ordering = ('ascii_name',  )
    search_fields = ('name', 'ascii_name',)
    list_editable = ('population',)
    list_display = ('name', 'ascii_name', 'slug', 'population')
    list_display_links = ('name',)
    
    
class RealEstateAdmin(OSMGeoAdmin):
    list_display = ('id', 'region', 'type', 'address', 'area', 'price',
                    'estimated_price', 'owner')
    list_editable = ('type', 'address', 'area', 'price')
    
    list_filter = ('type', 'region', 'owner')
    
    search_fields = ('id', 'region', 'type', 'area', 'price', 'estimated_price',
                    'owner',  'address', 'notes')
    exclude = ('region',)
        
    map_width = 800
    map_height = 600
    default_zoom = 8
    default_lon, default_lat = pnt.coords
    max_resolution = 21664300.0339

class RealEstateOwnerAdmin(OSMGeoAdmin):    
    list_display = ('first_name', 'last_name', 'person_id', 'phone', 'email')
    list_editable = ('phone', 'email')
    list_display_links = ('person_id',)
    search_fields = ('first_name', 'last_name', 'person_id')
    ordering = ('first_name', 'last_name')
    


site.register(Region, RegionAdmin)
site.register(RealEstateOwner, RealEstateOwnerAdmin)
site.register(RealEstate, RealEstateAdmin)