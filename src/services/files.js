import { sendFormData, getData, sendRequest } from './helpers';

export function uploadFile(formData) {
    return sendFormData('/api/contract/upload', formData);
}

export function getApprovers() {
    return getData('/api/company/users');
}

export function getCreatorContractsList() {
    return getData('/api/contracts/created');
}

export function getApproverContractsList() {
    return getData('/api/contracts/for');
}

export function sendApproval(cvu_id, body) {
    return sendRequest(`/api/comment/${cvu_id}`, body);
}

export function getContractInfo(id) {
    return getData(`/api/contract/${id}`);
}
