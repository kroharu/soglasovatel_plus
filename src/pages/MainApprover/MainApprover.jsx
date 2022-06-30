import Header from '../../components/Header/Header';
import ApproverTable from '../../components/ApproverTable/ApproverTable';

function MainApprover() {
    return (
        <>
            <Header />
            <div className="main-title">Договоры для согласования</div>
            <ApproverTable />
        </>
    );
}

export default MainApprover;
