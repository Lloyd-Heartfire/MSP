from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.core.exceptions import ValidationError


class UserProfile(models.Model):
    # use Django User model
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    # add extra fields
    user_function = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="Function"
    )
    
    user_organization = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="Organization",
        help_text="Organization or company where the user works"
    )
    
    last_connection = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name="Last connection"
    )
    
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Creation date"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Update date"
    )

    class Meta:
        db_table = 'user_profiles'
        verbose_name = "User profile"
        verbose_name_plural = "User profiles"
        
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.user_organization}"

    @property
    def full_name(self):
        # returns the user name
        return f"{self.user.first_name} {self.user.last_name}".strip()


# function to create additional role groups
def create_user_groups():
    # list of groups corresponding
    groups_config = {
        'admin': {
            'description': 'Administrateur système - accès complet'
        },
        'analyst': {
            'description': 'Analyste de données - consulter, analyser et faire des rapports'
        },
        'viewer': {
            'description': 'Visualiseur - lecture données et tableaux de bord'
        },
        'api_user': {
            'description': 'Utilisateur API'
        }
    }
    
    # in case is not created
    created_groups = []
    for group_name, config in groups_config.items():
        group, created = Group.objects.get_or_create(
            name=group_name,
            defaults={'name': group_name}
        )
        if created:
            created_groups.append(group_name)
    
    return created_groups


# model for Pandemics
class Pandemic(models.Model):
    PATHOGENE_CHOICES = [
        ('virus', 'Virus'),
        ('bacteria', 'Bacteria'),
        ('fungi', 'Fungi'),
        ('parasite', 'Parasite'),
    ]
    
    WHO_CLASSIFICATION_CHOICES = [
        ('pandemic', 'Pandemic'),
        ('epidemic', 'Epidemic'),
        ('outbreak', 'Outbreak'),
    ]
    
    pandemic_name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name="Nom de la pandémie"
    )
    
    start_date = models.DateField(
        null=False,
        blank=False,
        verbose_name="Date de début"
    )
    
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de fin",
        help_text="NULL si pandémie active"
    )
    
    pandemic_description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description"
    )
    
    pathogene_agent = models.CharField(
        max_length=50,
        choices=PATHOGENE_CHOICES,
        blank=True,
        null=True,
        verbose_name="Agent pathogène"
    )
    
    who_classification = models.CharField(
        max_length=50,
        choices=WHO_CLASSIFICATION_CHOICES,
        blank=True,
        null=True,
        verbose_name="Classification WHO"
    )
    
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Date de création"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de mise à jour"
    )

    class Meta:
        db_table = 'pandemics'
        verbose_name = "Pandémie"
        verbose_name_plural = "Pandémies"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.pandemic_name} ({self.start_date})"

    @property
    def duration_days(self):
        # calcule la durée en jours depuis le début si pandemie active
        end = self.end_date or timezone.now().date() 
        return (end - self.start_date).days

# model for Locations
class Location(models.Model):
    # continent = models.CharField(
    #     max_length=50,
    #     null=False,
    #     blank=False,
    #     verbose_name="Continent"
    # )
    
    country = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name="Pays"
    )
    
    province_state = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Province/État",
        help_text="Subdivision administrative si disponible"
    )
    
    city = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="City",
    )
    
    iso_code = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="Code ISO"
    )
    
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=8,
        null=True,
        blank=True,
        verbose_name="Latitude",
        help_text="Coordonnées GPS précises"
    )
    
    longitude = models.DecimalField(
        max_digits=11,
        decimal_places=8,
        null=True,
        blank=True,
        verbose_name="Longitude",
        help_text="Coordonnées GPS précises"
    )
    
    population = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Population"
    )
    
    who_region = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Région WHO"
    )
    
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Date de création"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de mise à jour"
    )

    class Meta:
        db_table = 'locations'
        verbose_name = "Localisation"
        verbose_name_plural = "Localisations"
        # Index 
        indexes = [
            models.Index(fields=['country', 'province_state'], name='idx_location_hierarchy'),
            models.Index(fields=['who_region'], name='idx_who_region'),
        ]

    def __str__(self):
        if self.province_state:
            return f"{self.province_state}, {self.country}"
        return f"{self.country}"


    @property
    def full_location(self):
        #localisation pays province
        parts = [self.country]
        if self.province_state:
            parts.append(self.province_state)
        if self.city:
            parts.append(self.city)
        return " > ".join(parts)

    @property
    def coordinates(self):
        # donne les cordonnées GPS 
        if self.latitude and self.longitude:
            return f"{self.latitude}, {self.longitude}"
        return None

