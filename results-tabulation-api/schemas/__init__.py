from app import db, ma
from orm.entities import Election, Proof, Area, Party, Template, TallySheetVersionRow, \
    TallySheet, TallySheetVersion
from orm.entities.Area import AreaAreaModel
from orm.entities.Audit import Stamp
from orm.entities.Election import ElectionCandidate, InvalidVoteCategory
from orm.entities.IO import File
from orm.entities.Meta import MetaData
from orm.entities.Template import TemplateRowModel
from orm.entities.Workflow import WorkflowStatusModel, WorkflowActionModel, WorkflowInstance
from orm.entities.Workflow.WorkflowInstance import WorkflowInstanceLog
from orm.enums import ProofTypeEnum, ElectorateTypeEnum, AreaTypeEnum
from marshmallow_enum import EnumField


class StatusSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "workflowStatusId",
            "status"
        )

        model = WorkflowStatusModel
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class StatusActionSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "workflowActionId",
            "actionName",
            "actionType",
            "fromStatus",
            "toStatus",
            "allowed",
            "authorized"
        )

        model = WorkflowActionModel
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class StatusActionSchema_1(ma.ModelSchema):
    class Meta:
        fields = (
            "workflowActionId",
            "actionName",
            "actionType",
            "fromStatus",
            "toStatus"
        )

        model = WorkflowActionModel
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class WorkflowInstanceLogSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "workflowInstanceLogId",
            "action",
            "status",
            "metaDataList",
            "proof",
            "createdBy",
            "createdAt"
        )

        model = WorkflowInstanceLog.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    action = ma.Nested(StatusActionSchema_1)
    metaDataList = ma.Nested("MetaDataSchema", many=True)
    proof = ma.Nested("Proof_Schema")


class WorkflowInstanceSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "workflowId",
            # "workflowName",
            "actions",
            # "statuses",
            "status",
            # "latestLog",
            "proof"
        )

        model = WorkflowInstance.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    actions = ma.Nested(StatusActionSchema, many=True)
    statuses = ma.Nested(StatusSchema, many=True)
    proof = ma.Nested("Proof_Schema")


class StampSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "stampId",
            "createdBy",
            "createdAt"
        )

        model = Stamp.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class MetaDataSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "metaDataKey",
            "metaDataValue"
        )

        model = MetaData.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class File_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "fileId",
            "fileName",
            "fileMimeType",
            "fileContentLength",
            "fileCreatedBy",
            "fileCreatedAt",
            "urlInline",
            "urlDownload"
        )

        model = File.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class CandidateSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "candidateId",
            "candidateName",
            "candidateType",
            "candidateNumber",
            "candidateProfileImageFile",
            "qualifiedForPreferences"
        )

        model = ElectionCandidate.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    candidateProfileImageFile = ma.Nested(File_Schema)


class PartySchema(ma.ModelSchema):
    class Meta:
        fields = (
            "partyId",
            "partyName",
            "partySymbol",
            "partySymbolFile",
            "partyAbbreviation",
            "candidates"
        )

        model = Party.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    partySymbolFile = ma.Nested(File_Schema)
    candidates = ma.Nested(CandidateSchema, many=True)


class ElectionSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "electionId",
            "electionName",
            "electionTemplateName",
            "parties",
            "invalidVoteCategories",
            "voteType",
            "rootElectionId",
            "rootElection",
            "parentElectionId",
            "isListed",
            "metaDataList"
        )

        model = Election.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    parties = ma.Nested(PartySchema, many=True)
    invalidVoteCategories = ma.Nested("InvalidVoteCategory_Schema", many=True)
    rootElection = ma.Nested("self", only=[
        "electionId", "electionName", "voteType", "electionTemplateName", "parties", "invalidVoteCategories"
    ])
    parentElection = ma.Nested("self", only=[
        "electionId", "electionName", "voteType", "electionTemplateName", "parties", "invalidVoteCategories"
    ])
    metaDataList = ma.Nested(MetaDataSchema, many=True)


class TallySheetVersionRow_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetVersionRowId",
            "templateRowId",
            "templateRowType",
            "areaId",
            "areaName",
            "ballotBoxId",
            "candidateId",
            "candidateName",
            "partyId",
            "partyName",
            "numValue",
            "strValue",
            "invalidVoteCategoryId"
        )

        model = TallySheetVersionRow.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class AreaSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "areaId",
            "areaName",
            "areaType",
            "electionId",
            # "parents",
            # "children",
            "areaMapList"
        )

        model = Area.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    areaType = EnumField(AreaTypeEnum)
    electorateType = EnumField(ElectorateTypeEnum)
    # parents = ma.Nested('self', only="areaId", many=True)
    children = ma.Nested('AreaAreaSchema', only="childAreaId", many=True)
    parents = ma.Nested('AreaAreaSchema', only="parentAreaId", many=True)
    areaMapList = ma.Nested('AreaMapSchema', many=True, partial=True)


class AreaMapSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "pollingStationId",
            "pollingStationName",
            "pollingDistrictId",
            "pollingDistrictName",
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
            "countryName",
            "countryId"
        )


class MappedAreaSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetId",
            "areaId",
            "areaName",
            "areaType",
            "mappedAreaId",
            "mappedAreaName",
            "mappedAreaType",
        )


class AreaAreaSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "parentAreaId",
            "childAreaId"
        )

        model = AreaAreaModel
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class Proof_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "proofId",
            "proofType",
            "finished",
            "scannedFiles"
        )

        model = Proof.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    scannedFiles = ma.Nested(File_Schema, many=True)
    proofType = EnumField(ProofTypeEnum)


class TallySheetVersionSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetId",
            "tallySheetVersionId",
            "createdBy",
            "createdAt",
            # "htmlUrl",
            # "contentUrl",
            "content",
            "isComplete"
        )

        model = TallySheetVersion.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    content = ma.Nested(TallySheetVersionRow_Schema, many=True)


class TallySheetSchema_1(ma.ModelSchema):
    class Meta:
        fields = (
            "tallySheetId",
            "tallySheetCode",
            "templateId",
            "template",
            "electionId",
            "areaId",
            "area",
            "latestVersion",
            "metaDataList",
            "workflowInstanceId",
            "workflowInstance",
            "latestVersionId"
        )

        model = TallySheet.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    template = ma.Nested("TemplateSchema", only=["templateId", "templateName", "isDerived", "rows"])
    area = ma.Nested(AreaSchema, only=["areaId", "areaName"])
    versions = ma.Nested(TallySheetVersionSchema, only="tallySheetVersionId", many=True)
    latestVersion = ma.Nested(TallySheetVersionSchema)
    metaDataList = ma.Nested(MetaDataSchema, many=True)
    areaMapList = ma.Nested('AreaMapSchema', many=True, partial=True)
    workflowInstance = ma.Nested(WorkflowInstanceSchema, only=["workflowId", "actions", "status", "proof"])


class TemplateRowSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "templateRowId",
            "templateRowType",
            "hasMany",
            "isDerived"
        )

        model = TemplateRowModel
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session


class TemplateSchema(ma.ModelSchema):
    class Meta:
        fields = (
            "templateId",
            "templateName",
            "rows",
            "isDerived"
        )

        model = Template.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session

    rows = ma.Nested(TemplateRowSchema, many=True)


class InvalidVoteCategory_Schema(ma.ModelSchema):
    class Meta:
        fields = (
            "invalidVoteCategoryId",
            "categoryDescription",
            "invalidVoteCategoryType"
        )

        model = InvalidVoteCategory.Model
        # optionally attach a Session
        # to use for deserialization
        sqla_session = db.session
