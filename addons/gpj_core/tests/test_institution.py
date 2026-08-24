from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo.exceptions import ValidationError, AccessError
from odoo import fields
from odoo import Command


@tagged('post_install', '-at_install')
class TestGPJInstitutionFoundation(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Institution = self.env['gpj.institution']
        self.Campus = self.env['gpj.campus']
        self.Department = self.env['gpj.department']
        self.OU = self.env['gpj.organizational.unit']
        self.Designation = self.env['gpj.designation']
        self.Role = self.env['gpj.institutional.role']
        self.Membership = self.env['gpj.institution.membership']
        self.Users = self.env['res.users']

    # ============================================================
    # 1-6. Basic Model Creation Tests
    # ============================================================

    def test_institution_creation(self):
        inst = self.Institution.create({
            'name': 'Government Polytechnic Jalgaon',
            'code': 'GPJ',
            'dte_code': '5008',
            'msbte_code': '0018',
            'established_year': 1960,
            'institution_type': 'government',
        })
        self.assertEqual(inst.name, 'Government Polytechnic Jalgaon')
        self.assertTrue(inst.active)

    def test_campus_creation(self):
        inst = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        campus = self.Campus.create({'name': 'Main Campus', 'code': 'MAIN', 'institution_id': inst.id})
        self.assertEqual(campus.institution_id, inst)

    def test_department_creation(self):
        inst = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        campus = self.Campus.create({'name': 'Main', 'code': 'MAIN', 'institution_id': inst.id})
        dept = self.Department.create({'name': 'IT', 'code': 'IT', 'institution_id': inst.id, 'campus_id': campus.id})
        self.assertEqual(dept.institution_id, inst)
        self.assertEqual(dept.campus_id, campus)

    def test_organizational_unit_creation(self):
        inst = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        ou = self.OU.create({'name': 'Admin', 'code': 'ADM', 'institution_id': inst.id})
        self.assertEqual(ou.institution_id, inst)

    def test_designation_creation(self):
        inst = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        desig = self.Designation.create({'name': 'Professor', 'code': 'PROF', 'institution_id': inst.id})
        self.assertEqual(desig.institution_id, inst)

    def test_institutional_role_creation(self):
        inst = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        role = self.Role.create({'name': 'Dean', 'code': 'DEAN', 'institution_id': inst.id})
        self.assertEqual(role.institution_id, inst)

    # ============================================================
    # 7. Unique Institution Code
    # ============================================================

    def test_unique_institution_code(self):
        self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        with self.assertRaises(ValidationError):
            self.Institution.create({'name': 'Inst B', 'code': 'INSTA'})

    # ============================================================
    # 8. Institution-Scoped Unique Codes
    # ============================================================

    def test_institution_scoped_unique_campus_code(self):
        inst = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        self.Campus.create({'name': 'Campus 1', 'code': 'C1', 'institution_id': inst.id})
        with self.assertRaises(ValidationError):
            self.Campus.create({'name': 'Campus 2', 'code': 'C1', 'institution_id': inst.id})

    def test_institution_scoped_unique_department_code(self):
        inst = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        self.Department.create({'name': 'IT', 'code': 'IT', 'institution_id': inst.id})
        with self.assertRaises(ValidationError):
            self.Department.create({'name': 'CS', 'code': 'IT', 'institution_id': inst.id})

    def test_institution_scoped_unique_ou_code(self):
        inst = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        self.OU.create({'name': 'Admin', 'code': 'ADM', 'institution_id': inst.id})
        with self.assertRaises(ValidationError):
            self.OU.create({'name': 'HR', 'code': 'ADM', 'institution_id': inst.id})

    def test_institution_scoped_unique_designation_code(self):
        inst = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        self.Designation.create({'name': 'Prof', 'code': 'PROF', 'institution_id': inst.id})
        with self.assertRaises(ValidationError):
            self.Designation.create({'name': 'Assoc Prof', 'code': 'PROF', 'institution_id': inst.id})

    def test_institution_scoped_unique_role_code(self):
        inst = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        self.Role.create({'name': 'Dean', 'code': 'DEAN', 'institution_id': inst.id})
        with self.assertRaises(ValidationError):
            self.Role.create({'name': 'Director', 'code': 'DEAN', 'institution_id': inst.id})

    # ============================================================
    # 9. Invalid Cross-Institution Relationships
    # ============================================================

    def test_department_campus_institution_consistency(self):
        inst_a = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        inst_b = self.Institution.create({'name': 'Inst B', 'code': 'INSTB'})
        campus_b = self.Campus.create({'name': 'Campus B', 'code': 'CAMPB', 'institution_id': inst_b.id})

        with self.assertRaises(ValidationError):
            self.Department.create({
                'name': 'IT', 'code': 'IT',
                'institution_id': inst_a.id,
                'campus_id': campus_b.id,  # Campus belongs to Inst B
            })

    def test_campus_institution_fk_enforced(self):
        inst = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        campus = self.Campus.create({'name': 'Main', 'code': 'MAIN', 'institution_id': inst.id})
        # Changing campus institution should fail if depts reference it
        dept = self.Department.create({'name': 'IT', 'code': 'IT', 'institution_id': inst.id, 'campus_id': campus.id})
        with self.assertRaises(Exception):
            campus.write({'institution_id': self.Institution.create({'name': 'X', 'code': 'X'}).id})

    # ============================================================
    # 10. Department/Campus Consistency
    # ============================================================

    def test_onchange_campus_sets_institution(self):
        inst = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        campus = self.Campus.create({'name': 'Main', 'code': 'MAIN', 'institution_id': inst.id})
        dept = self.Department.new({'name': 'IT', 'code': 'IT'})
        dept.campus_id = campus
        dept._onchange_campus_id()
        self.assertEqual(dept.institution_id, inst)

    def test_department_without_campus_allowed(self):
        inst = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        dept = self.Department.create({'name': 'Central IT', 'code': 'CIT', 'institution_id': inst.id})
        self.assertFalse(dept.campus_id)

    # ============================================================
    # 11. Organizational Hierarchy
    # ============================================================

    def test_ou_hierarchy_parent_path(self):
        inst = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        root = self.OU.create({'name': 'Root', 'code': 'ROOT', 'institution_id': inst.id})
        child = self.OU.create({'name': 'Child', 'code': 'CHILD', 'institution_id': inst.id, 'parent_id': root.id})
        grandchild = self.OU.create({'name': 'Grandchild', 'code': 'GC', 'institution_id': inst.id, 'parent_id': child.id})

        self.assertTrue(root.parent_path)
        self.assertTrue(child.parent_path.startswith(root.parent_path))
        self.assertTrue(grandchild.parent_path.startswith(child.parent_path))

    def test_ou_cycle_prevention(self):
        inst = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        ou1 = self.OU.create({'name': 'OU1', 'code': 'OU1', 'institution_id': inst.id})
        ou2 = self.OU.create({'name': 'OU2', 'code': 'OU2', 'institution_id': inst.id, 'parent_id': ou1.id})
        with self.assertRaises(ValidationError):
            ou1.write({'parent_id': ou2.id})

    # ============================================================
    # 12. Archive Behavior (No Destructive Delete)
    # ============================================================

    def test_institution_archive_instead_of_delete(self):
        inst = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        self.Campus.create({'name': 'Main', 'code': 'MAIN', 'institution_id': inst.id})

        with self.assertRaises(ValidationError):
            inst.unlink()

        inst.write({'active': False})
        self.assertFalse(inst.active)

    def test_cascade_restrict_on_institution_delete(self):
        inst = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        campus = self.Campus.create({'name': 'Main', 'code': 'MAIN', 'institution_id': inst.id})
        dept = self.Department.create({'name': 'IT', 'code': 'IT', 'institution_id': inst.id})

        with self.assertRaises(Exception):
            self.env.cr.execute('DELETE FROM gpj_institution WHERE id = %s', [inst.id])

    # ============================================================
    # 13. Access Control - Multi-Institution Isolation
    # ============================================================

    def test_user_sees_only_own_institution(self):
        inst_a = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        inst_b = self.Institution.create({'name': 'Inst B', 'code': 'INSTB'})

        user_a = self._create_user('user_a', [inst_a])
        user_b = self._create_user('user_b', [inst_b])

        campus_a = self.Campus.create({'name': 'Campus A', 'code': 'CA', 'institution_id': inst_a.id})
        campus_b = self.Campus.create({'name': 'Campus B', 'code': 'CB', 'institution_id': inst_b.id})

        # User A sees only Inst A campus
        campuses_a = self.Campus.with_user(user_a).search([])
        self.assertEqual(campuses_a, campus_a)
        self.assertNotIn(campus_b, campuses_a)

        # User B sees only Inst B campus
        campuses_b = self.Campus.with_user(user_b).search([])
        self.assertEqual(campuses_b, campus_b)

    def test_user_cannot_read_other_institution(self):
        inst_a = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        inst_b = self.Institution.create({'name': 'Inst B', 'code': 'INSTB'})

        user_a = self._create_user('user_a', [inst_a])
        campus_b = self.Campus.create({'name': 'Campus B', 'code': 'CB', 'institution_id': inst_b.id})

        with self.assertRaises(AccessError):
            campus_b.with_user(user_a).read()

    def test_user_cannot_write_other_institution(self):
        inst_a = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        inst_b = self.Institution.create({'name': 'Inst B', 'code': 'INSTB'})

        user_a = self._create_user('user_a', [inst_a])
        campus_b = self.Campus.create({'name': 'Campus B', 'code': 'CB', 'institution_id': inst_b.id})

        with self.assertRaises(AccessError):
            campus_b.with_user(user_a).write({'name': 'Hacked'})

    def test_user_cannot_create_in_other_institution(self):
        inst_a = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        inst_b = self.Institution.create({'name': 'Inst B', 'code': 'INSTB'})

        user_a = self._create_user('user_a', [inst_a])

        with self.assertRaises(AccessError):
            self.Campus.with_user(user_a).create({
                'name': 'Hacked', 'code': 'HACK', 'institution_id': inst_b.id
            })

    def test_user_cannot_delete_other_institution(self):
        inst_a = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        inst_b = self.Institution.create({'name': 'Inst B', 'code': 'INSTB'})

        user_a = self._create_user('user_a', [inst_a])
        campus_b = self.Campus.create({'name': 'Campus B', 'code': 'CB', 'institution_id': inst_b.id})

        with self.assertRaises(AccessError):
            campus_b.with_user(user_a).unlink()

    # ============================================================
    # 14. Institution Isolation Between Users
    # ============================================================

    def test_multi_institution_user_sees_both(self):
        inst_a = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        inst_b = self.Institution.create({'name': 'Inst B', 'code': 'INSTB'})

        user = self._create_user('user_multi', [inst_a, inst_b])

        campus_a = self.Campus.create({'name': 'Campus A', 'code': 'CA', 'institution_id': inst_a.id})
        campus_b = self.Campus.create({'name': 'Campus B', 'code': 'CB', 'institution_id': inst_b.id})

        campuses = self.Campus.with_user(user).search([])
        self.assertEqual(len(campuses), 2)
        self.assertIn(campus_a, campuses)
        self.assertIn(campus_b, campuses)

    def test_default_institution_used_for_context(self):
        inst_a = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        inst_b = self.Institution.create({'name': 'Inst B', 'code': 'INSTB'})

        user = self._create_user('user_multi', [inst_a, inst_b], default_inst=inst_a)

        self.assertEqual(user.gpj_active_institution_id, inst_a)
        self.assertIn(inst_a, user.gpj_institution_ids)
        self.assertIn(inst_b, user.gpj_institution_ids)

    # ============================================================
    # 15. Administrator Access
    # ============================================================

    def test_admin_can_unlink_in_own_institution(self):
        inst = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        admin = self._create_user('admin', [inst], groups='gpj_core.group_gpj_admin')
        campus = self.Campus.create({'name': 'Main', 'code': 'MAIN', 'institution_id': inst.id})

        # Admin can unlink
        campus.with_user(admin).unlink()
        self.assertFalse(campus.exists())

    def test_admin_cannot_access_other_institution(self):
        inst_a = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        inst_b = self.Institution.create({'name': 'Inst B', 'code': 'INSTB'})

        admin_a = self._create_user('admin_a', [inst_a], groups='gpj_core.group_gpj_admin')
        campus_b = self.Campus.create({'name': 'Campus B', 'code': 'CB', 'institution_id': inst_b.id})

        with self.assertRaises(AccessError):
            campus_b.with_user(admin_a).read()

    def test_admin_manages_memberships_only_in_own_institution(self):
        inst_a = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        inst_b = self.Institution.create({'name': 'Inst B', 'code': 'INSTB'})

        admin_a = self._create_user('admin_a', [inst_a], groups='gpj_core.group_gpj_admin')
        user_b = self._create_user('user_b', [])

        # Admin A cannot create membership for user in Inst B
        with self.assertRaises(AccessError):
            self.Membership.with_user(admin_a).create({
                'user_id': user_b.id,
                'institution_id': inst_b.id,
            })

        # Admin A can create membership in Inst A
        membership = self.Membership.with_user(admin_a).create({
            'user_id': user_b.id,
            'institution_id': inst_a.id,
        })
        self.assertTrue(membership.exists())

    # ============================================================
    # Cross-Institution Reporting
    # ============================================================

    def test_cross_institution_read_only(self):
        inst_a = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        inst_b = self.Institution.create({'name': 'Inst B', 'code': 'INSTB'})

        reporter = self._create_user('reporter', [], groups='gpj_core.group_gpj_cross_institution')
        campus_a = self.Campus.create({'name': 'Campus A', 'code': 'CA', 'institution_id': inst_a.id})
        campus_b = self.Campus.create({'name': 'Campus B', 'code': 'CB', 'institution_id': inst_b.id})

        # Can read both
        campuses = self.Campus.with_user(reporter).search([])
        self.assertEqual(len(campuses), 2)

        # Cannot write
        with self.assertRaises(AccessError):
            campus_a.with_user(reporter).write({'name': 'Hacked'})

        # Cannot create
        with self.assertRaises(AccessError):
            self.Campus.with_user(reporter).create({'name': 'New', 'code': 'NEW', 'institution_id': inst_a.id})

        # Cannot unlink
        with self.assertRaises(AccessError):
            campus_a.with_user(reporter).unlink()

    # ============================================================
    # Read-Only User
    # ============================================================

    def test_readonly_user_cannot_write(self):
        inst = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        readonly = self._create_user('readonly', [inst], groups='gpj_core.group_gpj_readonly')
        campus = self.Campus.create({'name': 'Main', 'code': 'MAIN', 'institution_id': inst.id})

        with self.assertRaises(AccessError):
            campus.with_user(readonly).write({'name': 'Hacked'})

        with self.assertRaises(AccessError):
            self.Campus.with_user(readonly).create({'name': 'New', 'code': 'NEW', 'institution_id': inst.id})

        with self.assertRaises(AccessError):
            campus.with_user(readonly).unlink()

    # ============================================================
    # Membership Tests
    # ============================================================

    def test_membership_unique_per_user_per_institution(self):
        inst = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        user = self._create_user('user1', [])

        self.Membership.create({'user_id': user.id, 'institution_id': inst.id})
        with self.assertRaises(ValidationError):
            self.Membership.create({'user_id': user.id, 'institution_id': inst.id})

    def test_single_default_membership_per_user(self):
        inst_a = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        inst_b = self.Institution.create({'name': 'Inst B', 'code': 'INSTB'})
        user = self._create_user('user1', [])

        self.Membership.create({'user_id': user.id, 'institution_id': inst_a.id, 'is_default': True})
        with self.assertRaises(ValidationError):
            self.Membership.create({'user_id': user.id, 'institution_id': inst_b.id, 'is_default': True})

    def test_membership_computed_fields(self):
        inst_a = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        inst_b = self.Institution.create({'name': 'Inst B', 'code': 'INSTB'})
        user = self._create_user('user1', [])

        self.Membership.create({'user_id': user.id, 'institution_id': inst_a.id, 'is_default': True, 'active': True})
        self.Membership.create({'user_id': user.id, 'institution_id': inst_b.id, 'active': True})

        self.assertEqual(len(user.gpj_institution_ids), 2)
        self.assertEqual(user.gpj_active_institution_id, inst_a)

    # ============================================================
    # Superuser Bypass
    # ============================================================

    def test_superuser_bypasses_record_rules(self):
        inst_a = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})
        inst_b = self.Institution.create({'name': 'Inst B', 'code': 'INSTB'})

        user_a = self._create_user('user_a', [inst_a])
        campus_b = self.Campus.create({'name': 'Campus B', 'code': 'CB', 'institution_id': inst_b.id})

        # Superuser can read everything
        campuses = self.Campus.with_user(self.env.ref('base.user_root')).search([])
        self.assertEqual(len(campuses), 1)

    # ============================================================
    # Validation Tests
    # ============================================================

    def test_established_year_validation(self):
        current_year = fields.Date.today().year
        inst = self.Institution.create({'name': 'Inst A', 'code': 'INSTA'})

        inst.write({'established_year': 1900})
        self.assertEqual(inst.established_year, 1900)

        with self.assertRaises(ValidationError):
            inst.write({'established_year': 1700})

        with self.assertRaises(ValidationError):
            inst.write({'established_year': current_year + 2})

    def _create_user(self, login, institutions, groups='gpj_core.group_gpj_user', default_inst=None):
        group = self.env.ref(groups) if isinstance(groups, str) else groups
        base_user = self.env.ref('base.group_user')
        user = self.Users.with_context(no_reset_password=True).create({
            'name': login,
            'login': login,
            'group_ids': [(6, 0, [group.id, base_user.id])],
        })
        for inst in institutions:
            vals = {'user_id': user.id, 'institution_id': inst.id, 'active': True}
            if default_inst and inst == default_inst:
                vals['is_default'] = True
            self.Membership.create(vals)
        user.invalidate_recordset(['gpj_institution_ids', 'gpj_active_institution_id'])
        return user