import React from 'react';
import {ButtonGroup, Button} from "@material-ui/core";


class BoardRow extends React.Component {

    render() {
        const letters = this.props.letters;
        const onDiceClick = this.props.onDiceClick;
        const gameInProcess = this.props.gameInProcess;

        const dices = letters.map((letter, i) =>
            <Button
                key={i}
                size="large"
                type="button"
                disabled={!gameInProcess}
                onClick={() => onDiceClick(letter)}
            >
                {letter}
            </Button>
        );

        return (
            <ButtonGroup
                fullWidth
            >
                {dices}
            </ButtonGroup>
        );
    }
}

export default BoardRow;


