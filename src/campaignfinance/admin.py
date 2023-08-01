from django.contrib import admin

from .models import (Industry, IndustrySector, EntityCategory, Entity, ExternalId,
                    RelationshipCategory, Relationship, CampaignCategory, Office,
                    FormerOfficeHolder, Campaign, ElectionCategory, Election,
                    DocumentCategory, Document, ReportedTotals, ReportedSubtotals,
                    TransactionCategory, Transaction, AddressCategory, Address,
                    PhoneNumber, Email, Website, AssumedName)


class EntityFilterModelAdmin(admin.ModelAdmin):
    entity_categories = {}

    def get_queryset_by_type(self, name):
        category = EntityCategory.objects.get(name=name)
        entities_queryset = Entity.objects.filter(category=category)
        if entities_queryset.exists():
            return entities_queryset
        else:
            return Entity.objects.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print(db_field.name)
        if db_field.name in self.entity_categories:
            entity_category_name = self.entity_categories[db_field.name]
            kwargs['queryset'] = self.get_queryset_by_type(entity_category_name)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class EntityCategoryAdmin(admin.ModelAdmin):
    fields = ['name']


admin.site.register(EntityCategory, EntityCategoryAdmin)


class IndustrySectorAdmin(admin.ModelAdmin):
    fields = ['name']


admin.site.register(IndustrySector, IndustrySectorAdmin)


class IndustryAdmin(admin.ModelAdmin):
    fields = ['name', 'sector']

    search_fields = ['name']


admin.site.register(Industry, IndustryAdmin)


class EntityAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['category']}),
        ('Name', {'fields': ['prefix', 'first_name', 'middle_name', 'last_name', 'suffix', 'nickname']}),
        ('Employment', {'fields': ['occupation', 'industry']}),
        ('Notes', {'fields': ['notes']})
    ]

    search_fields = ['first_name', 'middle_name', 'last_name']

    autocomplete_fields = ['industry']


admin.site.register(Entity, EntityAdmin)


class ExternalIdAdmin(EntityFilterModelAdmin):
    entity_categories = {
        'parent_entity': 'government'
    }

    def reporting_agency(self, obj):
        return obj.parent_entity.last_name

    def reported_entity(self, obj):
        return obj.child_entity.last_name

    fieldsets = [
        ('Reporting Agency', {'fields': ['parent_entity']}),
        ('Organization', {'fields': ['child_entity']}),
        ('Agency Internal ID Number', {'fields': ['number']})
    ]

    list_display = ('reporting_agency', 'reported_entity', 'number')

    autocomplete_fields = ['parent_entity', 'child_entity']


admin.site.register(ExternalId, ExternalIdAdmin)


class RelationshipCategoryAdmin(admin.ModelAdmin):
    fields = ['name']


admin.site.register(RelationshipCategory, RelationshipCategoryAdmin)


class RelationshipAdmin(admin.ModelAdmin):
    def parent_entity(self, obj):
        return f"{obj.parent_entity.first_name} {obj.parent_entity.last_name}"

    def child_entity(self, obj):
        return f"{obj.child_entity.first_name} {obj.child_entity.last_name}"

    fieldsets = [
        ('Relationship Type', {'fields': ['category']}),
        ('Relationship Members', {'fields': ['parent_entity', 'child_entity']}),
        ('Notes', {'fields': ['notes']})
    ]

    list_display = ('category', 'parent_entity', 'child_entity')

    autocomplete_fields = ['parent_entity', 'child_entity']


admin.site.register(Relationship, RelationshipAdmin)


class CampaignCategoryAdmin(admin.ModelAdmin):
    fields = ['name']


admin.site.register(CampaignCategory, CampaignCategoryAdmin)


class OfficeAdmin(EntityFilterModelAdmin):

    entity_categories = {
        'government_entity': 'government',
        'holder_entity': 'individual'
    }

    def government(self, obj):
        return f"{obj.government_entity.last_name}"

    def office_holder(self, obj):
        holder = ''

        if obj.holder_entity:
            holder = f"{obj.holder_entity.first_name} {obj.holder_entity.last_name}"
        
        return holder

    fields = ['name', 'government_entity', 'holder_entity']

    list_display = ('name', 'government_entity', 'office_holder')

    search_fields = ['name']

    autocomplete_fields = ['government_entity', 'holder_entity']


