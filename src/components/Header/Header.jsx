import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Navigate } from 'react-router-dom';
import { logOut } from '../../redux/auth/actions';
import { requestLogout } from '../../services/auth';

import './Header.css';

function Header() {
    const [needRedir, setNeedRedir] = React.useState(false);
    const login = useSelector(state => state.auth.login);
    const dispatch = useDispatch();

    if (needRedir) {
        return <Navigate to="/" />;
    }

    const onLogOutClick = () => {
        requestLogout().then(() => {
            localStorage.clear();
            dispatch(logOut());
        });
    };

    const navToMainPage = () => {
        setNeedRedir(true);
    };

    return (
        <header className="d-flex flex-wrap align-items-center justify-content-center justify-content-md-between py-3 mb-4 border-bottom header">
            <div className="header-left" onClick={navToMainPage}>
                {' '}
                СогласовательПлюс{' '}
            </div>
            <div className="header-right">
                <div>{login}</div>
                <button
                    type="button"
                    className="btn btn-outline-primary me-2"
                    onClick={onLogOutClick}
                >
                    Выход
                </button>
            </div>
        </header>
    );
}

export default Header;
