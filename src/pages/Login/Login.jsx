import React from 'react';
import { Navigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { setUser } from '../../redux/auth/actions';
import { requestLogin } from '../../services/auth';

import './Login.css';

function Login() {
    const [login, setLogin] = React.useState('');
    const [password, setPassword] = React.useState('');
    const isAuth = useSelector(state => state.auth.isAuth);
    const dispatch = useDispatch();

    if (isAuth) {
        return <Navigate to="/" />;
    }

    const onLoginChange = e => {
        setLogin(e.target.value);
    };

    const onPasswordChange = e => {
        setPassword(e.target.value);
    };

    const handleLogin = () => {
        requestLogin(login, password).then(({ status }) => {
            if (status === 200) {
                localStorage.setItem('isAuth', 'true');
                localStorage.setItem('login', login);
                dispatch(setUser(login));
            }
        });
    };

    return (
        <div className="login-container">
            <section className="text-center text-lg-start  align-middle">
                <div className="card mb-3">
                    <div className="row g-0 d-flex align-items-center">
                        <div className="col-lg-4 d-none d-lg-flex">
                            <img
                                src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.webp"
                                alt="icon"
                                className="w-100 rounded-t-5 rounded-tr-lg-0 rounded-bl-lg-5"
                            />
                        </div>
                        <div className="col-lg-8">
                            <div className="card-body py-5 px-md-5">
                                <form>
                                    <div className="form-outline mb-4">
                                        <input
                                            type="email"
                                            id="form2Example1"
                                            className="form-control"
                                            onChange={onLoginChange}
                                        />
                                        <label className="form-label" htmlFor="form2Example1">
                                            Логин
                                        </label>
                                    </div>

                                    <div className="form-outline mb-4">
                                        <input
                                            type="password"
                                            id="form2Example2"
                                            className="form-control"
                                            onChange={onPasswordChange}
                                        />
                                        <label className="form-label" htmlFor="form2Example2">
                                            Пароль
                                        </label>
                                    </div>

                                    <button
                                        type="button"
                                        className="btn btn-primary btn-block mb-4"
                                        onClick={handleLogin}
                                    >
                                        Войти
                                    </button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}

export default Login;
