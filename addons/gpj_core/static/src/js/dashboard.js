/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";


export class GPJDashboard extends Component {

    setup() {

        // ================================================================
        // SERVICES
        // ================================================================

        this.orm = useService("orm");
        this.actionService = useService("action");


        // ================================================================
        // STATE
        // ================================================================

        this.state = useState({
            stats: [],
            quickActions: [],
            alerts: [],
            activities: [],

            alertsCount: 0,

            loading: true,
            error: false,
        });


        // ================================================================
        // INITIAL LOAD
        // ================================================================

        onWillStart(async () => {
            await this.loadDashboardData();
        });
    }


    // ====================================================================
    // LOAD DASHBOARD DATA
    // ====================================================================

    async loadDashboardData() {

        this.state.loading = true;
        this.state.error = false;

        try {

            // ------------------------------------------------------------
            // INSTITUTIONS
            // ------------------------------------------------------------

            const institutions = await this.orm.searchRead(
                "gpj.institution",
                [],
                [
                    "id",
                    "name",
                ]
            );

            const institutionIds = institutions.map(
                (institution) => institution.id
            );


            // ------------------------------------------------------------
            // COUNTS
            // ------------------------------------------------------------

            let campusCount = 0;
            let departmentCount = 0;
            let organizationalUnitCount = 0;
            let designationCount = 0;
            let roleCount = 0;
            let membershipCount = 0;


            /*
             * If there are no institutions, the "in" domain would be
             * unnecessary. Keep the result at zero.
             */

            if (institutionIds.length) {

                [
                    campusCount,
                    departmentCount,
                    organizationalUnitCount,
                    designationCount,
                    roleCount,
                    membershipCount,
                ] = await Promise.all([

                    this.orm.searchCount(
                        "gpj.campus",
                        [
                            [
                                "institution_id",
                                "in",
                                institutionIds,
                            ],
                        ]
                    ),

                    this.orm.searchCount(
                        "gpj.department",
                        [
                            [
                                "institution_id",
                                "in",
                                institutionIds,
                            ],
                        ]
                    ),

                    this.orm.searchCount(
                        "gpj.organizational.unit",
                        [
                            [
                                "institution_id",
                                "in",
                                institutionIds,
                            ],
                        ]
                    ),

                    this.orm.searchCount(
                        "gpj.designation",
                        [
                            [
                                "institution_id",
                                "in",
                                institutionIds,
                            ],
                        ]
                    ),

                    this.orm.searchCount(
                        "gpj.institutional.role",
                        [
                            [
                                "institution_id",
                                "in",
                                institutionIds,
                            ],
                        ]
                    ),

                    this.orm.searchCount(
                        "gpj.institution.membership",
                        [
                            [
                                "institution_id",
                                "in",
                                institutionIds,
                            ],
                        ]
                    ),

                ]);
            }


            // ============================================================
            // STAT CARDS
            // ============================================================

            this.state.stats = [

                {
                    id: "campuses",
                    label: "Campuses",
                    value: campusCount,
                    trendText: "+12%",
                    actionXmlId: "gpj_core.action_gpj_campus",
                    viewMode: "list",
                    icon: "fa-university",
                    color: "primary",
                },

                {
                    id: "departments",
                    label: "Departments",
                    value: departmentCount,
                    trendText: "Stable",
                    actionXmlId: "gpj_core.action_gpj_department",
                    viewMode: "list",
                    icon: "fa-building",
                    color: "info",
                },

                {
                    id: "organizational_units",
                    label: "Org. Units",
                    value: organizationalUnitCount,
                    trendText: "+5%",
                    actionXmlId: "gpj_core.action_gpj_organizational_unit",
                    viewMode: "list",
                    icon: "fa-sitemap",
                    color: "success",
                },

                {
                    id: "designations",
                    label: "Designations",
                    value: designationCount,
                    trendText: "2 new",
                    actionXmlId: "gpj_core.action_gpj_designation",
                    viewMode: "list",
                    icon: "fa-id-badge",
                    color: "warning",
                },

                {
                    id: "roles",
                    label: "Roles",
                    value: roleCount,
                    trendText: "Stable",
                    actionXmlId: "gpj_core.action_gpj_institutional_role",
                    viewMode: "list",
                    icon: "fa-shield",
                    color: "danger",
                },

                {
                    id: "memberships",
                    label: "Memberships",
                    value: membershipCount,
                    trendText: "+8%",
                    actionXmlId: "gpj_core.action_gpj_institution_membership",
                    viewMode: "list",
                    icon: "fa-users",
                    color: "secondary",
                },

            ];


            // ============================================================
            // QUICK ACTIONS
            // ============================================================

            this.state.quickActions = [

                {
                    id: "new_campus",
                    label: "New Campus",
                    icon: "fa-plus-circle",
                    actionXmlId: "gpj_core.action_gpj_campus",
                    viewMode: "form",
                    btnClass: "btn-outline-primary",
                },

                {
                    id: "new_department",
                    label: "New Department",
                    icon: "fa-plus-circle",
                    actionXmlId: "gpj_core.action_gpj_department",
                    viewMode: "form",
                    btnClass: "btn-outline-info",
                },

                {
                    id: "new_org_unit",
                    label: "New Org Unit",
                    icon: "fa-plus-circle",
                    actionXmlId: "gpj_core.action_gpj_organizational_unit",
                    viewMode: "form",
                    btnClass: "btn-outline-success",
                },

                {
                    id: "manage_roles",
                    label: "Manage Roles",
                    icon: "fa-cogs",
                    actionXmlId: "gpj_core.action_gpj_institutional_role",
                    viewMode: "list",
                    btnClass: "btn-outline-warning",
                },

            ];


            // ============================================================
            // ALERTS
            // ============================================================

            this.state.alerts = [

                {
                    id: "backup_failed",
                    title: "Database Backup Failed",
                    message:
                        "Scheduled daily backup for 'Academic Data' failed to complete at 03:00 AM.",
                    time: "2 hours ago",
                    type: "danger",
                },

                {
                    id: "module_update",
                    title: "New Module Update Available",
                    message:
                        "ERP Core v2.4.1 is ready for installation.",
                    time: "Yesterday",
                    type: "primary",
                },

            ];

            this.state.alertsCount = this.state.alerts.length;


            // ============================================================
            // RECENT ACTIVITY
            // ============================================================

            this.state.activities = [

                {
                    id: "curriculum_updated",
                    title: "Curriculum Updated",
                    message:
                        "Dr. A. Sharma updated course syllabus for CSE-301",
                    time: "10:45 AM",
                    icon: "fa-pencil",
                },

                {
                    id: "faculty_created",
                    title: "Faculty Created",
                    message:
                        "New faculty profile created in Civil Dept",
                    time: "09:15 AM",
                    icon: "fa-user-plus",
                },

                {
                    id: "system_backup",
                    title: "System Backup",
                    message:
                        "System backup initiated by Admin",
                    time: "Yesterday, 11:30 PM",
                    icon: "fa-database",
                },

            ];


        } catch (error) {

            console.error(
                "GPJ Dashboard: Error loading data",
                error
            );

            this.state.error = true;

        } finally {

            this.state.loading = false;

        }
    }


