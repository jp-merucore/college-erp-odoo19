from odoo import api, fields, models, _


class CollegeDepartment(models.Model):
    _name = "college.department"
    _description = "College Department"
    _rec_name = "name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Department Name",
        required=True,
        tracking=True
    )

    department_code = fields.Char(
        string="Department Code",
        readonly=True,
        copy=False,
        default=lambda self: _("New"),
        tracking=True
    )

    description = fields.Text(
        string="Description"
    )

    student_ids = fields.One2many(
        "college.student",
        "department_id",
        string="Students",
        ondelete='cascade'
    )

    course_ids = fields.One2many(
        "college.course",
        "department_id",
        string="Courses"
    )

    student_count = fields.Integer(
        string="Student count",
        compute="_compute_counts",
        store=False
    )

    # active = fields.Boolean(
    #     default=True
    # )

    course_count = fields.Integer(
        string="Course Count",
        compute="_compute_counts",
        store=False
    )

    teacher_ids = fields.One2many(
        "college.teacher",
        "department_id",
        string="Teachers",
    )

    @api.depends("student_ids", "course_ids")
    def _compute_counts(self):
        for rec in self:
            rec.student_count = len(rec.student_ids)
            rec.course_count = len(rec.course_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("department_code", _("New")) == _("New"):
                vals["department_code"] = (
                        self.env["ir.sequence"].next_by_code(
                            "college.department"
                        ) or _("New")
                )
        return super().create(vals_list)

    def action_view_students(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Students"),
            "res_model": "college.student",
            "view_mode": "list,form",
            "domain": [("department_id", "=", self.id)],
        }

    def action_view_courses(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Courses"),
            "res_model": "college.course",
            "view_mode": "list,form",
            "domain": [("department_id", "=", self.id)],
        }
