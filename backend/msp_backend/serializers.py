from rest_framework import serializers
from .models import Location, Pandemic, PandemicData
from datetime import datetime


class ContinentSerializer(serializers.Serializer):
    #serializer continents
    id = serializers.CharField()
    name = serializers.CharField()


class CountrySerializer(serializers.Serializer):
    #serializer pour les pays avec leur continent d'origine
    id = serializers.CharField()
    name = serializers.CharField()
    continent = serializers.CharField()


class StateSerializer(serializers.Serializer):
    #serializer pour les états/provinces avec leur pays
    id = serializers.CharField()
    name = serializers.CharField()
    country = serializers.CharField()


class Admin2Serializer(serializers.Serializer):
    #serializer pour les villes
    id = serializers.CharField()
    name = serializers.CharField()
    state = serializers.CharField()


class DataRequestSerializer(serializers.Serializer):
    #serializer pour requêtes POST /api/data
    #choix de la pandémie
    pandemie = serializers.CharField(required=True)
    #filtres géographiques avec validation max 3 items
    continents = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True,
        default=list)
    
    countries = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True,
        default=list
    ) 
    states = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True,
        default=list
    )
    cities = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        allow_empty=True,
        default=list
    )

    #période temporelle
    startDate = serializers.DateField(
        required=True,
        input_formats=['%Y-%m-%d']
    )
    endDate = serializers.DateField(
        required=True,
        input_formats=['%Y-%m-%d']
    )
    
    #métriques (potentiellement à revoir)
    metrics = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=['cases', 'new_cases', 'deaths', 'new_deaths', 'recovered']
    )
    
    #granularité temporelle
    granularity = serializers.ChoiceField(
        choices=['daily', 'weekly', 'monthly'],
        default='monthly'
    )
    
    def validate(self, data):
        #validation startDate <= endDate
        if data['startDate'] > data['endDate']:
            raise serializers.ValidationError({
                'dates': 'la Date de début doit être antérieure ou égale à la Date de fin'
            })
        
        #validation max 3 items par niveau sauf world ou *
        for field in ['continents', 'countries', 'states', 'cities']:
            values = data.get(field, [])
            
            #si world ou * alors on accepte
            if values and values[0] in ['world', '*']:
                continue
                
            #sinon max 3 items
            if len(values) > 3:
                raise serializers.ValidationError({
                    field: f'maximum 3 {field} autorisés (ou utilisez "world" ou "*" pour tous)'
                })
        
        #validation des métriques connues
        valid_metrics = ['cases', 'new_cases', 'deaths', 'new_deaths', 'recovered', 'incident_rate', 'mortality_rate']
        for metric in data.get('metrics', []):
            if metric not in valid_metrics:
                raise serializers.ValidationError({
                    'metrics': f'métrique inconnue : {metric}. valeurs autorisées : {", ".join(valid_metrics)}'
                })
        
        return data


class PandemicDataSerializer(serializers.ModelSerializer):
    #serializer pour données de pandémie
    pandemic_name = serializers.CharField(source='pandemic.pandemic_name', read_only=True)
    #on garde le nom continent dans lapi pour compatibilité mais cest who_region en db
    continent = serializers.CharField(source='location.who_region', read_only=True)
    country = serializers.CharField(source='location.country', read_only=True)
    province_state = serializers.CharField(source='location.province_state', read_only=True)
    admin2 = serializers.CharField(source='location.city', read_only=True)
    population = serializers.IntegerField(source='location.population', read_only=True)
    
    class Meta:
        model = PandemicData
        fields = [
            'pandemic_name',
            'continent',
            'country',
            'province_state',
            'admin2',
            'observation_date',
            'total_cases',
            'new_cases',
            'total_deaths',
            'new_deaths',
            'total_recovered',
            'active_cases',
            'incident_rate',
            'population'
        ]


class ChartJsResponseSerializer(serializers.Serializer):
    #serializer pour json complet
    abscisse = serializers.ListField(
        child=serializers.CharField(),
        help_text="labels temporels au format YYYY-MM"
    )
    ordonne = serializers.ListField(
        child=serializers.DictField(),
        help_text="datasets prêts pour chart.js avec label, data, type"
    )
    data = serializers.ListField(
        child=serializers.DictField(),
        help_text="à compléter"
    )
