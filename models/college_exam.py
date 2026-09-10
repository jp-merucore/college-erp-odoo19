from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CollegeExam(models.Model):
    _name = "college.exam"
    _description = "College Exam"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "exam_no"

    exam_no = fields.Char(
        string="Exam Number",
        readonly=True,
        copy=False,
        default=lambda self: _("New")
    )

    name = fields.Char(
        string="Exam Name",
        required=True,
        tracking=True
    )

    exam_date = fields.Date(
        required=True,
        default=fields.Date.context_today
    )

    department_id = fields.Many2one(
        "college.department",
        required=True
    )

    course_id = fields.Many2one(
        "college.course",
        required=True
    )

    total_marks = fields.Float(
        default=100
    )

    pass_marks = fields.Float(
        default=35
    )

    result_ids = fields.One2many(
        "college.exam.result",
        "exam_id",
        string="Results"
    )

    state = fields.Selection([
        ("draft", "Draft"),
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
        ("cancel", "Cancelled")
    ], default="draft", tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("exam_no", _("New")) == _("New"):
                vals["exam_no"] = self.env[
                    "ir.sequence"
                ].next_by_code("college.exam") or _("New")

        return super().create(vals_list)

    def action_start(self):
        self.state = "ongoing"

    def action_complete(self):
        self.state = "completed"

    def action_cancel(self):
        self.state = "cancel"

    def action_draft(self):
        self.state = "draft"