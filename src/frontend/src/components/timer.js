import React from 'react';
import {Button} from "@material-ui/core";

class GameTimer extends React.Component {
    render() {
        const time = this.props.time;


        return (
            <Button fullWidth disabled type="button">
                {time.minutes}:{time.seconds}
            </Button>
        );
    }
}

export default GameTimer;


