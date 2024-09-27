import axios from 'axios';
import {TABULATION_API_URL} from "../../config";
import {getAccessToken} from "../../auth";

export const ENDPOINT_PATH_ELECTIONS = () => "/election";
export const ENDPOINT_PATH_ELECTIONS_BY_ID = (electionId) => `/election/${electionId}`;
export const ENDPOINT_PATH_ELECTION_AREA_MAP_BY_ID = (electionId) => `/election/${electionId}/area-map`;
export const ENDPOINT_PATH_ELECTION_MAPPED_AREA_BY_ID = (electionId,tallySheetIds,areaType) => `/election/${electionId}/mapped-area?tallySheetIds=${tallySheetIds.toString()}&requestedAreaType=${areaType}`;
export const ENDPOINT_PATH_AREAS = () => "/area";
export const ENDPOINT_PATH_AREAS_BY_ID = (areaId) => `/area/${areaId}`;
export const ENDPOINT_PATH_TALLY_SHEETS = () => "/tally-sheet";
export const ENDPOINT_PATH_TALLY_SHEETS_BY_ID = (tallySheetId) => `/tally-sheet/${tallySheetId}`;
export const ENDPOINT_PATH_TALLY_SHEET_VERSION_BY_ID = (tallySheetId, tallySheetCode, tallySheetVersionId) => {
    let path = `/tally-sheet/${tallySheetId}/version`;
    if (tallySheetVersionId) {
        path += `/${tallySheetVersionId}`;
    }

    return path;
};
export const ENDPOINT_PATH_TALLY_SHEET_WORKFLOW = (tallySheetId) => `/tally-sheet/${tallySheetId}/workflow`;
export const ENDPOINT_PATH_TALLY_SHEET_VERSION_HTML = (tallySheetId, tallySheetVersionId) => `/tally-sheet/${tallySheetId}/version/${tallySheetVersionId}/html`;
export const ENDPOINT_PATH_TALLY_SHEET_VERSION_PDF = (tallySheetId, tallySheetVersionId) => `/tally-sheet/${tallySheetId}/version/${tallySheetVersionId}/pdf`;
export const ENDPOINT_PATH_TALLY_SHEET_VERSION_LETTER_HTML = (tallySheetId, tallySheetVersionId) => `/tally-sheet/${tallySheetId}/version/${tallySheetVersionId}/letter/html`;
export const ENDPOINT_PATH_TALLY_SHEET_VERSION_LETTER_PDF = (tallySheetId, tallySheetVersionId) => `/tally-sheet/${tallySheetId}/version/${tallySheetVersionId}/letter/pdf`;

export const ENDPOINT_PATH_TALLY_SHEET_PROOF = (tallySheetId, proofId) => `/tally-sheet/${tallySheetId}/workflow/proof/${proofId}`;
export const ENDPOINT_PATH_TALLY_SHEET_WORKFLOW_LOGS = (tallySheetId) => `/tally-sheet/${tallySheetId}/workflow/logs`;
export const ENDPOINT_PATH_TALLY_SHEET_PROOF_FINISH = (proofId) => `/proof/${proofId}/finish`;
export const ENDPOINT_PATH_FILE = (tallySheetId, fileId) => `/tally-sheet/${tallySheetId}/workflow/proof/file/${fileId}`;
export const ENDPOINT_PATH_FILE_DOWNLOAD = (tallySheetId, fileId) => `/tally-sheet/${tallySheetId}/workflow/proof/file/${fileId}/download`;


