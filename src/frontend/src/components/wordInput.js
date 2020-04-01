import React from 'react';
import {Container, TextField, Box, Button} from "@material-ui/core";

class WordInput extends React.Component {
    render() {
        const gameInProcess = this.props.gameInProcess;
        const currentWord = this.props.currentWord;
        const onUpdate = this.props.onUpdate;
        const onSubmit = this.props.onSubmit;

        return (
            <Container>
                <Box component="div" display="inline">
                    <TextField
                        placeholder="Enter word"
                        onChange={(event) => onUpdate(event)}
                        value={currentWord}
                        disabled={!gameInProcess}
                    />
                </Box>
                <Box component="div" display="inline">
                    <Button
                        type="button"
                        onClick={() => onSubmit()}
                        disabled={!gameInProcess}
                    >
                        Submit
                    </Button>
                </Box>
            </Container>
        );
    }
}

export default WordInput;


