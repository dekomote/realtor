from django.views.generic.simple import direct_to_template
from olwidget.widgets import Map, InfoLayer
from models import Region, RealEstate
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from shapes.views.export import ShpResponder


def region_map(request, region_slug):
    
    region = get_object_or_404(Region, slug = region_slug)
    realestates = RealEstate.objects.filter(poly__contained = region.poly)
    
    
    app_info = region._meta.app_label, region._meta.module_name
    map = Map([
            InfoLayer([
                    (region.poly, '<h2>%s</h2><br/><a href="%s">%s</a><br/><br/>%s' % (
                        _("Region %s") % region.name, 
                        reverse("admin:%s_%s_change" % app_info, args = (region.id,)),
                        _("Go to %s administration page") % region.name,
                        region.add_realestate_link
                        ),)
                ],
                {"name": _("Region")}
                ),
            InfoLayer([
                    (realestate.poly, '<h2>%s: %s</h2><br/><a href="%s">%s</a>' % (
                        _("ID: %s") % realestate.id,
                        _("Type: %s") % realestate.type,
                        reverse("admin:%s_%s_change" % (
                            realestate._meta.app_label,
                            realestate._meta.module_name,), args = (region.id,)),
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
    
    return direct_to_template(request, "admin/realestate/region_map.html",
                              extra_context = {"map": map, "region": region,})


def export_shapefile(modeladmin, request, queryset):
    return ShpResponder(queryset, geo_field = "poly")()
    
def export_shapefile_regions(modeladmin, request, queryset):
    qs = RealEstate.objects.filter(region__in = queryset)
    return ShpResponder(qs, geo_field = "poly")()