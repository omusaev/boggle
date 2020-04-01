import React from 'react';
import {Box, TextField} from "@material-ui/core";


class ShareGameLink extends React.Component {
    render() {
        const shareLink = this.props.shareLink;

        if (!shareLink) {
            return ''
        }

        return (
            <Box>
                Challenge your friends with this combination!
                <TextField
                    fullWidth
                    value={shareLink}
                    InputProps={{
                        readOnly: true,
                    }}
                />
            </Box>
        )
    }
}

export default ShareGameLink;


