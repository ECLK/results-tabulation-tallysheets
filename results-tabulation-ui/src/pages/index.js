import {PATH_ELECTION, PATH_ELECTION_BY_ID, PATH_ELECTION_TALLY_ACTIVITY_SHEET_VIEW} from "../App";
import React, {Component, useContext, useEffect, useState} from "react";
import BreadCrumb from "../components/bread-crumb";
import {getTallySheetCodeStr} from "../utils/tallySheet";
import IconButton from "@material-ui/core/IconButton";
import InfoIcon from "@material-ui/icons/Info";
import {ElectionContext} from "../services/election.provider";


function ElectionBreadCrumb({election, additionalLinks}) {
    const electionContext = useContext(ElectionContext);

    const [links, setLinks] = useState([]);

    const getBreadCrumbLinks = async () => {
        let _election = election;
        let _electionLinks = [];
        while (_election) {
            if (_election.isListed) {
                _electionLinks.unshift({
                    label: _election.electionName, to: PATH_ELECTION_BY_ID(_election.electionId)
                });
            }

            _election = await electionContext.getParentElection(_election.electionId);
        }

        const breadCrumbLinks = [
            {label: "elections", to: PATH_ELECTION()},
            ..._electionLinks,
            ...additionalLinks
        ];

        return breadCrumbLinks;
    };

    useEffect(() => {
        getBreadCrumbLinks().then(setLinks);
    }, []);

    return <BreadCrumb links={links}/>
}

export default class TabulationPage extends Component {
    render() {
        const {election, additionalBreadCrumbLinks = [], children} = this.props;

        return <div className="page">
            <ElectionBreadCrumb election={election} additionalLinks={additionalBreadCrumbLinks}/>
            {children}
        </div>
    }
}


export function TabulationTallySheetPage(props) {
    const {election, additionalBreadCrumbLinks = [], tallySheet, history, children} = props;

    const {tallySheetId, tallySheetCode} = tallySheet;
    const {rootElection, voteType} = election;
    const headerSuffix = tallySheet.electoralDistrictName ? "Electoral District: " + tallySheet.electoralDistrictName +
        (tallySheet.pollingDivisionName ? " Polling Division: " + tallySheet.pollingDivisionName : null) : null;

    return <div className="page">
        <ElectionBreadCrumb election={election} additionalLinks={additionalBreadCrumbLinks}/>
        <div className="tally-sheet-page-header">
            <h4 className="tally-sheet-page-header-election">{rootElection.electionName}</h4>

            <h5 className="tally-sheet-page-header-area">{tallySheet.electoralDistrictName ? "Electoral District: " : null}</h5>
            <strong className="tally-sheet-page-header-election">
                {tallySheet.electoralDistrictName ? tallySheet.electoralDistrictName : null}
            </strong>
            <h5 className="tally-sheet-page-header-area">{tallySheet.pollingDivisionName ? " Polling Division: " : null}</h5>
            <strong className="tally-sheet-page-header-election">
                {tallySheet.pollingDivisionName ? tallySheet.pollingDivisionName : null}
            </strong>

            <strong className="tally-sheet-page-header-tally-sheet-code">
                {getTallySheetCodeStr({tallySheetCode, voteType})}
            </strong>
            <h5 className="tally-sheet-page-header-area">{tallySheet.area.areaName}</h5>
            <IconButton
                aria-label="delete" style={{float: "right"}}
                className="tally-sheet-page-header-info-link"
                onClick={() => {
                    history.push(PATH_ELECTION_TALLY_ACTIVITY_SHEET_VIEW(tallySheetId))
                }}
            >
                <InfoIcon/>
            </IconButton>
        </div>
        {children}
    </div>
}
