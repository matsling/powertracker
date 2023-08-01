from django.views import generic
from django.shortcuts import render
from django.http import Http404

# Models from campaign finance
from .models import (EntityCategory, Entity, ExternalId, IndustrySector, Industry,
                    FormerOfficeHolder, RelationshipCategory, Relationship, CampaignCategory,
                    Campaign, Office, ElectionCategory, Election,
                    DocumentCategory, Document, ReportedTotals,
                    ReportedSubtotals, TransactionCategory, Transaction,
                    AddressCategory, Address, PhoneNumber, Email, Website,
                    AssumedName)

# Add easy urls like /spending and /giving that go to transaction
# fields with relevant arguments to only show relavent transactions


class HomePageIndex(generic.ListView):
    template_name = 'campaignfinance/index.html'
    context_object_name = 'transaction_list'

    def get_queryset(self):
        return Transaction.objects.filter(category__name='contribution').order_by('-recorded_date')[:10]


def glossaryindex(request):
    return render(request, 'campaignfinance/glossaryindex.html')


class EntityIndexView(generic.ListView):
    template_name = 'campaignfinance/entityindex.html'
    context_object_name = 'entity_list'

    filter_categories = {
        'select': None,
        'person': 'individual',
        'company': 'corporation',
        'religious': 'religious',
        'government': 'government',
        'committee': 'committee',
    }

    sort_by_fields = {
        'select': 'last_name',
        'first name': 'first_name',
        'last name': 'last_name',
        'industry': 'industry',
    }

    def get_queryset(self):
        try:
            category_name = self.filter_categories[self.request.GET.get('category')]
        except KeyError:
            category_name = None
        sort_by = self.sort_by_fields[self.request.GET.get('sortby', 'last name')]

        if category_name is not None:
            category = EntityCategory.objects.get(name=category_name)
            queryset = Entity.objects.filter(category=category).order_by(sort_by)
        else:
            queryset = Entity.objects.all().order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = self.request.GET.get('category')
        sortby = self.request.GET.get('sortby')
        context['filter_categories'] = self.filter_categories
        context['sort_by_fields'] = self.sort_by_fields
        context['selected_category'] = category
        context['selected_sortby'] = sortby
        
        return context


class EntityDetailView(generic.DetailView):
    model = Entity
    template_name = 'campaignfinance/entitydetail.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


class IndustrySectorIndexView(generic.ListView):
    template_name = 'campaignfinance/industrysectorindex.html'
    context_object_name = 'industry_sector_list'

    # default sort by sector name

    def get_queryset(self):
        return IndustrySector.objects.all().order_by('name')


class IndustrySectorDetailView(generic.DetailView):
    model = IndustrySector
    template_name = 'campaignfinance/industrysectordetail.html'
    slug_field = "uuid"
    slug_url_kwarg = "uuid"


class IndustryIndexView(generic.ListView):
    model = Industry
    template_name = 'campaignfinance/industryindex.html'
    context_object_name = "industry_list"

    def get_queryset(self):
        return Industry.objects.all().order_by('name')


class ExternalIdIndexView(generic.ListView):
    model = ExternalId
    template_name = 'campaignfinance/externalidindex.html'
    context_object_name = 'external_id_list'

    def get_queryset(self):
        return ExternalId.objects.all().order_by('pk')


class ExternalIdDetailView(generic.DetailView):
    model = ExternalId
    template_name = 'campaignfinance/externaliddetail.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