    // ====================================================================
    // OPEN ODOO ACTION
    // ====================================================================

    async openAction(actionXmlId, viewMode = "list") {

        if (!actionXmlId) {

            console.warn(
                "GPJ Dashboard: No actionXmlId provided"
            );

            return;
        }


        try {

            await this.actionService.doAction(
                actionXmlId,
                {
                    views: [
                        [false, viewMode],
                    ],
                }
            );


        } catch (error) {

            console.error(
                `GPJ Dashboard: Failed to open action ${actionXmlId}`,
                error
            );

        }
    }


    // ====================================================================
    // QUICK ACTION CLICK
    // ====================================================================

    handleQuickAction(event) {

        const button = event.currentTarget;

        const actionXmlId =
            button.dataset.action;

        const viewMode =
            button.dataset.mode || "list";


        this.openAction(
            actionXmlId,
            viewMode
        );
    }


    // ====================================================================
    // STAT CARD CLICK
    // ====================================================================

    handleStatClick(event) {

        const card = event.currentTarget;

        const actionXmlId =
            card.dataset.action;

        const viewMode =
            card.dataset.mode || "list";


        this.openAction(
            actionXmlId,
            viewMode
        );
    }


    // ====================================================================
    // RELOAD
    // ====================================================================

    async reloadDashboard() {

        await this.loadDashboardData();

    }
}


// ========================================================================
// OWL CLIENT ACTION REGISTRATION
// ========================================================================
//
// IMPORTANT:
// This is the ONLY place where "gpj_dashboard" is registered.
//
// institution_ui.js MUST NOT register this same key.
// ========================================================================

GPJDashboard.template =
    "gpj_core.gpj_dashboard_template";


registry
    .category("actions")
    .add("gpj_dashboard", GPJDashboard);