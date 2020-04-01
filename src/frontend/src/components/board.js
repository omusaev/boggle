import React from 'react';
import {Box} from "@material-ui/core";
import BoardRow from "./boardRow"


class Board extends React.Component {
    render() {
        const letters = this.props.letters;
        const onDiceClick = this.props.onDiceClick;
        const gameInProcess = this.props.gameInProcess;

        const numberOfCols = 4;

        let rows = [];
        let i, j;

        for (i = 0, j = letters.length; i < j; i += numberOfCols) {
            rows.push(letters.slice(i, i + numberOfCols));
        }

        const boardRows = rows.map((rowLetters, i) =>
            <Box key={i}>
                <BoardRow
                    letters={rowLetters}
                    onDiceClick={onDiceClick}
                    gameInProcess={gameInProcess}
                />
            </Box>
        );

        return (
            <Box>
                {boardRows}
            </Box>
        );
    }
}

export default Board;


