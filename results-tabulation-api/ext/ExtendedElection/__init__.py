from jose import jwt
from sqlalchemy import bindparam
from sqlalchemy.orm import aliased
from app import db, cache
from constants.AUTH_CONSTANTS import ADMIN_ROLE, DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VIEWER_ROLE, \
    POLLING_DIVISION_REPORT_VERIFIER_ROLE, ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, \
    ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE, NATIONAL_REPORT_VIEWER_ROLE, NATIONAL_REPORT_VERIFIER_ROLE, \
    EC_LEADERSHIP_ROLE, ROLE_PREFIX, ROLE_CLAIM, AREA_CLAIM_PREFIX, SUB
from ext.ExtendedElection.WORKFLOW_STATUS_TYPE import WORKFLOW_STATUS_TYPE_VERIFIED, \
    WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY, WORKFLOW_STATUS_TYPE_CERTIFIED, WORKFLOW_STATUS_TYPE_RELEASED, \
    WORKFLOW_STATUS_TYPE_RELEASE_NOTIFIED
from ext.ExtendedTallySheet import ExtendedTallySheet

def get_extended_election(election):
    from constants.ELECTION_TEMPLATES import PRESIDENTIAL_ELECTION_2019, PARLIAMENT_ELECTION_2020, PROVINCIAL_COUNCIL_ELECTION_2021
    from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021 import ExtendedElectionProvincialCouncilElection2021
    from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020 import ExtendedElectionParliamentaryElection2020
    from ext.ExtendedElection.ExtendedElectionPresidentialElection2019 import ExtendedElectionPresidentialElection2019

    EXTENDED_ELECTION_MAP = {
        PRESIDENTIAL_ELECTION_2019: ExtendedElectionPresidentialElection2019,
        PARLIAMENT_ELECTION_2020: ExtendedElectionParliamentaryElection2020,
        PROVINCIAL_COUNCIL_ELECTION_2021: ExtendedElectionProvincialCouncilElection2021
    }

    if election.electionTemplateName in EXTENDED_ELECTION_MAP:
        return EXTENDED_ELECTION_MAP[election.electionTemplateName](election=election)
    else:
        return None


