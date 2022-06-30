import PropTypes from 'prop-types';

function CreatorRemarksModal(props) {
    const commentsToTable = props.comments?.map((comm, ind) => (
        <tr key={ind}>
            <th scope="row">{comm.clause}</th>
            <td>{comm.original}</td>
            <td style={{ display: 'flex', justifyContent: 'space-between' }}>{comm.modified}</td>
        </tr>
    ));

    return (
        <div className="remarks-modal-container" style={{ display: props.modal ? 'flex' : 'none' }}>
            <div role="document">
                <div className="modal-content">
                    <div className="modal-header">
                        <h5 className="modal-title">Комментарии согласующего</h5>
                        <div className="button-close" onClick={props.handleModal}>
                            <span>&times;</span>
                        </div>
                    </div>
                    <div className="modal-body">
                        {props.comments?.length ? (
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
                            className="btn btn-primary"
                            onClick={props.handleModal}
                        >
                            Закрыть
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

CreatorRemarksModal.propTypes = {
    modal: PropTypes.bool,
    handleModal: PropTypes.func,
    comments: PropTypes.arrayOf(Object),
    handleComments: PropTypes.func,
};

export default CreatorRemarksModal;
