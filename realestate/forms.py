from django import forms
from olwidget.fields import MapField, EditableLayerField, InfoLayerField
from django.utils.translation import ugettext as _



class PolySearchForm(forms.Form):
        poly = MapField(fields = [
            EditableLayerField({'geometry': 'polygon', 'name': _('polygon')}),
        ],
        options = {
            "default_lat": 41.6,
            "default_lon": 22,
            "default_zoom": 8,
            "map_div_style": {
                "width": "600px",
                "height": "300px",
            }
        },
        label = "", required = False,)

class PointSearchForm(forms.Form):
        poly = MapField(fields = [
            EditableLayerField({'geometry': 'polygon', 'name': _('polygon')}),
        ],
        options = {
            "default_lat": 41.6,
            "default_lon": 22,
            "default_zoom": 8,
            "map_div_style": {
                "width": "600px",
                "height": "300px",
            }
        },
        label = "", required = False,)
