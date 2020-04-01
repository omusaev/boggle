import React from 'react';
import {Box, TextField, Typography} from "@material-ui/core";


class ShareGameLink extends React.Component {
    render() {
        const shareLink = this.props.shareLink;

        if (!shareLink) {
            return ''
        }

        return (
            <Box>
                <Box pb={1} pl={1}>
                    <Typography variant="overline">
                      Challenge a friend with this board!
                    </Typography>
                </Box>
                <TextField
                    variant="outlined"
                    fullWidth
                    value={shareLink}
                    inputProps={{style: { textAlign: 'center' }}}
                    InputProps={{
                        readOnly: true,
                    }}
                />
            </Box>
        )
    }
}

export default ShareGameLink;


