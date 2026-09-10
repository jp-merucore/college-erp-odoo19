/** @odoo-module **/

import { registry } from "@web/core/registry";
import { CollegeDashboard } from "./dashboard";

registry.category("actions").add(
    "college_dashboard",
    CollegeDashboard
);