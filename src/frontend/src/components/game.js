import React from 'react';
import {Container, Box} from "@material-ui/core";

import Board from './board';
import Timer from './timer';
import Message from './message';
import WordInput from './wordInput';
import ScoreTable from './scoreTable';

class Game extends React.Component {
    render() {
        const letters = this.props.letters;
        const time = this.props.time;
        const foundWords = this.props.foundWords;
        const finalScore = this.props.finalScore;
        const onCurrentWordUpdate = this.props.onCurrentWordUpdate;
        const onNewWordSubmit = this.props.onNewWordSubmit;
        const message = this.props.message;
        const currentWord = this.props.currentWord;
        const onDiceClick = this.props.onDiceClick;
        const gameInProcess = this.props.gameInProcess;

        return (
            <Container>
                <Box>
                    <Board
                        gameInProcess={gameInProcess}
                        letters={letters}
                        onDiceClick={onDiceClick}
                    />
                </Box>
                <Box>
                    <Timer
                        time={time}
                    />
                </Box>
                <Message
                    message={message}
                />
                <WordInput
                    gameInProcess={gameInProcess}
                    currentWord={currentWord}
                    onUpdate={onCurrentWordUpdate}
                    onSubmit={onNewWordSubmit}
                />
                <ScoreTable
                    foundWords={foundWords}
                    finalScore={finalScore}
                />
            </Container>
        );
    }
}

export default Game;
