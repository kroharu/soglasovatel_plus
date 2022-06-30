import { AUTH_ACTION_TYPES } from './types';

export const setUser = login => ({
    type: AUTH_ACTION_TYPES.LOGIN,
    payload: { login },
});

export const logOut = () => ({
    type: AUTH_ACTION_TYPES.LOGOUT,
});
