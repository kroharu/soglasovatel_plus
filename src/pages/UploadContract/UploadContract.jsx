import React from 'react';
import { Navigate } from 'react-router-dom';
import Header from '../../components/Header/Header';
import AddApproverModal from '../../components/AddApproverModal/AddApproverModal';
import { uploadFile, getApprovers } from '../../services/files';
import { setApprovers, deleteChosenApprover, setDirectorId } from '../../redux/files/actions';
import { useDispatch, useSelector } from 'react-redux';
import './UploadContract.css';

function UploadContract() {
    const [modal, setModal] = React.useState(false);
    const [needRedir, setNeedRedir] = React.useState(false);
    const formRef = React.useRef();
    const dispatch = useDispatch();
    const title = React.useRef();
    const partner = React.useRef();
    const chosenApprovers = useSelector(state => state.files.chosenApprovers || []);
    const directorId = useSelector(state => state.files.directorId);
    let approversToTable;

    if (needRedir) {
        return <Navigate to="/" />;
    }

    const closeModal = () => {
        setModal(false);
    };

    const getApr = () => {
        getApprovers()
            .then(res => res.json())
            .then(json => {
                if (json.status === 'ok') {
                    const directorId = json.roles.find(({ role }) => role === 'Директор').users[0].id;
                    dispatch(setApprovers(json.roles));
                    dispatch(setDirectorId(directorId));
                }
            });
    };

    const openModal = () => {
        setModal(true);
        getApr();
    };

    const handleDeleteChosenApprover = e => {
        const nameToDelete = e.target.getAttribute('data-name');
        dispatch(deleteChosenApprover(nameToDelete));
    };

    if (chosenApprovers && chosenApprovers.length) {
        approversToTable = chosenApprovers.map(approver => (
            <tr key={approver.name}>
                <th scope="row">{approver.role}</th>
                <td style={{ display: 'flex', justifyContent: 'space-between' }}>
                    {approver.name}
                    <button
                        type="button"
                        className="btn btn-danger"
                        data-name={approver.name}
                        onClick={handleDeleteChosenApprover}
                    >
                        Удалить
                    </button>
                </td>
            </tr>
        ));
    }

    function onUploadClick(e) {
        e.preventDefault();
        const formData = new FormData(formRef.current);
        formData.append(
            'agreements',
            chosenApprovers.map(({ id }) => id),
        );
        formData.append('sign', directorId);
        uploadFile(formData).then(response => {
            setNeedRedir(true);
        });
    }

    return (
        <>
            <AddApproverModal handleModal={closeModal} modal={modal} />
            <Header />
            <div className="main-title">Загрузка договора</div>
            <div className="upload-contract-container">
                <div className="upload-contract-container__left">
                    <form onSubmit={onUploadClick} ref={formRef} encType="multipart/form-data">
                        <div className="second-title">Информация о договоре</div>
                        <label htmlFor="upload-input" className="form-label">
                            Файл договора
                        </label>
                        <input className="form-control" id="upload-input" type="file" name="file" />
                        <label htmlFor="conract-name-input" className="form-label">
                            Название договора
                        </label>
                        <input
                            name="title"
                            className="form-control"
                            id="conract-name-input"
                            type="text"
                            placeholder="Название договора"
                            ref={title}
                        />
                        <label htmlFor="requisites-textarea" className="form-label">
                            Контрагент
                        </label>
                        <input
                            name="partner"
                            className="form-control"
                            id="requisites-textarea"
                            rows="3"
                            placeholder="Контрагент"
                            ref={partner}
                        />

                        {chosenApprovers.length && title.current && partner.current ? (
                            <input
                                type="submit"
                                className="btn btn-primary"
                                value="Отправить на согласование"
                            />
                        ) : null}
                    </form>
                </div>
                <div className="upload-contract-container__right">
                    <div className="second-title">Согласующие подразделения</div>
                    {chosenApprovers.length ? (
                        <table className="table">
                            <thead>
                                <tr>
                                    <th scope="col">Подразделение</th>
                                    <th scope="col">ФИО</th>
                                </tr>
                            </thead>
                            <tbody>{approversToTable}</tbody>
                        </table>
                    ) : null}

                    <button type="button" className="btn btn-primary" onClick={openModal}>
                        Добавить подразделение
                    </button>
                </div>
            </div>
        </>
    );
}

export default UploadContract;
