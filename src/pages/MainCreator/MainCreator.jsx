import React from 'react';
import { Navigate } from 'react-router-dom';
import Header from '../../components/Header/Header';
import CreatorTable from '../../components/CreatorTable/CreatorTable';
import ApproverTable from '../../components/ApproverTable/ApproverTable';
import './MainCreator.css';

function MainCreator() {
    const [needRedir, setNeedRedir] = React.useState(false);

    if (needRedir) {
        return <Navigate to="/upload_contract" />;
    }

    function onUploadClick() {
        setNeedRedir(true);
    }

    return (
        <>
            <Header />
            <div className="main-title">Главная страница</div>
            <div className="contract-upload-button">
                <div className="draft-contracts">Проекты договоров</div>
                <button type="button" className="btn btn-primary" onClick={onUploadClick}>
                    Загрузить договор
                </button>
            </div>
            <CreatorTable />
            <ApproverTable />
        </>
    );
}

export default MainCreator;