class RelationshipIndexView(generic.ListView):
    model = Relationship
    template_name = 'campaignfinance/relationshipindex.html'
    context_object_name = "relationship_list"

    filter_categories = {
        'select': None,
        'spouse': 'spouse',
        'employer': 'employer',
        'family': 'family',
        'owner': 'owner',
    }

    sort_by_fields = {
        'select': 'category',
        'category': 'category',
        'member 1': 'parent_entity',
        'member 2': 'child_entity',
    }

    # sorty by category on default

    def get_queryset(self):
        try:
            category_name = self.filter_categories[self.request.GET.get('category')]
        except KeyError:
            category_name = None
        sort_by = self.sort_by_fields[self.request.GET.get('sortby', 'category')]

        if category_name is not None:
            category = RelationshipCategory.objects.get(name=category_name)
            queryset = Relationship.objects.filter(category=category).order_by(sort_by)
        else:
            queryset = Relationship.objects.all().order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = self.request.GET.get('category')
        sortby = self.request.GET.get('sortby')

        context['filter_categories'] = self.filter_categories
        context['sort_by_fields'] = self.sort_by_fields
        context['selected_category'] = category
        context['selected_sortby'] = sortby
        
        return context


class RelationshipDetailView(generic.DetailView):
    model = Relationship
    template_name = 'campaignfinance/relationshipdetail.html'
    slug_field = "uuid"
    slug_url_kwarg = "uuid"


class CampaignIndexView(generic.ListView):
    model = Campaign
    template_name = 'campaignfinance/campaignindex.html'
    context_object_name = "campaign_list"

    filter_categories = {
        'select category': None,
        'candidate': 'candidate',
        'recall': 'recall',
        'ballot initiative': 'ballot initiative',
    }

    sort_by_fields = {
        'select': 'name',
        'name': 'name',
        'date': 'registration_date',
        'office': 'office_sought',
    }

    def get_queryset(self):
        try:
            category_name = self.filter_categories[self.request.GET.get('category')]
        except KeyError:
            category_name = None
        sort_by = self.sort_by_fields[self.request.GET.get('sortby', 'name')]

        if category_name is not None:
            category = CampaignCategory.objects.get(name=category_name)
            queryset = Campaign.objects.filter(category=category).order_by(sort_by)
        else:
            queryset = Campaign.objects.all().order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = self.request.GET.get('category')
        sortby = self.request.GET.get('sortby')

        context['filter_categories'] = self.filter_categories
        context['sort_by_fields'] = self.sort_by_fields
        context['selected_category'] = category
        context['selected_sortby'] = sortby
        
        return context



class CampaignDetailView(generic.DetailView):
    model = Campaign
    template_name = 'campaignfinance/campaigndetail.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


