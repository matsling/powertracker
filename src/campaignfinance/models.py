import uuid
from django.db import models
from django.core.exceptions import ValidationError

# ID fields are created automatically


def validate_integer(value):
    if not isinstance(value, int):
        raise ValidationError("Value must be an integer")


class EntityCategory(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    name = models.CharField(
        max_length=300,
        unique=True,
    )

    def __str__(self):
        return f"{self.name}"


class IndustrySector(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    name = models.CharField(
        max_length=300,
        unique=True,
    )

    def __str__(self):
        return f"{self.name}"


class Industry(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    name = models.CharField(
        max_length=300,
        unique=True,
    )

    sector = models.ForeignKey(
        IndustrySector,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sector_industries",
    )

    def __str__(self):
        return f"{self.name}"


class Entity(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    category = models.ForeignKey(
        EntityCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="category_entities",
    )

    first_name = models.CharField(
        max_length=100,
        blank=True,
    )

    middle_name = models.CharField(
        max_length=100,
        blank=True,
    )

    last_name = models.CharField(
        max_length=300,
    )

    prefix = models.CharField(
        max_length=100,
        blank=True,
    )
    
    suffix = models.CharField(
        max_length=100,
        blank=True,
    )

    nickname = models.CharField(
        max_length=100,
        blank=True,
    )

    occupation = models.CharField(
        max_length=100,
        blank=True,
    )

    industry = models.ForeignKey(
        Industry,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='industry_entities',
    )

    notes = models.TextField(
        blank=True,
    )

    opencorporates_link = models.CharField(
        max_length=300,
        blank=True,
    )

    opencorporates_link = models.URLField(
        max_length=300,
        blank=True,
    )

    littlesis_link = models.CharField(
        max_length=300,
        blank=True,
    )

    def __str__(self):
        return f"{self.last_name}, {self.first_name} {self.middle_name} {self.suffix}"


# External IDs such as IRS, TEC, FEC, etc
class ExternalId(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    parent_entity = models.ForeignKey(
        Entity,
        on_delete=models.SET_NULL,
        null=True,
        related_name="entity_parent_ids",
    )

    child_entity = models.ForeignKey(
        Entity,
        on_delete=models.SET_NULL,
        null=True,
        related_name="entity_child_ids",
    )

    number = models.CharField(
        max_length=300,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    def __str__(self):
        return f"{self.number}"


class RelationshipCategory(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    name = models.CharField(
        max_length=300,
        unique=True,
    )

    def __str__(self):
        return f"{self.name}"


class Relationship(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    category = models.ForeignKey(
        RelationshipCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="category_relationships",
    )

    parent_entity = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name='entity_parent_relationships',
    )

    child_entity = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name='entity_child_relationships',
    )

    notes = models.TextField(
        blank=True,
    )

    def __str__(self):
        return f"{self.category} {self.parent_entity} {self.child_entity}"


class CampaignCategory(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    name = models.CharField(
        max_length=300,
        unique=True,
    )

    def __str__(self):
        return f"{self.name}"


class Office(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    government_entity = models.ForeignKey(
        Entity,
        on_delete=models.SET_NULL,
        null=True,
        related_name='entity_offices',
    )

    name = models.CharField(
        max_length=300,
    )

    holder_entity = models.ForeignKey(
        Entity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entity_holder_offices',
    )

    notes = models.TextField(
        blank=True,
    )

    def __str__(self):
        return f"{self.name}"


class FormerOfficeHolder(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    office = models.ForeignKey(
        Office,
        on_delete=models.SET_NULL,
        null=True,
        related_name='office_former_holders',
    )

    entity = models.ForeignKey(
        Entity,
        on_delete=models.SET_NULL,
        null=True,
        related_name='entity_former_offices',
    )

    def __str__(self):
        return f"{self.office} {self.entity}"


class ElectionCategory(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    name = models.CharField(
        max_length=300,
        unique=True,
    )

    def __str__(self):
        return f"{self.name}"


class Election(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    category = models.ForeignKey(
        ElectionCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="category_elections",
    )

    government_entity = models.ForeignKey(
        Entity,
        on_delete=models.SET_NULL,
        null=True,
        related_name='entity_government_elections',
    )

    # Date format is in YYYY-MM-DD as a string
    date = models.DateField()

    notes = models.TextField(
        blank=True,
    )

    def __str__(self):
        return f"{self.date}"


class Campaign(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    category = models.ForeignKey(
        CampaignCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="category_campaigns",
    )

    name = models.CharField(
        max_length=1000,
    )

    registration_date = models.DateField()

    election = models.ForeignKey(
        Election,
        on_delete=models.SET_NULL,
        null=True,
        related_name='election_campaigns',
    )

    candidate_entity = models.ForeignKey(
        Entity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entity_candidate_campaigns',
    )

    treasurer_entity = models.ForeignKey(
        Entity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entity_treasurer_campaigns',
    )

    committee_entity = models.ForeignKey(
        Entity,
        on_delete=models.SET_NULL,
        null=True,
        related_name='entity_committee_campaigns',
    )

    office_sought = models.ForeignKey(
        Office,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="office_campaigns",
    )

    notes = models.TextField(
        blank=True,
    )

    def __str__(self):
        return f"{self.name}"


class DocumentCategory(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    name = models.CharField(
        max_length=300,
        unique=True,
    )

    def __str__(self):
        return f"{self.name}"


class Document(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    category = models.ForeignKey(
        DocumentCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="category_documents",
    )

    name = models.CharField(
        max_length=1000,
    )

    filer_entity = models.ForeignKey(
        Entity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entity_document_filers",
    )

    officer_oath_entity = models.ForeignKey(
        Entity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entity_officer_oaths',
    )

    date_filed = models.DateField()
    coverage_start_date = models.DateField()
    coverage_end_date = models.DateField()

    uploaded_file = models.FileField(
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    def __str__(self):
        return f"{self.name}"


class ReportedTotals(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    document = models.OneToOneField(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        related_name='document_reported_totals',
    )

    unitemized_contributions = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    contributions = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    unitemized_expenditures = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    expenditures = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    maintained_contributions = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    principal_outstanding_loans = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    def __str__(self):
        return f"{self.document}"


class ReportedSubtotals(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    document = models.OneToOneField(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        related_name='document_reported_subtotals',
    )

    monetary_political_contributions = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    non_monetary_political_contributions = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    pledged_contributions = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    monetary_corporate_labor_contributions = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    non_monetary_corporate_labor_contributions = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    pledged_corporate_labor_contributions = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    loans = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    expenditures_from_contributions = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    unpaid_incurred_obligations = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    purchased_investments_with_contributions = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    expenditures_credit_card = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    expenditures_personal_funds = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    expenditures_from_contributions_candidate_business = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    expenditures_non_political_from_contributions = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    interest_credit_gains_refunds_contributions_returned = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    def __str__(self):
        return f"{self.document}"


class TransactionCategory(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    name = models.CharField(
        max_length=300,
        unique=True,
    )

    def __str__(self):
        return f"{self.name}"


class Transaction(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    category = models.ForeignKey(
        TransactionCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="category_transactions",
    )

    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.SET_NULL,
        null=True,
        related_name='campaign_transactions',
    )

    payer_entity = models.ForeignKey(
        Entity,
        on_delete=models.SET_NULL,
        null=True, 
        related_name="entity_payer_transactions",
    )

    payee_entity = models.ForeignKey(
        Entity,
        on_delete=models.SET_NULL,
        null=True,
        related_name="entity_payee_transactions",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    recorded_date = models.DateField(
        blank=True,
    )

    reason = models.CharField(
        max_length=1000,
        blank=True,
    )

    document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        related_name="document_transactions",
    )

    notes = models.TextField(
        blank=True,
    )

    def __str__(self):
        return f"{self.category} {self.payer_entity} {self.payee_entity} {self.amount}"


class AddressCategory(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    name = models.CharField(
        max_length=300,
        unique=True,
    )

    def __str__(self):
        return f"{self.name}"


class Address(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    category = models.ForeignKey(
        AddressCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="category_addresses",
    )

    building_number = models.CharField(
        max_length=300,
        blank=True,
    )

    street_name = models.CharField(
        max_length=300,
        blank=True,
    )

    unit_number = models.CharField(
        max_length=300,
        blank=True,
    )

    floor_number = models.CharField(
        max_length=300,
        blank=True,
    )

    city_name = models.CharField(
        max_length=300,
        blank=True,
    )

    state_name = models.CharField(
        max_length=300,
        blank=True,
    )

    county_name = models.CharField(
        max_length=300,
        blank=True,
    )

    zip_code = models.CharField(
        max_length=300,
    )

    zip_code_extension = models.CharField(
        max_length=300,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    # Defines the assocation table to express residency at an address
    residents = models.ManyToManyField(
        Entity,
        related_name="entity_residences",
        blank=True,
    )

    # Defines the association table to express ownership of an address
    owners = models.ManyToManyField(
        Entity,
        related_name="entity_owners",
        blank=True,
    )

    def __str__(self):
        return f"{self.building_number} {self.unit_number} {self.city_name} {self.state_name} {self.zip_code}"


class PhoneNumber(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    country_code = models.CharField(
        max_length=2,
        blank=True,
    )

    area_code = models.CharField(
        max_length=3,
        blank=True,
    )

    number = models.CharField(
        max_length=7,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    owner = models.ForeignKey(
        Entity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entity_phone_number_owners',
    )

    # Defines the association table for entities and phone numbers
    associated_entities = models.ManyToManyField(
        Entity,
        related_name="entity_phone_numbers",
        blank=True,
    )

    def __str__(self):
        return f"{self.area_code} {self.number}"


class Email(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    address = models.CharField(
        max_length=300,
        unique=True,
    )

    owner = models.ForeignKey(
        Entity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entity_email_owners',
    )

    notes = models.TextField(
        blank=True,
    )

    # Defines assocation table for entities and email addresses
    associated_entities = models.ManyToManyField(
        Entity,
        related_name="entity_emails",
        blank=True,
    )

    def __str__(self):
        return f"{self.address}"


class Website(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    address = models.CharField(
        max_length=300,
        unique=True,
    )

    owner = models.ForeignKey(
        Entity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entity_website_owners',
    )

    notes = models.TextField(
        blank=True,
    )

    # Defines the association table for entites and websites
    associated_entities = models.ManyToManyField(
        Entity,
        related_name="entity_websites",
        blank=True,
    )

    def __str__(self):
        return f"{self.address}"


class AssumedName(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    name = models.CharField(
        max_length=300,
    )

    notes = models.TextField(
        blank=True,
    )

    # Defines the association table for entites and assumed names (DBA)
    associated_entities = models.ManyToManyField(
        Entity,
        related_name="entity_assumed_names",
        blank=True,
    )

    def __str__(self):
        return f"{self.name}"
