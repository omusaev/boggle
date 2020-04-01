import React from 'react';
import {Box} from "@material-ui/core";

import Board from './board';
import GameInfo from './gameInfo';
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
            <Box>
                <Box>
                    <Board
                        gameInProcess={gameInProcess}
                        letters={letters}
                        onDiceClick={onDiceClick}
                    />
                </Box>
                <Box>
                    <GameInfo
                        time={time}
                        finalScore={finalScore}
                    />
                </Box>
                <Box display="flex" justifyContent="center">
                    <Box width={1/2}>
                        <Message
                            message={message}
                        />
                    </Box>
                </Box>
                <Box display="flex" justifyContent="center" pt={3}>
                    <WordInput
                        gameInProcess={gameInProcess}
                        currentWord={currentWord}
                        onUpdate={onCurrentWordUpdate}
                        onSubmit={onNewWordSubmit}
                    />
                </Box>
                <Box display="flex" justifyContent="center" pt={3}>
                    <Box>
                        <ScoreTable
                            foundWords={foundWords}
                        />
                    </Box>
                </Box>
            </Box>
        );
    }
}

export default Game;