const axiosInstance = axios.create({
    baseURL: TABULATION_API_URL,
    headers: {
        'Authorization': "Bearer " + getAccessToken(),
        // 'X-Jwt-Assertion': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL3VzZXJuYW1lIjoiamFuYWtAY2FyYm9uLnN1cGVyIiwiaHR0cDovL3dzbzIub3JnL2NsYWltcy9hcmVhX2Fzc2lnbl9hZG1pbiI6IltdIiwiaHR0cDovL3dzbzIub3JnL2NsYWltcy9hcmVhX2Fzc2lnbl9kYXRhX2VkaXRvciI6Ilt7J2FyZWFJZCc6IDg2NSwgJ2FyZWFOYW1lJzogJzMxJ30sIHsnYXJlYUlkJzogODY2LCAnYXJlYU5hbWUnOiAnMzInfSwgeydhcmVhSWQnOiA4NjcsICdhcmVhTmFtZSc6ICczMyd9LCB7J2FyZWFJZCc6IDg2OCwgJ2FyZWFOYW1lJzogJzM0J30sIHsnYXJlYUlkJzogODY5LCAnYXJlYU5hbWUnOiAnMzUnfSwgeydhcmVhSWQnOiA4NzAsICdhcmVhTmFtZSc6ICczNid9LCB7J2FyZWFJZCc6IDg3MSwgJ2FyZWFOYW1lJzogJzM3J30sIHsnYXJlYUlkJzogODcyLCAnYXJlYU5hbWUnOiAnMzgnfSwgeydhcmVhSWQnOiA4NzMsICdhcmVhTmFtZSc6ICczOSd9LCB7J2FyZWFJZCc6IDg3NCwgJ2FyZWFOYW1lJzogJzQwJ30sIHsnYXJlYUlkJzogODc1LCAnYXJlYU5hbWUnOiAnNDEnfSwgeydhcmVhSWQnOiA4NzYsICdhcmVhTmFtZSc6ICc0Mid9LCB7J2FyZWFJZCc6IDcsICdhcmVhTmFtZSc6ICcxJ30sIHsnYXJlYUlkJzogMTAsICdhcmVhTmFtZSc6ICcyJ30sIHsnYXJlYUlkJzogMTMsICdhcmVhTmFtZSc6ICczJ30sIHsnYXJlYUlkJzogMTYsICdhcmVhTmFtZSc6ICc0J30sIHsnYXJlYUlkJzogMTksICdhcmVhTmFtZSc6ICc1J30sIHsnYXJlYUlkJzogMjIsICdhcmVhTmFtZSc6ICc2J30sIHsnYXJlYUlkJzogMjUsICdhcmVhTmFtZSc6ICc3J30sIHsnYXJlYUlkJzogMTg3LCAnYXJlYU5hbWUnOiAnOCd9LCB7J2FyZWFJZCc6IDE5MCwgJ2FyZWFOYW1lJzogJzExJ30sIHsnYXJlYUlkJzogMTkzLCAnYXJlYU5hbWUnOiAnMTAnfSwgeydhcmVhSWQnOiAxOTgsICdhcmVhTmFtZSc6ICcxMid9LCB7J2FyZWFJZCc6IDIwMywgJ2FyZWFOYW1lJzogJzknfSwgeydhcmVhSWQnOiAzNDUsICdhcmVhTmFtZSc6ICcxMyd9LCB7J2FyZWFJZCc6IDM0OCwgJ2FyZWFOYW1lJzogJzE0J30sIHsnYXJlYUlkJzogMzUxLCAnYXJlYU5hbWUnOiAnMTUnfSwgeydhcmVhSWQnOiAzNTQsICdhcmVhTmFtZSc6ICcxNid9LCB7J2FyZWFJZCc6IDM1NywgJ2FyZWFOYW1lJzogJzE3J30sIHsnYXJlYUlkJzogMzYwLCAnYXJlYU5hbWUnOiAnMTgnfSwgeydhcmVhSWQnOiAzNjMsICdhcmVhTmFtZSc6ICcxOSd9LCB7J2FyZWFJZCc6IDM2NiwgJ2FyZWFOYW1lJzogJzIwJ30sIHsnYXJlYUlkJzogNTYyLCAnYXJlYU5hbWUnOiAnMjEnfSwgeydhcmVhSWQnOiA1NjUsICdhcmVhTmFtZSc6ICcyMid9LCB7J2FyZWFJZCc6IDU2OCwgJ2FyZWFOYW1lJzogJzIzJ30sIHsnYXJlYUlkJzogNTcxLCAnYXJlYU5hbWUnOiAnMjQnfSwgeydhcmVhSWQnOiA1NzQsICdhcmVhTmFtZSc6ICcyNSd9LCB7J2FyZWFJZCc6IDU3NywgJ2FyZWFOYW1lJzogJzI2J30sIHsnYXJlYUlkJzogNTgwLCAnYXJlYU5hbWUnOiAnMjcnfSwgeydhcmVhSWQnOiA1ODMsICdhcmVhTmFtZSc6ICcyOCd9LCB7J2FyZWFJZCc6IDU4NiwgJ2FyZWFOYW1lJzogJzI5J30sIHsnYXJlYUlkJzogNTg5LCAnYXJlYU5hbWUnOiAnMzAnfV0iLCJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL2FyZWFfYXNzaWduX3BvbF9kaXZfcmVwX3ZpZXciOiJbeydhcmVhSWQnOiAzLCAnYXJlYU5hbWUnOiAnQS1NdWxraXJpZ2FsYSd9LCB7J2FyZWFJZCc6IDE4NSwgJ2FyZWFOYW1lJzogJ0ItQmVsaWF0dGEnfSwgeydhcmVhSWQnOiAzNDMsICdhcmVhTmFtZSc6ICdDIC1UYW5nYWxsZSd9LCB7J2FyZWFJZCc6IDU2MCwgJ2FyZWFOYW1lJzogJ0QtIFRpc3NhbWFoYXJhbWEnfV0iLCJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL2FyZWFfYXNzaWduX3BvbF9kaXZfcmVwX3ZlcmYiOiJbeydhcmVhSWQnOiAzLCAnYXJlYU5hbWUnOiAnQS1NdWxraXJpZ2FsYSd9LCB7J2FyZWFJZCc6IDE4NSwgJ2FyZWFOYW1lJzogJ0ItQmVsaWF0dGEnfSwgeydhcmVhSWQnOiAzNDMsICdhcmVhTmFtZSc6ICdDIC1UYW5nYWxsZSd9LCB7J2FyZWFJZCc6IDU2MCwgJ2FyZWFOYW1lJzogJ0QtIFRpc3NhbWFoYXJhbWEnfV0iLCJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL2FyZWFfYXNzaWduX2VsY19kaXNfcmVwX3ZpZXciOiJbeydhcmVhSWQnOiAyLCAnYXJlYU5hbWUnOiAnMDkgLSBIYW1iYW50b3RhJ31dIiwiaHR0cDovL3dzbzIub3JnL2NsYWltcy9hcmVhX2Fzc2lnbl9lbGNfZGlzX3JlcF92ZXJmIjoiW3snYXJlYUlkJzogMiwgJ2FyZWFOYW1lJzogJzA5IC0gSGFtYmFudG90YSd9XSIsImh0dHA6Ly93c28yLm9yZy9jbGFpbXMvYXJlYV9hc3NpZ25fbmF0X2Rpc19yZXBfdmlldyI6IltdIiwiaHR0cDovL3dzbzIub3JnL2NsYWltcy9hcmVhX2Fzc2lnbl9uYXRfZGlzX3JlcF92ZXJmIjoiW10iLCJodHRwOi8vd3NvMi5vcmcvY2xhaW1zL2FyZWFfYXNzaWduX2VjX2xlYWRlcnNoaXAiOiJbXSJ9.uScN6UOLRd7Ep95k8PpLiSUzQbnOgR0PjuFR76a77so',
        // 'X-Jwt-Assertion': window.prompt("'X-Jwt-Assertion': "),
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Cache-Control': 'no-store',
        'Pragma': 'no-cache',
        'X-Requested-With': 'XMLHttpRequest'
    }
});

export function request(config) {
    return axiosInstance.request(config).then((res) => res.data)
}


export function getAreas({electionId, associatedAreaId, areaType, limit = 10000, offset = 0}) {
    return request({
        url: ENDPOINT_PATH_AREAS(),
        method: 'get', // default,
        params: {electionId, associatedAreaId, areaType, limit, offset}
    })
}





