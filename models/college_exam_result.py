from odoo import api, fields, models


class CollegeExamResult(models.Model):
    _name = "college.exam.result"
    _description = "College Exam Result"

    exam_id = fields.Many2one(
        "college.exam",
        required=True,
        ondelete="cascade"
    )

    student_id = fields.Many2one(
        "college.student",
        required=True,
        ondelete = 'cascade'
    )

    department_id = fields.Many2one(
        related="student_id.department_id",
        store=True
    )

    course_ids = fields.Many2many(
        related="student_id.course_ids"
    )

    marks = fields.Float()

    percentage = fields.Float(
        compute="_compute_percentage",
        store=True
    )

    result = fields.Selection(
        [
            ("pass", "Pass"),
            ("fail", "Fail")
        ],
        compute="_compute_percentage",
        store=True
    )

    @api.depends(
        "marks",
        "exam_id.total_marks",
        "exam_id.pass_marks"
    )
    def _compute_percentage(self):
        for rec in self:

            if rec.exam_id.total_marks:

                rec.percentage = (
                                         rec.marks /
                                         rec.exam_id.total_marks
                                 ) * 100

            else:
                rec.percentage = 0

            if rec.marks >= rec.exam_id.pass_marks:
                rec.result = "pass"
            else:
                rec.result = "fail"
