/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class GPJDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            stats: [],
            quickActions: [],
            alerts: [],
            activities: [],
            alertsCount: 0,
        });

        onWillStart(async () => {
            await this.loadDashboardData();
        });
    }

    async loadDashboardData() {
        try {
            // Fetch institution data for stats
            const institutions = await this.orm.searchRead("gpj.institution", [], ["id", "name"]);
            const institutionIds = institutions.map(i => i.id);

            // Fetch counts for various models
            const [
                campusCount,
                departmentCount,
                ouCount,
                designationCount,
                roleCount,
                membershipCount,
            ] = await Promise.all([
                this.orm.searchCount("gpj.campus", [["institution_id", "in", institutionIds]]),
                this.orm.searchCount("gpj.department", [["institution_id", "in", institutionIds]]),
                this.orm.searchCount("gpj.organizational.unit", [["institution_id", "in", institutionIds]]),
                this.orm.searchCount("gpj.designation", [["institution_id", "in", institutionIds]]),
                this.orm.searchCount("gpj.institutional.role", [["institution_id", "in", institutionIds]]),
                this.orm.searchCount("gpj.institution.membership", [["institution_id", "in", institutionIds]]),
            ]);

            this.state.stats = [
                { label: "Campuses", value: campusCount, icon: "location_city", trendIcon: "trending_up", trendText: "+12%", trendColor: "success" },
                { label: "Departments", value: departmentCount, icon: "domain", trendIcon: "horizontal_rule", trendText: "Stable", trendColor: "secondary" },
                { label: "Org. Units", value: ouCount, icon: "apartment", trendIcon: "trending_up", trendText: "+5%", trendColor: "success" },
                { label: "Designations", value: designationCount, icon: "badge", trendIcon: "warning", trendText: "2 new", trendColor: "danger" },
                { label: "Roles", value: roleCount, icon: "security", trendIcon: "horizontal_rule", trendText: "Stable", trendColor: "secondary" },
                { label: "Memberships", value: membershipCount, icon: "groups", trendIcon: "trending_up", trendText: "+8%", trendColor: "success" },
            ];

            this.state.quickActions = [
                { label: "New Campus", icon: "add_location", bgColor: "primary", textColor: "white", url: "/web#action=action_gpj_campus&view_type=form" },
                { label: "New Department", icon: "add_business", bgColor: "secondary", textColor: "white", url: "/web#action=action_gpj_department&view_type=form" },
                { label: "New Org Unit", icon: "summarize", bgColor: "info", textColor: "white", url: "/web#action=action_gpj_organizational_unit&view_type=form" },
                { label: "Manage Roles", icon: "admin_panel_settings", bgColor: "warning", textColor: "dark", url: "/web#action=action_gpj_institutional_role&view_type=list" },
            ];

            // Mock alerts - in production, these would come from a real alert system
            this.state.alerts = [
                { title: "Database Backup Failed", message: "Scheduled daily backup for 'Academic Data' failed to complete at 03:00 AM.", time: "2 hours ago", color: "danger" },
                { title: "New Module Update Available", message: "ERP Core v2.4.1 is ready for installation. Requires system restart.", time: "Yesterday", color: "primary" },
            ];
            this.state.alertsCount = this.state.alerts.length;

            // Mock activities - in production, these would come from mail.activity or audit log
            this.state.activities = [
                { message: "<strong>Dr. A. Sharma</strong> updated course syllabus for <span class='text-primary'>CSE-301</span>", time: "10:45 AM", icon: "edit", bgColor: "primary", textColor: "white" },
                { message: "New faculty profile created in <span class='text-primary'>Civil Dept</span>", time: "09:15 AM", icon: "person_add", bgColor: "secondary", textColor: "white" },
                { message: "System backup initiated by <strong>Admin</strong>", time: "Yesterday, 11:30 PM", icon: "backup", bgColor: "secondary", textColor: "white" },
            ];

        } catch (error) {
            console.error("Failed to load dashboard data:", error);
        }
    }

    navigateToAction(url) {
        window.location.href = url;
    }
}

GPJDashboard.template = "gpj_core.gpj_dashboard_template";
GPJDashboard.components = {};

registry.category("actions").add("gpj_dashboard", GPJDashboard);