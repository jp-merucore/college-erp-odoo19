from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CollegeAdmission(models.Model):
    _name = "college.admission"
    _description = "College Admission"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "admission_no"

    admission_no = fields.Char(
        string="Admission Number",
        readonly=True,
        copy=False,
        default=lambda self: _("New"),
        tracking=True
    )

    applicant_name = fields.Char(
        string="Applicant Name",
        required=True,
        tracking=True
    )

    email = fields.Char(
        tracking=True
    )

    phone = fields.Char(
        tracking=True
    )

    admission_date = fields.Date(
        default=fields.Date.context_today,
        tracking=True
    )

    department_id = fields.Many2one(
        "college.department",
        string="Department",
        required=True
    )

    course_ids = fields.Many2many(
        "college.course",
        string="Courses"
    )

    student_id = fields.Many2one(
        "college.student",
        string="Student",
        readonly=True,
        copy=False,
        ondelete = 'cascade'
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("rejected", "Rejected")
        ],
        default="draft",
        tracking=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("admission_no", _("New")) == _("New"):
                vals["admission_no"] = self.env[
                    "ir.sequence"
                ].next_by_code("college.admission") or _("New")

        return super().create(vals_list)

    def action_confirm(self):
        for rec in self:

            if rec.state == "rejected":
                raise UserError(
                    _("Rejected admission cannot be confirmed.")
                )

            if rec.student_id:
                raise UserError(
                    _("Student already created for this admission.")
                )

            student = self.env["college.student"].create({
                "name": rec.applicant_name,
                "email": rec.email,
                "phone": rec.phone,
                "department_id": rec.department_id.id,
                "course_ids": [(6, 0, rec.course_ids.ids)],
                "admission_id": rec.id,
            })

            rec.student_id = student.id
            rec.state = "confirmed"

        return True

    def action_reject(self):
        self.state = "rejected"

    def action_draft(self):
        self.state = "draft"