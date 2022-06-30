import React from 'react';
import { Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import Header from '../../components/Header/Header';
import RemarksModal from '../../components/RemarksModal/RemarksModal';
import { sendApproval } from '../../services/files';
import './Approval.css';

function Approval() {
    const [needRedir, setNeedRedir] = React.useState(false);
    const [clause, setClause] = React.useState('');
    const [originalText, setOriginalText] = React.useState('');
    const [modifiedText, setModifiedText] = React.useState('');
    const [comments, changeComments] = React.useState([]);
    const [modal, setModal] = React.useState(false);
    const params = useParams();
    const contracts = useSelector(state => state.files.approverContracts);
    let currentContract;

    if (!contracts.length) {
        return <Navigate to="/approver_contracts" />;
    } else {
        currentContract = contracts.find(({ version }) => version == params.id);
    }

    if (needRedir) {
        return <Navigate to="/" />;
    }

    const closeModal = () => {
        setModal(false);
    };

    const openModal = () => {
        setModal(true);
    };

    const handleClauseChange = event => {
        setClause(event.target.value);
    };
    const handleOriginalTextChange = event => {
        setOriginalText(event.target.value);
    };
    const handleModifiedTextChange = event => {
        setModifiedText(event.target.value);
    };

    const addComment = () => {
        const comment = {
            modified: modifiedText,
            clause,
            original: originalText,
        };
        changeComments([...comments, comment]);
        setClause('');
        setOriginalText('');
        setModifiedText('');
    };

    const deleteComment = e => {
        const ind = e.target.getAttribute('data-index');
        comments.splice(Number(ind), 1);
        changeComments([...comments]);
    };

    const approvalWithRemarks = () => {
        const remarks = {
            status: false,
            comments,
        };
        sendApproval(currentContract.version, remarks);
        setNeedRedir(true);
    };

    const approvalWithoutRemarks = () => {
        const remarks = {
            status: true,
            comments: [],
        };
        sendApproval(currentContract.version, remarks)
            .then(res => res.json())
            .then(json => {
                if (json.status === 'ok') {
                    // alert('Договор согласован');
                }
            });
        setNeedRedir(true);
    };

    return (
        <>
            <RemarksModal
                handleModal={closeModal}
                modal={modal}
                comments={comments}
                handleComments={deleteComment}
                handleApproval={approvalWithRemarks}
            />
            <Header />
            <div className="approval">
                <div className="approval__left">
                    <div className="main-title">{currentContract.title}</div>
                    <div className="conract-info">
                        <div className="conract-info__description">
                            Дата регистрации: {currentContract.created_at}
                        </div>
                        <div className="conract-info__description">Контрагент: ООО Ромашка</div>
                        <div className="second-title">Согласование</div>
                        <textarea
                            className="form-control"
                            rows="1"
                            placeholder="Номер положения"
                            onChange={handleClauseChange}
                            value={clause}
                        />
                        <textarea
                            className="form-control"
                            rows="3"
                            placeholder="Комментируемое положение договора"
                            onChange={handleOriginalTextChange}
                            value={originalText}
                        />
                        <textarea
                            className="form-control"
                            rows="3"
                            placeholder="Измененное положение"
                            onChange={handleModifiedTextChange}
                            value={modifiedText}
                        />
                        {!clause && !originalText && !modifiedText && !comments.length ? (
                            <button
                                type="button"
                                className="btn btn-primary approval__button"
                                onClick={approvalWithoutRemarks}
                            >
                                Согласовать
                            </button>
                        ) : null}
                        {clause && originalText && modifiedText ? (
                            <button
                                type="button"
                                className="btn btn-primary approval__button"
                                onClick={addComment}
                            >
                                Добавить замечание
                            </button>
                        ) : null}
                        {comments.length ? (
                            <button
                                type="button"
                                className="btn btn-primary approval__button"
                                onClick={approvalWithRemarks}
                            >
                                Согласовать с замечаниями
                            </button>
                        ) : null}
                        {comments.length ? (
                            <button
                                type="button"
                                className="btn btn-primary approval__button"
                                onClick={openModal}
                            >
                                Посмотреть замечания
                            </button>
                        ) : null}
                    </div>
                </div>
                <iframe
                    style={{ width: '750px', height: '650px', border: '1px solid black' }}
                    src="https://www.rembrigada.ru/images/dogovor.pdf"
                />
            </div>
        </>
    );
}

export default Approval;
