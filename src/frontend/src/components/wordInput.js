import React from 'react';
import {TextField, Box, Button} from "@material-ui/core";

class WordInput extends React.Component {
    render() {
        const gameInProcess = this.props.gameInProcess;
        const currentWord = this.props.currentWord;
        const onUpdate = this.props.onUpdate;
        const onSubmit = this.props.onSubmit;

        return (
            <Box>
                <Box display="inline">
                    <TextField
                        inputProps={{style: { textAlign: 'center' }}}
                        placeholder="Enter word"
                        onChange={(event) => onUpdate(event)}
                        value={currentWord}
                        disabled={!gameInProcess}
                    />
                </Box>
                <Box display="inline">
                    <Button
                        type="button"
                        onClick={() => onSubmit()}
                        disabled={!gameInProcess}
                    >
                        Submit
                    </Button>
                </Box>
            </Box>
        );
    }
}

export default WordInput;


