import React from 'react';
import PropTypes from 'prop-types';
import { useSelector, useDispatch } from 'react-redux';
import { setChosenApprover } from '../../redux/files/actions';
import './AddApproverModel.css';

function AddApproverModal(props) {
    const apprRef = React.useRef();
    const dispatch = useDispatch();
    const approvers = useSelector(state => state.files.approvers || []);
    const [curRole, setCurRole] = React.useState('');
    const chosenApprovers = useSelector(state => state.files.chosenApprovers || []);

    if (approvers && approvers.length && !curRole) {
        setCurRole(approvers[0].role);
    }

    const onRoleChange = event => {
        const role = event.target.value;
        setCurRole(role);
    };

    let approversRolesToOption;
    let approversNamesToOption;

    if (approvers) {
        approversRolesToOption = approvers.map(approver => (
            <option key={approver.role}>{approver.role}</option>
        ));

        approversNamesToOption = approvers
            .filter(({ role }) => role === curRole)
            .map(approver =>
                approver.users.map(user => <option key={user.id}>{user.name}</option>),
            );
    }

    const handleChooseApprover = () => {
        const isDuplicate = chosenApprovers.find(({ name }) => name === apprRef.current.value);

        if (!isDuplicate) {
            const { id } = approvers
                .reduce((accum, { users }) => [...accum, ...users], [])
                .find(({ name }) => name === apprRef.current.value);
            dispatch(setChosenApprover({ name: apprRef.current.value, role: curRole, id }));
        }

        props.handleModal();
    };

    return (
        <div className="modal-container" style={{ display: props.modal ? 'block' : 'none' }}>
            <div className="modal-dialog" role="document">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5 className="modal-title">Выбор согласующего</h5>
                        <div className="button-close" onClick={props.handleModal}>
                            <span>&times;</span>
                        </div>
                    </div>
                    <div className="modal-body">
                        <select
                            className="form-select"
                            aria-label="Default select example"
                            onChange={onRoleChange}
                        >
                            {approversRolesToOption}
                        </select>
                        <select
                            className="form-select"
                            aria-label="Default select example"
                            ref={apprRef}
                        >
                            {approversNamesToOption}
                        </select>
                    </div>
                    <div className="modal-footer">
                        <button
                            type="button"
                            className="btn btn-secondary"
                            onClick={props.handleModal}
                        >
                            Отмена
                        </button>
                        <button
                            type="button"
                            className="btn btn-primary"
                            onClick={handleChooseApprover}
                        >
                            Выбрать
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

AddApproverModal.propTypes = {
    modal: PropTypes.bool,
    handleModal: PropTypes.func,
};

export default AddApproverModal;
