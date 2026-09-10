from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CollegeAttendance(models.Model):
    _name = "college.attendance"
    _description = "College Attendance"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "attendance_no"

    attendance_no = fields.Char(
        string="Attendance No",
        readonly=True,
        copy=False,
        default=lambda self: _("New")
    )

    attendance_date = fields.Date(
        required=True,
        default=fields.Date.context_today,
        tracking=True
    )

    student_id = fields.Many2one(
        "college.student",
        required=True,
        tracking=True,
        ondelete = "cascade"
    )

    department_id = fields.Many2one(
        related="student_id.department_id",
        store=True
    )

    course_id = fields.Many2one(
        "college.course",
        required=True
    )

    status = fields.Selection(
        [
            ("present", "Present"),
            ("absent", "Absent"),
            ("late", "Late"),
            ("leave", "Leave"),
        ],
        default="present",
        required=True,
        tracking=True
    )

    note = fields.Text()

    _sql_constraints = [
        (
            "unique_attendance",
            "unique(student_id,course_id,attendance_date)",
            "Attendance already exists for this student on this date."
        )
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("attendance_no", _("New")) == _("New"):
                vals["attendance_no"] = self.env[
                                            "ir.sequence"
                                        ].next_by_code("college.attendance") or _("New")

        return super().create(vals_list)

    @api.constrains("student_id", "course_id")
    def _check_course_student(self):
        for rec in self:
            if rec.course_id not in rec.student_id.course_ids:
                raise ValidationError(
                    _("Selected course is not assigned to this student.")
                )

    @api.onchange("student_id")
    def _onchange_student_id(self):
        self.course_id = False

        if not self.student_id:
            return {}

        return {
            "domain": {
                "course_id": [
                    ("id", "in", self.student_id.course_ids.ids)
                ]
            }
        }
