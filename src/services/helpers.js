const backUrl = 'http://localhost:8000';

export function sendRequest(path, body) {
    const url = backUrl + path;
    const options = {
        method: 'POST',
        mode: 'cors',
        credentials: 'include',
    };
    options.headers = { 'Content-Type': 'application/json; charset=utf-8' };
    options.body = JSON.stringify(body);
    return fetch(url, options);
}

export function sendFormData(path, body) {
    const url = backUrl + path;
    const options = {
        method: 'POST',
        mode: 'cors',
        credentials: 'include',
    };
    options.body = body;
    return fetch(url, options);
}

export function getData(path) {
    const url = backUrl + path;
    const options = {
        method: 'GET',
        credentials: 'include',
    };
    return fetch(url, options);
}
