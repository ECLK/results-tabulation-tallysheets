import connexion
from app import db, cache
from auth import ADMIN_ROLE, authorize, get_user_access_area_ids
from constants.AUTH_CONSTANTS import ALL_ROLES
from exception import NotFoundException
from exception.messages import MESSAGE_CODE_ELECTION_NOT_FOUND
from orm.entities import Election
from schemas import ElectionSchema as Schema, AreaMapSchema, MappedAreaSchema
from util import RequestBody


@authorize(required_roles=ALL_ROLES)
def get_all(parentElectionId=None, rootElectionId=None, isListed=None):
    user_access_area_ids = get_user_access_area_ids()

    return _cache_get_all(user_access_area_ids=user_access_area_ids, parentElectionId=parentElectionId,
                          rootElectionId=rootElectionId, isListed=isListed)


@cache.memoize()
def _cache_get_all(user_access_area_ids, parentElectionId=None, rootElectionId=None, isListed=None):
    if isListed == "false":
        isListed = False
    elif isListed == "true":
        isListed = True

    result = Election.get_all(parentElectionId=parentElectionId, rootElectionId=rootElectionId, isListed=isListed)

    return Schema(many=True).dump(result).data


@authorize(required_roles=ALL_ROLES)
def get_by_id(electionId):
    user_access_area_ids = get_user_access_area_ids()

    return _cache_get_by_id(user_access_area_ids=user_access_area_ids, electionId=electionId)


@cache.memoize()
def _cache_get_by_id(user_access_area_ids, electionId):
    result = Election.get_by_id(electionId=electionId)
    if result is None:
        raise NotFoundException(
            message="Election not found (electionId=%d)" % electionId,
            code=MESSAGE_CODE_ELECTION_NOT_FOUND
        )

    return Schema().dump(result).data


@authorize(required_roles=[ADMIN_ROLE])
def create(body):
    request_body = RequestBody(body)
    election_name = request_body.get("electionName")
    election_template_name = request_body.get("electionTemplateName")

    files = connexion.request.files
    polling_stations_dataset = files.get("pollingStationsDataset")
    postal_counting_centres_dataset = files.get("postalCountingCentresDataset")
    party_candidates_dataset = files.get("partyCandidatesDataset")
    invalid_vote_categories_dataset = files.get("invalidVoteCategoriesDataset")
    number_of_seats_dataset_file = files.get("numberOfSeatsDataset")

    election = Election.create(
        electionTemplateName=election_template_name, electionName=election_name, isListed=True,
        party_candidate_dataset_file=party_candidates_dataset,
        polling_station_dataset_file=polling_stations_dataset,
        postal_counting_centers_dataset_file=postal_counting_centres_dataset,
        invalid_vote_categories_dataset_file=invalid_vote_categories_dataset,
        number_of_seats_dataset_file=number_of_seats_dataset_file)

    db.session.commit()

    return Schema().dump(election).data


@authorize(required_roles=[ADMIN_ROLE])
def getRootToken(electionId):
    from ext.ExtendedElection import get_extended_election

    election = Election.Model.query.filter(Election.Model.electionId == electionId).one_or_none()
    extended_election = get_extended_election(election=election)
    return extended_election.get_root_token()


@authorize(required_roles=ALL_ROLES)
def get_area_map(electionId=None):
    user_access_area_ids = get_user_access_area_ids()

    return _cache_get_area_map(user_access_area_ids=user_access_area_ids, electionId=electionId)


@authorize(required_roles=ALL_ROLES)
def get_mapped_area(electionId=None, tallySheetIds=None, requestedAreaType=None):
    election = Election.get_by_id(electionId=electionId)
    if election is None:
        raise NotFoundException(
            message="Election not found (electionId=%d)" % electionId,
            code=MESSAGE_CODE_ELECTION_NOT_FOUND
        )

    extended_election = election.get_extended_election()
    mapped_area = extended_election.get_mapped_area(tallySheetIds, requestedAreaType)

    return MappedAreaSchema(many=True).dump(mapped_area).data


@cache.memoize()
def _cache_get_area_map(user_access_area_ids, electionId):
    election = Election.get_by_id(electionId=electionId)
    if election is None:
        raise NotFoundException(
            message="Election not found (electionId=%d)" % electionId,
            code=MESSAGE_CODE_ELECTION_NOT_FOUND
        )

    extended_election = election.get_extended_election()
    area_map = extended_election.get_area_map()

    return AreaMapSchema(many=True).dump(area_map).data
