from odoo.tests.common import TransactionCase


class TestGPJInstitutionFoundation(TransactionCase):

    def test_institution_and_related_records(self):
        institution = self.env['gpj.institution'].create({
            'name': 'Government Polytechnic Jalgaon',
            'code': 'GPJ',
            'dte_code': '5008',
            'msbte_code': '0018',
            'established_year': 1960,
            'institution_type': 'government',
        })

        campus = self.env['gpj.campus'].create({
            'name': 'Main Campus',
            'code': 'MAIN',
            'institution_id': institution.id,
        })

        department = self.env['gpj.department'].create({
            'name': 'Information Technology',
            'code': 'IT',
            'institution_id': institution.id,
            'campus_id': campus.id,
        })

        self.assertEqual(department.institution_id, institution)
        self.assertEqual(department.campus_id, campus)
