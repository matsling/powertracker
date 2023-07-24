# Generated by Django 4.2.1 on 2023-06-13 01:27

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddressCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=300, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=1000)),
                ('registration_date', models.DateField()),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CampaignCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=300, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=1000)),
                ('date_filed', models.DateField()),
                ('coverage_start_date', models.DateField()),
                ('coverage_end_date', models.DateField()),
                ('file_name', models.CharField(max_length=1000)),
                ('uploaded_file', models.FileField(blank=True, upload_to='')),
                ('notes', models.TextField(blank=True)),
                ('campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='campaign_documents', to='campaignfinance.campaign')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=300, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('date', models.DateField()),
                ('notes', models.TextField(blank=True)),
                ('campaigns', models.ManyToManyField(blank=True, related_name='election_campaigns', to='campaignfinance.campaign')),
            ],
        ),
        migrations.CreateModel(
            name='ElectionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=300, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(max_length=300)),
                ('prefix', models.CharField(blank=True, max_length=100)),
                ('suffix', models.CharField(blank=True, max_length=100)),
                ('nickname', models.CharField(blank=True, max_length=100)),
                ('occupation', models.CharField(blank=True, max_length=100)),
                ('notes', models.TextField(blank=True)),
                ('opencorporates_link', models.URLField(blank=True, max_length=300)),
                ('littlesis_link', models.CharField(blank=True, max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='EntityCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=300, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='IndustrySector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=300, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RelationshipCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=300, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=300, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('address', models.CharField(max_length=300, unique=True)),
                ('notes', models.TextField(blank=True)),
                ('associated_entities', models.ManyToManyField(blank=True, related_name='entity_websites', to='campaignfinance.entity')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entity_website_owners', to='campaignfinance.entity')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('recorded_date', models.DateField(blank=True)),
                ('reason', models.CharField(blank=True, max_length=1000)),
                ('notes', models.TextField(blank=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_transactions', to='campaignfinance.transactioncategory')),
                ('document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='document_transactions', to='campaignfinance.document')),
                ('election', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='election_transactions', to='campaignfinance.election')),
                ('government_entity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entity_government_transactions', to='campaignfinance.entity')),
                ('payee_entity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entity_payee_transactions', to='campaignfinance.entity')),
                ('payer_entity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entity_payer_transactions', to='campaignfinance.entity')),
            ],
        ),
        migrations.CreateModel(
            name='ReportedTotals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('unitemized_contributions', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('contributions', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('unitemized_expenditures', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('expenditures', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('maintained_contributions', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('principal_outstanding_loans', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('document', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='document_reported_totals', to='campaignfinance.document')),
            ],
        ),
        migrations.CreateModel(
            name='ReportedSubtotals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('monetary_political_contributions', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('non_monetary_political_contributions', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('pledged_contributions', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('monetary_corporate_labor_contributions', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('non_monetary_corporate_labor_contributions', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('pledged_corporate_labor_contributions', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('loans', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('expenditures_from_contributions', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('unpaid_incurred_obligations', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('purchased_investments_with_contributions', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('expenditures_credit_card', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('expenditures_personal_funds', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('expenditures_from_contributions_candidate_business', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('expenditures_non_political_from_contributions', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('interest_credit_gains_refunds_contributions_returned', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('document', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='document_reported_subtotals', to='campaignfinance.document')),
            ],
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('relationship_notes', models.TextField(blank=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_relationships', to='campaignfinance.relationshipcategory')),
                ('child_entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entity_child_relationships', to='campaignfinance.entity')),
                ('parent_entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entity_parent_relationships', to='campaignfinance.entity')),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('country_code', models.CharField(blank=True, max_length=2)),
                ('area_code', models.CharField(blank=True, max_length=3)),
                ('number', models.CharField(blank=True, max_length=7)),
                ('notes', models.TextField(blank=True)),
                ('associated_entities', models.ManyToManyField(blank=True, related_name='entity_phone_numbers', to='campaignfinance.entity')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entity_phone_number_owners', to='campaignfinance.entity')),
            ],
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=300)),
                ('notes', models.TextField(blank=True)),
                ('government_entity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entity_offices', to='campaignfinance.entity')),
                ('holder_entity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entity_holder_offices', to='campaignfinance.entity')),
            ],
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=300, unique=True)),
                ('sector', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sector_industries', to='campaignfinance.industrysector')),
            ],
        ),
        migrations.CreateModel(
            name='FormerOfficeHolder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('entity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entity_former_offices', to='campaignfinance.entity')),
                ('office', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='office_former_holders', to='campaignfinance.office')),
            ],
        ),
        migrations.CreateModel(
            name='ExternalId',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('number', models.CharField(blank=True, max_length=300)),
                ('notes', models.TextField(blank=True)),
                ('child_entity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entity_child_ids', to='campaignfinance.entity')),
                ('parent_entity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entity_parent_ids', to='campaignfinance.entity')),
            ],
        ),
        migrations.AddField(
            model_name='entity',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_entities', to='campaignfinance.entitycategory'),
        ),
        migrations.AddField(
            model_name='entity',
            name='industry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='industry_entities', to='campaignfinance.industry'),
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('address', models.CharField(max_length=300, unique=True)),
                ('notes', models.TextField(blank=True)),
                ('associated_entities', models.ManyToManyField(blank=True, related_name='entity_emails', to='campaignfinance.entity')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entity_email_owners', to='campaignfinance.entity')),
            ],
        ),
        migrations.AddField(
            model_name='election',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_elections', to='campaignfinance.electioncategory'),
        ),
        migrations.AddField(
            model_name='election',
            name='government_entity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entity_government_elections', to='campaignfinance.entity'),
        ),
        migrations.AddField(
            model_name='document',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_documents', to='campaignfinance.documentcategory'),
        ),
        migrations.AddField(
            model_name='document',
            name='filer_entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entity_document_filers', to='campaignfinance.entity'),
        ),
        migrations.AddField(
            model_name='document',
            name='government_entity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entity_government_documents', to='campaignfinance.entity'),
        ),
        migrations.AddField(
            model_name='document',
            name='officer_oath_entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entity_officer_oaths', to='campaignfinance.entity'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='candidate_entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entity_candidate_campaigns', to='campaignfinance.entity'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_campaigns', to='campaignfinance.campaigncategory'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='committee_entity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entity_committee_campaigns', to='campaignfinance.entity'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='government_entity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entity_government_campaigns', to='campaignfinance.entity'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='office_sought',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='office_campaigns', to='campaignfinance.office'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='treasurer_entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entity_treasurer_campaigns', to='campaignfinance.entity'),
        ),
        migrations.CreateModel(
            name='AssumedName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=300)),
                ('notes', models.TextField(blank=True)),
                ('associated_entities', models.ManyToManyField(blank=True, related_name='entity_assumed_names', to='campaignfinance.entity')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('building_number', models.CharField(blank=True, max_length=300)),
                ('street_name', models.CharField(blank=True, max_length=300)),
                ('unit_number', models.CharField(blank=True, max_length=300)),
                ('floor_number', models.CharField(blank=True, max_length=300)),
                ('city_name', models.CharField(blank=True, max_length=300)),
                ('state_name', models.CharField(blank=True, max_length=300)),
                ('county_name', models.CharField(blank=True, max_length=300)),
                ('zip_code', models.CharField(max_length=300)),
                ('zip_code_extension', models.CharField(blank=True, max_length=300)),
                ('notes', models.TextField(blank=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_addresses', to='campaignfinance.addresscategory')),
                ('owners', models.ManyToManyField(blank=True, related_name='entity_owners', to='campaignfinance.entity')),
                ('residents', models.ManyToManyField(blank=True, related_name='entity_residences', to='campaignfinance.entity')),
            ],
        ),
    ]