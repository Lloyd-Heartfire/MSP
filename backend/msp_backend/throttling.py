from rest_framework.throttling import UserRateThrottle


class BurstRateThrottle(UserRateThrottle):
    #throttling custom pour gérer les pics de requêtes en mode rafale
    #utile pour éviter quun user lance 50 requêtes dun coup comme un bourrin
    scope = 'burst'


class DataAPIThrottle(UserRateThrottle):
    #throttling spécifique pour lendpoint de data qui peut être lourd
    #on limite un peu plus serré ici vu que ca tape fort en db
    scope = 'data_api'
    rate = '100/hour'
