// /** @odoo-module **/

// import { Component, onWillStart, useState } from "@odoo/owl";

// import { registry } from "@web/core/registry";
// import { useService } from "@web/core/utils/hooks";


// export class GPJDashboard extends Component {

//     setup() {

//         // ================================================================
//         // SERVICES
//         // ================================================================

//         this.orm = useService("orm");
//         this.actionService = useService("action");


//         // ================================================================
//         // STATE
//         // ================================================================

//         this.state = useState({

//             loading: true,

//             stats: [],

//             quickActions: [],

//             alerts: [],

//             alertsCount: 0,

//             activities: [],

//         });


//         // ================================================================
//         // INITIAL LOAD
//         // ================================================================

//         onWillStart(async () => {
//             await this.loadDashboardData();
//         });

//     }


//     // ====================================================================
//     // LOAD DASHBOARD DATA
//     // ====================================================================

//     async loadDashboardData() {

//         this.state.loading = true;

//         try {

//             // ------------------------------------------------------------
//             // GET INSTITUTIONS
//             // ------------------------------------------------------------

//             const institutions = await this.orm.searchRead(
//                 "gpj.institution",
//                 [],
//                 ["id"]
//             );

//             const institutionIds = institutions.map(
//                 (institution) => institution.id
//             );


//             // ------------------------------------------------------------
//             // DATABASE COUNTS
//             // ------------------------------------------------------------

//             let campusCount = 0;
//             let departmentCount = 0;
//             let ouCount = 0;
//             let designationCount = 0;
//             let roleCount = 0;
//             let membershipCount = 0;


//             /*
//              * If there are no institutions, an "in" domain with an empty
//              * array is unnecessary. Keep all counts at zero.
//              */

//             if (institutionIds.length) {

//                 [
//                     campusCount,
//                     departmentCount,
//                     ouCount,
//                     designationCount,
//                     roleCount,
//                     membershipCount,
//                 ] = await Promise.all([

//                     this.orm.searchCount(
//                         "gpj.campus",
//                         [
//                             [
//                                 "institution_id",
//                                 "in",
//                                 institutionIds,
//                             ],
//                         ]
//                     ),

//                     this.orm.searchCount(
//                         "gpj.department",
//                         [
//                             [
//                                 "institution_id",
//                                 "in",
//                                 institutionIds,
//                             ],
//                         ]
//                     ),

//                     this.orm.searchCount(
//                         "gpj.organizational.unit",
//                         [
//                             [
//                                 "institution_id",
//                                 "in",
//                                 institutionIds,
//                             ],
//                         ]
//                     ),

//                     this.orm.searchCount(
//                         "gpj.designation",
//                         [
//                             [
//                                 "institution_id",
//                                 "in",
//                                 institutionIds,
//                             ],
//                         ]
//                     ),

//                     this.orm.searchCount(
//                         "gpj.institutional.role",
//                         [
//                             [
//                                 "institution_id",
//                                 "in",
//                                 institutionIds,
//                             ],
//                         ]
//                     ),

//                     this.orm.searchCount(
//                         "gpj.institution.membership",
//                         [
//                             [
//                                 "institution_id",
//                                 "in",
//                                 institutionIds,
//                             ],
//                         ]
//                     ),

//                 ]);

//             }


//             // ============================================================
//             // STAT CARDS
//             // ============================================================

//             this.state.stats = [

//                 {
//                     label: "Campuses",
//                     value: campusCount,
//                     trendText: "Manage",
//                     actionXmlId: "gpj_core.action_gpj_campus",
//                     icon: "fa-university",
//                     color: "primary",
//                 },

//                 {
//                     label: "Departments",
//                     value: departmentCount,
//                     trendText: "Manage",
//                     actionXmlId: "gpj_core.action_gpj_department",
//                     icon: "fa-building",
//                     color: "info",
//                 },

//                 {
//                     label: "Organizational Units",
//                     value: ouCount,
//                     trendText: "Manage",
//                     actionXmlId: "gpj_core.action_gpj_organizational_unit",
//                     icon: "fa-sitemap",
//                     color: "success",
//                 },

