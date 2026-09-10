import base64

from odoo import http, fields
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class CollegePortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):

        values = super()._prepare_home_portal_values(counters)

        if counters:
            return values

        student = request.env[
            "college.student"
        ].sudo().search(
            [
                ("partner_id", "=", request.env.user.partner_id.id)
            ],
            limit=1,
        )

        values["student"] = student

        return values

    @http.route(
        ['/my/profile'],
        type='http',
        auth='user',
        website=True
    )
    def portal_student(self, **kw):
        student = request.env[
            'college.student'
        ].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)],
            limit=1
        )

        values = {
            'student': student,
            'page_name': 'profile',
        }

        return request.render(
            'college_erp_ready.portal_student_profile',
            values
        )

    @http.route(
        ['/my/attendance'],
        type='http',
        auth='user',
        website=True
    )
    def portal_attendance(self, **kw):

        student = request.env[
            'college.student'
        ].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)],
            limit=1
        )

        attendance = request.env[
            'college.attendance'
        ].sudo().search(
            [('student_id', '=', student.id)],
            order='attendance_date desc'
        )

        present = len(attendance.filtered(
            lambda a: a.status == 'present'
        ))

        absent = len(attendance.filtered(
            lambda a: a.status == 'absent'
        ))

        leave = len(attendance.filtered(
            lambda a: a.status == 'leave'
        ))

        late = len(attendance.filtered(
            lambda a: a.status == 'late'
        ))

        attendance_percent = (
            round((present / len(attendance)) * 100, 2)
            if attendance else 0
        )

        values = {
            "student": student,
            "attendance": attendance,
            "present": present,
            "absent": absent,
            "leave": leave,
            "late": late,
            "attendance_percent": attendance_percent,
            "page_name": "attendance",
        }

        return request.render(
            "college_erp_ready.portal_attendance",
            values
        )

    @http.route(
        ['/my/results'],
        type='http',
        auth='user',
        website=True
    )
    def portal_results(self, **kw):

        student = request.env['college.student'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)],
            limit=1
        )

        results = request.env['college.exam.result'].sudo().search(
            [('student_id', '=', student.id)],
            order='id desc'
        )

        total_exam = len(results)

        passed = len(results.filtered(
            lambda r: r.result == 'pass'
        ))

        failed = len(results.filtered(
            lambda r: r.result == 'fail'
        ))

        average = (
            round(sum(results.mapped('percentage')) / total_exam, 2)
            if total_exam else 0
        )

        values = {
            "student": student,
            "results": results,
            "total_exam": total_exam,
            "passed": passed,
            "failed": failed,
            "average": average,
            "page_name": "results",
        }

        return request.render(
            "college_erp_ready.portal_results",
            values
        )

    @http.route(
        ['/my/fees'],
        type='http',
        auth='user',
        website=True
    )
    def portal_fees(self, **kw):

        student = request.env[
            'college.student'
        ].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)],
            limit=1
        )

        fees = request.env[
            'college.fee'
        ].sudo().search(
            [('student_id', '=', student.id)],
            order='due_date desc'
        )

        total_fee = sum(fees.mapped("amount"))

        paid_fee = sum(
            fees.filtered(
                lambda f: f.state == "paid"
            ).mapped("amount")
        )

        pending_fee = total_fee - paid_fee

        values = {
            "student": student,
            "fees": fees,
            "total_fee": total_fee,
            "paid_fee": paid_fee,
            "pending_fee": pending_fee,
            "page_name": "fees",
        }

        return request.render(
            "college_erp_ready.portal_fees",
            values
        )

    @http.route(
        ['/my/idcard'],
        type='http',
        auth='user',
        website=True
    )
    def portal_id_card(self, **kw):

        student = request.env[
            'college.student'
        ].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)],
            limit=1
        )

        if not student:
            return request.not_found()

        values = {
            "student": student,
            "page_name": "idcard",
        }

        return request.render(
            "college_erp_ready.portal_idcard",
            values
        )

    @http.route(
        ['/my/idcard/download'],
        type='http',
        auth='user',
        website=True
    )
    def download_id_card(self, **kw):

        student = request.env[
            'college.student'
        ].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)],
            limit=1
        )

        if not student:
            return request.not_found()

        report = request.env.ref(
            "college_erp_ready.action_report_student_id_card"
        ).sudo()

        pdf, _ = report._render_qweb_pdf(
            report.report_name,
            res_ids=student.ids,
        )

        headers = [
            ('Content-Type', 'application/pdf'),
            ('Content-Disposition',
             'attachment; filename=Student_ID_Card.pdf'),
        ]

        return request.make_response(
            pdf,
            headers=headers,
        )

    @http.route(
        ['/my/dashboard'],
        type='http',
        auth='user',
        website=True
    )
    def portal_dashboard(self, **kw):

        student = request.env[
            'college.student'
        ].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)],
            limit=1
        )

        if not student:
            return request.not_found()

        # Total Courses
        course_count = len(student.course_ids)

        # Attendance
        attendance = request.env[
            'college.attendance'
        ].sudo().search([
            ('student_id', '=', student.id)
        ])

        # Recent Attendance
        recent_attendance = request.env[
            'college.attendance'
        ].sudo().search(
            [('student_id', '=', student.id)],
            order='attendance_date desc',
            limit=5
        )

        present = len(attendance.filtered(
            lambda a: a.status == 'present'
        ))

        attendance_percent = (
            round((present / len(attendance)) * 100, 2)
            if attendance else 0
        )

        # Pending Fees
        pending_fee = sum(
            student.fee_ids.filtered(
                lambda f: f.state != 'paid'
            ).mapped('amount')
        )

        # Latest Result
        latest_result = (
            student.exam_result_ids[:1].result
            if student.exam_result_ids
            else "N/A"
        )

        # Latest Exam Result
        latest_exam = request.env[
            'college.exam.result'
        ].sudo().search(
            [('student_id', '=', student.id)],
            order='id desc',
            limit=1
        )

        # ===========================
        # Fee Summary
        # ===========================

        fees = request.env[
            'college.fee'
        ].sudo().search(
            [('student_id', '=', student.id)]
        )

        total_fee = sum(fees.mapped('amount'))

        paid_fee = sum(
            fees.filtered(
                lambda f: f.state == 'paid'
            ).mapped('amount')
        )

        pending_fee = total_fee - paid_fee

        fee_percentage = (
            round((paid_fee / total_fee) * 100, 2)
            if total_fee else 0
        )

        # ===========================
        # Upcoming Exams
        # ===========================

        today = fields.Date.today()

        upcoming_exams = request.env[
            'college.exam'
        ].sudo().search(
            [
                ('department_id', '=', student.department_id.id),
                ('exam_date', '>=', today),
                ('state', '=', 'ongoing'),
            ],
            order='exam_date asc',
            limit=5,
        )
        # ===========================
        # Notices
        # ===========================

        today = fields.Date.today()

        all_notices = request.env[
            'college.notice'
        ].sudo().search(
            [('active', '=', True)],
            order='notice_date desc'
        )

        notices = all_notices.filtered(
            lambda n:
            (
                    not n.department_ids
                    or student.department_id in n.department_ids
            )
            and (
                    not n.expiry_date
                    or n.expiry_date >= today
            )
        )[:5]

        values = {
            "student": student,
            "course_count": course_count,
            "attendance_percent": attendance_percent,
            "pending_fee": pending_fee,
            "latest_result": latest_result,
            "recent_attendance": recent_attendance,
            "latest_exam": latest_exam,
            "total_fee": total_fee,
            "paid_fee": paid_fee,
            "fee_percentage": fee_percentage,
            "upcoming_exams": upcoming_exams,
            "notices": notices,
            "page_name": "dashboard",
        }

        return request.render(
            "college_erp_ready.portal_student_dashboard",
            values
        )

    @http.route(
        ['/my/notice/download/<int:notice_id>'],
        type='http',
        auth='user',
        website=True
    )
    def download_notice_attachment(self, notice_id, **kw):

        notice = request.env['college.notice'].sudo().browse(notice_id)

        if not notice.exists() or not notice.attachment:
            return request.not_found()

        file_data = base64.b64decode(notice.attachment)

        headers = [
            ('Content-Type', 'application/octet-stream'),
            (
                'Content-Disposition',
                'attachment; filename="%s"' % (
                        notice.attachment_name or 'attachment'
                )
            ),
        ]

        return request.make_response(
            file_data,
            headers=headers
        )

    @http.route(
        ['/my/notices'],
        type='http',
        auth='user',
        website=True
    )
    def portal_notices(self, **kw):

        student = request.env[
            'college.student'
        ].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)],
            limit=1
        )

        if not student:
            return request.not_found()

        today = fields.Date.today()

        all_notices = request.env[
            'college.notice'
        ].sudo().search(
            [('active', '=', True)],
            order='notice_date desc'
        )

        notices = all_notices.filtered(
            lambda n:
            (
                    not n.department_ids
                    or student.department_id in n.department_ids
            )
            and (
                    not n.expiry_date
                    or n.expiry_date >= today
            )
        )

        values = {
            "student": student,
            "notices": notices,
            "page_name": "notices",
        }

        return request.render(
            "college_erp_ready.portal_notices",
            values
        )

    @http.route(
        ['/my/courses'],
        type='http',
        auth='user',
        website=True
    )
    def portal_courses(self, **kw):

        student = request.env[
            'college.student'
        ].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)],
            limit=1
        )

        if not student:
            return request.not_found()

        courses = student.course_ids

        # ===========================
        # Statistics
        # ===========================

        total_courses = len(courses)

        running_courses = len(
            courses.filtered(
                lambda c: c.state == "running"
            )
        )

        completed_courses = len(
            courses.filtered(
                lambda c: c.state == "completed"
            )
        )

        draft_courses = len(
            courses.filtered(
                lambda c: c.state == "draft"
            )
        )

        cancelled_courses = len(
            courses.filtered(
                lambda c: c.state == "cancel"
            )
        )

        values = {
            "student": student,
            "courses": courses,

            "total_courses": total_courses,
            "running_courses": running_courses,
            "completed_courses": completed_courses,
            "draft_courses": draft_courses,
            "cancelled_courses": cancelled_courses,

            "page_name": "courses",
        }

        return request.render(
            "college_erp_ready.portal_courses",
            values
        )
