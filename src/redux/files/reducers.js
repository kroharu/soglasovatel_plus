import { FILES_ACTION_TYPES } from './types';

export default function filesReducer(state, { type, payload }) {
    switch (type) {
        case FILES_ACTION_TYPES.SET_APPROVERS:
            return {
                ...state,
                approvers: payload.approvers,
            };
        case FILES_ACTION_TYPES.SET_CHOSEN_APPROVER:
            return {
                ...state,
                chosenApprovers: [...state.chosenApprovers, payload.chosenApprover],
            };
        case FILES_ACTION_TYPES.DELETE_CHOSEN_APPROVER:
            return {
                ...state,
                chosenApprovers: state.chosenApprovers.filter(
                    ({ name }) => name !== payload.approverNameToDelete,
                ),
            };
        case FILES_ACTION_TYPES.SET_DIRECTOR_ID:
            return {
                ...state,
                directorId: payload.directorId,
            };
        case FILES_ACTION_TYPES.SET_CREATOR_CONTRACTS:
            return {
                ...state,
                creatorContracts: [...payload.creatorContracts],
            };
        case FILES_ACTION_TYPES.SET_APPROVER_CONTRACTS:
            return {
                ...state,
                approverContracts: [...payload.approverContracts],
            };
        default:
            return { ...state };
    }
}
