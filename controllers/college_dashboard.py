from odoo import http
from odoo.http import request


class CollegeDashboard(http.Controller):

    @http.route(
        '/college/dashboard/data',
        type='jsonrpc',
        auth='user'
    )
    def dashboard_data(self):
        return {

            'students':
                request.env['college.student']
                .sudo()
                .search_count([]),

            'admissions':
                request.env['college.admission']
                .sudo()
                .search_count([]),

            'departments':
                request.env['college.department']
                .sudo()
                .search_count([]),

            'courses':
                request.env['college.course']
                .sudo()
                .search_count([]),

            'fees':
                request.env['college.fee']
                .sudo()
                .search_count([]),

            'paid_fees':
                request.env['college.fee']
                .sudo()
                .search_count([
                    ('state', '=', 'paid')
                ]),

            'pending_fees':
                request.env['college.fee']
                .sudo()
                .search_count([
                    ('state', '=', 'pending')
                ]),
        }
