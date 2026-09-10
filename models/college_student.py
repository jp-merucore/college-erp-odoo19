from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class CollegeStudent(models.Model):
    _name = 'college.student'
    _description = "College Student"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        required=True,
        string="Student Name",
        tracking=True
    )

    student_code = fields.Char(
        string="Student Code"
    )

    partner_id = fields.Many2one(
        "res.partner",
        string="Contact"
    )

    active = fields.Boolean(
        default=True
    )

    admission_date = fields.Date(
        string="Admission Date",
        default=fields.Date.context_today,
        tracking=True
    )

    birth_date = fields.Date(
        string="Birth Date",
    )

    age = fields.Char(
        string="Age",
        compute="_compute_age",
        store=True
    )

    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("other", "Other")],
        string="Gender"
    )

    email = fields.Char(
        string="Email"
    )

    phone = fields.Char(
        string="Phone Number"
    )

    image_1920 = fields.Image(
        string="Student Photo"
    )

    department_id = fields.Many2one(
        "college.department",
        required=True
    )
    #
    course_ids = fields.Many2many(
        "college.course",
        string="Courses"
    )

    admission_id = fields.Many2one(
        "college.admission",
        string="Admission",
        copy=False
    )

    fee_ids = fields.One2many(
        "college.fee",
        "student_id"
    )

    attendance_ids = fields.One2many(
        "college.attendance",
        "student_id",
        string="Attendance"
    )

    attendance_count = fields.Integer(
        compute="_compute_attendance_count"
    )

    exam_result_ids = fields.One2many(
        "college.exam.result",
        "student_id",
        string="Exam Results"
    )

    exam_count = fields.Integer(
        compute="_compute_exam_count"
    )

    total_fee = fields.Monetary(
        compute="_compute_total_fee",
        currency_field="currency_id",
        store=True)

    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id
    )

    # Monetary field is used for money/amount
    # currency_id automatically takes the current company currency (like INR/USD) :-$.
    # total_fee is auto-calculated by _compute_total_fee and displayed using that currency symbol:-$5000.

    state = fields.Selection(
        [("draft", "Draft"), ("active", "Active"), ("blocked", "Blocked"), ("alumni", "Alumni")],
        default="draft",
        tracking=True
    )

    user_id = fields.Many2one(
        "res.users",
        string="Portal User",
        readonly=True,
        copy=False
    )

    _sql_constraints = [
        ("student_code_unique", "unique(student_code)", "Student code must be unique."),
    ]

    # create mutliple record at time
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # vals return key value pair.  val.get("student_code") value of student_code check, if value is not then assign New using _("New")
            # when value is not get then they asign New and then condition become New=New then generate student code below.
            if vals.get("student_code", _("New")) == _("New"):
                vals["student_code"] = self.env["ir.sequence"].next_by_code("college.student") or _("New")
        return super().create(vals_list)

    @api.depends('birth_date')
    def _compute_age(self):
        today = fields.Date.today()

        for rec in self:
            if rec.birth_date:
                diff = relativedelta(today, rec.birth_date)

                if diff.years > 0:
                    rec.age = f"{diff.years} Year(s)"
                elif diff.months > 0:
                    rec.age = f"{diff.months} Month(s)"
                else:
                    rec.age = f"{diff.days} Day(s)"
            else:
                rec.age = 0

    # relativedelta(today, rec.birth_date) means calculate difference between today and birthdate in month, year and days

    @api.constrains("email")
    def _check_email(self):
        for rec in self:
            if rec.email and "@" not in rec.email:
                raise ValidationError(_("Please enter a valid student email."))

    @api.depends("fee_ids.amount", "fee_ids.state")
    def _compute_total_fee(self):
        for rec in self:
            rec.total_fee = sum(
                rec.fee_ids.filtered(
                    lambda f: f.state != "cancel"
                ).mapped("amount")
            )

    # @api.constrains use for validation means value check before saving to database
    # @api.depend when value depend on another field
    # @api.model_create_multi when we need to overriding create method and need to create multiple records at one time
    # @api.create when we need to overriding create method

    def action_activate(self):
        for student in self:

            if not student.email:
                raise UserError(_("Email is required before activating a student."))

            student.state = "active"

            student.message_post(
                body=_("Student activated.")
            )

        return True

    def action_blocked(self):
        self.write({'state': 'blocked'})

        self.message_post(
            body=_("Student blocked.")
        )

        return True

    def action_alumni(self):
        self.write({'state': 'alumni'})

        self.message_post(
            body=_("Student moved to Alumni.")
        )

        return True

    def action_draft(self):
        self.write({'state': 'draft'})

        self.message_post(
            body=_("Student reset to draft.")
        )

        return True

    @api.onchange("department_id")
    def _onchange_department_id(self):
        self.course_ids = False
        return {
            "domain": {
                "course_ids": [
                    ("department_id", "=", self.department_id.id)
                ]
            }
        }

    def _compute_attendance_count(self):
        for rec in self:
            rec.attendance_count = len(rec.attendance_ids)

    def action_view_attendance(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": _("Attendance"),
            "res_model": "college.attendance",
            "view_mode": "list,form",
            "domain": [("student_id", "=", self.id)],
        }

    def _compute_exam_count(self):
        for rec in self:
            rec.exam_count = len(rec.exam_result_ids)

    def action_view_exam_results(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": _("Exam Results"),
            "res_model": "college.exam.result",
            "view_mode": "list,form",
            "domain": [("student_id", "=", self.id)],
        }

    # when we change department_id then course_ids will be empty and only show courses related to that department in course_ids field.
    # for example user select first it department course but change department to mechanical then course automatically empty.
    # Show only courses whose department_id is equal to selected department.

    def action_create_portal_user(self):
        self.ensure_one()

        if self.user_id:
            raise UserError(_("Portal user already exists."))

        if not self.email:
            raise UserError(_("Student email is required."))

        # Create Partner
        partner = self.partner_id

        if not partner:
            partner = self.env["res.partner"].create({
                "name": self.name,
                "email": self.email,
                "phone": self.phone,
            })

            self.partner_id = partner.id

        # Portal Group
        portal_group = self.env.ref("base.group_portal")

        # Create User
        user = self.env["res.users"].sudo().create({
            "name": self.name,
            "login": self.email,
            "email": self.email,
            "partner_id": partner.id,
            "group_ids": [(6, 0, [portal_group.id])],
        })
        user.password = "REMOVED_DUMMY_PASSWORD"

        self.user_id = user.id

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Success"),
                "message": _("Portal user created successfully."),
                "type": "success",
            }
        }
