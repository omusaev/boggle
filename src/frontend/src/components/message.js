import React from 'react';
import {Alert} from '@material-ui/lab';


class Message extends React.Component {
    render() {
        const message = this.props.message;
        const severity = message.isError ? 'error': 'success';
        if (! message.text) {
            return '';
        }

        return (
            <Alert severity={severity}>
                {message.text}
            </Alert>
        );
    }
}

export default Message;


