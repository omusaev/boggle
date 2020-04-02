import React from 'react';
import {Box, List, ListItem} from "@material-ui/core";


class ScoreTable extends React.Component {
    render() {
        const foundWords = this.props.foundWords;

        const rows = foundWords.map((word, i) =>
            <ListItem
                key={i}
            >
                <Box display="flex" justifyContent="center">
                    <Box width={30}>
                        ({word.score})
                    </Box>
                    <Box>
                        {word.word}
                    </Box>
                </Box>
            </ListItem>
        );

        return (
            <Box>
                <List>
                    {rows}
                </List>
            </Box>
        );
    }
}

export default ScoreTable;


