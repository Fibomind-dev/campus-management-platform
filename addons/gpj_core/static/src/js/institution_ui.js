/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class GPJInstitutionUI extends Component {
    static template = "gpj_core.InstitutionUI";

    setup() {
        this.orm = useService("orm");

        this.state = useState({
            loading: true,
            institution: null,
            error: null,
        });

        onWillStart(async () => {
            try {
                const ids = await this.orm.search("gpj.institution", [], {
                    limit: 1,
                });

                if (ids.length) {
                    const records = await this.orm.read(
                        "gpj.institution",
                        [ids[0]],
                        [
                            "name",
                            "code",
                            "dte_code",
                            "msbte_code",
                            "established_year",
                            "institution_type",
                            "active",
                            "campus_ids",
                            "department_ids",
                            "organizational_unit_ids",
                            "designation_ids",
                            "institutional_role_ids",
                        ],
                    );

                    this.state.institution = records[0];
                }
            } catch (error) {
                console.error("GPJ Institution UI:", error);
                this.state.error = error;
            } finally {
                this.state.loading = false;
            }
        });
    }

    get institution() {
        return this.state.institution;
    }

    get institutionType() {
        if (!this.institution?.institution_type) {
            return "—";
        }

        return this.institution.institution_type;
    }

    get campusesCount() {
        return this.institution?.campus_ids?.length || 0;
    }

    get departmentsCount() {
        return this.institution?.department_ids?.length || 0;
    }

    get organizationalUnitsCount() {
        return this.institution?.organizational_unit_ids?.length || 0;
    }

    get designationsCount() {
        return this.institution?.designation_ids?.length || 0;
    }

    get institutionalRolesCount() {
        return this.institution?.institutional_role_ids?.length || 0;
    }
}

registry.category("actions").add(
    "gpj_institution_ui",
    GPJInstitutionUI
);
