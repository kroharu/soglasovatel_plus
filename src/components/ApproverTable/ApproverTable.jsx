import React from 'react';
import { Navigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { setApproverContracts } from '../../redux/files/actions';
import { getApproverContractsList } from '../../services/files';

function ApproverTable() {
    const [needRedir, setNeedRedir] = React.useState(false);
    const [contracts, setContracts] = React.useState([]);
    const [version, setVersion] = React.useState(null);
    const dispatch = useDispatch();

    React.useEffect(() => {
        getApproverContractsList()
            .then(r => r.json())
            .then(result => {
                if (result) {
                    setContracts(result.contracts);
                    dispatch(setApproverContracts(result.contracts));
                }
            });
    }, []);

    if (needRedir) {
        return <Navigate to={`/approval/${version}`} />;
    }

    function onContractOpenClick(e) {
        const version = e.target.getAttribute('data-version');
        setVersion(version);
        setNeedRedir(true);
    }

    let contractsToTable = null;
    if (contracts.length) {
        contractsToTable = contracts.map(({ title, created_at, version }, i) => (
            <tr key={created_at}>
                <th scope="row">{i + 1}</th>
                <td>{title}</td>
                <td>{created_at}</td>
                <td style={{ display: 'flex', justifyContent: 'space-between' }}>
                    Ожидает согласования{' '}
                    <button
                        type="button"
                        className="btn btn-primary"
                        data-version={version}
                        onClick={onContractOpenClick}
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

export default ApproverTable;