# model for Data Sources
class DataSource(models.Model):
    SOURCE_TYPE_CHOICES = [
        ('official', 'Official'),
        ('academic', 'Academic'),
        ('aggregator', 'Aggregator'),
    ]
    
    source_name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name="Nom de la source",
        help_text="Our World in Data, JHU CSSE, WHO"
    )
    
    source_url = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="URL de la source"
    )
    
    source_type = models.CharField(
        max_length=50,
        choices=SOURCE_TYPE_CHOICES,
        null=True,
        blank=True,
        verbose_name="Type de source"
    )
    
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Date de création"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de mise à jour"
    )

    class Meta:
        db_table = 'sources'
        verbose_name = "Source de données"
        verbose_name_plural = "Sources de données"
        ordering = ['source_name']

    def __str__(self):
        return f"{self.source_name} ({self.get_source_type_display()})"

    @property
    def is_official(self):
        # indique si la source est officielle
        return self.source_type == 'official'

    @property 
    def reliability_score(self):
        # score en fonction du niveau de fiabilité sur 10 ( à voir si on garde)
        scores = {
            'official': 10,
            'academic': 8,
            'aggregator': 6,
        }
        return scores.get(self.source_type, 5)

# model for Data Files
class DataFile(models.Model):
    file_name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name="Nom du fichier"
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploaded_files',
        verbose_name="Utilisateur"
    )
    
    source = models.ForeignKey(
        DataSource,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name="Source de données"
    )
    
    upload_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="Date d'import"
    )

    class Meta:
        db_table = 'files'
        verbose_name = "Fichier de données"
        verbose_name_plural = "Fichiers de données"
        ordering = ['-upload_date']
        # Index 
        indexes = [
            models.Index(fields=['source'], name='idx_source_tracking'),
            models.Index(fields=['user'], name='idx_user_files'),
        ]

    def __str__(self):
        return f"{self.file_name} - {self.source.source_name}"

    @property
    def uploader_name(self):
        # le nom de la personne qui upload
        return f"{self.user.first_name} {self.user.last_name}".strip()

    @property
    def file_age_days(self):
        # âge du fichier en jours
        return (timezone.now() - self.upload_date).days

    @property
    def source_reliability(self):
        # score de fiabilité de la source
        return self.source.reliability_score

# model for Pandemic Data
class PandemicData(models.Model):
    pandemic = models.ForeignKey(
        Pandemic,
        on_delete=models.RESTRICT,
        related_name='data_points',
        verbose_name="Pandémie"
    )
    
    location = models.ForeignKey(
        Location,
        on_delete=models.RESTRICT,
        related_name='pandemic_data',
        verbose_name="Localisation"
    )
    
    file = models.ForeignKey(
        DataFile,
        on_delete=models.RESTRICT,
        related_name='data_records',
        verbose_name="Fichier source"
    )
    
    observation_date = models.DateField(
        null=False,
        blank=False,
        verbose_name="Date d'observation"
    )
    
    # Données cumulées 
    total_cases = models.PositiveIntegerField(
        default=0,
        verbose_name="Cas cumulés confirmés"
    )
    
    new_cases = models.PositiveIntegerField(
        default=0,
        verbose_name="Nouveaux cas quotidiens"
    )
    
    total_deaths = models.PositiveIntegerField(
        default=0,
        verbose_name="Décès cumulés"
    )
    
    new_deaths = models.PositiveIntegerField(
        default=0,
        verbose_name="Nouveaux décès quotidiens"
    )
    
    total_recovered = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Total guérisons",
        help_text="Peut être NULL si pas rapporté"
    )
    
    active_cases = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Cas actifs",
        help_text="Calculé ou rapporté selon source"
    )
    
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Date de création"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de mise à jour"
    )

    class Meta:
        db_table = 'pandemics_data'
        verbose_name = "Donnée de pandémie"
        verbose_name_plural = "Données de pandémies"
        ordering = ['-observation_date', 'location__country']
        
        # Index 
        indexes = [
            models.Index(fields=['observation_date'], name='idx_time_series'),
            models.Index(fields=['file'], name='idx_file_tracking'),
        ]
        
        constraints = [
            models.UniqueConstraint(
                fields=['pandemic', 'location', 'observation_date'], 
                name='idx_unique_observation'
            ),
        ]

    def __str__(self):
        return f"{self.pandemic.pandemic_name} - {self.location} ({self.observation_date})"



# fonction pour valider les données (nbr de mort et nbr de cas)
    def clean(self):
        errors = {}
    
        # >= 0 (PositiveIntegerField) mais également le nbr de décès ne peut pas dépasser le nbr de cas
        if self.total_deaths > self.total_cases:
            errors['total_deaths'] = 'le nbre de décès ne peut pas dépasser le nbre total de cas'
        
        # les guérisons ne peuvent pas dépasser les cas totaux
        if self.total_recovered and self.total_recovered > self.total_cases:
            errors['total_recovered'] = 'le nbre de guérisons ne peut pas dépasser le nbre total de cas'
        
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


