import React from 'react';
import { Navigate } from 'react-router-dom';
import { getCreatorContractsList } from '../../services/files';

function CreatorTable() {
    const [needRedir, setNeedRedir] = React.useState(false);
    const [contracts, setContracts] = React.useState([]);
    const [id, setId] = React.useState(null);

    React.useEffect(() => {
        getCreatorContractsList()
            .then(r => r.json())
            .then(result => {
                if (result) {
                    setContracts(result);
                }
            });
    }, []);

    if (needRedir) {
        return <Navigate to={`/contract_info/${id}`} />;
    }

    const onContractOpenClick = e => {
        const c_id = e.target.getAttribute('data-id');
        setId(c_id);
        setNeedRedir(true);
    };

    let contractsToTable = null;
    if (contracts.length) {
        contractsToTable = contracts.map(({ id, title, created_at }, i) => (
            <tr key={id}>
                <th scope="row">{i + 1}</th>
                <td>{title}</td>
                <td>{created_at}</td>
                <td style={{ display: 'flex', justifyContent: 'space-between' }}>
                    Ожидает согласования{' '}
                    <button
                        type="button"
                        className="btn btn-primary"
                        onClick={onContractOpenClick}
                        data-id={id}
                    >
                        Открыть
                    </button>
                </td>
            </tr>
        ));
    }

    return (
        <div>
            {contracts.length ? (
                <table className="table">
                    <thead>
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">Название договора</th>
                            <th scope="col">Дата регистрации</th>
                            <th scope="col">Срок</th>
                        </tr>
                    </thead>
                    <tbody>{contractsToTable}</tbody>
                </table>
            ) : null}
        </div>
    );
}

CreatorTable.propTypes = {};

export default CreatorTable;
