import React from 'react';
import {Box, TextField, Button} from "@material-ui/core";


class GameStart extends React.Component {
    render() {
        const isChallenge = this.props.isChallenge;
        const gameInProcess = this.props.gameInProcess;
        const onStartGame = this.props.onStartGame;
        const onPlayerNameUpdate = this.props.onPlayerNameUpdate;

        return (
            <Box>
                <Box display="flex" justifyContent="center">
                    <TextField
                        inputProps={{style: { textAlign: 'center' }}}
                        placeholder="Enter your name"
                        disabled={gameInProcess}
                        onChange={event => onPlayerNameUpdate(event)}
                    />
                </Box>
                <Box display="flex" justifyContent="center" pt={2}>
                    {isChallenge &&
                    <Button
                        type="button"
                        onClick={() => onStartGame(true)}
                        disabled={gameInProcess}
                    >
                        Accept challenge
                    </Button>
                    }
                    <Button
                        type="button"
                        onClick={() => onStartGame(false)}
                        disabled={gameInProcess}
                    >
                        New game
                    </Button>
                </Box>
            </Box>
        );
    }
}

export default GameStart;