admin.site.register(Office, OfficeAdmin)


class FormerOfficeHolderAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Office', {'fields': ['office']}),
        ('Former Office Holder', {'fields': ['entity']})
    ]

    list_display = ('office', 'entity')

    autocomplete_fields = ['office', 'entity']


admin.site.register(FormerOfficeHolder, FormerOfficeHolderAdmin)


class CampaignAdmin(EntityFilterModelAdmin):
    entity_categories = {
        'candidate_entity': 'individual',
        'treasurer_entity': 'individual',
        'committee_entity': 'committee',
    }

    fieldsets = [
        (None, {'fields': ['category', 'name', 'registration_date']}),
        ('Office Information', {'fields': ['office_sought']}),
        ('Campaign Members', {'fields': ['candidate_entity', 'treasurer_entity', 'committee_entity']}),
        ('Notes', {'fields': ['notes']}),
        ('Elections' , {'fields': ['election']})
    ]

    list_display = ['name',
                    'registration_date',
                    'committee_entity',
                    'category',
                    'candidate_entity',
                    'office_sought',
    ]

    search_fields = ['name']

    autocomplete_fields = ['election', 'office_sought', 'candidate_entity', 'treasurer_entity', 'committee_entity']


admin.site.register(Campaign, CampaignAdmin)


class ElectionCategoryAdmin(admin.ModelAdmin):
    fields = ['name']


admin.site.register(ElectionCategory, ElectionCategoryAdmin)


class ElectionAdmin(EntityFilterModelAdmin):
    entity_categories = {
        'government_entity': 'government'
    }

    fieldsets = [
        (None, {'fields': ['category']}),
        ('Election Information', {'fields': ['government_entity', 'date']}),
        ('Notes', {'fields': ['notes']})
    ]

    list_display = ['date', 'government_entity', 'category']

    search_fields = ['date']

    autocomplete_fields = ['government_entity']


admin.site.register(Election, ElectionAdmin)


class DocumentCategoryAdmin(admin.ModelAdmin):
    fields = ['name']


admin.site.register(DocumentCategory, DocumentCategoryAdmin)


class DocumentAdmin(EntityFilterModelAdmin):
    entity_categories = {
        'officer_oath_entity': 'individual'
    }

    fieldsets = [
        (None, {'fields': ['category']}),
        ('Document Information', {'fields': ['name', 'filer_entity', 'officer_oath_entity']}),
        ('Dates', {'fields': ['date_filed', 'coverage_start_date', 'coverage_end_date']}),
        ('File Information', {'fields': ['uploaded_file']}),
        ('Notes', {'fields': ['notes']})
    ]

    list_display = ['name', 'category', 'date_filed']

    search_fields = ['name']

    autocomplete_fields = ['filer_entity', 'officer_oath_entity']


admin.site.register(Document, DocumentAdmin)


class ReportedTotalsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Parent Document', {'fields': ['document']}),
        ('Contributions', {'fields': [
            'unitemized_contributions',
            'contributions'
        ]}),
        ('Expenditures', {'fields': [
            'unitemized_expenditures',
            'expenditures',
        ]}),
        ('Maintained Contributions', {'fields': [
            'maintained_contributions'
        ]}),
        ('Loans', {'fields': [
            'principal_outstanding_loans'
        ]})
    ]

    list_display = ['document', 'contributions', 'expenditures']

    autocomplete_fields = ['document']


admin.site.register(ReportedTotals, ReportedTotalsAdmin)


class ReportedSubtotalsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Parent Document', {'fields': [
            'document',
        ]}),
        ('Contributions', {'fields': [
            'monetary_political_contributions',
            'non_monetary_political_contributions',
            'pledged_contributions',
            'monetary_corporate_labor_contributions',
            'non_monetary_corporate_labor_contributions',
            'pledged_corporate_labor_contributions',
        ]}),
        ('Expenditures', {'fields': [
            'expenditures_from_contributions',
            'purchased_investments_with_contributions',
            'expenditures_credit_card',
            'expenditures_personal_funds',
            'expenditures_from_contributions_candidate_business',
            'expenditures_non_political_from_contributions',
        ]}),
        ('Loans', {'fields': [
            'loans',
        ]}),
        ('Unpaid Obligations', {'fields': [
            'unpaid_incurred_obligations',
        ]}),
        ('Gains/Interest/Credits/Refunds', {'fields': [
            'interest_credit_gains_refunds_contributions_returned',
        ]})
    ]

    list_display = [
        'document',
        'monetary_political_contributions',
        'expenditures_from_contributions',
    ]

    autocomplete_fields = ['document']


admin.site.register(ReportedSubtotals, ReportedSubtotalsAdmin)


class TransactionCategoryAdmin(admin.ModelAdmin):
    fields = ['name']


admin.site.register(TransactionCategory, TransactionCategoryAdmin)


class TransactionAdmin(EntityFilterModelAdmin):
    entity_categories = {
        'government_entity': 'government',
    }

    fieldsets = [
        (None, {'fields': ['category']}),
        ('Campaign', {'fields': ['campaign']}),
        ('Payer', {'fields': ['payer_entity']}),
        ('Recipient', {'fields': ['payee_entity']}),
        ('Amount', {'fields': ['amount']}),
        ('Date', {'fields': ['recorded_date']}),
        ('Transaction Information', {'fields': [
            'reason',
            'document',
        ]}),
        ('Notes', {'fields': ['notes']}),
    ]

    list_display = ['recorded_date', 'payer_entity', 'payee_entity', 'amount']

    autocomplete_fields = ['campaign', 'payer_entity', 'payee_entity', 'document']


admin.site.register(Transaction, TransactionAdmin)


class AddressCategoryAdmin(admin.ModelAdmin):
    fields = ['name']


admin.site.register(AddressCategory, AddressCategoryAdmin)


class AddressAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['category']}),
        ('Street Address', {'fields': [
            'building_number',
            'street_name',
            'unit_number',
            'floor_number',
            'city_name',
            'state_name',
            'county_name',
        ]}),
        ('Zip Code', {'fields': [
            'zip_code',
            'zip_code_extension',
        ]}),
        ('Notes', {'fields': ['notes']}),
        ('Residents', {'fields': ['residents']}),
        ('Owners', {'fields': ['owners']})
    ]

    list_display = [
        'category',
        'building_number',
        'street_name',
        'unit_number',
        'city_name',
        'state_name',
        'zip_code',
    ]

    autocomplete_fields = ['residents','owners']


admin.site.register(Address, AddressAdmin)


class PhoneNumberAdmin(admin.ModelAdmin):
    fields = [
        'country_code',
        'area_code',
        'number',
        'owner',
        'notes',
        'associated_entities',
    ]

    list_display = [
        'area_code',
        'number',
        'owner',
    ]

    autocomplete_fields = ['owner', 'associated_entities']


admin.site.register(PhoneNumber, PhoneNumberAdmin)


class EmailAdmin(admin.ModelAdmin):
    fields = [
        'address',
        'owner',
        'notes',
        'associated_entities',
    ]

    list_display = [
        'address',
        'owner',
    ]

    autocomplete_fields = ['owner', 'associated_entities']


admin.site.register(Email, EmailAdmin)


class WebsiteAdmin(admin.ModelAdmin):
    fields = [
        'address',
        'owner',
        'notes',
        'associated_entities',
    ]

    list_display = [
        'address',
        'owner',
    ]

    autocomplete_fields = ['owner', 'associated_entities']


admin.site.register(Website, WebsiteAdmin)


class AssumedNameAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'notes',
        'associated_entities',
    ]

    list_display = ['name']

    autocomplete_fields = ['associated_entities']


admin.site.register(AssumedName, AssumedNameAdmin)
