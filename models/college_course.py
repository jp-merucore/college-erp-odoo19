from odoo import api, fields, models, _


class CollegeCourse(models.Model):
    _name = "college.course"
    _description = "College Course"
    _rec_name = "name"
    # WHEN WE SELECTING THE COURSE IN MANY2ONE FIELD THEN NAME SHOW LIKE SCIENCE COURSE INSTEAD OF 1,2,3
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Course Name",
        required=True,
        tracking=True
    )

    course_code = fields.Char(
        string="Course Code",
    )

    department_id = fields.Many2one(
        "college.department",
        string="Department",
        # required=True
    )

    description = fields.Text(
        string="Course Description"
    )

    fees = fields.Monetary(
        string="Course Fees",
        currency_field="currency_id"
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id
    )

    start_date = fields.Date(
        string="Start Date"
    )

    end_date = fields.Date(
        string="End Date"
    )

    active = fields.Boolean(
        default=True
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("running", "Running"),
            ("completed", "Completed"),
            ("cancel", "Cancelled")
        ],
        string="Status",
        default="draft",
        tracking=True
    )

    student_ids = fields.Many2many(
        "college.student",
        string="Students",
        ondelete='cascade'
    )

    total_students = fields.Integer(
        string="Total Students",
        compute="_compute_total_students"
    )

    subject_ids = fields.One2many(
        "college.subject",
        "course_id",
        string="Subjects",
    )

    subject_count = fields.Integer(
        compute="_compute_subject_count",
        string="Subjects",
    )

    @api.depends("student_ids")
    def _compute_total_students(self):
        for rec in self:
            rec.total_students = len(rec.student_ids)

    def action_view_students(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": _("Students"),
            "res_model": "college.student",
            "view_mode": "list,form",
            "domain": [("id", "in", self.student_ids.ids)],
        }

    def _compute_subject_count(self):
        for rec in self:
            rec.subject_count = len(rec.subject_ids)

    def action_view_subjects(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Subjects",
            "res_model": "college.subject",
            "view_mode": "list,form",
            "domain": [("course_id", "=", self.id)],
            "context": {
                "default_course_id": self.id,
                "default_department_id": self.department_id.id,
            },
        }

    # Recalculate total_students whenever students are added to or removed from the course.
    # total_students automatically counts how many students are assigned to this course.
    # action_view_students() is used by the smart button to open and show only students belonging to the current course.

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # vals return key value pair.  val.get("course_code") value of course_code check, if value is not then assign New using _("New")
            # when value is not get then they asign New and then condition become New=New then generate course code below.
            if vals.get("course_code", _("New")) == _("New"):
                vals["course_code"] = self.env["ir.sequence"].next_by_code("college.course") or _("New")
        return super().create(vals_list)

    def action_start(self):
        self.write({"state": "running"})

    def action_complete(self):
        self.write({"state": "completed"})

    def action_cancel(self):
        self.write({"state": "cancel"})

    def action_reset_draft(self):
        self.write({"state": "draft"})
