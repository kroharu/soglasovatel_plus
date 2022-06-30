import React from 'react';
import Header from '../../components/Header/Header';
import { useParams } from 'react-router-dom';
import { getContractInfo } from '../../services/files';
import './ContractInfo.css';
import CreatorRemarksModal from '../../components/CreatorRemarksModal/CreatorRemarksModal';

function ContractInfo() {
    const [contract, setContract] = React.useState(null);
    const [modal, setModal] = React.useState(false);
    const [targetApproverId, setTargetApproverId] = React.useState(null);
    const params = useParams();

    const closeModal = () => {
        setModal(false);
    };

    const openModal = e => {
        setTargetApproverId(e.target.getAttribute('data-index'));
        setModal(true);
    };

    React.useEffect(() => {
        getContractInfo(params.id)
            .then(r => r.json())
            .then(json => {
                if (json.status == 'ok') {
                    setContract(json.contract);
                }
            });
    }, []);

    const ageementsToTable = contract?.agreements.map(
        ({ role_name, name, status, comments }, i) => (
            <tr key={i}>
                <th scope="row">{i + 1}</th>
                <td>{role_name}</td>
                <td>{name}</td>
                <td>{status ? 'Согласовано' : 'Осталось 3 дня'}</td>
                <td>
                    {comments.length ? (
                        <a className="open-remarks" data-index={i} onClick={openModal}>
                            Есть комментарии
                        </a>
                    ) : (
                        'Нет комментариев'
                    )}
                </td>
            </tr>
        ),
    );

    return (
        <>
            <CreatorRemarksModal
                handleModal={closeModal}
                modal={modal}
                comments={contract?.agreements[targetApproverId]?.comments}
            />
            <Header />
            <div className="main-title">{contract?.title}</div>
            <div className="conract-info">
                <div className="conract-info__description">
                    Дата регистрации: {contract?.created_at}
                </div>
                <div className="conract-info__description">Контрагент: ООО Ромашка</div>
                <div className="second-title">Версия договора от {contract?.created_at}</div>
                <table className="table">
                    <thead>
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">Подразделение</th>
                            <th scope="col">ФИО</th>
                            <th scope="col">Статус</th>
                            <th scope="col">Правки</th>
                        </tr>
                    </thead>
                    <tbody>{ageementsToTable}</tbody>
                </table>
                {contract?.argeed_by_all ? (
                    <button type="button" className="btn btn-primary">
                        Визировать и отправить на подписание
                    </button>
                ) : null}
            </div>
        </>
    );
}

export default ContractInfo;
