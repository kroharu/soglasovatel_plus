import { FILES_ACTION_TYPES } from './types';

export const setApprovers = approvers => ({
    type: FILES_ACTION_TYPES.SET_APPROVERS,
    payload: { approvers },
});

export const setChosenApprover = chosenApprover => ({
    type: FILES_ACTION_TYPES.SET_CHOSEN_APPROVER,
    payload: { chosenApprover },
});

export const deleteChosenApprover = approverNameToDelete => ({
    type: FILES_ACTION_TYPES.DELETE_CHOSEN_APPROVER,
    payload: { approverNameToDelete },
});

export const setDirectorId = directorId => ({
    type: FILES_ACTION_TYPES.SET_DIRECTOR_ID,
    payload: { directorId },
});

export const setCreatorContracts = creatorContracts => ({
    type: FILES_ACTION_TYPES.SET_CREATOR_CONTRACTS,
    payload: { creatorContracts },
});

export const setApproverContracts = approverContracts => ({
    type: FILES_ACTION_TYPES.SET_APPROVER_CONTRACTS,
    payload: { approverContracts },
});
