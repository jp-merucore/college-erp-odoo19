from odoo import fields, models


class CollegeNotice(models.Model):
    _name = "college.notice"
    _description = "College Notice"
    _order = "notice_date desc"

    name = fields.Char(
        string="Title",
        required=True
    )

    description = fields.Html(
        string="Description"
    )

    notice_date = fields.Date(
        default=fields.Date.context_today,
        required=True
    )

    priority = fields.Selection(
        [
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        string="Priority",
        default="medium",
        required=True
    )

    department_ids = fields.Many2many(
        "college.department",
        string="Departments",
        help="Leave empty to show this notice to all departments."
    )

    attachment = fields.Binary(
        string="Attachment"
    )

    attachment_name = fields.Char(
        string="File Name"
    )

    active = fields.Boolean(
        default=True
    )

    expiry_date = fields.Date(
        string="Expiry Date",
        help="Leave empty if the notice should never expire."
    )