//                 {
//                     label: "Designations",
//                     value: designationCount,
//                     trendText: "Manage",
//                     actionXmlId: "gpj_core.action_gpj_designation",
//                     icon: "fa-id-badge",
//                     color: "warning",
//                 },

//                 {
//                     label: "Roles",
//                     value: roleCount,
//                     trendText: "Manage",
//                     actionXmlId: "gpj_core.action_gpj_institutional_role",
//                     icon: "fa-shield",
//                     color: "danger",
//                 },

//                 {
//                     label: "Memberships",
//                     value: membershipCount,
//                     trendText: "Manage",
//                     actionXmlId: "gpj_core.action_gpj_institution_membership",
//                     icon: "fa-users",
//                     color: "secondary",
//                 },

//             ];


//             // ============================================================
//             // QUICK ACTIONS
//             // ============================================================

//             this.state.quickActions = [

//                 {
//                     label: "New Campus",
//                     icon: "fa-plus-circle",
//                     actionXmlId: "gpj_core.action_gpj_campus",
//                     mode: "create",
//                     btnClass: "btn-outline-primary",
//                 },

//                 {
//                     label: "New Department",
//                     icon: "fa-plus-circle",
//                     actionXmlId: "gpj_core.action_gpj_department",
//                     mode: "create",
//                     btnClass: "btn-outline-info",
//                 },

//                 {
//                     label: "New Org Unit",
//                     icon: "fa-plus-circle",
//                     actionXmlId: "gpj_core.action_gpj_organizational_unit",
//                     mode: "create",
//                     btnClass: "btn-outline-success",
//                 },

//                 {
//                     label: "Manage Roles",
//                     icon: "fa-cogs",
//                     actionXmlId: "gpj_core.action_gpj_institutional_role",
//                     mode: "list",
//                     btnClass: "btn-outline-warning",
//                 },

//             ];


//             // ============================================================
//             // ALERTS
//             // ============================================================

//             /*
//              * These are currently static dashboard alerts.
//              *
//              * Later these can be replaced with real ORM data.
//              */

//             this.state.alerts = [

//                 {
//                     id: 1,
//                     title: "Database Backup Failed",
//                     message:
//                         "Scheduled daily backup for 'Academic Data' failed to complete at 03:00 AM.",
//                     time: "2 hours ago",
//                     type: "danger",
//                     icon: "fa-database",
//                 },

//                 {
//                     id: 2,
//                     title: "New Module Update Available",
//                     message:
//                         "ERP Core v2.4.1 is ready for installation.",
//                     time: "Yesterday",
//                     type: "primary",
//                     icon: "fa-download",
//                 },

//             ];

//             this.state.alertsCount = this.state.alerts.length;


//             // ============================================================
//             // RECENT ACTIVITY
//             // ============================================================

//             /*
//              * Static for now.
//              *
//              * This can later be connected to mail.message,
//              * audit logs, or your own activity model.
//              */

//             this.state.activities = [

//                 {
//                     id: 1,
//                     title: "Curriculum Updated",
//                     message:
//                         "Dr. A. Sharma updated course syllabus for CSE-301",
//                     time: "10:45 AM",
//                     icon: "fa-pencil",
//                 },

//                 {
//                     id: 2,
//                     title: "Faculty Created",
//                     message:
//                         "New faculty profile created in Civil Department",
//                     time: "09:15 AM",
//                     icon: "fa-user-plus",
//                 },

//                 {
//                     id: 3,
//                     title: "System Backup",
//                     message:
//                         "System backup initiated by Admin",
//                     time: "Yesterday, 11:30 PM",
//                     icon: "fa-database",
//                 },

//             ];

//         } catch (error) {

//             console.error(
//                 "GPJ Dashboard: error loading data",
//                 error
//             );

//         } finally {

//             this.state.loading = false;

//         }

//     }


//     // ====================================================================
//     // OPEN ODOO ACTION
//     // ====================================================================

