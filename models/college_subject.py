from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CollegeSubject(models.Model):
    _name = "college.subject"
    _description = "College Subject"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(
        string="Subject Name",
        required=True,
        tracking=True,
    )

    subject_code = fields.Char(
        string="Subject Code",
        required=True,
        tracking=True,
    )

    department_id = fields.Many2one(
        "college.department",
        string="Department",
        required=True,
        tracking=True,
    )

    course_id = fields.Many2one(
        "college.course",
        string="Course",
        required=True,
        tracking=True,
    )

    credits = fields.Integer(
        string="Credits",
        default=4,
        tracking=True,
    )

    semester = fields.Selection(
        [
            ("1", "Semester 1"),
            ("2", "Semester 2"),
            ("3", "Semester 3"),
            ("4", "Semester 4"),
            ("5", "Semester 5"),
            ("6", "Semester 6"),
            ("7", "Semester 7"),
            ("8", "Semester 8"),
        ],
        string="Semester",
        required=True,
        tracking=True,
    )

    teacher_ids = fields.Many2many(
        "college.teacher",
        string="Teachers",
    )

    description = fields.Text(
        string="Description"
    )

    active = fields.Boolean(
        default=True
    )

    _sql_constraints = [
        (
            "subject_code_unique",
            "unique(subject_code)",
            "Subject Code must be unique.",
        )
    ]

    @api.constrains("credits")
    def _check_credit(self):
        for rec in self:
            if rec.credits <= 0:
                raise ValidationError(
                    "Credits must be greater than zero."
                )
