from datetime import datetime

from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.urls import reverse

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


# Testing Industry & Sectors
class IndustryModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.industry_sector_default = IndustrySector.objects.create(name="Construction")
        cls.industry_default = Industry.objects.create(sector=cls.industry_sector_default, name="Home Builders")
        cls.industry_sector_default.save()
        cls.industry_default.save()

    # Create industry sector
    def test_industry_sector_creation(self):
        industry_sector = IndustrySector.objects.create(name="Media")
        industry_sector.save()
        self.assertEqual(
            IndustrySector.objects.get(
                name="Media").name,
                "Media"
            )

    # Create industry
    def test_industry_creation(self):
        industry_sector = IndustrySector.objects.create(name="Media")
        industry_sector.save()
        industry = Industry.objects.create(sector=industry_sector, name="Television")
        industry.save()
        self.assertEqual(
            Industry.objects.get(
                name="Television").name,
                "Television"
        )

    # Ensure duplicates sectors cannot be created
    def test_industry_sector_duplicate(self):
        with self.assertRaises(IntegrityError):
            IndustrySector.objects.create(name="Construction")

    # Ensure duplicate industries cannot be created
    def test_industry_duplicate(self):
        with self.assertRaises(IntegrityError):
            Industry.objects.create(name="Home Builders")

    # Delete Industry without deleting sector
    def test_industry_delete(self):
        industry = Industry.objects.create(sector=self.industry_sector_default, name="Concrete")
        industry.save()
        Industry.objects.get(name="Concrete").delete()

        with self.assertRaises(ObjectDoesNotExist):
            Industry.objects.get(name="Concrete")

        self.assertEqual(
            IndustrySector.objects.get(name="Construction").name,
            "Construction"
        )

    # Refer to sector through foriegn key relationship
    def test_industry_retrieve_sector(self):
        self.assertEqual(
            Industry.objects.get(pk=1).sector.name,
            "Construction"
        )


# Testing Entity and Entity Types
class EntityModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.industry_sector_default = IndustrySector.objects.create(name="Construction")
        cls.industry_sector_default.save()
        cls.industry_default = Industry.objects.create(sector=cls.industry_sector_default, name="Home Building")
        cls.industry_default.save()

    def test_entity_category_creation(self):
        EntityCategory.objects.create(name='Individual').save()
        self.assertEqual(EntityCategory.objects.get(pk=1).name,"Individual")

        with self.assertRaises(IntegrityError):
            EntityCategory.objects.create(name="Individual")

    def test_entity_creation(self):
        entity_category = EntityCategory.objects.create(name="Individual")
        entity_category.save()
        Entity.objects.create(
            category=entity_category,
            first_name="John",
            middle_name="Smith",
            last_name="Doe",
            prefix="Mr",
            suffix="Sr",
            nickname="Jo",
            occupation="Writer",
            industry=self.industry_default,
            notes="Some placeholder notes"
        ).save()

        retrieved_entity = Entity.objects.get(pk=1)

        self.assertEqual(retrieved_entity.category.name, "Individual")
        self.assertEqual(retrieved_entity.first_name, "John")
        self.assertEqual(retrieved_entity.middle_name, "Smith")
        self.assertEqual(retrieved_entity.last_name, "Doe")
        self.assertEqual(retrieved_entity.prefix, "Mr")
        self.assertEqual(retrieved_entity.suffix, "Sr")
        self.assertEqual(retrieved_entity.nickname, "Jo")
        self.assertEqual(retrieved_entity.occupation, "Writer")
        self.assertEqual(retrieved_entity.industry.name, "Home Building")
        self.assertEqual(retrieved_entity.notes, "Some placeholder notes")


class ExternalIdTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entity_category1 = EntityCategory.objects.create(name='Reporting Agency')
        cls.entity_category2 = EntityCategory.objects.create(name='Individual')
        cls.entity1 = Entity.objects.create(category=cls.entity_category1, last_name='Texas Ethics Commission')
        cls.entity2 = Entity.objects.create(category=cls.entity_category2, last_name='test1')

    def test_external_id_creation(self):
        ExternalId(
            parent_entity=self.entity1,
            child_entity=self.entity2,
            number='123456'
        ).save()

        retrieved_external_id = ExternalId.objects.get(pk=1)

        self.assertEqual(retrieved_external_id.parent_entity.last_name, 'Texas Ethics Commission')
        self.assertEqual(retrieved_external_id.child_entity.last_name, 'test1')
        self.assertEqual(retrieved_external_id.number, '123456')


class RelationshipModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entity_category = EntityCategory.objects.create(name='Individual')
        cls.entity1 = Entity.objects.create(category=cls.entity_category, last_name='test1')
        cls.entity2 = Entity.objects.create(category=cls.entity_category, last_name='test2')
        cls.entity_category.save()
        cls.entity1.save()
        cls.entity2.save()

    def test_relationship_category_creation(self):
        RelationshipCategory.objects.create(name='Family').save()

        self.assertEqual(
            RelationshipCategory.objects.get(pk=1).name,
            "Family"
        )

    def test_relationship_category_duplicate(self):
        RelationshipCategory.objects.create(name='Family').save()

        with self.assertRaises(IntegrityError):
            RelationshipCategory.objects.create(name='Family')

    def test_relationship_creation(self):
        relationship_category = RelationshipCategory.objects.create(name='Family')

        Relationship.objects.create(
            category=relationship_category,
            parent_entity=self.entity1,
            child_entity=self.entity2,
            notes="Testing notes"
        ).save()

        retrieved_relationship = Relationship.objects.get(pk=1)

        self.assertEqual(retrieved_relationship.category.name, "Family")
        self.assertEqual(retrieved_relationship.parent_entity.last_name, "test1")
        self.assertEqual(retrieved_relationship.child_entity.last_name, "test2")
        self.assertEqual(retrieved_relationship.notes, "Testing notes")

    def test_relationship_invalid(self):
        relationship_category = RelationshipCategory.objects.create(name='Family')

        with self.assertRaises(IntegrityError):
            Relationship.objects.create(
                category=relationship_category,
                parent_entity=self.entity1,
                child_entity=None
            )

    def test_relationship_deletion(self):
        relationship_category = RelationshipCategory.objects.create(name='Family')
        relationship_category.save()

        relationship = Relationship.objects.create(
            category=relationship_category,
            parent_entity=self.entity1,
            child_entity=self.entity2,
            notes="Testing notes."
        )
        relationship.save()

        Entity.objects.get(last_name="test1").delete()

        with self.assertRaises(ObjectDoesNotExist):
            Relationship.objects.get(category=1)


class OfficeModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entity_category1 = EntityCategory.objects.create(name='Government')
        cls.entity_category2 = EntityCategory.objects.create(name='Individual')
        cls.entity1 = Entity.objects.create(category=cls.entity_category1, last_name='City of San Angelo')
        cls.entity2 = Entity.objects.create(category=cls.entity_category2, last_name='test1')
        cls.entity3 = Entity.objects.create(category=cls.entity_category2, last_name='test2')
        cls.entity_category1.save()
        cls.entity_category2.save()
        cls.entity1.save()
        cls.entity2.save()
        cls.entity3.save()

    def test_office_creation(self):
        Office.objects.create(
            government_entity=self.entity1,
            name="Mayor",
            holder_entity=self.entity2
        ).save()

        retrieved_office = Office.objects.get(pk=1)

        self.assertEqual(retrieved_office.government_entity.last_name, "City of San Angelo")
        self.assertEqual(retrieved_office.holder_entity.last_name, "test1")
        self.assertEqual(retrieved_office.name, "Mayor")

    def test_office_entity_deletion(self):
        Office.objects.create(
            name="Mayor",
            holder_entity=self.entity2
        )
        Entity.objects.get(pk=2).delete()

        cache.clear()

        with self.assertRaises(AttributeError):
            Office.objects.get(pk=1).holder_entity.last_name

    def test_office_holder_change(self):
        office = Office.objects.create(
            holder_entity=self.entity2,
            name="Mayor"
        )
        office.save()

        office.holder_entity = self.entity3
        office.save()

        retrieved_office = Office.objects.get(pk=1)

        self.assertEqual(retrieved_office.holder_entity.last_name, "test2")


class FormerOfficeHolderModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.office = Office.objects.create(name='Mayor')
        cls.entity_category = EntityCategory.objects.create(name='Individual')
        cls.entity = Entity.objects.create(category=cls.entity_category, last_name='entity1')

    def test_former_office_holder_creation(self):
        FormerOfficeHolder.objects.create(
            office=self.office,
            entity=self.entity
        ).save()

        retrieved_former = FormerOfficeHolder.objects.get(pk=1)

        self.assertEqual(retrieved_former.entity.last_name, 'entity1')
        self.assertEqual(retrieved_former.office.name, 'Mayor')


class CampaignModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entity_category1 = EntityCategory.objects.create(name='Government')
        cls.entity_category2 = EntityCategory.objects.create(name='Individual')
        cls.entity_category3 = EntityCategory.objects.create(name='Political Action Committee')
        cls.entity_category4 = EntityCategory.objects.create(name='Reporting Agency')
        cls.entity1 = Entity.objects.create(category=cls.entity_category1, last_name='City of San Angelo')
        cls.entity2 = Entity.objects.create(category=cls.entity_category2, last_name='test1')
        cls.entity3 = Entity.objects.create(category=cls.entity_category2, last_name='test2')
        cls.entity4 = Entity.objects.create(category=cls.entity_category3, last_name='Committee to elect test2')
        cls.office = Office.objects.create(
            government_entity=cls.entity1,
            name='Mayor',
            holder_entity=cls.entity2
        )
        cls.agency = Entity.objects.create(category=cls.entity_category4, last_name='Texas Ethics Commission')

    def test_campaign_category_creation(self):
        CampaignCategory.objects.create(name='Municipal').save()

        retrieved_campaign_category = CampaignCategory.objects.get(pk=1)

        self.assertEqual(retrieved_campaign_category.name, 'Municipal')

    def test_campaign_creation(self):
        campaign_category = CampaignCategory.objects.create(name="Municipal")

        Campaign.objects.create(
            category=campaign_category,
            candidate_entity=self.entity2,
            treasurer_entity=self.entity3,
            committee_entity=self.entity4,
            office_sought=self.office,
            registration_date='2023-01-01',
            notes="Testing notes"
        ).save()

        retrieved_campaign = Campaign.objects.get(pk=1)

        self.assertEqual(CampaignCategory.objects.get(pk=1).name, "Municipal")
        self.assertEqual(retrieved_campaign.candidate_entity.last_name, "test1")
        self.assertEqual(retrieved_campaign.treasurer_entity.last_name, "test2")
        self.assertEqual(retrieved_campaign.committee_entity.last_name, "Committee to elect test2")
        self.assertEqual(retrieved_campaign.office_sought.name, "Mayor")
        self.assertEqual(
            retrieved_campaign.registration_date,
            datetime.strptime('2023-01-01', '%Y-%m-%d').date()    
        )
        self.assertEqual(retrieved_campaign.notes, "Testing notes")


class ElectionModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entity_category1 = EntityCategory.objects.create(name='government')
        cls.entity_category2 = EntityCategory.objects.create(name='individual')
        cls.entity1 = Entity.objects.create(category=cls.entity_category2, last_name='test1')
        cls.entity2 = Entity.objects.create(category=cls.entity_category2, last_name='test2')
        cls.government_entity = Entity.objects.create(category=cls.entity_category1, last_name='city of san angelo')

    def test_election_creation(self):

        election_category = ElectionCategory.objects.create(name="primary")
        Election.objects.create(
            category=election_category,
            government_entity=self.government_entity,
            date="2023-03-30"
        ).save()

        retrieved_election = Election.objects.get(pk=1)

        self.assertEqual(retrieved_election.category.name, "primary")
        self.assertEqual(retrieved_election.government_entity.last_name, "city of san angelo")
        self.assertEqual(
            retrieved_election.date,
            datetime.strptime("2023-03-30", '%Y-%m-%d').date()
        )

        def test_elections_with_multiple_campaigns(self):
            election_category1 = ElectionCategory.objects.create(name="primary")
            election_category2 = ElectionCategory.objects.create(name="runoff")
            campaign_category = CampaignCategory.objects.create(name="candidate")
            campaign1 = Campaign.objects.create(
                category=campaign_category,
                government_entity=self.government_entity,
                candidate_entity=self.entity1,
            )
            campaign2 = Campaign.objects.create(
                category=campaign_category,
                government_entity=self.government_entity,
                candidate_entity=self.entity2,
            )
            election1 = Election.objects.create(
                category=election_category1,
                government_entity=self.government_entity,
                date="2023-05-06"
            )
            election2 = Election.objects.create(
                category=election_category2,
                government_entity=self.government_entity,
                date="2023-06-01"
            )

            # Associate campaigns and elections
            election1.campaigns.add(campaign1, campaign2)
            election2.campaigns.add(campaign1, campaign2)

            retrieved_election1 = Election.objects.get(pk=1)
            retrieved_election2 = Election.objects.get(pk=2)

            retrieved_campaign1 = Campaign.objects.get(pk=1)
            retrieved_campaign2 = Campaign.objects.get(pk=2)

            # Assert IDs are correct with object numbers
            self.assertEqual(retrieved_election1.pk, 1)
            self.assertEqual(retrieved_election2.pk, 2)
            self.assertEqual(retrieved_campaign1.pk, 1)
            self.assertEqual(retrieved_campaign2.pk, 2)

            # Assert lookup of campaigns through election objects work
            self.assertEqual(retrieved_election1.campaigns.get(pk=1).candidate_entity.last_name, "test1")
            self.assertEqual(retrieved_election1.campaigns.get(pk=2).candidate_entity.last_name, "test2")
            self.assertEqual(retrieved_election2.campaigns.get(pk=1).candidate_entity.last_name, "test1")
            self.assertEqual(retrieved_election2.campaigns.get(pk=2).candidate_entity.last_name, "test2")

            # Assert reverse lookup of elections through campaign objects work
            self.assertEqual(retrieved_campaign1.election_set.get(pk=1).date, datetime.strptime("2023-05-06", '%Y-%m-%d').date())
            self.assertEqual(retrieved_campaign1.election_set.get(pk=2).date, datetime.strptime("2023-06-01", '%Y-%m-%d').date())
            self.assertEqual(retrieved_campaign2.election_set.get(pk=1).date, datetime.strptime("2023-05-06", '%Y-%m-%d').date())
            self.assertEqual(retrieved_campaign2.election_set.get(pk=2).date, datetime.strptime("2023-06-01", '%Y-%m-%d').date())

            # Assert all related campaigns returned for election
            all_campaigns = election1.campaigns.all()
            expected_campaign_ids = [1, 2]

            for campaign in all_campaigns:
                self.assertIn(campaign.pk, expected_campaign_ids)

            # Assert all related elections returned for campaign
            all_elections = campaign1.election_set.all()
            expected_election_ids = [1, 2]

            for election in all_elections:
                self.assertIn(election.pk, expected_election_ids)


class DocumentModelTests(TestCase):
    def test_document_category_creation(self):
        document_category = DocumentCategory.objects.create(name="8 days before election")

        self.assertEqual(document_category.name, "8 days before election")

    def test_document_creation(self):
        document_category = DocumentCategory.objects.create(name="8 days before election")

        Document.objects.create(
            category=document_category,
            date_filed="2023-04-06",
            coverage_start_date="2023-01-01",
            coverage_end_date="2023-04-06",
        ).save()

        retrieved_document = Document.objects.get(pk=1)

        self.assertEqual(retrieved_document.category.name, "8 days before election")
        self.assertEqual(retrieved_document.date_filed, datetime.strptime("2023-04-06", '%Y-%m-%d').date())
        self.assertEqual(retrieved_document.coverage_start_date, datetime.strptime("2023-01-01", '%Y-%m-%d').date())
        self.assertEqual(retrieved_document.coverage_end_date, datetime.strptime("2023-04-06", '%Y-%m-%d').date())


class ReportedTotalsModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.document_category = DocumentCategory.objects.create(name='8 day before election')
        cls.document = Document.objects.create(
            category=cls.document_category,
            date_filed="2023-04-06",
            coverage_start_date="2023-01-01",
            coverage_end_date="2023-04-06",
        )

    def test_reported_totals_creation(self):
        ReportedTotals.objects.create(
            document=self.document,
            unitemized_contributions=1500.00,
            contributions=2000.15,
            unitemized_expenditures=1500.00,
            expenditures=2000.15,
            maintained_contributions=1500.00,
            principal_outstanding_loans=2000.15
        ).save()

        retrieved_reported_totals = ReportedTotals.objects.get(pk=1)

        self.assertEqual(
            retrieved_reported_totals.document.date_filed,
            datetime.strptime('2023-04-06', '%Y-%m-%d').date()
        )
        self.assertEqual(
            float(retrieved_reported_totals.unitemized_contributions),
            1500.00
        )
        self.assertEqual(
            float(retrieved_reported_totals.contributions),
            2000.15
        )
        self.assertEqual(
            float(retrieved_reported_totals.unitemized_expenditures),
            1500.00
        )
        self.assertEqual(
            float(retrieved_reported_totals.expenditures),
            2000.15
        )
        self.assertEqual(
            float(retrieved_reported_totals.maintained_contributions),
            1500.00
        )
        self.assertEqual(
            float(retrieved_reported_totals.principal_outstanding_loans),
            2000.15
        )


class ReportedSubtotalsModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.document_category = DocumentCategory.objects.create(name='8 day before election')
        cls.document = Document.objects.create(
            category=cls.document_category,
            date_filed="2023-04-06",
            coverage_start_date="2023-01-01",
            coverage_end_date="2023-04-06",
        )

    def test_reported_subtotals_creation(self):
        ReportedSubtotals.objects.create(
            document=self.document,
            monetary_political_contributions=100.10,
            non_monetary_political_contributions=200.20,
            pledged_contributions=300.30,
            monetary_corporate_labor_contributions=400.40,
            non_monetary_corporate_labor_contributions=500.50,
            pledged_corporate_labor_contributions=600.60,
            loans=700.70,
            expenditures_from_contributions=800.80,
            unpaid_incurred_obligations=900.90,
            purchased_investments_with_contributions=1000.10,
            expenditures_credit_card=1100.11,
            expenditures_personal_funds=1200.12,
            expenditures_from_contributions_candidate_business=1300.13,
            expenditures_non_political_from_contributions=1400.14,
            interest_credit_gains_refunds_contributions_returned=1500.15
        ).save()

        retrieved_reported_subtotals = ReportedSubtotals.objects.get(pk=1)

        self.assertEqual(
            retrieved_reported_subtotals.document.date_filed,
            datetime.strptime('2023-04-06', '%Y-%m-%d').date()
        )
        self.assertEqual(
            float(retrieved_reported_subtotals.monetary_political_contributions),
            100.10
        )
        self.assertEqual(
            float(retrieved_reported_subtotals.non_monetary_political_contributions),
            200.20
        )
        self.assertEqual(
            float(retrieved_reported_subtotals.pledged_contributions),
            300.30
        )
        self.assertEqual(
            float(retrieved_reported_subtotals.monetary_corporate_labor_contributions),
            400.40
        )
        self.assertEqual(
            float(retrieved_reported_subtotals.non_monetary_corporate_labor_contributions),
            500.50
        )
        self.assertEqual(
            float(retrieved_reported_subtotals.pledged_corporate_labor_contributions),
            600.60
        )
        self.assertEqual(
            float(retrieved_reported_subtotals.loans),
            700.70
        )
        self.assertEqual(
            float(retrieved_reported_subtotals.expenditures_from_contributions),
            800.80
        )
        self.assertEqual(
            float(retrieved_reported_subtotals.unpaid_incurred_obligations),
            900.90
        )
        self.assertEqual(
            float(retrieved_reported_subtotals.purchased_investments_with_contributions),
            1000.10
        )
        self.assertEqual(
            float(retrieved_reported_subtotals.expenditures_credit_card),
            1100.11
        )
        self.assertEqual(
            float(retrieved_reported_subtotals.expenditures_personal_funds),
            1200.12
        )
        self.assertEqual(
            float(retrieved_reported_subtotals.expenditures_from_contributions_candidate_business),
            1300.13
        )
        self.assertEqual(
            float(retrieved_reported_subtotals.expenditures_non_political_from_contributions),
            1400.14
        )
        self.assertEqual(
            float(retrieved_reported_subtotals.interest_credit_gains_refunds_contributions_returned),
            1500.15
        )


class TransactionModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entity_category1 = EntityCategory.objects.create(name='individual')
        cls.entity_category2 = EntityCategory.objects.create(name='candidate')
        cls.entity_category3 = EntityCategory.objects.create(name='government')
        cls.entity1 = Entity.objects.create(category=cls.entity_category1, last_name='test1')
        cls.entity2 = Entity.objects.create(category=cls.entity_category2, last_name='test2')
        cls.government_entity = Entity.objects.create(category=cls.entity_category2, last_name='city of san angelo')
        cls.document_category = DocumentCategory.objects.create(name='8 days before election')
        cls.document = Document.objects.create(
            category=cls.document_category,
            date_filed="2023-04-06",
            coverage_start_date="2023-01-01",
            coverage_end_date="2023-04-06",
        )
        cls.election_category = ElectionCategory.objects.create(name='primary')
        cls.election = Election.objects.create(
            category=cls.election_category,
            government_entity=cls.government_entity,
            date='2023-05-06',
        )
        cls.campaign_category = CampaignCategory.objects.create(name='candidate')
        cls.campaign = Campaign.objects.create(
            category=cls.campaign_category,
            name='test campaign',
            candidate_entity=cls.entity1,
            election=cls.election,
            registration_date='2023-06-06',
        )

    def test_transaction_category_creation(self):
        TransactionCategory.objects.create(name='contribution').save()

        retrieved_transaction_category = TransactionCategory.objects.get(pk=1)
        self.assertEqual(retrieved_transaction_category.name, 'contribution')
    
    def test_transaction_creation(self):
        transaction_category = TransactionCategory.objects.create(name="contribution")
        Transaction.objects.create(
            category=transaction_category,
            payer_entity=self.entity1,
            payee_entity=self.entity2,
            amount=100.10,
            recorded_date="2023-04-03",
            document=self.document,
            campaign=self.campaign,
        )

        retrieved_transaction = Transaction.objects.get(pk=1)

        self.assertTrue(
            retrieved_transaction.category.name,
            "Contribution"
        )
        self.assertTrue(
            retrieved_transaction.payer_entity.last_name,
            "test1"
        )
        self.assertTrue(
            retrieved_transaction.payee_entity.last_name,
            "test2"
        )
        self.assertTrue(
            float(retrieved_transaction.amount),
            100.00
        )
        self.assertTrue(
            retrieved_transaction.recorded_date,
            datetime.strptime("2023-04-03", '%Y-%m-%d').date()
        )
        self.assertTrue(
            retrieved_transaction.document.date_filed,
            datetime.strptime("2023-04-06", '%Y-%m-%d').date()
        )
        self.assertTrue(
            retrieved_transaction.campaign.name,
            'test campaign'
        )


class AddressModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entity_category1 = EntityCategory.objects.create(name='individual')
        cls.entity_category2 = EntityCategory.objects.create(name='government')
        cls.entity1 = Entity.objects.create(category=cls.entity_category1, last_name='test1')
        cls.entity2 = Entity.objects.create(category=cls.entity_category1, last_name='test2')
        cls.government_entity = Entity.objects.create(category=cls.entity_category2, last_name='city of san angelo')

    def test_address_category_create(self):
        AddressCategory.objects.create(name='building').save()
        
        retrieved_address_type = AddressCategory.objects.get(pk=1)
        self.assertEqual(retrieved_address_type.name, 'building')

    def test_address_creation(self):
        address_category1 = AddressCategory.objects.create(name="building")
        address_category2 = AddressCategory.objects.create(name="po box")
        address1 = Address.objects.create(
            category=address_category1,
            building_number='1234',
            street_name="irving street",
            unit_number="1234",
            floor_number='2h',
            city_name="san angelo",
            state_name="texas",
            county_name="tom green",
            zip_code='76904',
            zip_code_extension='1234',
            notes='test notes 1',
        )
        address2 = Address.objects.create(
            category=address_category2,
            building_number='321',
            city_name="san angelo",
            state_name="texas",
            county_name="tom green",
            zip_code='76906',
        )

        # Associated Addresses with Owners & Residents
        address1.residents.add(self.entity1, self.entity2)
        address1.owners.add(self.government_entity)
        address2.residents.add(self.entity1)
        address2.owners.add(self.entity1, self.entity2)

        # Retrieve database objects
        retrieved_address1 = Address.objects.get(pk=1)
        retrieved_address2 = Address.objects.get(pk=2)
        retrieved_entity1 = Entity.objects.get(pk=1)
        retrieved_entity2 = Entity.objects.get(pk=2)
        
        # Assert address info stored correctly
        self.assertEqual(retrieved_address1.category.name,"building")
        self.assertEqual(retrieved_address1.building_number, '1234')
        self.assertEqual(retrieved_address1.unit_number, '1234')
        self.assertEqual(retrieved_address1.floor_number, '2h')
        self.assertEqual(retrieved_address1.street_name, "irving street")
        self.assertEqual(retrieved_address1.city_name, "san angelo")
        self.assertEqual(retrieved_address1.state_name, "texas")
        self.assertEqual(retrieved_address1.county_name, "tom green")
        self.assertEqual(retrieved_address1.zip_code, '76904')
        self.assertEqual(retrieved_address1.notes, 'test notes 1')

        self.assertEqual(retrieved_address2.category.name, "po box")
        self.assertEqual(retrieved_address2.building_number, '321')
        self.assertEqual(retrieved_address2.city_name, "san angelo")
        self.assertEqual(retrieved_address2.state_name, "texas")
        self.assertEqual(retrieved_address2.county_name, "tom green")
        self.assertEqual(retrieved_address2.zip_code, '76906')

        # Assert all related residents returned for address
        all_residents_address1 = address1.residents.all()
        all_residents_address2 = address2.residents.all()
        expected_resident_ids1 = [1, 2]
        expected_resident_ids2 = [1]

        for resident in all_residents_address1:
            self.assertIn(resident.pk, expected_resident_ids1)

        for resident in all_residents_address2:
            self.assertIn(resident.pk, expected_resident_ids2)

        # Assert all related owners returned for address
        all_owners_address1 = address1.owners.all()
        all_owners_address2 = address2.owners.all()
        expected_owners_ids1 = [3]
        expected_owners_ids2 = [1, 2]

        for owner in all_owners_address1:
            self.assertIn(owner.pk, expected_owners_ids1)

        for owner in all_owners_address2:
            self.assertIn(owner.pk, expected_owners_ids2)

        # Assert lookup of residents through address objects work
        self.assertEqual(retrieved_address1.residents.get(pk=1).last_name, "test1")
        self.assertEqual(retrieved_address1.residents.get(pk=2).last_name, "test2")

        # Assert lookup of owners through address objects work
        self.assertEqual(retrieved_address2.owners.get(pk=1).last_name, "test1")
        self.assertEqual(retrieved_address2.owners.get(pk=2).last_name, "test2")

        # Assert reverse lookup through entity objects work
        self.assertEqual(retrieved_entity1.entity_owners.get(pk=2).building_number, '321')
        self.assertEqual(retrieved_entity1.entity_residences.get(pk=1).building_number, '1234')


class PhoneNumberModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entity_category = EntityCategory.objects.create(name='individual')
        cls.entity1 = Entity.objects.create(category=cls.entity_category, last_name='test1')
        cls.entity2 = Entity.objects.create(category=cls.entity_category, last_name='test2')
        cls.entity3 = Entity.objects.create(category=cls.entity_category, last_name='test3')

    def test_phone_number_creation(self):
        phone_number = PhoneNumber.objects.create(
            country_code='1',
            area_code='325',
            number='5550492',
            notes='test notes 1',
            owner=self.entity3,
        )

        phone_number.associated_entities.add(self.entity1, self.entity2)

        retrieved_phone_number = PhoneNumber.objects.get(pk=1)

        self.assertEqual(retrieved_phone_number.country_code, '1')
        self.assertEqual(retrieved_phone_number.area_code, '325')
        self.assertEqual(retrieved_phone_number.number, '5550492')
        self.assertEqual(retrieved_phone_number.notes, 'test notes 1')
        self.assertEqual(retrieved_phone_number.owner.last_name, 'test3')

        all_entities = retrieved_phone_number.associated_entities.all()
        all_entities_expected = [1, 2]

        for entity in all_entities:
            self.assertIn(entity.pk, all_entities_expected)

        self.assertEqual(retrieved_phone_number.associated_entities.get(pk=1).last_name, "test1")
        self.assertEqual(retrieved_phone_number.associated_entities.get(pk=2).last_name, "test2")
        self.assertEqual(Entity.objects.get(pk=1).entity_phone_numbers.get(pk=1).number, '5550492')
        self.assertEqual(Entity.objects.get(pk=2).entity_phone_numbers.get(pk=1).number, '5550492')


class EmailModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entity_category = EntityCategory.objects.create(name='individual')
        cls.entity1 = Entity.objects.create(category=cls.entity_category, last_name='test1')
        cls.entity2 = Entity.objects.create(category=cls.entity_category, last_name='test2')
        cls.entity3 = Entity.objects.create(category=cls.entity_category, last_name='test3')

    def test_email_creation(self):
        email = Email.objects.create(
            address="test@example.com",
            owner=self.entity3,
            notes='test notes 1',
        )

        email.associated_entities.add(self.entity1, self.entity2)

        retrieved_email = Email.objects.get(pk=1)
        retrieved_email_entities = retrieved_email.associated_entities.all()
        expected_entities = [1, 2]

        self.assertEqual(retrieved_email.address, "test@example.com")
        self.assertEqual(retrieved_email.owner.last_name, 'test3')
        self.assertEqual(retrieved_email.notes, 'test notes 1')

        for entity in retrieved_email_entities:
            self.assertIn(entity.pk, expected_entities)
        
        self.assertEqual(retrieved_email.associated_entities.get(pk=1).last_name, "test1")
        self.assertEqual(retrieved_email.associated_entities.get(pk=2).last_name, "test2")
        self.assertEqual(Entity.objects.get(pk=1).entity_emails.get(pk=1).address, "test@example.com")
        self.assertEqual(Entity.objects.get(pk=2).entity_emails.get(pk=1).address, "test@example.com")


class WebsiteModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entity_category = EntityCategory.objects.create(name='individual')
        cls.entity1 = Entity.objects.create(category=cls.entity_category, last_name='test1')
        cls.entity2 = Entity.objects.create(category=cls.entity_category, last_name='test2')
        cls.entity3 = Entity.objects.create(category=cls.entity_category, last_name='test3')

    def test_website_creation(self):
        website = Website.objects.create(
            address="https://testing.com",
            owner=self.entity3,
            notes='test notes 1',
        )

        website.associated_entities.add(self.entity1, self.entity2)

        retrieved_website = Website.objects.get(pk=1)
        retrieved_website_entities = retrieved_website.associated_entities.all()
        expected_entities = [1, 2]

        self.assertEqual(retrieved_website.address, "https://testing.com")
        self.assertEqual(retrieved_website.owner.last_name, 'test3')
        self.assertEqual(retrieved_website.notes, 'test notes 1')

        for entity in retrieved_website_entities:
            self.assertIn(entity.pk, expected_entities)

        self.assertEqual(retrieved_website.associated_entities.get(pk=1).last_name, "test1")
        self.assertEqual(retrieved_website.associated_entities.get(pk=2).last_name, "test2")
        self.assertEqual(Entity.objects.get(pk=1).entity_websites.get(pk=1).address, "https://testing.com")
        self.assertEqual(Entity.objects.get(pk=2).entity_websites.get(pk=1).address, "https://testing.com")


class AssumedNameModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.entity_category = EntityCategory.objects.create(name='individual')
        cls.entity1 = Entity.objects.create(category=cls.entity_category, last_name='test1')
        cls.entity2 = Entity.objects.create(category=cls.entity_category, last_name='test2')

    def test_assumed_name_creation(self):
        assumed_name = AssumedName.objects.create(
            name="test partners",
            notes='test notes 1',
        )

        assumed_name.associated_entities.add(self.entity1, self.entity2)

        retrieved_assumed_name = AssumedName.objects.get(pk=1)
        retrieved_assumed_name_entities = retrieved_assumed_name.associated_entities.all()
        expected_entities = [1, 2]

        self.assertEqual(retrieved_assumed_name.name, "test partners")
        self.assertEqual(retrieved_assumed_name.notes, "test notes 1")

        for entity in retrieved_assumed_name_entities:
            self.assertIn(entity.pk, expected_entities)

        self.assertEqual(retrieved_assumed_name.associated_entities.get(pk=1).last_name, "test1")
        self.assertEqual(retrieved_assumed_name.associated_entities.get(pk=2).last_name, "test2")
        self.assertEqual(Entity.objects.get(pk=1).entity_assumed_names.get(pk=1).name, "test partners")
        self.assertEqual(Entity.objects.get(pk=2).entity_assumed_names.get(pk=1).name, "test partners")


