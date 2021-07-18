# -*- coding: utf-8 -*-

"""
    Application Template for Rhineland-Palatinate (RLP) Crisis Management
    - used to register beneficiaries and their needs, and broker emergency assistance

    @license MIT
"""

from collections import OrderedDict

from gluon import current, URL, A, DIV, TAG, \
                  IS_EMPTY_OR, IS_IN_SET, IS_INT_IN_RANGE, IS_NOT_EMPTY

from gluon.storage import Storage

from s3 import FS, IS_FLOAT_AMOUNT, ICON, IS_ONE_OF, S3Represent, s3_str
from s3dal import original_tablename

from templates.RLPPTM.rlpgeonames import rlp_GeoNames

# =============================================================================
def config(settings):

    T = current.T

    names = {"region": "Rheinland-Pfalz"}
    settings.base.system_name = T("%(region)s Emergency Relief") % names
    settings.base.system_name_short = T("%(region)s Emergency Relief") % names
    settings.custom.homepage_title = T("Emergency Relief")

    # PrePopulate data
    settings.base.prepopulate.append("BRCMS/RLP")
    settings.base.prepopulate_demo.append("BRCMS/RLP/Demo")

    # Theme
    settings.base.theme = "RLP"
    settings.base.theme_layouts = "BRCMS/RLP"

    # Auth settings
    settings.auth.password_min_length = 8
    settings.auth.consent_tracking = True

    # Custom Logo
    settings.ui.menu_logo = URL(c="static", f="themes", args=["RLP", "img", "logo_rlp.png"])

    # Restrict the Location Selector to just certain countries
    settings.gis.countries = ("DE",)
    #gis_levels = ("L1", "L2", "L3")

    # Use custom geocoder
    settings.gis.geocode_service = rlp_GeoNames

    # L10n settings
    # Languages used in the deployment (used for Language Toolbar, GIS Locations, etc)
    # http://www.loc.gov/standards/iso639-2/php/code_list.php
    settings.L10n.languages = OrderedDict([
       ("de", "German"),
       ("en", "English"),
    ])
    # Default language for Language Toolbar (& GIS Locations in future)
    settings.L10n.default_language = "de"
    # Uncomment to Hide the language toolbar
    #settings.L10n.display_toolbar = False
    # Default timezone for users
    settings.L10n.timezone = "Europe/Berlin"
    # Default date/time formats
    settings.L10n.date_format = "%d.%m.%Y"
    settings.L10n.time_format = "%H:%M"
    # Number formats (defaults to ISO 31-0)
    # Decimal separator for numbers (defaults to ,)
    settings.L10n.decimal_separator = "."
    # Thousands separator for numbers (defaults to space)
    settings.L10n.thousands_separator = " "
    # Uncomment this to Translate Layer Names
    #settings.L10n.translate_gis_layer = True
    # Uncomment this to Translate Location Names
    #settings.L10n.translate_gis_location = True
    # Uncomment this to Translate Organisation Names/Acronyms
    #settings.L10n.translate_org_organisation = True
    # Finance settings
    settings.fin.currencies = {
        "EUR" : "Euros",
    #    "GBP" : "Great British Pounds",
    #    "USD" : "United States Dollars",
    }
    settings.fin.currency_default = "EUR"

    # -------------------------------------------------------------------------
    settings.pr.hide_third_gender = False
    settings.pr.separate_name_fields = 2
    settings.pr.name_format= "%(last_name)s, %(first_name)s"

    # -------------------------------------------------------------------------
    # UI Settings
    settings.ui.calendar_clear_icon = True

    # -------------------------------------------------------------------------
    # TODO Realm Rules
    #
    def brcms_realm_entity(table, row):
        """
            Assign a Realm Entity to records
        """

        db = current.db
        s3db = current.s3db

        tablename = original_tablename(table)

        realm_entity = 0

        if tablename == "pr_person":

            # Client records are owned by the organisation
            # the case is assigned to
            ctable = s3db.br_case
            query = (ctable.person_id == row.id) & \
                    (ctable.deleted == False)
            case = db(query).select(ctable.organisation_id,
                                    limitby = (0, 1),
                                    ).first()

            if case and case.organisation_id:
                realm_entity = s3db.pr_get_pe_id("org_organisation",
                                                 case.organisation_id,
                                                 )

        elif tablename in ("pr_address",
                           "pr_contact",
                           "pr_contact_emergency",
                           "pr_image",
                           ):

            # Inherit from person via PE
            table = s3db.table(tablename)
            ptable = s3db.pr_person
            query = (table._id == row.id) & \
                    (ptable.pe_id == table.pe_id)
            person = db(query).select(ptable.realm_entity,
                                      limitby = (0, 1),
                                      ).first()
            if person:
                realm_entity = person.realm_entity

        elif tablename in ("br_appointment",
                           "br_case_activity",
                           "br_case_language",
                           "br_assistance_measure",
                           "br_note",
                           "pr_group_membership",
                           "pr_person_details",
                           "pr_person_tag",
                           ):

            # Inherit from person via person_id
            table = s3db.table(tablename)
            ptable = s3db.pr_person
            query = (table._id == row.id) & \
                    (ptable.id == table.person_id)
            person = db(query).select(ptable.realm_entity,
                                      limitby = (0, 1),
                                      ).first()
            if person:
                realm_entity = person.realm_entity

        elif tablename == "br_case_activity_update":

            # Inherit from case activity
            table = s3db.table(tablename)
            atable = s3db.br_case_activity
            query = (table._id == row.id) & \
                    (atable.id == table.case_activity_id)
            activity = db(query).select(atable.realm_entity,
                                        limitby = (0, 1),
                                        ).first()
            if activity:
                realm_entity = activity.realm_entity

        elif tablename == "br_assistance_measure_theme":

            # Inherit from measure
            table = s3db.table(tablename)
            mtable = s3db.br_assistance_measure
            query = (table._id == row.id) & \
                    (mtable.id == table.measure_id)
            activity = db(query).select(mtable.realm_entity,
                                        limitby = (0, 1),
                                        ).first()
            if activity:
                realm_entity = activity.realm_entity

        elif tablename == "pr_group":

            # No realm-entity for case groups
            table = s3db.pr_group
            query = table._id == row.id
            group = db(query).select(table.group_type,
                                     limitby = (0, 1),
                                     ).first()
            if group and group.group_type == 7:
                realm_entity = None

        elif tablename == "project_task":

            # Inherit the realm entity from the assignee
            assignee_pe_id = row.pe_id
            instance_type = s3db.pr_instance_type(assignee_pe_id)
            if instance_type:
                table = s3db.table(instance_type)
                query = table.pe_id == assignee_pe_id
                assignee = db(query).select(table.realm_entity,
                                            limitby = (0, 1),
                                            ).first()
                if assignee and assignee.realm_entity:
                    realm_entity = assignee.realm_entity

            # If there is no assignee, or the assignee has no
            # realm entity, fall back to the user organisation
            if realm_entity == 0:
                auth = current.auth
                user_org_id = auth.user.organisation_id if auth.user else None
                if user_org_id:
                    realm_entity = s3db.pr_get_pe_id("org_organisation",
                                                     user_org_id,
                                                     )
        return realm_entity

    settings.auth.realm_entity = brcms_realm_entity

    # -------------------------------------------------------------------------
    def customise_cms_post_resource(r, tablename):

        s3db = current.s3db

        table = s3db.cms_post

        from s3 import S3SQLCustomForm, \
                       S3SQLInlineComponent, \
                       S3SQLInlineLink, \
                       s3_text_represent

        field = table.body
        field.represent = lambda v, row=None: \
                          s3_text_represent(v, lines=20, _class = "cms-item-body")

        record = r.record
        if r.tablename == "cms_series" and \
           record and record.name == "Announcements":
            table = s3db.cms_post
            field = table.priority
            field.readable = field.writable = True

            crud_fields = ["name",
                           "body",
                           "priority",
                           "date",
                           "expired",
                           S3SQLInlineLink("roles",
                                           label = T("Roles"),
                                           field = "group_id",
                                           ),
                           ]
            list_fields = ["date",
                           "priority",
                           "name",
                           "body",
                           "post_role.group_id",
                           "expired",
                           ]
            orderby = "cms_post.date desc"
        else:
            crud_fields = ["name",
                           "body",
                           "date",
                           S3SQLInlineComponent("document",
                                                name = "file",
                                                label = T("Attachments"),
                                                fields = ["file", "comments"],
                                                filterby = {"field": "file",
                                                            "options": "",
                                                            "invert": True,
                                                            },
                                                ),
                           "comments",
                           ]
            list_fields = ["post_module.module",
                           "post_module.resource",
                           "name",
                           "date",
                           "comments",
                           ]
            orderby = "cms_post.name"

        s3db.configure("cms_post",
                       crud_form = S3SQLCustomForm(*crud_fields),
                       list_fields = list_fields,
                       orderby = orderby,
                       )

    settings.customise_cms_post_resource = customise_cms_post_resource

    # -----------------------------------------------------------------------------
    def customise_cms_post_controller(**attr):

        s3 = current.response.s3

        # Custom prep
        standard_prep = s3.prep
        def prep(r):
            # Call standard prep
            result = standard_prep(r) if callable(standard_prep) else True

            table = r.table
            context = r.get_vars.get("resource")
            if context == "Privacy":
                page = URL(c="default", f="index", args=["privacy"])
                r.resource.configure(create_next = page,
                                     update_next = page,
                                     )
                table.name.default = "Privacy Notice"
            elif context == "Legal":
                page = URL(c="default", f="index", args=["legal"])
                r.resource.configure(create_next = page,
                                     update_next = page,
                                     )
                table.name.default = "Legal Notice"
            return result
        s3.prep = prep

        return attr

    settings.customise_cms_post_controller = customise_cms_post_controller

    # -----------------------------------------------------------------------------
    # TODO customise br_assistance_offer

    # -----------------------------------------------------------------------------
    # TODO customise br_case_activity
    #
    def customise_br_case_activity_resource(r, tablename):

        # TODO Configure CRUD form

        # TODO Configure List fields and filters

        # TODO Adjust CRUD strings

        pass

    settings.customise_br_case_activity_resource = customise_br_case_activity_resource

    # -----------------------------------------------------------------------------
    def customise_br_case_activity_controller(**attr):

        s3 = current.response.s3

        # Custom prep
        standard_prep = s3.prep
        def prep(r):
            # Call standard prep
            result = standard_prep(r) if callable(standard_prep) else True

            # TODO if not mine, filter for current activities only

            # TODO DRY roles list with menus.py
            if not current.auth.s3_has_roles(("EVENT_MANAGER", "CASE_MANAGER", "RELIEF_PROVIDER")):
                r.resource.configure(insertable = True,
                                     deletable = True,
                                     )

                # TODO set default for pr_person (to logged-in person)

            return result
        s3.prep = prep

        # TODO postp to override list-button in read-views to return to mine if mine

        return attr

    settings.customise_br_case_activity_controller = customise_br_case_activity_controller

    # -----------------------------------------------------------------------------
    # TODO customise event_event

    # -----------------------------------------------------------------------------
    # TODO customise org_organisation

    # -----------------------------------------------------------------------------
    # TODO customise pr_person (Case file, Profile)

# END =========================================================================