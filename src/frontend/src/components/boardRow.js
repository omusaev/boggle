import React from 'react';
import {Box, Button} from "@material-ui/core";


class BoardRow extends React.Component {

    render() {
        const letters = this.props.letters;
        const onDiceClick = this.props.onDiceClick;
        const gameInProcess = this.props.gameInProcess;

        const dice = letters.map((letter, i) =>
            <Button
                key={i}
                size="large"
                type="button"
                variant="outlined"
                disabled={!gameInProcess}
                onClick={() => onDiceClick(letter)}
            >
                {letter}
            </Button>
        );

        return (
            <Box display="flex" justifyContent="center">
                {dice}
            </Box>
        );
    }
}

export default BoardRow;