class OfficeIndexView(generic.ListView):
    model = Office
    template_name = 'campaignfinance/officeindex.html'
    context_object_name = 'office_list'

    sort_by_fields = {
        'select': 'name',
        'title': 'name',
        'government': 'government_entity',
        'current office holder': 'holder_entity',
    }

    # default sort by title/name of office

    def get_queryset(self):
        sort_by = self.sort_by_fields[self.request.GET.get('sortby', 'title')]
        queryset = Office.objects.all().order_by(sort_by)

        return queryset

    def get_context_date(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sortby = self.request.GET.get('sortby')
        context['sort_by_fields'] = self.sort_by_fields
        context['selected_sortby'] = sortby

        return context


class OfficeDetailView(generic.DetailView):
    model = Office
    template_name = 'campaignfinance/officedetail.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


class FormerOfficeHolderIndexView(generic.ListView):
    model = FormerOfficeHolder
    template_name = 'campaignfinance/formerofficeholderindex.html'
    context_object_name = 'former_office_holder_list'

    sort_by_fields = {
        'select': 'office',
        'office': 'office',
        'former holder': 'entity',
    }

    def get_queryset(self):
        sort_by = self.sort_by_fields[self.request.GET.get('sortby', 'office')]
        queryset = FormerOfficeHolder.objects.all().order_by(sort_by)

        return queryset

    def get_context_date(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sortby = self.request.GET.get('sortby')
        context['sort_by_fields'] = self.sort_by_fields
        context['selected_sortby'] = sortby

        return context


class ElectionIndexView(generic.ListView):
    model = Election
    template_name = 'campaignfinance/electionindex.html'
    context_object_name = 'election_list'

    filter_categories = {
        'select': None,
        'primary': 'primary',
        'runoff': 'runoff',
        'general': 'general',
    }

    sort_by_fields = {
        'select': '-date',
        'date': '-date',
        'government juridiction': 'government_entity',
    }

    # default sort by latest

    def get_queryset(self):
        try:
            category_name = self.filter_categories[self.request.GET.get('category')]
        except KeyError:
            category_name = None
        sort_by = self.sort_by_fields[self.request.GET.get('sortby', 'date')]

        if category_name is not None:
            category = ElectionCategory.objects.get(name=category_name)
            queryset = Election.objects.filter(category=category).order_by(sort_by)
        else:
            queryset = Election.objects.all().order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = self.request.GET.get('category')
        sortby = self.request.GET.get('sortby')

        context['filter_categories'] = self.filter_categories
        context['sort_by_fields'] = self.sort_by_fields
        context['selected_category'] = category
        context['selected_sortby'] = sortby
        
        return context


class ElectionDetailView(generic.DetailView):
    model = Election
    template_name = 'campaignfinance/electiondetail.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


class DocumentIndexView(generic.ListView):
    model = Document
    template_name = 'campaignfinance/documentindex.html'
    context_object_name = 'document_list'

    sort_by_fields = {
        'select': '-date_filed',
        'name': 'name',
        'date': 'date_filed',
        'coverage start': 'coverage_start_date',
        'coverage end' : 'coverage_end_date',
    }

    # default sort by latest

    def get_queryset(self):
        sort_by = self.sort_by_fields[self.request.GET.get('sortby', 'date')]
        queryset = Document.objects.all().order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = self.request.GET.get('category')
        sortby = self.request.GET.get('sortby')

        context['sort_by_fields'] = self.sort_by_fields
        context['selected_sortby'] = sortby
        
        return context


class DocumentDetailView(generic.DetailView):
    model = Document
    template_name = 'campaignfinance/documentdetail.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


class ReportedTotalsIndexView(generic.ListView):
    model = ReportedTotals
    template_name = 'campaignfinance/reportedtotalsindex.html'
    context_object_name = 'reported_totals_list'

    # default sort by source document name

    def get_queryset(self):
        return ReportedTotals.objects.all().order_by('pk')


class ReportedTotalsDetailView(generic.DetailView):
    model = ReportedTotals
    template_name = 'campaignfinance/reportedtotalsdetail.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


class ReportedSubtotalsIndexView(generic.ListView):
    model = ReportedSubtotals
    template_name = 'campaignfinance/reportedsubtotalsindex.html'
    context_object_name = 'reported_subtotals_list'

    # default sort by source document name

    def get_queryset(self):
        return ReportedSubtotals.objects.all().order_by('pk')


class ReportedSubtotalsDetailView(generic.DetailView):
    model = ReportedSubtotals
    template_name = 'campaignfinance/reportedsubtotalsdetail.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


class TransactionIndexView(generic.ListView):
    model = Transaction
    template_name = 'campaignfinance/transactionindex.html'
    context_object_name = 'transaction_list'

    filter_categories = {
        'select category': None,
        'contribution': 'contribution',
        'expenditure': 'expenditure',
        'refund': 'refund',
        'loan': 'loan',
        'in kind': 'inkind',
    }

    sort_by_fields = {
        'select': '-recorded_date',
        'payer': 'payer_entity',
        'recipient': 'payee_entity',
        'date': 'recorded_date',
        'amount': 'amount',
    }

    def get_queryset(self):
        try:
            category_name = self.filter_categories[self.request.GET.get('category')]
        except KeyError:
            category_name = None
        sort_by = self.sort_by_fields[self.request.GET.get('sortby', 'date')]

        if category_name is not None:
            category = TransactionCategory.objects.get(name=category_name)
            queryset = Transaction.objects.filter(category=category).order_by(sort_by)
        else:
            queryset = Transaction.objects.all().order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = self.request.GET.get('category')
        sortby = self.request.GET.get('sortby')

        context['filter_categories'] = self.filter_categories
        context['sort_by_fields'] = self.sort_by_fields
        context['selected_category'] = category
        context['selected_sortby'] = sortby
        
        return context


class TransactionDetailView(generic.DetailView):
    model = Transaction
    template_name = 'campaignfinance/transactiondetail.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


class AddressIndexView(generic.ListView):
    model = Address
    template_name = 'campaignfinance/addressindex.html'
    context_object_name = 'address_list'

    filter_categories = {
        'select category': None,
        'p.o. box': 'po box',
        'building': 'building',
    }

    sort_by_fields = {
        'select': 'street_name',
        'street': 'street_name',
        'city': 'city_name',
        'state': 'state_name',
        'zip code': 'zip_code',
    }

    #default should be street name

    def get_queryset(self):
        try:
            category_name = self.filter_categories[self.request.GET.get('category')]
        except KeyError:
            category_name = None
        sort_by = self.sort_by_fields[self.request.GET.get('sortby', 'street')]

        if category_name is not None:
            category = AddressCategory.objects.get(name=category_name)
            queryset = Address.objects.filter(category=category).order_by(sort_by)
        else:
            queryset = Address.objects.all().order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category = self.request.GET.get('category')
        sortby = self.request.GET.get('sortby')

        context['filter_categories'] = self.filter_categories
        context['sort_by_fields'] = self.sort_by_fields
        context['selected_category'] = category
        context['selected_sortby'] = sortby
        
        return context


class AddressDetailView(generic.DetailView):
    model = Address
    template_name = 'campaignfinance/addressdetail.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


class PhoneNumberIndexView(generic.ListView):
    model = PhoneNumber
    template_name = 'campaignfinance/phonenumberindex.html'
    context_object_name = 'phone_number_list'

    sort_by_fields = {
        'select': 'phone_number',
        'phone number': 'area_code',
        'owner': 'owner_entity',
    }

    def get_queryset(self):
        sort_by = self.sort_by_fields[self.request.GET.get('sortby', 'phone number')]
        queryset = PhoneNumber.objects.all().order_by(sort_by)

        return queryset

    def get_context_date(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sortby = self.request.GET.get('sortby')
        context['sort_by_fields'] = self.sort_by_fields
        context['selected_sortby'] = sortby

        return context


class PhoneNumberDetailView(generic.DetailView):
    model = PhoneNumber
    template_name = 'campaignfinance/phonenumberdetail.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


class EmailIndexView(generic.ListView):
    template_name = 'campaignfinance/emailindex.html'
    context_object_name = 'email_list'

    sort_by_fields = {
        'select': 'address',
        'address': 'address',
        'owner': 'owner_entity',
    }

    def get_queryset(self):
        sort_by = self.sort_by_fields[self.request.GET.get('sortby', 'address')]
        queryset = Email.objects.all().order_by(sort_by)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sortby = self.request.GET.get('sortby')
        context['sort_by_fields'] = self.sort_by_fields
        context['selected_sortby'] = sortby

        return context


class EmailDetailView(generic.DetailView):
    model = Email
    template_name = 'campaignfinance/emaildetail.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


class WebsiteIndexView(generic.ListView):
    model = Website
    template_name = 'campaignfinance/websiteindex.html'
    context_object_name = 'website_list'

    # default sort by website address

    def get_queryset(self):
        return Website.objects.all().order_by('address')


class WebsiteDetailView(generic.DetailView):
    model = Website
    template_name = 'campaignfinance/websitedetail.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'


class AssumedNameIndexView(generic.ListView):
    model = AssumedName
    template_name = 'campaignfinance/assumednameindex.html'
    context_object_name = 'assumed_name_list'

    # default sort should be alphabetical 

    def get_queryset(self):
        return AssumedName.objects.all().order_by('name')


class AssumedNameDetailView(generic.DetailView):
    model = AssumedName
    template_name = 'campaignfinance/assumednamedetail.html'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
