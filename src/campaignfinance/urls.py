from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'campaignfinance'
urlpatterns = [
    path('', views.HomePageIndex.as_view(), name='homepageindex'),

    path('glossary', views.glossaryindex, name='glossaryindex'),

    path('entity', views.EntityIndexView.as_view(), name='entityindex'),
    path('entity/<uuid:uuid>/', views.EntityDetailView.as_view(), name='entitydetail'),

    path('industrysector', views.IndustrySectorIndexView.as_view(), name='industrysectorindex'),
    path('industrysector/<uuid:uuid>/', views.IndustrySectorDetailView.as_view(), name="industrysectordetail"),

    path('industry', views.IndustryIndexView.as_view(), name='industryindex'),

    path('externalid', views.ExternalIdIndexView.as_view(), name='externalidindex'),
    path('externalid/<uuid:uuid>/', views.ExternalIdDetailView.as_view(), name='externaliddetail'),

    path('relationship', views.RelationshipIndexView.as_view(), name='relationshipindex'),
    path('relationship/<uuid:uuid>/', views.RelationshipDetailView.as_view(), name='relationshipdetail'),

    path('campaign', views.CampaignIndexView.as_view(), name='campaignindex'),
    path('campaign/<uuid:uuid>/', views.CampaignDetailView.as_view(), name='campaigndetail'),

    path('office', views.OfficeIndexView.as_view(), name='officeindex'),
    path('office/<uuid:uuid>/', views.OfficeDetailView.as_view(), name='officedetail'),

    path('formerofficeholder', views.FormerOfficeHolderIndexView.as_view(), name='formerofficeholderindex'),

    path('election', views.ElectionIndexView.as_view(), name='electionindex'),
    path('election/<uuid:uuid>/', views.ElectionDetailView.as_view(), name='electiondetail'),

    path('document', views.DocumentIndexView.as_view(), name='documentindex'),
    path('document/<uuid:uuid>/', views.DocumentDetailView.as_view(), name='documentdetail'),

    path('reportedtotals', views.ReportedTotalsIndexView.as_view(), name='reportedtotalsindex'),
    path('reportedtotals/<uuid:uuid>/', views.ReportedTotalsDetailView.as_view(), name='reportedtotalsdetail'),

    path('reportedsubtotals', views.ReportedSubtotalsIndexView.as_view(), name='reportedsubtotalsindex'),
    path('reportedsubtotals/<uuid:uuid>/', views.ReportedSubtotalsDetailView.as_view(), name='reportedsubtotalsdetail'),

    path('transaction', views.TransactionIndexView.as_view(), name='transactionindex'),
    path('transaction/<uuid:uuid>/', views.TransactionDetailView.as_view(), name='transactiondetail'),

    path('address', views.AddressIndexView.as_view(), name='addressindex'),
    path('address/<uuid:uuid>/', views.AddressDetailView.as_view(), name='addressdetail'),

    path('phonenumber', views.PhoneNumberIndexView.as_view(), name='phonenumberindex'),
    path('phonenumber/<uuid:uuid>/', views.PhoneNumberDetailView.as_view(), name="phonenumberdetail"),

    path('email', views.EmailIndexView.as_view(), name='emailindex'),
    path('email/<uuid:uuid>/', views.EmailDetailView.as_view(), name='emaildetail'),

    path('website', views.WebsiteIndexView.as_view(), name='websiteindex'),
    path('website/<uuid:uuid>/', views.WebsiteDetailView.as_view(), name='websitedetail'),

    path('assumedname', views.AssumedNameIndexView.as_view(), name='assumednameindex'),
    path('assumedname/<uuid:uuid>/', views.AssumedNameDetailView.as_view(), name='assumednamedetail'),
]
