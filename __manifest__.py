{
    "name": "College ERP",
    "author": "Jalay Patel",
    "version": "19.0.1.0.0",
    "category": "Education",
    "license": "LGPL-3",
    "summary": "Admissions, students, fees, attendance, exams and portal",
    "depends": ['base', 'mail', 'portal', ],
    "data": [
        'security/ir.model.access.csv',
        "data/ir_sequence.xml",
        'views/backend/college_dashboard.xml',
        'views/backend/college_student_views.xml',
        'views/backend/college_subject_views.xml',
        'views/backend/college_teacher_views.xml',
        'views/backend/college_course_views.xml',
        'views/backend/college_department_views.xml',
        'views/backend/college_fee_views.xml',
        'views/backend/college_admission_views.xml',
        'views/backend/college_attendance_views.xml',
        'views/backend/college_exam_views.xml',
        'views/backend/college_exam_result_views.xml',
        'views/backend/college_notice_views.xml',
        'views/backend/college_timetable_views.xml',
        'views/backend/college_menus.xml',

        'views/portal/layout/portal_layout.xml',
        'views/portal/layout/portal_sidebar.xml',
        'views/portal/layout/portal_header.xml',

        'views/portal/components/portal_page.xml',
        'views/portal/components/portal_page_header.xml',

        'views/portal/pages/portal_home.xml',
        'views/portal/pages/portal_profile.xml',
        'views/portal/pages/portal_attendance.xml',
        'views/portal/pages/portal_results.xml',
        'views/portal/pages/portal_fees.xml',
        'views/portal/pages/portal_courses.xml',
        'views/portal/pages/student_dashboard_templates.xml',
        'views/portal/pages/portal_idcard.xml',
        'views/portal/pages/portal_notices.xml',

        "report/report_actions.xml",
        "report/student_report.xml",
        "report/student_id_card.xml",
    ],
    "assets": {
        "web.assets_backend": [

            'college_erp_ready/static/src/dashboard/dashboard.js',
            'college_erp_ready/static/src/dashboard/dashboard_action.js',
            'college_erp_ready/static/src/dashboard/dashboard.xml',
        ],

        'web.assets_frontend': [
            'college_erp_ready/static/src/css/portal_dashboard.css',
            'college_erp_ready/static/src/css/portal_layout.css',
        ],
    },
    "application": True,
    "installable": True,
}
