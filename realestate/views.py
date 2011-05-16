from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.simple import direct_to_template
from django.utils.translation import ugettext as _
from models import Region, RealEstate
from olwidget.widgets import Map, InfoLayer
from shapes.views.export import ShpResponder


def region_map(request, region_slug):
    
    region = get_object_or_404(Region, slug = region_slug)
    realestates = RealEstate.objects.filter(poly__contained = region.poly)
    map = poly_map(regions = [region])
    
    return direct_to_template(request, "admin/realestate/regions_map.html",
                              extra_context = {"map": map, "regions": [region], })


def regions_map(modeladmin, request, queryset):
    
    map = poly_map(regions = queryset,
                realestates = RealEstate.objects.filter(region__in = queryset))
    
    return direct_to_template(request, "admin/realestate/regions_map.html",
                              extra_context = {"map": map,
                                               "regions": queryset,})


def realestates_map(modeladmin, request, queryset):
    
    map = poly_map(realestates = queryset)
    return direct_to_template(request, "admin/realestate/realestates_map.html",
                              extra_context = {"map": map, })


def poly_map(regions = [], realestates = []):
    
    app_info = Region._meta.app_label, Region._meta.module_name    
    return Map([
            InfoLayer([
                    (region.poly, '<h2>%s</h2><br/><a href="%s">%s</a><br/><br/>%s' % (
                        _("Region %s") % region.name, 
                        reverse("admin:%s_%s_change" % app_info, args = (region.id,)),
                        _("Go to %s administration page") % region.name,
                        region.add_realestate_link
                        ),) for region in regions
                ],
                {"name": _("Region")}
                ),
            InfoLayer([
                    (realestate.poly, '<h2>%s: %s</h2><br/><a href="%s">%s</a>' % (
                        _("ID: %s") % realestate.id,
                        _("Type: %s") % realestate.get_type_display(),
                        reverse("admin:%s_%s_change" % (
                            realestate._meta.app_label,
                            realestate._meta.module_name,), args = (realestate.region.id,)),
                        _("Go to this realestate administration page")
                        ),) for realestate in realestates
                ],
                {
                    "name": _("Real Estates"),
                    "overlay_style": {"fill_color": "#0000ff",
                                   "stroke_color":"#000"}
                }
            ),
        ],
        options = {
            "map_div_style": {
                "width": "800px",
                "height": "600px"
                }
            })
    

def export_shapefile(modeladmin, request, queryset):
    return ShpResponder(queryset, geo_field = "poly")()


def export_shapefile_regions(modeladmin, request, queryset):
    qs = RealEstate.objects.filter(region__in = queryset)
    return ShpResponder(qs, geo_field = "poly")()
