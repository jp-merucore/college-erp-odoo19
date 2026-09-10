from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CollegeFee(models.Model):
    _name = "college.fee"
    _description = "College Fee"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "fee_number"

    fee_number = fields.Char(
        string="Fee Number",
        readonly=True,
        copy=False,
        default=lambda self: _("New")
    )

    student_id = fields.Many2one(
        "college.student",
        string="Student",
        required=True,
        ondelete="cascade"
    )

    # ondelete="cascade" means if student record is deleted then all related fee records will be detected automatically

    department_id = fields.Many2one(
        related="student_id.department_id",
        store=True
    )

    amount = fields.Monetary(
        required=True,
        tracking=True
    )

    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id
    )

    due_date = fields.Date(
        required=True
    )

    paid_date = fields.Date()

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("open", "Open"),
            ("pending", "Pending"),
            ("paid", "Paid"),

        ],
        default="draft",
        tracking=True
    )

    note = fields.Html()



    @api.constrains("amount")
    def _check_amount(self):
        for rec in self:
            if rec.amount <= 0:
                raise ValidationError(
                    _("Fee amount must be greater than zero.")
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("fee_number", _("New")) == _("New"):
                vals["fee_number"] = self.env["ir.sequence"].next_by_code(
                    "college.fee"
                ) or _("New")

        return super().create(vals_list)

    def action_open(self):
        self.write({"state": "open"})

    def action_pending(self):
        self.write({"state": "pending"})

    def action_paid(self):
        self.write({
            "state": "paid",
            "paid_date": fields.Date.today()
        })

    def action_draft(self):
        self.write({"state": "draft"})