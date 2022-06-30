import { sendRequest } from './helpers';

export const requestLogin = (login, password) => {
    return sendRequest('/api/login', { login: login, password: password });
};

export const requestLogout = () => {
    return sendRequest('/api/logout');
};
