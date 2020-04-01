import React from 'react';
import {Container, TextField, ButtonGroup, Button} from "@material-ui/core";


class GameStart extends React.Component {
    render() {
        const isChallenge = this.props.isChallenge;
        const gameInProcess = this.props.gameInProcess;
        const onStartGame = this.props.onStartGame;
        const onPlayerNameUpdate = this.props.onPlayerNameUpdate;

        return (
            <Container>
                <TextField
                    placeholder="Enter your name"
                    fullWidth
                    disabled={gameInProcess}
                    onChange={event => onPlayerNameUpdate(event)}
                />
                <ButtonGroup
                    size="large"
                    fullWidth
                >
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
                </ButtonGroup>
            </Container>
        );
    }
}

export default GameStart;


