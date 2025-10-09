from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Sum
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .models import Location, Pandemic, PandemicData
from .serializers import (
    ContinentSerializer,
    CountrySerializer,
    StateSerializer,
    Admin2Serializer,
    DataRequestSerializer,
    PandemicDataSerializer
)
from collections import defaultdict
from datetime import datetime
import csv


@extend_schema(
    summary="liste des continents",
    description="retourne tous les continents",
    responses={
        200: {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'string', 'example': 'europe'},
                    'name': {'type': 'string', 'example': 'Europe'}
                }
            }
        }
    },
    tags=['Filtres']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_continents(request):
    #retourne la liste des continents
    continents = Location.objects.values_list('continent', flat=True).distinct().order_by('continent')
    
    #formater en [{id, name}]
    data = [
        {'id': continent.lower().replace(' ', '_'), 'name': continent}
        for continent in continents if continent
    ]
    
    return Response(data, status=status.HTTP_200_OK)


@extend_schema(
    summary="liste des pays",
    description="retourne les pays filtrés par continents",
    parameters=[
        OpenApiParameter(
            name='continents',
            type=str,
            location=OpenApiParameter.QUERY,
            description="continents :",
            examples=[
                OpenApiExample('un continent', value='europe'),
                OpenApiExample('plusieurs continents', value='europe,asia,africa'),
            ]
        )
    ],
    responses={
        200: {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'string', 'example': 'france'},
                    'name': {'type': 'string', 'example': 'France'},
                    'continent': {'type': 'string', 'example': 'europe'}
                }
            }
        },
    },
    tags=['Filtres']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_countries(request):
    #retourne la liste des pays filtrés par continents
    continents_param = request.query_params.get('continents', '')
    continents = [c.strip() for c in continents_param.split(',') if c.strip()]
    
    #validation max 3 sauf world ou *
    if continents and continents[0] not in ['world', '*']:
        if len(continents) > 3:
            return Response(
                {'error': 'maximum 3 continents autorisés'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    #requête de base
    queryset = Location.objects.all()
    
    #filtre par continents si pas world
    if continents and continents[0] not in ['world', '*']:
        #normaliser les noms (première lettre en majuscule)
        continents_normalized = [c.replace('_', ' ').title() for c in continents]
        queryset = queryset.filter(continent__in=continents_normalized)
    
    #récupérer les pays distincts avec leur continent
    countries = queryset.values('country', 'continent').distinct().order_by('continent', 'country')
    
    #formater en {id, name, continent}
    data = [
        {
            'id': country['country'].lower().replace(' ', '_'),
            'name': country['country'],
            'continent': country['continent'].lower().replace(' ', '_') if country['continent'] else None
        }
        for country in countries if country['country']
    ]
    
    return Response(data, status=status.HTTP_200_OK)


@extend_schema(
    summary="liste des états/provinces",
    description="retourne les états filtrés par pays",
    parameters=[
        OpenApiParameter(
            name='countries',
            type=str,
            location=OpenApiParameter.QUERY,
            description="pays",
            examples=[
                OpenApiExample('un pays', value='united_states'),
                OpenApiExample('plusieurs pays', value='united_states,canada,mexico'),

            ]
        )
    ],
    responses={
        200: {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'string', 'example': 'california'},
                    'name': {'type': 'string', 'example': 'California'},
                    'country': {'type': 'string', 'example': 'united_states'}
                }
            }
        },
    },
    tags=['Filtres']
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_states(request):
    # retourne la liste des états/provinces filtrés par pays

    countries_param = request.query_params.get('countries', '')
    countries = [c.strip() for c in countries_param.split(',') if c.strip()]
    
    #validation max 3 sauf world ou *
    if countries and countries[0] not in ['world', '*']:
        if len(countries) > 3:
            return Response(
                {'error': 'maximum 3 pays autorisés'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    #requête de base sur la table locations avec province_state
    queryset = Location.objects.exclude(province_state__isnull=True).exclude(province_state='')
    
    #filtre par pays si pas world
    if countries and countries[0] not in ['world', '*']:
        #normaliser les noms
        countries_normalized = [c.replace('_', ' ').title() for c in countries]
        queryset = queryset.filter(country__in=countries_normalized)
    
    #récupérer états avec pays
    states = queryset.values('province_state', 'country').distinct().order_by('country', 'province_state')
    
    #formater en {id, name, country}
    data = [
        {
            'id': state['province_state'].lower().replace(' ', '_'),
            'name': state['province_state'],
            'country': state['country'].lower().replace(' ', '_') if state['country'] else None
        }
        for state in states if state['province_state']
    ]
    
    return Response(data, status=status.HTTP_200_OK)


@extend_schema(exclude=True)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_admin2(request):
    #retourne la liste des admin2_usa filtrés par états
    states_param = request.query_params.get('states', '')
    states = [s.strip() for s in states_param.split(',') if s.strip()]
    
    #validation max 3 sauf world ou *
    if states and states[0] not in ['world', '*']:
        if len(states) > 3:
            return Response(
                {'error': 'maximum 3 états autorisés'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    #requête de base sur la table locations avec admin2_usa
    queryset = Location.objects.exclude(admin2_usa__isnull=True).exclude(admin2_usa='')
    
    #filtre par états si pas world
    if states and states[0] not in ['world', '*']:
        #normaliser les noms
        states_normalized = [s.replace('_', ' ').title() for s in states]
        queryset = queryset.filter(province_state__in=states_normalized)
    
    #récupérer les admin2
    admin2_list = queryset.values('admin2_usa', 'province_state').distinct().order_by('province_state', 'admin2_usa')
    
    #formater en [{id, name, state}]
    data = [
        {
            'id': admin2['admin2_usa'].lower().replace(' ', '_'),
            'name': admin2['admin2_usa'],
            'state': admin2['province_state'].lower().replace(' ', '_') if admin2['province_state'] else None
        }
        for admin2 in admin2_list if admin2['admin2_usa']
    ]
    
    return Response(data, status=status.HTTP_200_OK)


@extend_schema(
    summary="Données de pandémie",
    description="retourne la data (uniquement mensuelle pour l'instant)selon les filtres géographiques et métriques",
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'pandemie': {'type': 'string', 'example': 'COVID-19'},
                'startDate': {'type': 'string', 'format': 'date', 'example': '2020-01-01'},
                'endDate': {'type': 'string', 'format': 'date', 'example': '2020-12-31'},
                'granularity': {'type': 'string', 'enum': ['monthly'], 'example': 'monthly'},
                'continents': {'type': 'array', 'items': {'type': 'string'}, 'example': ['europe', 'asia']},
                'countries': {'type': 'array', 'items': {'type': 'string'}, 'example': ['france', 'italy']},
                'states': {'type': 'array', 'items': {'type': 'string'}, 'example': ['california']},
                'admin2': {'type': 'array', 'items': {'type': 'string'}, 'example': ['los_angeles']},
                'metrics': {'type': 'array', 'items': {'type': 'string'}, 'example': ['cases', 'deaths']}
            },
            'required': ['pandemie', 'startDate', 'endDate', 'granularity', 'metrics']
        }
    },
    responses={
        200: {
            'description': 'données pour chart.js',
            'content': {
                'application/json': {
                    'example': {
                        'abscisse': ['2020-01', '2020-02'],
                        'ordonne': [
                            {'label': 'Cas - France', 'data': [100, 200], 'type': 'line'}
                        ],
                        'data': [
                            {
                                'pandemie': 'COVID-19',
                                'country': 'France',
                                'values': [{'period': '2020-01', 'cases': 4000, 'deaths': 4000}]
                            }
                        ]
                    }
                }
            }
        },
    },
    tags=['Données']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_pandemic_data(request):
    # endpoint pour récupérer data de pandémie
    #vlidation du payload
    serializer = DataRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    #récupérer la pandémie
    try:
        pandemic = Pandemic.objects.get(pandemic_name=data['pandemie'])
    except Pandemic.DoesNotExist:
        return Response(
            {'error': f'pandémie "{data["pandemie"]}" introuvable'},
            status=status.HTTP_404_NOT_FOUND)
    
    #construction du queryset
    queryset = PandemicData.objects.filter(
        pandemic=pandemic,
        observation_date__gte=data['startDate'],
        observation_date__lte=data['endDate']
    )
    #appliquer les filtres géographiques
    location_filter = Q()
    filter_applied = None
    
    #priorité -- admin2
    admin2_list = data.get('admin2', [])
    if admin2_list and admin2_list[0] not in ['world', '*']:
        admin2_normalized = [a.replace('_', ' ').title() for a in admin2_list]
        location_filter = Q(location__admin2_usa__in=admin2_normalized)
        filter_applied = 'admin2'
    
    #priorité -- states (si admin2 vide)
    elif not filter_applied:
        states_list = data.get('states', [])
        if states_list and states_list[0] not in ['world', '*']:
            states_normalized = [s.replace('_', ' ').title() for s in states_list]
            location_filter = Q(location__province_state__in=states_normalized)
            filter_applied = 'states'
    
    #priorité -- countrie (si states et admin2 vides)
    if not filter_applied:
        countries_list = data.get('countries', [])
        if countries_list and countries_list[0] not in ['world', '*']:
            countries_normalized = [c.replace('_', ' ').title() for c in countries_list]
            location_filter = Q(location__country__in=countries_normalized)
            filter_applied = 'countries'
    
    #priorité -- continents (si tout le reste est vide)
    if not filter_applied:
        continents_list = data.get('continents', [])
        if continents_list and continents_list[0] not in ['world', '*']:
            continents_normalized = [c.replace('_', ' ').title() for c in continents_list]
            location_filter = Q(location__continent__in=continents_normalized)
            filter_applied = 'continents'
    
    #appliquer le filtre si défini
    if filter_applied:
        queryset = queryset.filter(location_filter)
    
    #agrégation mensuelle selon la granularité
    if data['granularity'] == 'monthly':
        #grouper par mois et location
        aggregated = queryset.annotate(
            period=TruncMonth('observation_date')
        ).values(
            'period',
            'location__continent',
            'location__country',
            'location__province_state',
            'location__admin2_usa',
            'location__population'
        ).annotate(
            total_cases=Sum('total_cases'),
            new_cases=Sum('new_cases'),
            total_deaths=Sum('total_deaths'),
            new_deaths=Sum('new_deaths'),
            total_recovered=Sum('total_recovered')
        ).order_by('period', 'location__country')
        
        #construction du dataset au fotmat chart.js
        response_data = build_chartjs_response(aggregated, data['metrics'], data['pandemie'])
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    else:
        #a voir si on implemente le mensuel et le daily par la suite
        return Response(
            {'error': 'daily/weekly pas encore implémentée'},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )


def build_chartjs_response(aggregated_data, metrics, pandemic_name):
    #fonction pour construire la réponse au format chart.js
    #organiser les données par période et location
    periods_set = set()
    data_by_location = defaultdict(lambda: defaultdict(dict))
    
    for row in aggregated_data:
        period_str = row['period'].strftime('%Y-%m')
        periods_set.add(period_str)
        #identifier la location 
        location_key = row['location__country']
        if row['location__province_state']:
            location_key = f"{row['location__country']} - {row['location__province_state']}"
        if row['location__admin2_usa']:
            location_key = f"{row['location__country']} - {row['location__province_state']} - {row['location__admin2_usa']}"
       


        #stocker les métriques pour cette période
        data_by_location[location_key][period_str] = {
            'cases': row['total_cases'] or 0,
            'new_cases': row['new_cases'] or 0,
            'deaths': row['total_deaths'] or 0,
            'new_deaths': row['new_deaths'] or 0,
            'recovered': row['total_recovered'] or 0,
            'continent': row['location__continent'],
            'country': row['location__country'],
            'province_state': row['location__province_state'],
            'admin2': row['location__admin2_usa'],
            'population': row['location__population']}
    
    #créer l'abscisse
    abscisse = sorted(list(periods_set))
    #créer les datasets pour chart.js et l'ordonné
    ordonne = []
    detailed_data = []
    
    #dataset par location et métrique
    for location_key, periods_data in data_by_location.items():
        #créer un dataset par métrique demandée
        for metric in metrics:
            metric_label_map = {
                'cases': 'Cas',
                'new_cases': 'Nouveaux cas',
                'deaths': 'Décès',
                'new_deaths': 'Nouveaux décès',
                'recovered': 'Guérisons'
            }
            label = f"{metric_label_map.get(metric, metric)} - {location_key}"
            #extraire les valeurs dans l'ordre des périodes
            values = [periods_data.get(period, {}).get(metric, 0) for period in abscisse]

            #type de graphique selon la métrique
            chart_type = 'bar' if 'new_' in metric else 'line'
            #ajouter au dataset pour l'ordonné
            ordonne.append({
                'label': label,
                'data': values,
                'type': chart_type
            })

        #ajouter les détails métiers (utile pour tooltips)
        location_details = {
            'pandemie': pandemic_name,
            'continent': None,
            'country': None,
            'province_state': None,
            'admin2': None,
            'meta': {'population': None},
            'values': []
        }
        #pour chaque période (l'abscisse)
        for period in abscisse:
            period_data = periods_data.get(period, {})
            
            #maj infos de location
            if not location_details['country']:
                location_details['continent'] = period_data.get('continent')
                location_details['country'] = period_data.get('country')
                location_details['province_state'] = period_data.get('province_state')
                location_details['admin2'] = period_data.get('admin2')
                location_details['meta']['population'] = period_data.get('population')
            
            #ajouter les valeurs pour cette période
            location_details['values'].append({
                'period': period,
                'cases': period_data.get('cases', 0),
                'new_cases': period_data.get('new_cases', 0),
                'deaths': period_data.get('deaths', 0),
                'new_deaths': period_data.get('new_deaths', 0),
                'recovered': period_data.get('recovered', 0)
            })
        detailed_data.append(location_details)
    
    return {
        'abscisse': abscisse,
        'ordonne': ordonne,
        'data': detailed_data
    }



@extend_schema(exclude=True)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# méthode ppour télécharger les données en csv
def download_pandemic_data_csv(request):
    serializer = DataRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    
    #récupérer la pandémie
    try:
        pandemic = Pandemic.objects.get(pandemic_name=data['pandemie'])
    except Pandemic.DoesNotExist:
        return Response(
            {'error': f'pandémie "{data["pandemie"]}" introuvable'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    #construction du query (on garde la meme logique que pour get_pandemic_data)
    queryset = PandemicData.objects.filter(
        pandemic=pandemic,
        observation_date__gte=data['startDate'],
        observation_date__lte=data['endDate']
    )
    
    # filtres géographiques
    location_filter = Q()
    filter_applied = None
    
    #priorité -- admin2
    admin2_list = data.get('admin2', [])
    if admin2_list and admin2_list[0] not in ['world', '*']:
        admin2_normalized = [a.replace('_', ' ').title() for a in admin2_list]
        location_filter = Q(location__admin2_usa__in=admin2_normalized)
        filter_applied = 'admin2'
    
    #priorité -- states
    elif not filter_applied:
        states_list = data.get('states', [])
        if states_list and states_list[0] not in ['world', '*']:
            states_normalized = [s.replace('_', ' ').title() for s in states_list]
            location_filter = Q(location__province_state__in=states_normalized)
            filter_applied = 'states'
    
    #priorité -- countries
    if not filter_applied:
        countries_list = data.get('countries', [])
        if countries_list and countries_list[0] not in ['world', '*']:
            countries_normalized = [c.replace('_', ' ').title() for c in countries_list]
            location_filter = Q(location__country__in=countries_normalized)
            filter_applied = 'countries'
    
    #priorité -- continents
    if not filter_applied:
        continents_list = data.get('continents', [])
        if continents_list and continents_list[0] not in ['world', '*']:
            continents_normalized = [c.replace('_', ' ').title() for c in continents_list]
            location_filter = Q(location__continent__in=continents_normalized)
            filter_applied = 'continents'
    
    #on applique le filtre
    if filter_applied:
        queryset = queryset.filter(location_filter)
    
    #agrégation mensuelle (pour le moment uniquement mensuelle)
    if data['granularity'] == 'monthly':
        aggregated = queryset.annotate(
            #truncMonth pour grouper par mois
            period=TruncMonth('observation_date')
        ).values(
            'period',
            'location__continent',
            'location__country',
            'location__province_state',
            'location__admin2_usa',
            'location__population',
            'location__who_region'
            #ajoute des champs utiles
        ).annotate(
            total_cases=Sum('total_cases'),
            new_cases=Sum('new_cases'),
            total_deaths=Sum('total_deaths'),
            new_deaths=Sum('new_deaths'),
            total_recovered=Sum('total_recovered')
        ).order_by('period', 'location__country')
        
        #créer le CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="pandemic_data_{pandemic.pandemic_name}_{data["startDate"]}_{data["endDate"]}.csv"'
        
        writer = csv.writer(response)
        
        #nom des colonnes du CSV
        writer.writerow([
            'Période',
            'Pandémie',
            'Continent',
            'Pays',
            'Province/État',
            'Admin2 (USA)',
            'Région OMS',
            'Population',
            'Cas totaux',
            'Nouveaux cas',
            'Décès totaux',
            'Nouveaux décès',
            'Guérisons totales'
        ])
        
        # on complète les lignes du CSV
        for row in aggregated:
            writer.writerow([
                row['period'].strftime('%Y-%m'),
                pandemic.pandemic_name,
                row['location__continent'] or '',
                row['location__country'] or '',
                row['location__province_state'] or '',
                row['location__admin2_usa'] or '',
                row['location__who_region'] or '',
                row['location__population'] or 0,
                row['total_cases'] or 0,
                row['new_cases'] or 0,
                row['total_deaths'] or 0,
                row['new_deaths'] or 0,
                row['total_recovered'] or 0
            ])
            #on retourne le fichier
        return response
    
    else:
        #a voir si on implemente le mensuel et le daily par la suite
        return Response(
            {'error': 'granularité daily/weekly pas encore implémentée'},
            status=status.HTTP_501_NOT_IMPLEMENTED
        )
