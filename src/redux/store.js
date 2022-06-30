import { createStore, combineReducers, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import authReducer from './auth/reducers';
import filesReducer from './files/reducers';

const initialState = {
    auth: {
        login: localStorage.getItem('login'),
        isAuth: localStorage.getItem('isAuth'),
    },
    files: {
        approvers: null,
        chosenApprovers: [],
        directorId: null,
        creatorContracts: [],
        approverContracts: [],
    },
};

const store = createStore(
    combineReducers({
        auth: authReducer,
        files: filesReducer,
        thunk: applyMiddleware(thunk),
    }),
    initialState,
);

export default store;
