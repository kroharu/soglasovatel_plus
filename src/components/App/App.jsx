import { Route, BrowserRouter, Routes, Navigate } from 'react-router-dom';
import { Provider } from 'react-redux';
import { useSelector } from 'react-redux';
import ContractInfo from '../../pages/ContractInfo/ContractInfo';
import Login from '../../pages/Login/Login';
import MainApprover from '../../pages/MainApprover/MainApprover';
import MainCreator from '../../pages/MainCreator/MainCreator';
import UploadContract from '../../pages/UploadContract/UploadContract';
import Approval from '../../pages/Approval/Approval';
import store from '../../redux/store';
import './App.css';

function InnerApp() {
    const isAuth = useSelector(state => state.auth.isAuth);
    const login = useSelector(state => state.auth.login);

    const redirToMain = <Navigate to="/" />;
    const redirToLogin = <Navigate to="/login" />;
    const mainPage = login === 'юрист' ? <MainCreator /> : <MainApprover />;

    return (
        <div className="App">
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={!isAuth ? redirToLogin : mainPage} />
                    <Route path="/login" element={isAuth ? redirToMain : <Login />} />
                    <Route
                        path="/creator_contracts"
                        element={!isAuth ? redirToLogin : <MainCreator />}
                    />
                    <Route
                        path="/upload_contract"
                        element={!isAuth ? redirToLogin : <UploadContract />}
                    />
                    <Route
                        path="/contract_info/:id"
                        element={!isAuth ? redirToLogin : <ContractInfo />}
                    />
                    <Route
                        path="/approver_contracts"
                        element={!isAuth ? redirToLogin : <MainApprover />}
                    />
                    <Route path="/approval/:id" element={!isAuth ? redirToLogin : <Approval />} />
                </Routes>
            </BrowserRouter>
        </div>
    );
}

function App() {
    return (
        <Provider store={store}>
            <InnerApp />
        </Provider>
    );
}

export default App;
