import { AUTH_ACTION_TYPES } from './types';

export default function authReducer(state, { type, payload }) {
    switch (type) {
        case AUTH_ACTION_TYPES.LOGIN:
            return {
                ...state,
                isAuth: Boolean(payload.login),
                login: payload.login,
            };
        case AUTH_ACTION_TYPES.LOGOUT:
            return {
                ...state,
                isAuth: false,
                login: '',
            };
        default:
            return { ...state };
    }
}