//     async openAction(actionXmlId, mode = "list") {

//         if (!actionXmlId) {

//             console.warn(
//                 "GPJ Dashboard: No actionXmlId provided"
//             );

//             return;

//         }


//         try {

//             // ------------------------------------------------------------
//             // CREATE MODE
//             // ------------------------------------------------------------

//             if (mode === "create") {

//                 await this.actionService.doAction(
//                     actionXmlId,
//                     {
//                         views: [
//                             [false, "form"],
//                         ],

//                         res_id: false,
//                     }
//                 );

//                 return;
//             }


//             // ------------------------------------------------------------
//             // LIST / OTHER VIEW
//             // ------------------------------------------------------------

//             await this.actionService.doAction(
//                 actionXmlId,
//                 {
//                     views: [
//                         [false, mode],
//                     ],
//                 }
//             );

//         } catch (error) {

//             console.error(
//                 `GPJ Dashboard: Failed to open action ${actionXmlId}`,
//                 error
//             );

//         }

//     }


//     // ====================================================================
//     // RELOAD DASHBOARD
//     // ====================================================================

//     async reloadDashboard() {

//         await this.loadDashboardData();

//     }

// }


// // ========================================================================
// // REGISTER CLIENT ACTION
// // ========================================================================

// GPJDashboard.template = "gpj_core.gpj_dashboard_template";

// registry
//     .category("actions")
//     .add("gpj_dashboard", GPJDashboard);



/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";


/**
 * GPJ Institution UI
 *
 * This file is intentionally independent from dashboard.js.
 *
 * IMPORTANT:
 * Do NOT register "gpj_dashboard" from this file.
 * The dashboard action belongs exclusively to dashboard.js.
 */
export class GPJInstitutionUI extends Component {

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
            loading: true,
            institutions: [],
            selectedInstitution: null,
        });


        // ================================================================
        // INITIALIZATION
        // ================================================================

        onWillStart(async () => {
            await this.loadInstitutions();
        });
    }


    // ====================================================================
    // LOAD INSTITUTIONS
    // ====================================================================

    async loadInstitutions() {

        this.state.loading = true;

        try {

            this.state.institutions = await this.orm.searchRead(
                "gpj.institution",
                [],
                [
                    "id",
                    "name",
                    "code",
                    "active",
                ]
            );

        } catch (error) {

            console.error(
                "GPJ Institution UI: Failed to load institutions",
                error
            );

            this.state.institutions = [];

        } finally {

            this.state.loading = false;

        }
    }


    // ====================================================================
    // OPEN INSTITUTION
    // ====================================================================

    async openInstitution(institutionId) {

        if (!institutionId) {
            return;
        }

        try {

            await this.actionService.doAction(
                "gpj_core.action_gpj_institution",
                {
                    views: [
                        [false, "form"],
                    ],
                    res_id: institutionId,
                }
            );

        } catch (error) {

            console.error(
                "GPJ Institution UI: Failed to open institution",
                error
            );

        }
    }


    // ====================================================================
    // CREATE INSTITUTION
    // ====================================================================

    async createInstitution() {

        try {

            await this.actionService.doAction(
                "gpj_core.action_gpj_institution",
                {
                    views: [
                        [false, "form"],
                    ],
                    res_id: false,
                }
            );

        } catch (error) {

            console.error(
                "GPJ Institution UI: Failed to create institution",
                error
            );

        }
    }


    // ====================================================================
    // REFRESH
    // ====================================================================

    async reload() {
        await this.loadInstitutions();
    }
}


// ========================================================================
// TEMPLATE
// ========================================================================
//
// This registration is OPTIONAL.
// If institution_ui.xml uses this component as an OWL client action,
// register it under a UNIQUE key.
//
// IMPORTANT:
// NEVER use "gpj_dashboard" here.
//
// ========================================================================

GPJInstitutionUI.template = "gpj_core.gpj_institution_ui";

registry
    .category("actions")
    .add("gpj_institution_ui", GPJInstitutionUI);