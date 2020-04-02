import React from 'react';
import {Box} from "@material-ui/core";


class GameInfo extends React.Component {
    render() {
        const time = this.props.time;
        const finalScore = this.props.finalScore;

        return (
            <Box display="flex" justifyContent="center">
                <Box p={2} width={30}>
                    {time.minutes}:{time.seconds}
                </Box>
                <Box p={2}>
                    {finalScore}
                </Box>
            </Box>
        );
    }
}

export default GameInfo;