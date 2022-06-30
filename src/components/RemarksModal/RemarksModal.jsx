import PropTypes from 'prop-types';
import './RemarksModal.css';

function RemarksModal(props) {
    const commentsToTable = props.comments.map((comm, ind) => (
        <tr key={ind}>
            <th scope="row">{comm.clause}</th>
            <td>{comm.original}</td>
            <td style={{ display: 'flex', justifyContent: 'space-between' }}>
                {comm.modified}
                <button
                    type="button"
                    className="btn btn-danger"
                    data-index={ind}
                    onClick={props.handleComments}
                >
                    Удалить
                </button>
            </td>
        </tr>
    ));

    return (
        <div className="remarks-modal-container" style={{ display: props.modal ? 'flex' : 'none' }}>
            <div role="document">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5 className="modal-title">Комментарии</h5>
                        <div className="button-close" onClick={props.handleModal}>
                            <span>&times;</span>
                        </div>
                    </div>
                    <div className="modal-body">
                        {props.comments.length ? (
                            <table className="table">
                                <thead>
                                    <tr>
                                        <th scope="col">Номер положения</th>
                                        <th scope="col">Комментируемое положение договора</th>
                                        <th scope="col">Измененное положение</th>
                                    </tr>
                                </thead>
                                <tbody>{commentsToTable}</tbody>
                            </table>
                        ) : (
                            'Нет замечаний'
                        )}
                    </div>
                    <div className="modal-footer">
                        <button
                            type="button"
                            className="btn btn-secondary"
                            onClick={props.handleModal}
                        >
                            Отмена
                        </button>
                        <button
                            type="button"
                            className="btn btn-primary"
                            onClick={props.handleApproval}
                        >
                            Отправить замечания
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

RemarksModal.propTypes = {
    modal: PropTypes.bool,
    handleModal: PropTypes.func,
    comments: PropTypes.arrayOf(Object),
    handleComments: PropTypes.func,
    handleApproval: PropTypes.func,
};

export default RemarksModal;
