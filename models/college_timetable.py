from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CollegeTimetable(models.Model):
    _name = "college.timetable"
    _description = "College Timetable"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "day_of_week, start_time"

    name = fields.Char(
        string="Lecture",
        compute="_compute_name",
        store=True,
    )

    subject_id = fields.Many2one(
        "college.subject",
        string="Subject",
        required=True,
        tracking=True,
    )

    teacher_id = fields.Many2one(
        "college.teacher",
        string="Teacher",
        required=True,
        tracking=True,
    )

    course_id = fields.Many2one(
        "college.course",
        string="Course",
        required=True,
        tracking=True,
    )

    department_id = fields.Many2one(
        "college.department",
        string="Department",
        required=True,
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

    academic_year = fields.Char(
        string="Academic Year",
        default="2026-2027",
        tracking=True,
    )

    day_of_week = fields.Selection(
        [
            ("monday", "Monday"),
            ("tuesday", "Tuesday"),
            ("wednesday", "Wednesday"),
            ("thursday", "Thursday"),
            ("friday", "Friday"),
            ("saturday", "Saturday"),
        ],
        string="Day",
        required=True,
        tracking=True,
    )

    start_time = fields.Float(
        string="Start Time",
        required=True,
        tracking=True,
    )

    end_time = fields.Float(
        string="End Time",
        required=True,
        tracking=True,
    )

    room = fields.Char(
        string="Room",
        tracking=True,
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("active", "Active"),
            ("cancel", "Cancelled"),
        ],
        default="draft",
        tracking=True,
    )

    note = fields.Text(
        string="Notes"
    )

    active = fields.Boolean(
        default=True
    )

    @api.depends("subject_id", "teacher_id")
    def _compute_name(self):
        for rec in self:
            if rec.subject_id and rec.teacher_id:
                rec.name = "%s - %s" % (
                    rec.subject_id.name,
                    rec.teacher_id.name,
                )
            else:
                rec.name = False

    @api.constrains("start_time", "end_time")
    def _check_time(self):
        for rec in self:
            if rec.start_time >= rec.end_time:
                raise ValidationError(
                    "End Time must be greater than Start Time."
                )
