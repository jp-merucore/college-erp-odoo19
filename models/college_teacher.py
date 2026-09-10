from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CollegeTeacher(models.Model):
    _name = "college.teacher"
    _description = "College Teacher"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(
        required=True,
        tracking=True,
    )

    employee_code = fields.Char(
        string="Employee ID",
        required=True,
        tracking=True,
    )

    image_1920 = fields.Image(
        string="Photo"
    )

    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
        ],
        default="male",
        tracking=True,
    )

    email = fields.Char(
        tracking=True,
    )

    mobile = fields.Char(
        tracking=True,
    )

    department_id = fields.Many2one(
        "college.department",
        required=True,
        tracking=True,
    )

    subject_ids = fields.Many2many(
        "college.subject",
        string="Subjects",
    )

    course_ids = fields.Many2many(
        "college.course",
        string="Courses",
    )

    joining_date = fields.Date(
        tracking=True,
    )

    experience = fields.Integer(
        string="Experience (Years)",
        default=0,
    )

    qualification = fields.Char()

    address = fields.Text()

    active = fields.Boolean(
        default=True
    )

    _sql_constraints = [
        (
            "employee_code_unique",
            "unique(employee_code)",
            "Employee ID must be unique.",
        )
    ]

    @api.constrains("experience")
    def _check_experience(self):
        for rec in self:
            if rec.experience < 0:
                raise ValidationError(
                    "Experience cannot be negative."
                )
