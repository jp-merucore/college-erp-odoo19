/** @odoo-module **/

import {Component, onWillStart, useState} from "@odoo/owl";
import {rpc} from "@web/core/network/rpc";

export class CollegeDashboard extends Component {

    setup() {

        this.state = useState({
            students: 0, admissions: 0, departments: 0, courses: 0, fees: 0, paid_fees: 0, pending_fees: 0,
        });

        onWillStart(async () => {

            const result = await rpc("/college/dashboard/data", {});

            Object.assign(this.state, result);
        });
    }
}

CollegeDashboard.template = "college_erp_ready.CollegeDashboard";