class AddressIndexViewTests(TestCase):
    def test_correct_template(self):
        response = self.client.get(reverse('campaignfinance:addressindex'))
        self.assertTemplateUsed(response, 'campaignfinance/addressindex.html')

    def test_no_addresses(self):
        response = self.client.get(reverse('campaignfinance:addressindex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No data found.")
        self.assertQuerysetEqual(response.context['address_list'], [])

    def test_two_addresses(self):
        address_category = AddressCategory.objects.create(name="building")
        address1 = Address.objects.create(
            category=address_category,
            building_number='1234',
            street_name='jackson street',
            unit_number='4',
            city_name='san angelo',
            state_name='texas',
            county_name='tom green',
            zip_code='76903',
            zip_code_extension='5555'
        )
        address2 = Address.objects.create(
            category=address_category,
            building_number='4321',
            street_name='Tom Avenue',
            city_name='Lubbock',
            state_name='Texas',
            county_name='Lubbock',
            zip_code='56789'
        )
        response = self.client.get(reverse('campaignfinance:addressindex'))
        self.assertQuerysetEqual(response.context['address_list'], [address2, address1])


class AddressDetailViewTests(TestCase):
    def test_incorrect_uuid_404(self):
        response = self.client.get(reverse('campaignfinance:addressdetail', args=('dd8a0db4-7fb3-4a8b-a8a9-74e5c3b998b5',)))
        self.assertEqual(response.status_code, 404)

    def test_address_detail(self):
        address_category = AddressCategory.objects.create(name='Building')
        address = Address.objects.create(
            category=address_category,
            building_number=1234,
            street_name='John Street',
            unit_number=12,
            floor_number=3,
            city_name='San Angelo',
            state_name='Texas',
            county_name='Tom Green',
            zip_code=76901,
            zip_code_extension='1111',
            notes='Test Notes',
        )
        entity_category = EntityCategory.objects.create(name='Individual')
        entity1 = Entity.objects.create(category=entity_category, last_name='entity1')
        entity2 = Entity.objects.create(category=entity_category, last_name='entity2')
        address.owners.add(entity1)
        address.residents.add(entity2)
        response = self.client.get(reverse('campaignfinance:addressdetail', args=(address.uuid,)))
        self.assertContains(response, '1234')
        self.assertContains(response, 'John Street')
        self.assertContains(response, '12')
        self.assertContains(response, '3')
        self.assertContains(response, 'San Angelo')
        self.assertContains(response, 'Texas')
        self.assertContains(response, 'Tom Green')
        self.assertContains(response, '76901')
        self.assertContains(response, '1111')
        self.assertContains(response, 'Test Notes')
        self.assertContains(response, 'entity1')
        self.assertContains(response, 'entity2')


class AssumedNameIndexViewTests(TestCase):
    def test_correct_template(self):
        response = self.client.get(reverse('campaignfinance:assumednameindex'))
        self.assertTemplateUsed(response, 'campaignfinance/assumednameindex.html')

    def test_no_assumed_names(self):
        response = self.client.get(reverse('campaignfinance:assumednameindex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No data found.')
        self.assertQuerysetEqual(response.context['assumed_name_list'], [])

    def test_two_assumed_names(self):
        assumed_name1 = AssumedName.objects.create(name='name1')
        assumed_name2 = AssumedName.objects.create(name='name2')
        response = self.client.get(reverse('campaignfinance:assumednameindex'))
        self.assertQuerysetEqual(response.context['assumed_name_list'], [assumed_name1, assumed_name2])


class AssumedNameDetailViewTests(TestCase):
    def test_incorrect_uuid_404(self):
        response = self.client.get(reverse('campaignfinance:assumednamedetail', args=('dd8a0db4-7fb3-4a8b-a8a9-74e5c3b998b5',)))
        self.assertEqual(response.status_code, 404)

    def test_assumed_name_detail(self):
        assumed_name = AssumedName.objects.create(
            name='Brothers LLC',
            notes='Test notes'
        )
        entity_category = EntityCategory.objects.create(name='Individual')
        entity1 = Entity.objects.create(category=entity_category, last_name='entity1')
        entity2 = Entity.objects.create(category=entity_category, last_name='entity2')
        assumed_name.associated_entities.add(entity1, entity2)
        response = self.client.get(reverse('campaignfinance:assumednamedetail', args=(assumed_name.uuid,)))
        self.assertContains(response, 'Brothers LLC')
        self.assertContains(response, 'Test notes')
        self.assertContains(response, 'entity1')
        self.assertContains(response, 'entity2')


class CampaignIndexViewTests(TestCase):
    def test_correct_template(self):
        response = self.client.get(reverse('campaignfinance:campaignindex'))
        self.assertTemplateUsed(response, 'campaignfinance/campaignindex.html')

    def test_no_campaigns(self):
        response = self.client.get(reverse('campaignfinance:campaignindex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No data found.')
        self.assertQuerysetEqual(response.context['campaign_list'], [])

    def test_two_campaigns(self):
        entity_category1 = EntityCategory.objects.create(name='Government')
        entity_category2 = EntityCategory.objects.create(name='Individual')
        campaign_category = CampaignCategory.objects.create(name='Candidate')
        candidate_entity1 = Entity.objects.create(category=entity_category2, last_name='candidate1')
        candidate_entity2 = Entity.objects.create(category=entity_category2, last_name='candidate2')
        office = Office.objects.create(name='Mayor')
        campaign1 = Campaign.objects.create(
            category=campaign_category,
            name='campaign1',
            candidate_entity=candidate_entity1,
            office_sought=office,
            registration_date='2023-03-01',
        )
        campaign2 = Campaign.objects.create(
            category=campaign_category,
            name='campaign2',
            candidate_entity=candidate_entity2,
            office_sought=office,
            registration_date='2023-02-01',
        )
        response = self.client.get(reverse('campaignfinance:campaignindex'))
        self.assertQuerysetEqual(response.context['campaign_list'], [campaign1, campaign2],)
        self.assertContains(response, 'campaign1')
        self.assertContains(response, 'campaign2')
        self.assertContains(response, 'Candidate')
        self.assertContains(response, 'Mayor')
        self.assertContains(response, 'March 1, 2023')
        self.assertContains(response, 'Feb. 1, 2023')


class CampaignDetailViewTests(TestCase):
    def test_incorrect_uuid_404(self):
        response = self.client.get(reverse('campaignfinance:campaigndetail', args=('dd8a0db4-7fb3-4a8b-a8a9-74e5c3b998b5',)))
        self.assertEqual(response.status_code, 404)

    def test_campaign_detail(self):
        campaign_category = CampaignCategory.objects.create(name='Primary')
        entity_category1 = EntityCategory.objects.create(name='Government')
        entity_category2 = EntityCategory.objects.create(name='Individual')
        entity_category3 = EntityCategory.objects.create(name='Committee')
        government_entity = Entity.objects.create(category=entity_category1, last_name='government1')
        candidate_entity = Entity.objects.create(category=entity_category2, last_name='candidate1')
        treasurer_entity = Entity.objects.create(category=entity_category2, last_name='treasurer1')
        committee_entity = Entity.objects.create(category=entity_category3, last_name='committee1')        
        office = Office.objects.create(name='office1')
        campaign = Campaign.objects.create(
            category=campaign_category,
            name='campaign1',
            candidate_entity=candidate_entity,
            treasurer_entity=treasurer_entity,
            committee_entity=committee_entity,
            office_sought=office,
            notes='Test notes',
            registration_date='2023-01-01',
        )
        contributor = Entity.objects.create(category=entity_category2, last_name='contributor1')
        recipient = Entity.objects.create(category=entity_category2, last_name='recipient1')
        transaction_category1 = TransactionCategory.objects.create(name='Contribution')
        transaction_category2 = TransactionCategory.objects.create(name='Expenditure')
        contribution = Transaction.objects.create(
            category=transaction_category1,
            payer_entity=contributor,
            payee_entity=committee_entity,
            recorded_date='2023-01-01',
            amount=12.34
        )
        expenditure = Transaction.objects.create(
            category=transaction_category2,
            payer_entity=committee_entity,
            payee_entity=recipient,
            recorded_date='2023-02-01',
            amount=43.21
        )
        response = self.client.get(reverse('campaignfinance:campaigndetail', args=(campaign.uuid,)))
        self.assertTemplateUsed(response, 'campaignfinance/campaigndetail.html')
        self.assertContains(response, 'Primary')
        self.assertContains(response, 'campaign1')
        self.assertContains(response, 'candidate1')
        self.assertContains(response, 'treasurer1')
        self.assertContains(response, 'committee1')
        self.assertContains(response, 'office1')
        self.assertContains(response, 'Test notes')
        self.assertContains(response, 'Jan. 1, 2023')
        self.assertContains(response, 'contributor1')
        self.assertContains(response, 'recipient1')
        self.assertContains(response, 'Jan. 1, 2023')
        self.assertContains(response, '$12.34')
        self.assertContains(response, 'Feb. 1, 2023')
        self.assertContains(response, '$43.21')


class DocumentIndexViewTests(TestCase):
    def test_correct_template(self):
        response = self.client.get(reverse('campaignfinance:documentindex'))
        self.assertTemplateUsed(response, 'campaignfinance/documentindex.html')

    def test_no_documents(self):
        response = self.client.get(reverse('campaignfinance:documentindex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No data found.')
        self.assertQuerysetEqual(response.context['document_list'], [])

    def test_two_documents(self):
        document_category1 = DocumentCategory.objects.create(name='8 Days Before Election')
        document_category2 = DocumentCategory.objects.create(name='30 Days Before Election')
        entity_category = EntityCategory.objects.create(name='Individual')
        filer_entity1 = Entity.objects.create(category=entity_category, last_name='filer_entity1')
        filer_entity2 = Entity.objects.create(category=entity_category, last_name='filer_entity2')
        document1 = Document.objects.create(
            category=document_category1,
            filer_entity=filer_entity1,
            name='document1',
            date_filed='2023-04-06',
            coverage_start_date='2023-03-01',
            coverage_end_date='2023-04-06',
        )
        document2 = Document.objects.create(
            category=document_category2,
            filer_entity=filer_entity2,
            name='document2',
            date_filed='2023-02-27',
            coverage_start_date='2023-02-01',
            coverage_end_date='2023-02-27',
        )
        response = self.client.get(reverse('campaignfinance:documentindex'))
        self.assertQuerysetEqual(response.context['document_list'], [document2, document1],)
        self.assertContains(response, 'document1')
        self.assertContains(response, 'document2')
        self.assertContains(response, 'filer_entity1')
        self.assertContains(response, 'filer_entity2')
        self.assertContains(response, 'April 6, 2023')
        self.assertContains(response, 'Feb. 27, 2023')


class DocumentDetailViewTests(TestCase):
    def test_incorrect_uuid_404(self):
        response = self.client.get(reverse('campaignfinance:documentdetail', args=('dd8a0db4-7fb3-4a8b-a8a9-74e5c3b998b5',)))
        self.assertEqual(response.status_code, 404)

    def test_document_detail(self):
        document_category = DocumentCategory.objects.create(name='documenttype1')
        entity_category1 = EntityCategory.objects.create(name='Government')
        entity_category2 = EntityCategory.objects.create(name='Individual')
        government_entity = Entity.objects.create(category=entity_category1, last_name='government1')
        filer = Entity.objects.create(category=entity_category2, last_name='filer1')
        candidate = Entity.objects.create(category=entity_category2, last_name='candidate1')
        campaign = Campaign.objects.create(candidate_entity=candidate, registration_date='2023-04-04')
        officer = Entity.objects.create(category=entity_category2, last_name='officer1')
        document = Document.objects.create(
            category=document_category,
            name='document1',
            filer_entity=filer,
            officer_oath_entity=officer,
            date_filed='2023-01-01',
            coverage_start_date='2023-02-02',
            coverage_end_date='2023-03-03',
            notes='Test notes'
        )
        subtotals = ReportedSubtotals.objects.create(document=document)
        totals = ReportedTotals.objects.create(document=document)
        response = self.client.get(reverse('campaignfinance:documentdetail', args=(document.uuid,)))
        self.assertTemplateUsed(response, 'campaignfinance/documentdetail.html')
        self.assertContains(response, 'documenttype1')
        self.assertContains(response, 'document1')
        self.assertContains(response, 'filer1')
        self.assertContains(response, 'officer1')
        self.assertContains(response, 'Jan. 1, 2023')
        self.assertContains(response, 'Feb. 2, 2023')
        self.assertContains(response, 'March 3, 2023')
        self.assertContains(response, 'document1.pdf')
        self.assertContains(response, 'Test notes')


class ElectionIndexViewTests(TestCase):
    def test_correct_template(self):
        response = self.client.get(reverse('campaignfinance:electionindex'))
        self.assertTemplateUsed(response, 'campaignfinance/electionindex.html')

    def test_no_elections(self):
        response = self.client.get(reverse('campaignfinance:electionindex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No data found.')
        self.assertQuerysetEqual(response.context['election_list'], [])

    def test_two_elections(self):
        election_category1 = ElectionCategory.objects.create(name='Primary')
        election_category2 = ElectionCategory.objects.create(name='Runoff')
        entity_category = EntityCategory.objects.create(name='Government')
        government_entity = Entity.objects.create(category=entity_category, last_name='City of San Angelo')
        election1 = Election.objects.create(
            category=election_category1,
            government_entity=government_entity,
            date='2023-05-06',
        )
        election2 = Election.objects.create(
            category=election_category2,
            government_entity=government_entity,
            date='2023-05-10',
        )
        response = self.client.get(reverse('campaignfinance:electionindex'))
        self.assertQuerysetEqual(response.context['election_list'], [election2, election1],)
        self.assertContains(response, 'Primary')
        self.assertContains(response, 'Runoff')
        self.assertContains(response, 'May 6, 2023')
        self.assertContains(response, 'May 10, 2023')
        self.assertContains(response, 'City of San Angelo')


class ElectionDetailViewTests(TestCase):
    def test_incorrect_uuid_404(self):
        response = self.client.get(reverse('campaignfinance:electiondetail', args=('dd8a0db4-7fb3-4a8b-a8a9-74e5c3b998b5',)))
        self.assertEqual(response.status_code, 404)

    def test_election_detail(self):
        election_category = ElectionCategory.objects.create(name='Municipal')
        entity_category1 = EntityCategory.objects.create(name='Government')
        entity_category2 = EntityCategory.objects.create(name='Individual')
        government_entity = Entity.objects.create(category=entity_category1, last_name='government1')
        candidate_entity = Entity.objects.create(category=entity_category2, last_name='candidate1')
        campaign_category = CampaignCategory.objects.create(name='campaign1')
        office = Office.objects.create(name='office1')
        campaign = Campaign.objects.create(
            category=campaign_category,
            name='campaign1',
            candidate_entity=candidate_entity,
            office_sought=office,
            registration_date='2023-02-02',
        )
        election = Election.objects.create(
            category=election_category,
            government_entity=government_entity,
            date='2023-01-01',
        )
        election.election_campaigns.add(campaign)
        response = self.client.get(reverse('campaignfinance:electiondetail', args=(election.uuid,)))
        self.assertTemplateUsed(response, 'campaignfinance/electiondetail.html')
        self.assertContains(response, 'Municipal')
        self.assertContains(response, 'government1')
        self.assertContains(response, 'Jan. 1, 2023')
        self.assertContains(response, 'campaign1')
        self.assertContains(response, 'office1')


class EmailIndexViewTests(TestCase):
    def test_correct_template(self):
        response = self.client.get(reverse('campaignfinance:emailindex'))
        self.assertTemplateUsed(response, 'campaignfinance/emailindex.html')

    def test_no_emails(self):
        response = self.client.get(reverse('campaignfinance:emailindex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No data found.')
        self.assertQuerysetEqual(response.context['email_list'], [])

    def test_two_emails(self):
        email1 = Email.objects.create(address='test@example.com')
        email2 = Email.objects.create(address='johndoe@example.com')
        response = self.client.get(reverse('campaignfinance:emailindex'))
        self.assertQuerysetEqual(response.context['email_list'], [email2, email1],)
        self.assertContains(response, 'test@example.com')
        self.assertContains(response, 'johndoe@example.com')


class EmailDetailViewTests(TestCase):
    def test_incorrect_uuid_404(self):
        response = self.client.get(reverse('campaignfinance:emaildetail', args=('dd8a0db4-7fb3-4a8b-a8a9-74e5c3b998b5',)))
        self.assertEqual(response.status_code, 404)

    def test_email_detail(self):
        entity_category = EntityCategory.objects.create(name='Individual')
        entity1 = Entity.objects.create(category=entity_category, last_name='entity1')
        email = Email.objects.create(address='test@example.com')
        email.associated_entities.add(entity1)
        response = self.client.get(reverse('campaignfinance:emaildetail', args=(email.uuid,)))
        self.assertTemplateUsed(response, 'campaignfinance/emaildetail.html')
        self.assertContains(response, 'entity1')
        self.assertContains(response, 'test@example.com')


class ExternalIdIndexViewTests(TestCase):
    def test_correct_template(self):
        response = self.client.get(reverse('campaignfinance:externalidindex'))
        self.assertTemplateUsed(response, 'campaignfinance/externalidindex.html')

    def test_no_external_ids(self):
        response = self.client.get(reverse('campaignfinance:externalidindex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No data found.')
        self.assertQuerysetEqual(response.context['external_id_list'], [])

    def test_two_external_ids(self):
        entity_category1 = EntityCategory.objects.create(name='Government')
        entity_category2 = EntityCategory.objects.create(name='Committee')
        government_entity = Entity.objects.create(category=entity_category1, last_name='Texas Ethics Commission')
        entity1 = Entity.objects.create(category=entity_category2, last_name='committee1')
        entity2 = Entity.objects.create(category=entity_category2, last_name='committee2')
        external_id1 = ExternalId.objects.create(
            parent_entity=government_entity,
            child_entity=entity1,
            number='1234'
        )
        external_id2 = ExternalId.objects.create(
            parent_entity=government_entity,
            child_entity=entity2,
            number='5678'
        )
        response = self.client.get(reverse('campaignfinance:externalidindex'))
        self.assertQuerysetEqual(response.context['external_id_list'], [external_id1, external_id2],)
        self.assertContains(response, 'Texas Ethics Commission')
        self.assertContains(response, 'committee1')
        self.assertContains(response, 'committee2')
        self.assertContains(response, '1234')
        self.assertContains(response, '5678')


class ExternalIdDetailViewTests(TestCase):
    def test_incorrect_uuid_404(self):
        response = self.client.get(reverse('campaignfinance:externaliddetail', args=('dd8a0db4-7fb3-4a8b-a8a9-74e5c3b998b5',)))
        self.assertEqual(response.status_code, 404)

    def test_external_id_detail(self):
        entity_category1 = EntityCategory.objects.create(name='Government')
        entity_category2 = EntityCategory.objects.create(name='Committee')
        government_entity = Entity.objects.create(category=entity_category1, last_name='government1')
        committee_entity = Entity.objects.create(category=entity_category2, last_name='committee1')
        external_id = ExternalId.objects.create(
            parent_entity=government_entity,
            child_entity=committee_entity,
            number='123456'
        )
        response = self.client.get(reverse('campaignfinance:externaliddetail', args=(external_id.uuid,)))
        self.assertTemplateUsed(response, 'campaignfinance/externaliddetail.html')
        self.assertContains(response, 'government1')
        self.assertContains(response, 'committee1')
        self.assertContains(response, '123456')


class EntityIndexViewTests(TestCase):
    def test_correct_template(self):
        response = self.client.get(reverse('campaignfinance:entityindex'))
        self.assertTemplateUsed(response, 'campaignfinance/entityindex.html')

    def test_no_entities(self):
        response = self.client.get(reverse('campaignfinance:entityindex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No data found.')
        self.assertQuerysetEqual(response.context['entity_list'], [])

    def test_two_entities(self):
        entity_category = EntityCategory.objects.create(name='Individual')
        entity1 = Entity.objects.create(
            category=entity_category,
            first_name='John',
            last_name='Doe'
        )
        entity2 = Entity.objects.create(
            category=entity_category,
            first_name='Jane',
            last_name='Doe'
        )
        response = self.client.get(reverse('campaignfinance:entityindex'))
        self.assertQuerysetEqual(response.context['entity_list'], [entity1, entity2])
        self.assertContains(response, 'John')
        self.assertContains(response, 'Jane')
        self.assertContains(response, 'Doe')
        self.assertContains(response, 'Individual')


class EntityDetailViewTests(TestCase):
    def test_incorrect_uuid_404(self):
        response = self.client.get(reverse('campaignfinance:entitydetail', args=('dd8a0db4-7fb3-4a8b-a8a9-74e5c3b998b5',)))
        self.assertEqual(response.status_code, 404)

    def test_entity_detail(self):
        entity_category1 = EntityCategory.objects.create(name='individual')
        entity_category2 = EntityCategory.objects.create(name='government')
        entity_category3 = EntityCategory.objects.create(name='corporation')
        entity_category4 = EntityCategory.objects.create(name='committee')
        industry_sector1 = IndustrySector.objects.create(name='construction')
        industry1 = Industry.objects.create(sector=industry_sector1, name='Home Building')
        test_entity = Entity.objects.create(
            category=entity_category1,
            first_name='test_entity_first_name',
            middle_name='test_entity_middle_name',
            last_name='test_entity_last_name',
            prefix='Mr',
            suffix='Jr',
            nickname='test_entity_nickname',
            occupation='Carpenter',
            industry=industry1,
            notes='Test notes'
        )
        transaction_category1 = TransactionCategory.objects.create(name='Contribution')
        transaction_category2 = TransactionCategory.objects.create(name='Expenditure')
        committee_entity1 = Entity.objects.create(category=entity_category4, last_name='committee_entity1')
        contribution_transaction = Transaction.objects.create(
            category=transaction_category1,
            payer_entity=test_entity,
            payee_entity=committee_entity1,
            amount=12.34,
            recorded_date='2023-01-01'
        )
        committee_entity2 = Entity.objects.create(category=entity_category4, last_name='committee_entity2')
        expenditure_transaction = Transaction.objects.create(
            category=transaction_category2,
            payer_entity=committee_entity2,
            payee_entity=test_entity,
            amount=56.78,
            recorded_date='2023-02-02'
        )
        office1 = Office.objects.create(name='office1')
        campaign_category1 = CampaignCategory.objects.create(name='Primary')
        campaign1 = Campaign.objects.create(
            category=campaign_category1,
            name='campaign1',
            candidate_entity=test_entity,
            office_sought=office1,
            registration_date='2023-12-12',
        )
        office2 = Office.objects.create(name='office2', holder_entity=test_entity)
        office3 = Office.objects.create(name='office3')
        formeroffice1 = FormerOfficeHolder.objects.create(
            office=office3,
            entity=test_entity
        )
        employer_entity1 = Entity.objects.create(category=entity_category3, last_name='employer_entity1')
        relationship_category1 = RelationshipCategory.objects.create(name='Employer')
        relationship1 = Relationship.objects.create(
            category=relationship_category1,
            parent_entity=employer_entity1,
            child_entity=test_entity
        )
        address_category1 = AddressCategory.objects.create(name='Building')
        address1 = Address.objects.create(
            category=address_category1,
            building_number='9301',
            street_name='John Street',
            unit_number='101',
            city_name='San Angelo',
            state_name='Texas',
            zip_code='76901'
        )
        address1.residents.add(test_entity)
        address2 = Address.objects.create(
            category=address_category1,
            building_number='2845',
            street_name='Joe Avenue',
            unit_number='202',
            city_name='Seattle',
            state_name='Washington',
            zip_code='55555'
        )
        address2.owners.add(test_entity)
        email1 = Email.objects.create(address='test@example.com', owner=test_entity)
        phone_number1 = PhoneNumber.objects.create(
            country_code='1',
            area_code='325',
            number='6669009',
            owner=test_entity,
        )
        website1 = Website.objects.create(address='https://test.com', owner=test_entity)
        government_entity1 = Entity.objects.create(category=entity_category2, last_name='government_entity1')
        external_id1 = ExternalId.objects.create(
            parent_entity=government_entity1,
            child_entity=test_entity,
            number='78393027'
        )
        response = self.client.get(reverse('campaignfinance:entitydetail', args=(test_entity.uuid,)))
        self.assertTemplateUsed(response, 'campaignfinance/entitydetail.html')
        self.assertContains(response, 'Individual')
        self.assertContains(response, 'test_entity_first_name')
        self.assertContains(response, 'test_entity_middle_name')
        self.assertContains(response, 'test_entity_last_name')
        self.assertContains(response, 'Mr')
        self.assertContains(response, 'Jr')
        self.assertContains(response, 'test_entity_nickname')
        self.assertContains(response, 'Carpenter')
        self.assertContains(response, 'Home Building')
        self.assertContains(response, 'Test notes')
        self.assertContains(response, 'committee_entity1')
        self.assertContains(response, '12.34')
        self.assertContains(response, 'committee_entity2')
        self.assertContains(response, '56.78')
        self.assertContains(response, 'office1')
        self.assertContains(response, 'office2')
        self.assertContains(response, 'office3')
        self.assertContains(response, 'Employer')
        self.assertContains(response, 'employer_entity1')
        self.assertContains(response, '9301')
        self.assertContains(response, 'John Street')
        self.assertContains(response, '101')
        self.assertContains(response, 'San Angelo')
        self.assertContains(response, 'Texas')
        self.assertContains(response, '76901')
        self.assertContains(response, '2845')
        self.assertContains(response, 'Joe Avenue')
        self.assertContains(response, '202')
        self.assertContains(response, 'Seattle')
        self.assertContains(response, 'Washington')
        self.assertContains(response, '55555')
        self.assertContains(response, 'test@example.com')
        self.assertContains(response, '325')
        self.assertContains(response, '666')
        self.assertContains(response, '9009')
        self.assertContains(response, 'https://test.com')


class FormerOfficeHolderIndexViewTests(TestCase):
    def test_correct_template(self):
        response = self.client.get(reverse('campaignfinance:formerofficeholderindex'))
        self.assertTemplateUsed(response, 'campaignfinance/formerofficeholderindex.html')

    def test_no_former_office_holders(self):
        response = self.client.get(reverse('campaignfinance:formerofficeholderindex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No data found.')
        self.assertQuerysetEqual(response.context['former_office_holder_list'], [])

    def test_two_former_office_holders(self):
        office1 = Office.objects.create(name='Mayor')
        office2 = Office.objects.create(name='Council Member District 5')
        entity_category = EntityCategory.objects.create(name='Individual')
        entity1 = Entity.objects.create(
            category=entity_category,
            first_name='John',
            last_name='Doe'
        )
        entity2 = Entity.objects.create(
            category=entity_category,
            first_name='Jane',
            last_name='Doe'
        )
        formerholder1 = FormerOfficeHolder.objects.create(
            office=office1,
            entity=entity1,
        )
        formerholder2 = FormerOfficeHolder.objects.create(
            office=office2,
            entity=entity2
        )
        response = self.client.get(reverse('campaignfinance:formerofficeholderindex'))
        self.assertQuerysetEqual(response.context['former_office_holder_list'], [formerholder1, formerholder2])
        self.assertContains(response, 'Mayor')
        self.assertContains(response, 'Council Member District 5')
        self.assertContains(response, 'John')
        self.assertContains(response, 'Jane')
        self.assertContains(response, 'Doe')


class IndustryIndexViewTests(TestCase):
    def test_correct_template(self):
        response = self.client.get(reverse('campaignfinance:industryindex'))
        self.assertTemplateUsed(response, 'campaignfinance/industryindex.html')

    def test_no_industries(self):
        response = self.client.get(reverse('campaignfinance:industryindex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No data found.')
        self.assertQuerysetEqual(response.context['industry_list'], [])

    def test_two_industries(self):
        industrysector1 = IndustrySector.objects.create(name='Construction')
        industrysector2 = IndustrySector.objects.create(name='Media')
        industry1 = Industry.objects.create(sector=industrysector1, name='Home Building')
        industry2 = Industry.objects.create(sector=industrysector2, name='Television')
        response = self.client.get(reverse('campaignfinance:industryindex'))
        self.assertQuerysetEqual(response.context['industry_list'], [industry1, industry2],)
        self.assertContains(response, 'Construction')
        self.assertContains(response, 'Media')
        self.assertContains(response, 'Home Building')
        self.assertContains(response, 'Television') 


class IndustrySectorIndexViewTests(TestCase):
    def test_correct_template(self):
        response = self.client.get(reverse('campaignfinance:industrysectorindex'))
        self.assertTemplateUsed(response, 'campaignfinance/industrysectorindex.html')

    def test_no_industry_sectors(self):
        response = self.client.get(reverse('campaignfinance:industrysectorindex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No data found.')
        self.assertQuerysetEqual(response.context['industry_sector_list'], [])

    def test_two_industry_sectors(self):
        industrysector1 = IndustrySector.objects.create(name='Construction')
        industrysector2 = IndustrySector.objects.create(name='Media')
        response = self.client.get(reverse('campaignfinance:industrysectorindex'))
        self.assertQuerysetEqual(response.context['industry_sector_list'], [industrysector1, industrysector2],)
        self.assertContains(response, 'Construction')
        self.assertContains(response, 'Media')


class IndustrySectorDetailViewTests(TestCase):
    def test_incorrect_uuid_404(self):
        response = self.client.get(reverse('campaignfinance:industrysectordetail', args=('dd8a0db4-7fb3-4a8b-a8a9-74e5c3b998b5',)))
        self.assertEqual(response.status_code, 404)

    def test_industry_sector_detail(self):
        industry_sector1 = IndustrySector.objects.create(name='Construction')
        industry1 = Industry.objects.create(sector=industry_sector1, name='Home Building')
        response = self.client.get(reverse('campaignfinance:industrysectordetail', args=(industry_sector1.uuid,)))
        self.assertTemplateUsed(response, 'campaignfinance/industrysectordetail.html')
        self.assertContains(response, 'Construction')
        self.assertContains(response, 'Home Building')


class OfficeIndexViewTests(TestCase):
    def test_correct_template(self):
        response = self.client.get(reverse('campaignfinance:officeindex'))
        self.assertTemplateUsed(response, 'campaignfinance/officeindex.html')

    def test_no_offices(self):
        response = self.client.get(reverse('campaignfinance:officeindex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No data found.')
        self.assertQuerysetEqual(response.context['office_list'], [])

    def test_two_offices(self):
        entity_category1 = EntityCategory.objects.create(name='Government')
        entity_category2 = EntityCategory.objects.create(name='Individual')
        government_entity = Entity.objects.create(category=entity_category1, last_name='City of San Angelo')
        entity1 = Entity.objects.create(category=entity_category1, last_name='entity1')
        entity2 = Entity.objects.create(category=entity_category2, last_name='entity2')
        office1 = Office.objects.create(
            name='office1',
            government_entity=government_entity,
            holder_entity=entity1
        )
        office2 = Office.objects.create(
            name='office2',
            government_entity=government_entity,
            holder_entity=entity2
        )
        response = self.client.get(reverse('campaignfinance:officeindex'))
        self.assertQuerysetEqual(response.context['office_list'], [office1, office2],)
        self.assertContains(response, 'office1')
        self.assertContains(response, 'office2')
        self.assertContains(response, 'City of San Angelo')
        self.assertContains(response, 'entity1')
        self.assertContains(response, 'entity2')


class OfficeDetailViewTests(TestCase):
    def test_incorrect_uuid_404(self):
        response = self.client.get(reverse('campaignfinance:officedetail', args=('dd8a0db4-7fb3-4a8b-a8a9-74e5c3b998b5',)))

    def test_office_detail(self):
        entity_category1 = EntityCategory.objects.create(name='Individual')
        entity_category2 = EntityCategory.objects.create(name='Government')
        government_entity1 = Entity.objects.create(category=entity_category2, last_name='government_entity1')
        officer_holder1 = Entity.objects.create(category=entity_category1, last_name='office_holder1')
        office1 = Office.objects.create(
            government_entity=government_entity1,
            holder_entity=officer_holder1,
            name='office1'
        )
        response = self.client.get(reverse('campaignfinance:officedetail', args=(office1.uuid,)))
        self.assertTemplateUsed(response, 'campaignfinance/officedetail.html')
        self.assertContains(response, 'government_entity1')
        self.assertContains(response, 'office_holder1')
        self.assertContains(response, 'office1')


class PhoneNumberIndexViewTests(TestCase):
    def test_correct_template(self):
        response = self.client.get(reverse('campaignfinance:phonenumberindex'))
        self.assertTemplateUsed(response, 'campaignfinance/phonenumberindex.html')

    def test_no_phone_numbers(self):
        response = self.client.get(reverse('campaignfinance:phonenumberindex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No data found.')
        self.assertQuerysetEqual(response.context['phone_number_list'], [])

    def test_two_phone_numbers(self):
        phone_number1 = PhoneNumber.objects.create(
            country_code='1',
            area_code='325',
            number='5551234',
        )
        phone_number2 = PhoneNumber.objects.create(
            country_code='1',
            area_code='101',
            number='5555678',
        )
        response = self.client.get(reverse('campaignfinance:phonenumberindex'))
        self.assertQuerysetEqual(response.context['phone_number_list'], [phone_number2, phone_number1],)
        self.assertContains(response, '325 5551234')
        self.assertContains(response, '101 5555678')


class PhoneNumberDetailViewTests(TestCase):
    def test_incorrect_uuid_404(self):
        response = self.client.get(reverse('campaignfinance:phonenumberdetail', args=('dd8a0db4-7fb3-4a8b-a8a9-74e5c3b998b5',)))
        self.assertEqual(response.status_code, 404)

    def test_phone_number_detail(self):
        phone_number1 = PhoneNumber.objects.create(
            country_code='1',
            area_code='325',
            number='5559008',
        )
        entity_category1 = EntityCategory.objects.create(name='Individual')
        entity1 = Entity.objects.create(category=entity_category1, last_name='entity1')
        phone_number1.associated_entities.add(entity1)
        response = self.client.get(reverse('campaignfinance:phonenumberdetail', args=(phone_number1.uuid,)))
        self.assertTemplateUsed(response, 'campaignfinance/phonenumberdetail.html')
        self.assertContains(response, '1')
        self.assertContains(response, '325')
        self.assertContains(response, '5559008')
        self.assertContains(response, 'entity1')
        self.assertContains(response, '325 5559008')


class RelationshipIndexViewTests(TestCase):
    def test_correct_template(self):
        response = self.client.get(reverse('campaignfinance:relationshipindex'))
        self.assertTemplateUsed(response, 'campaignfinance/relationshipindex.html')

    def test_no_relationships(self):
        response = self.client.get(reverse('campaignfinance:relationshipindex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No data found.')
        self.assertQuerysetEqual(response.context['relationship_list'], [])

    def test_two_relationships(self):
        entity_category1 = EntityCategory.objects.create(name='Company')
        entity_category2 = EntityCategory.objects.create(name='Individual')
        entity1 = Entity.objects.create(category=entity_category1, last_name='company1')
        entity2 = Entity.objects.create(category=entity_category1, last_name='company2')
        entity3 = Entity.objects.create(category=entity_category2, last_name='entity1')
        entity4 = Entity.objects.create(category=entity_category2, last_name='entity2')
        relationship_category = RelationshipCategory.objects.create(name='Employer')
        relationship1 = Relationship.objects.create(
            category=relationship_category,
            parent_entity=entity1,
            child_entity=entity3,
        )
        relationship2 = Relationship.objects.create(
            category=relationship_category,
            parent_entity=entity2,
            child_entity=entity4,
        )
        response = self.client.get(reverse('campaignfinance:relationshipindex'))
        self.assertQuerysetEqual(response.context['relationship_list'], [relationship1, relationship2],)
        self.assertContains(response, 'company1')
        self.assertContains(response, 'company2')
        self.assertContains(response, 'entity1')
        self.assertContains(response, 'entity2')
        self.assertContains(response, 'Employer')


class RelationshipDetailViewTests(TestCase):
    def test_incorrect_uuid_404(self):
        response = self.client.get(reverse('campaignfinance:relationshipdetail', args=('dd8a0db4-7fb3-4a8b-a8a9-74e5c3b998b5',)))
        self.assertEqual(response.status_code, 404)

    def test_relationship_detail(self):
        entity_category1 = EntityCategory.objects.create(name='Corporation')
        entity_category2 = EntityCategory.objects.create(name='Individual')
        entity1 = Entity.objects.create(category=entity_category1, last_name='entity1')
        entity2 = Entity.objects.create(category=entity_category2, last_name='entity2')
        relationship_category1 = RelationshipCategory.objects.create(name='Employer')
        relationship1 = Relationship.objects.create(
            category=relationship_category1,
            parent_entity=entity1,
            child_entity=entity2,
            notes='Test notes'
        )
        response = self.client.get(reverse('campaignfinance:relationshipdetail', args=(relationship1.uuid,)))
        self.assertTemplateUsed(response, 'campaignfinance/relationshipdetail.html')
        self.assertContains(response, 'entity1')
        self.assertContains(response, 'entity2')
        self.assertContains(response, 'Employer')
        self.assertContains(response, 'Test notes')


class ReportedSubtotalsIndexViewTests(TestCase):
    def test_correct_template(self):
        response = self.client.get(reverse('campaignfinance:reportedsubtotalsindex'))
        self.assertTemplateUsed(response, 'campaignfinance/reportedsubtotalsindex.html')

    def test_no_reported_subtotals(self):
        response = self.client.get(reverse('campaignfinance:reportedsubtotalsindex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No data found.')
        self.assertQuerysetEqual(response.context['reported_subtotals_list'], [])

    def test_two_reported_subtotals(self):
        document_category = DocumentCategory.objects.create(name='8 Days Before Election')
        document1 = Document.objects.create(
            category=document_category,
            name='document1',
            date_filed='2023-02-01',
            coverage_start_date='2023-01-01',
            coverage_end_date='2023-01-31'
        )
        document2 = Document.objects.create(
            category=document_category,
            name='document2',
            date_filed='2023-04-01',
            coverage_start_date='2023-03-01',
            coverage_end_date='2023-03-30'
        )
        subtotals1 = ReportedSubtotals.objects.create(document=document1)
        subtotals2 = ReportedSubtotals.objects.create(document=document2)
        response = self.client.get(reverse('campaignfinance:reportedsubtotalsindex'))
        self.assertQuerysetEqual(response.context['reported_subtotals_list'], [subtotals1, subtotals2])
        self.assertContains(response, 'document1')
        self.assertContains(response, 'document2')


class ReportedSubtotalsDetailViewTests(TestCase):
    def test_incorrect_uuid_404(self):
        response = self.client.get(reverse('campaignfinance:reportedsubtotalsdetail', args=('dd8a0db4-7fb3-4a8b-a8a9-74e5c3b998b5',)))
        self.assertEqual(response.status_code, 404)

    def test_reported_subtotals_detail(self):
        entity_category1 = EntityCategory.objects.create(name='Government')
        entity_category2 = EntityCategory.objects.create(name='Individual')
        filer_entity1 = Entity.objects.create(category=entity_category2, last_name='filer_entity1')
        document1 = Document.objects.create(
            name='document1',
            filer_entity=filer_entity1,
            date_filed='2023-01-01',
            coverage_start_date='2023-02-02',
            coverage_end_date='2023-03-03',
        )
        reported_subtotals1 = ReportedSubtotals.objects.create(
            document=document1,
            monetary_political_contributions=1.11,
            non_monetary_political_contributions=2.22,
            pledged_contributions=3.33,
            monetary_corporate_labor_contributions=4.44,
            non_monetary_corporate_labor_contributions=5.55,
            pledged_corporate_labor_contributions=6.66,
            loans=7.77,
            expenditures_from_contributions=8.88,
            unpaid_incurred_obligations=9.99,
            purchased_investments_with_contributions=10.10,
            expenditures_credit_card=11.11,
            expenditures_personal_funds=12.12,
            expenditures_from_contributions_candidate_business=13.13,
            expenditures_non_political_from_contributions=14.14,
            interest_credit_gains_refunds_contributions_returned=15.15
        )
        response = self.client.get(reverse('campaignfinance:reportedsubtotalsdetail', args=(reported_subtotals1.uuid,)))
        self.assertTemplateUsed(response, 'campaignfinance/reportedsubtotalsdetail.html')
        self.assertContains(response, 'document1')
        self.assertContains(response, 'filer_entity1')
        self.assertContains(response, 'Feb. 2, 2023')
        self.assertContains(response, 'March 3, 2023')
        self.assertContains(response, '1.11')
        self.assertContains(response, '2.22')
        self.assertContains(response, '3.33')
        self.assertContains(response, '4.44')
        self.assertContains(response, '5.55')
        self.assertContains(response, '6.66')
        self.assertContains(response, '7.77')
        self.assertContains(response, '8.88')
        self.assertContains(response, '9.99')
        self.assertContains(response, '10.10')
        self.assertContains(response, '11.11')
        self.assertContains(response, '12.12')
        self.assertContains(response, '13.13')
        self.assertContains(response, '14.14')
        self.assertContains(response, '15.15')


class ReportedTotalsIndexViewTests(TestCase):
    def test_correct_template(self):
        response = self.client.get(reverse('campaignfinance:reportedtotalsindex'))
        self.assertTemplateUsed(response, 'campaignfinance/reportedtotalsindex.html')

    def test_no_reported_totals(self):
        response = self.client.get(reverse('campaignfinance:reportedtotalsindex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No data found.')
        self.assertQuerysetEqual(response.context['reported_totals_list'], [])

    def test_two_reported_totals(self):
        document_category = DocumentCategory.objects.create(name='8 Days Before Election')
        document1 = Document.objects.create(
            category=document_category,
            name='document1',
            date_filed='2023-02-01',
            coverage_start_date='2023-01-01',
            coverage_end_date='2023-01-31'
        )
        document2 = Document.objects.create(
            category=document_category,
            name='document2',
            date_filed='2023-04-01',
            coverage_start_date='2023-03-01',
            coverage_end_date='2023-03-30'
        )
        totals1 = ReportedTotals.objects.create(document=document1)
        totals2 = ReportedTotals.objects.create(document=document2)
        response = self.client.get(reverse('campaignfinance:reportedtotalsindex'))
        self.assertQuerysetEqual(response.context['reported_totals_list'], [totals1, totals2])
        self.assertContains(response, 'document1')
        self.assertContains(response, 'document2')


class ReportedTotalsDetailViewTests(TestCase):
    def test_incorrect_uuid_404(self):
        response = self.client.get(reverse('campaignfinance:reportedtotalsdetail', args=('dd8a0db4-7fb3-4a8b-a8a9-74e5c3b998b5',)))
        self.assertEqual(response.status_code, 404)

    def test_reported_totals_detail(self):
        entity_category1 = EntityCategory.objects.create(name='Government')
        entity_category2 = EntityCategory.objects.create(name='Individual')
        government_entity1 = Entity.objects.create(category=entity_category1, last_name='government_entity1')
        filer_entity1 = Entity.objects.create(category=entity_category2, last_name='filer_entity1')
        document1 = Document.objects.create(
            name='document1',
            filer_entity=filer_entity1,
            date_filed='2023-01-01',
            coverage_start_date='2023-02-02',
            coverage_end_date='2023-03-03',
        )
        reported_totals1 = ReportedTotals.objects.create(
            document=document1,
            unitemized_contributions=1.11,
            contributions=2.22,
            unitemized_expenditures=3.33,
            expenditures=4.44,
            maintained_contributions=5.55,
            principal_outstanding_loans=6.66
        )
        response = self.client.get(reverse('campaignfinance:reportedtotalsdetail', args=(reported_totals1.uuid,)))
        self.assertTemplateUsed(response, 'campaignfinance/reportedtotalsdetail.html')
        self.assertContains(response, 'document1')
        self.assertContains(response, 'filer_entity1')
        self.assertContains(response, 'Feb. 2, 2023')
        self.assertContains(response, 'March 3, 2023')
        self.assertContains(response, '1.11')
        self.assertContains(response, '2.22')
        self.assertContains(response, '3.33')
        self.assertContains(response, '4.44')
        self.assertContains(response, '5.55')
        self.assertContains(response, '6.66')


class TransactionIndexViewTests(TestCase):
    def test_correct_template(self):
        response = self.client.get(reverse('campaignfinance:reportedtotalsindex'))
        self.assertTemplateUsed(response, 'campaignfinance/reportedtotalsindex.html')

    def test_no_transactions(self):
        response = self.client.get(reverse('campaignfinance:transactionindex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No data found.')
        self.assertQuerysetEqual(response.context['transaction_list'], [])

    def test_two_transactions(self):
        entity_category1 = EntityCategory.objects.create(name='Campaign Committee')
        entity_category2 = EntityCategory.objects.create(name='Individual')
        entity_category3 = EntityCategory.objects.create(name='Corporation')
        committee1 = Entity.objects.create(category=entity_category1, last_name='committee1')
        committee2 = Entity.objects.create(category=entity_category1, last_name='committee2')
        entity1 = Entity.objects.create(category=entity_category2, last_name='entity1')
        corporation1 = Entity.objects.create(category=entity_category3, last_name='corporation1')
        transaction_category1 = TransactionCategory.objects.create(name='Contribution')
        transaction_category2 = TransactionCategory.objects.create(name='Expenditure')
        transaction1 = Transaction.objects.create(
            category=transaction_category1,
            payer_entity=entity1,
            payee_entity=committee1,
            recorded_date='2023-01-01',
            amount=12.34
        )
        transaction2 = Transaction.objects.create(
            category=transaction_category2,
            payer_entity=committee2,
            payee_entity=corporation1,
            recorded_date='2023-02-01',
            amount=34.91
        )
        response = self.client.get(reverse('campaignfinance:transactionindex'))
        self.assertQuerysetEqual(response.context['transaction_list'], [transaction1, transaction2])
        self.assertContains(response, 'committee1')
        self.assertContains(response, 'committee2')
        self.assertContains(response, 'entity1')
        self.assertContains(response, 'corporation1')
        self.assertContains(response, 'Contribution')
        self.assertContains(response, 'Expenditure')
        self.assertContains(response, 'Jan. 1, 2023')
        self.assertContains(response, 'Feb. 1, 2023')
        self.assertContains(response, '$12.34')
        self.assertContains(response, '$34.91')


class TransactionDetailViewTests(TestCase):
    def test_incorrect_uuid_404(self):
        response = self.client.get(reverse('campaignfinance:transactiondetail', args=('dd8a0db4-7fb3-4a8b-a8a9-74e5c3b998b5',)))
        self.assertEqual(response.status_code, 404)

    def test_transaction_detail(self):
        transaction_category1 = TransactionCategory.objects.create(name='Contribution')
        entity_category2 = EntityCategory.objects.create(name='Individual')
        entity_category3 = EntityCategory.objects.create(name='Committee')
        payer_entity1 = Entity.objects.create(category=entity_category2, last_name='payer_entity1')
        payee_entity1 = Entity.objects.create(category=entity_category3, last_name='payee_entity1')
        campaign_category1 = CampaignCategory.objects.create(name='campaign_category1')
        campaign1 = Campaign.objects.create(category=campaign_category1, name='campaign1', registration_date='2023-04-04')
        document1 = Document.objects.create(
            name='document1',
            date_filed='2023-01-01',
            coverage_start_date='2023-02-02',
            coverage_end_date='2023-03-03'
        )
        transaction1 = Transaction.objects.create(
            category=transaction_category1,
            payer_entity=payer_entity1,
            payee_entity=payee_entity1,
            amount=1.11,
            recorded_date='2023-05-05',
            reason='Test reason',
            document=document1,
            campaign=campaign1,
            notes='Test notes'
        )
        response = self.client.get(reverse('campaignfinance:transactiondetail', args=(transaction1.uuid,)))
        self.assertTemplateUsed(response, 'campaignfinance/transactiondetail.html')
        self.assertContains(response, 'payer_entity1')
        self.assertContains(response, 'payee_entity1')
        self.assertContains(response, '1.11')
        self.assertContains(response, 'May 5, 2023')
        self.assertContains(response, 'Test reason')
        self.assertContains(response, 'document1')
        self.assertContains(response, 'campaign1')
        self.assertContains(response, 'Test notes')


class WebsiteIndexViewTests(TestCase):
    def test_correct_template(self):
        response = self.client.get(reverse('campaignfinance:websiteindex'))
        self.assertTemplateUsed(response, 'campaignfinance/websiteindex.html')

    def test_no_websites(self):
        response = self.client.get(reverse('campaignfinance:websiteindex'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No data found.')
        self.assertQuerysetEqual(response.context['website_list'], [])

    def test_two_websites(self):
        website1 = Website.objects.create(address='https://www.bob.com')
        website2 = Website.objects.create(address='https://www.joe.com')
        response = self.client.get(reverse('campaignfinance:websiteindex'))
        self.assertQuerysetEqual(response.context['website_list'], [website1, website2],)
        self.assertContains(response, 'https://www.bob.com')
        self.assertContains(response, 'https://www.joe.com')


class WebsiteDetailViewTests(TestCase):
    def test_incorrect_uuid_404(self):
        response = self.client.get(reverse('campaignfinance:campaigndetail', args=('dd8a0db4-7fb3-4a8b-a8a9-74e5c3b998b5',)))
        self.assertEqual(response.status_code, 404)

    def test_website_detail(self):
        entity_category1 = EntityCategory.objects.create(name='Corporation')
        entity1 = Entity.objects.create(category=entity_category1, last_name='entity1')
        website1 = Website.objects.create(address='https://example.com')
        website1.associated_entities.add(entity1)
        response = self.client.get(reverse('campaignfinance:websitedetail', args=(website1.uuid,)))
        self.assertTemplateUsed(response, 'campaignfinance/websitedetail.html')
        self.assertContains(response, 'https://example.com')
        self.assertContains(response, 'entity1')
