from odoo.tests import TransactionCase, tagged
from odoo.exceptions import AccessError


@tagged('post_install', '-at_install')
class TestSimpleNotes(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({'name': 'Test Partner'})
        cls.other_partner = cls.env['res.partner'].create({'name': 'Other Partner'})

        cls.manager = cls.env['res.users'].create({
            'name': 'Manager',
            'login': 'manager',
            'groups_id': [(4, cls.env.ref('base.group_partner_manager').id)],
        })
        cls.user = cls.env['res.users'].create({
            'name': 'User',
            'login': 'user',
            'groups_id': [(4, cls.env.ref('base.group_user').id)],
        })

    def test_create_note_linked_to_partner(self):
        """Create a note linked to a partner, verify inverse relation."""
        note = self.env['simple.notes'].create({
            'name': 'Test Note',
            'partner_id': self.partner.id,
            'content': 'Note content',
        })
        self.assertEqual(note.partner_id, self.partner)
        self.assertIn(note, self.partner.simple_notes_ids)
        self.assertEqual(len(self.partner.simple_notes_ids), 1)

    def test_multiple_notes_per_partner(self):
        """Multiple notes can be linked to the same partner."""
        self.env['simple.notes'].create([
            {'name': 'Note 1', 'partner_id': self.partner.id},
            {'name': 'Note 2', 'partner_id': self.partner.id},
            {'name': 'Note 3', 'partner_id': self.other_partner.id},
        ])
        self.assertEqual(len(self.partner.simple_notes_ids), 2)
        self.assertEqual(len(self.other_partner.simple_notes_ids), 1)

    def test_manager_full_crud(self):
        """group_partner_manager has create, read, write, unlink."""
        notes = self.env['simple.notes'].with_user(self.manager)
        note = notes.create({'name': 'Manager Note', 'partner_id': self.partner.id})
        note.write({'content': 'Updated by manager'})
        note.unlink()
        self.assertFalse(note.exists())

    def test_user_read_only_via_acl(self):
        """group_user can read but not create/write/unlink (enforced by ACL)."""
        note = self.env['simple.notes'].create({
            'name': 'Existing Note',
            'partner_id': self.partner.id,
        })

        with self.assertRaises(AccessError):
            self.env['simple.notes'].with_user(self.user).create({
                'name': 'New Note',
                'partner_id': self.partner.id,
            })

        with self.assertRaises(AccessError):
            note.with_user(self.user).write({'content': 'Hacked'})

        with self.assertRaises(AccessError):
            note.with_user(self.user).unlink()

        read_note = self.env['simple.notes'].with_user(self.user).search([
            ('id', '=', note.id)
        ])
        self.assertEqual(read_note, note)

    def test_user_can_read_all_notes_via_search(self):
        """Without record rule, any internal user can search all notes."""
        note_other = self.env['simple.notes'].create({
            'name': 'Other Company Note',
            'partner_id': self.other_partner.id,
        })

        found = self.env['simple.notes'].with_user(self.user).search([
            ('id', '=', note_other.id)
        ])
        self.assertEqual(found, note_other)

    def test_cascade_delete_on_partner(self):
        """Deleting partner cascades to notes (ondelete='cascade')."""
        note = self.env['simple.notes'].create({
            'name': 'To Be Deleted',
            'partner_id': self.partner.id,
        })
        self.partner.unlink()
        self.assertFalse(note.exists())