class ExtendedElection:
    from orm.entities import Election

    role_based_access_config = None

    def __init__(self, election: Election, role_based_access_config=None):
        self.election = election
        self.role_based_access_config = role_based_access_config

    def tally_sheet_verified_statuses_list(self):
        return [
            WORKFLOW_STATUS_TYPE_VERIFIED,
            WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY,
            WORKFLOW_STATUS_TYPE_CERTIFIED,
            WORKFLOW_STATUS_TYPE_RELEASED,
            WORKFLOW_STATUS_TYPE_RELEASE_NOTIFIED
        ]

    def get_extended_tally_sheet_class(self, templateName):

        EXTENDED_TEMPLATE_MAP = {
            # TODO
        }

        if templateName in EXTENDED_TEMPLATE_MAP:
            return EXTENDED_TEMPLATE_MAP[templateName]
        else:
            return ExtendedTallySheet

    def build_election(self, party_candidate_dataset_file=None,
                       polling_station_dataset_file=None, postal_counting_centers_dataset_file=None,
                       invalid_vote_categories_dataset_file=None, number_of_seats_dataset_file=None):
        pass

    def get_area_map_for_tally_sheet(self, tally_sheet):
        area = tally_sheet.area

        return self.get_area_map(area=area)

    def get_mapped_area(self, tally_sheet_ids=None, requested_area_type=None):
        from orm.entities import Area, TallySheet
        from schemas import AreaMapSchema
        filtered_area_map = []

        for tally_sheet_id in str(tally_sheet_ids).split(","):
            input_tallysheet = TallySheet.Model.query.filter(TallySheet.Model.tallySheetId == tally_sheet_id).one_or_none()
            if input_tallysheet is not None:
                input_area = Area.Model.query.filter(Area.Model.areaId == input_tallysheet.areaId).one_or_none()
                area_map = self.get_area_map(area=input_area)
                area_map_data = AreaMapSchema(many=True).dump(area_map).data

                for area_data in area_map_data:
                    filtered_area_map.append({
                        "tallySheetId": tally_sheet_id,
                        "areaId": input_area.areaId,
                        "areaName": input_area.areaName,
                        "areaType": input_area.areaType.name,
                        "mappedAreaId": area_data[requested_area_type+"Id"],
                        "mappedAreaName": area_data[requested_area_type+"Name"],
                        "mappedAreaType": requested_area_type
                    })

        return filtered_area_map

    def get_area_map(self, area=None, group_by=None, filter_by=None):
        from orm.enums import AreaTypeEnum

        area_map_subquery = self.get_area_map_query().subquery()

        if area is None:
            return db.session.query(area_map_subquery).filter(
                area_map_subquery.c.electionId.in_(self.election.get_this_and_below_election_ids())
            )

        column_name_list = [
            "pollingStationId", "pollingStationName",
            "pollingDistrictId", "pollingDistrictName",
            "countingCentreId", "countingCentreName",
            "pollingDivisionId", "pollingDivisionName",
            "electoralDistrictId", "electoralDistrictName",
            "administrativeDistrictId", "administrativeDistrictName",
            "provinceId", "provinceName",
            "countryId", "countryName"
        ]
        column_name_to_column_map = {
            "pollingStationId": area_map_subquery.c.pollingStationId,
            "pollingStationName": area_map_subquery.c.pollingStationName,
            "pollingDistrictId": area_map_subquery.c.pollingDistrictId,
            "pollingDistrictName": area_map_subquery.c.pollingDistrictName,
            "countingCentreId": area_map_subquery.c.countingCentreId,
            "countingCentreName": area_map_subquery.c.countingCentreName,
            "pollingDivisionId": area_map_subquery.c.pollingDivisionId,
            "pollingDivisionName": area_map_subquery.c.pollingDivisionName,
            "electoralDistrictId": area_map_subquery.c.electoralDistrictId,
            "electoralDistrictName": area_map_subquery.c.electoralDistrictName,
            "administrativeDistrictId": area_map_subquery.c.administrativeDistrictId,
            "administrativeDistrictName": area_map_subquery.c.administrativeDistrictName,
            "provinceId": area_map_subquery.c.provinceId,
            "provinceName": area_map_subquery.c.provinceName,
            "countryId": area_map_subquery.c.countryId,
            "countryName": area_map_subquery.c.countryName
        }
        query_args = []
        query_filter = []
        query_group_by = []
        area_and_vote_type_wise_group_by_map = {
            AreaTypeEnum.CountingCentre: [
                "countingCentreId",
                "countingCentreName",
                "pollingDivisionId",
                "pollingDivisionName",
                "electoralDistrictId",
                "electoralDistrictName",
                "administrativeDistrictId",
                "administrativeDistrictName",
                "provinceId",
                "provinceName",
                "countryId",
                "countryName"
            ],
            AreaTypeEnum.PollingStation: [
                "pollingDistrictId",
                "pollingDistrictName",
                "pollingStationId",
                "pollingStationName",
                "countingCentreId",
                "countingCentreName",
                "pollingDivisionId",
                "pollingDivisionName",
                "electoralDistrictId",
                "electoralDistrictName",
                "administrativeDistrictId",
                "administrativeDistrictName",
                "provinceId",
                "provinceName",
                "countryId",
                "countryName"
            ],
            AreaTypeEnum.PollingDivision: [
                "pollingDivisionId",
                "pollingDivisionName",
                "electoralDistrictId",
                "electoralDistrictName",
                "administrativeDistrictId",
                "administrativeDistrictName",
                "provinceId",
                "provinceName",
                "countryId",
                "countryName"
            ],
            AreaTypeEnum.ElectoralDistrict: [
                "electoralDistrictId",
                "electoralDistrictName",
                "countryId",
                "countryName"
            ],
            AreaTypeEnum.AdministrativeDistrict: [
                "administrativeDistrictId",
                "administrativeDistrictName",
                "provinceId",
                "provinceName",
                "countryId",
                "countryName"
            ],
            AreaTypeEnum.Province: [
                "provinceId",
                "provinceName",
                "countryId",
                "countryName"
            ],
            AreaTypeEnum.Country: [
                "countryId",
                "countryName"
            ]
        }

        area_and_vote_type_wise_filter_map = {
            AreaTypeEnum.PollingStation: [area_map_subquery.c.pollingStationId == area.areaId],
            AreaTypeEnum.PollingDistrict: [area_map_subquery.c.pollingDistrictId == area.areaId],
            AreaTypeEnum.CountingCentre: [area_map_subquery.c.countingCentreId == area.areaId],
            AreaTypeEnum.PollingDivision: [area_map_subquery.c.pollingDivisionId == area.areaId],
            AreaTypeEnum.ElectoralDistrict: [area_map_subquery.c.electoralDistrictId == area.areaId],
            AreaTypeEnum.AdministrativeDistrict: [area_map_subquery.c.administrativeDistrictId == area.areaId],
            AreaTypeEnum.Province: [area_map_subquery.c.provinceId == area.areaId],
            AreaTypeEnum.Country: [area_map_subquery.c.countryId == area.areaId]
        }

        if group_by is None:
            if area.areaType in area_and_vote_type_wise_group_by_map:
                group_by = area_and_vote_type_wise_group_by_map[area.areaType]
            else:
                group_by = []

        for column_name in column_name_list:
            column = column_name_to_column_map[column_name]
            if column_name in group_by:
                query_group_by.append(column)

                # Append the column to query.
                query_args.append(column)
            else:
                query_args.append(bindparam(column_name, None))

        if filter_by is None:
            if area.areaType in area_and_vote_type_wise_filter_map:
                filter_by = area_and_vote_type_wise_filter_map[area.areaType]
            else:
                filter_by = []

        query_filter = filter_by

        area_map = db.session.query(*query_args).filter(*query_filter).group_by(*query_group_by).all()

        return area_map

    def get_area_map_query(self):

        from orm.entities import Election, Area
        from orm.entities.Area import AreaAreaModel
        from orm.enums import AreaTypeEnum

        country = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.Country).subquery()
        province = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.Province).subquery()
        electoral_district = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.ElectoralDistrict).subquery()
        administrative_district = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.AdministrativeDistrict).subquery()
        polling_division = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.PollingDivision).subquery()
        polling_district = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.PollingDistrict).subquery()
        polling_station = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.PollingStation).subquery()
        counting_centre = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.CountingCentre).subquery()
        district_centre = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.DistrictCentre).subquery()
        election_commission = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.ElectionCommission).subquery()

        country__province = aliased(AreaAreaModel)
        province__administrative_district = aliased(AreaAreaModel)
        country__electoral_district = aliased(AreaAreaModel)
        administrative_district__polling_division = aliased(AreaAreaModel)
        electoral_district__polling_division = aliased(AreaAreaModel)
        polling_division__polling_district = aliased(AreaAreaModel)
        polling_district__polling_station = aliased(AreaAreaModel)
        counting_centre__polling_station = aliased(AreaAreaModel)
        district_centre__counting_centre = aliased(AreaAreaModel)
        election_commission__district_centre = aliased(AreaAreaModel)

        query = db.session.query(
            country.c.areaId.label("countryId"),
            country.c.areaName.label("countryName"),
            province.c.areaId.label("provinceId"),
            province.c.areaName.label("provinceName"),
            electoral_district.c.areaId.label("electoralDistrictId"),
            electoral_district.c.areaName.label("electoralDistrictName"),
            administrative_district.c.areaId.label("administrativeDistrictId"),
            administrative_district.c.areaName.label("administrativeDistrictName"),
            polling_division.c.areaId.label("pollingDivisionId"),
            polling_division.c.areaName.label("pollingDivisionName"),
            polling_district.c.areaId.label("pollingDistrictId"),
            polling_district.c.areaName.label("pollingDistrictName"),
            polling_station.c.areaId.label("pollingStationId"),
            polling_station.c.areaName.label("pollingStationName"),
            counting_centre.c.areaId.label("countingCentreId"),
            counting_centre.c.areaName.label("countingCentreName"),
            Election.Model.voteType,
            Election.Model.electionId
        ).filter(
            country__electoral_district.parentAreaId == country.c.areaId,
            country__electoral_district.childAreaId == electoral_district.c.areaId,

            country__province.parentAreaId == country.c.areaId,
            country__province.childAreaId == province.c.areaId,

            province__administrative_district.parentAreaId == province.c.areaId,
            province__administrative_district.childAreaId == administrative_district.c.areaId,

            administrative_district__polling_division.parentAreaId == administrative_district.c.areaId,
            administrative_district__polling_division.childAreaId == polling_division.c.areaId,

            electoral_district__polling_division.parentAreaId == electoral_district.c.areaId,
            electoral_district__polling_division.childAreaId == polling_division.c.areaId,

            polling_division__polling_district.parentAreaId == polling_division.c.areaId,
            polling_division__polling_district.childAreaId == polling_district.c.areaId,

            polling_district__polling_station.parentAreaId == polling_district.c.areaId,
            polling_district__polling_station.childAreaId == polling_station.c.areaId,

            counting_centre__polling_station.parentAreaId == counting_centre.c.areaId,
            counting_centre__polling_station.childAreaId == polling_station.c.areaId,

            district_centre__counting_centre.parentAreaId == district_centre.c.areaId,
            district_centre__counting_centre.childAreaId == counting_centre.c.areaId,

            election_commission__district_centre.parentAreaId == election_commission.c.areaId,
            election_commission__district_centre.childAreaId == district_centre.c.areaId,

            Election.Model.electionId == counting_centre.c.electionId
        )

        return query

    def get_root_token(self):
        from orm.entities import Area
        from orm.enums import AreaTypeEnum

        electoral_districts = Area.get_associated_areas_query(
            areas=[], areaType=AreaTypeEnum.ElectoralDistrict, electionId=self.election.electionId
        ).all()

        countries = Area.get_associated_areas_query(
            areas=[], areaType=AreaTypeEnum.Country, electionId=self.election.electionId
        ).all()

        jwt_payload = {
            ROLE_CLAIM: [
                ROLE_PREFIX + ADMIN_ROLE,
                ROLE_PREFIX + DATA_EDITOR_ROLE,
                ROLE_PREFIX + POLLING_DIVISION_REPORT_VIEWER_ROLE,
                ROLE_PREFIX + POLLING_DIVISION_REPORT_VERIFIER_ROLE,
                ROLE_PREFIX + ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE,
                ROLE_PREFIX + ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE,
                ROLE_PREFIX + NATIONAL_REPORT_VIEWER_ROLE,
                ROLE_PREFIX + NATIONAL_REPORT_VERIFIER_ROLE,
                ROLE_PREFIX + EC_LEADERSHIP_ROLE
            ],
            SUB: "janak@carbon.super", AREA_CLAIM_PREFIX + ADMIN_ROLE: str([]),
            AREA_CLAIM_PREFIX + DATA_EDITOR_ROLE: str([{
                "areaId": electoral_district.areaId,
                "areaName": electoral_district.areaName
            } for electoral_district in electoral_districts]),
            AREA_CLAIM_PREFIX + POLLING_DIVISION_REPORT_VIEWER_ROLE: str([{
                "areaId": electoral_district.areaId,
                "areaName": electoral_district.areaName
            } for electoral_district in electoral_districts]),
            AREA_CLAIM_PREFIX + POLLING_DIVISION_REPORT_VERIFIER_ROLE: str([{
                "areaId": electoral_district.areaId,
                "areaName": electoral_district.areaName
            } for electoral_district in electoral_districts]),
            AREA_CLAIM_PREFIX + ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE: str([{
                "areaId": electoral_district.areaId,
                "areaName": electoral_district.areaName
            } for electoral_district in electoral_districts]),
            AREA_CLAIM_PREFIX + ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE: str([{
                "areaId": electoral_district.areaId,
                "areaName": electoral_district.areaName
            } for electoral_district in electoral_districts]),
            AREA_CLAIM_PREFIX + NATIONAL_REPORT_VIEWER_ROLE: str([{
                "areaId": country.areaId,
                "areaName": country.areaName
            } for country in countries]),
            AREA_CLAIM_PREFIX + NATIONAL_REPORT_VERIFIER_ROLE: str([{
                "areaId": country.areaId,
                "areaName": country.areaName
            } for country in countries]),
            AREA_CLAIM_PREFIX + EC_LEADERSHIP_ROLE: str([{
                "areaId": country.areaId,
                "areaName": country.areaName
            } for country in countries])
        }

        # Generate a token with claims for everything.
        key = "jwt_secret"
        encoded_jwt_token = jwt.encode(jwt_payload, key)

        return encoded_jwt_token
